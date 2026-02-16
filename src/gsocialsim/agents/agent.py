from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, List
from collections import OrderedDict
import random

from gsocialsim.agents.identity_state import IdentityState
from gsocialsim.agents.belief_state import BeliefStore
from gsocialsim.agents.emotion_state import EmotionState
from gsocialsim.agents.budget_state import BudgetState, BudgetKind
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.agents.attention_system import AttentionSystem
from gsocialsim.agents.belief_update_engine import BeliefUpdateEngine, BeliefDelta
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.policy.bandit_learner import BanditLearner, RewardVector
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from gsocialsim.agents.impression import Impression, IntakeMode

if TYPE_CHECKING:
    from gsocialsim.kernel.world_kernel import WorldContext


class MemoryStore:
    pass


@dataclass
class Agent:
    id: str
    seed: int
    identity: IdentityState = field(default_factory=IdentityState)
    beliefs: BeliefStore = field(default_factory=BeliefStore)
    emotion: EmotionState = field(default_factory=EmotionState)
    budgets: BudgetState = field(default_factory=BudgetState)
    personality: RewardWeights = field(default_factory=RewardWeights)
    rng: random.Random = field(init=False)
    attention: AttentionSystem = field(default_factory=AttentionSystem)
    belief_update_engine: BeliefUpdateEngine = field(default_factory=BeliefUpdateEngine)
    memory: MemoryStore = field(default_factory=MemoryStore)
    policy: BanditLearner = field(default_factory=BanditLearner)

    # Working memory
    max_recent_impressions: int = 200
    recent_impressions: OrderedDict[str, Impression] = field(default_factory=OrderedDict)

    # Daily buffers (for dream / consolidation)
    daily_impressions_consumed: List[Impression] = field(default_factory=list)
    daily_actions: List[Interaction] = field(default_factory=list)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.budgets._rng = self.rng

    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def _remember_impression(self, impression: Impression) -> None:
        content_id = getattr(impression, "content_id", None)
        if not content_id:
            return
        try:
            # Refresh recency if already present
            if content_id in self.recent_impressions:
                self.recent_impressions.move_to_end(content_id)
            self.recent_impressions[content_id] = impression
            # Bound memory growth (attention span)
            while len(self.recent_impressions) > max(1, int(self.max_recent_impressions)):
                self.recent_impressions.popitem(last=False)
        except Exception:
            # Fallback: do nothing on unexpected mapping issues
            pass

    def _update_trust_from_impression(
        self,
        context: "WorldContext",
        content: ContentItem,
        impression: Impression,
        prior_stance: float,
    ) -> None:
        gsr = getattr(context, "gsr", None)
        if gsr is None:
            return
        if content.author_id == self.id:
            return

        stance_diff = float(impression.stance_signal) - float(prior_stance)
        alignment = 1.0 - min(1.0, abs(stance_diff) / 2.0)  # [0,1]

        credibility = float(getattr(impression, "credibility_signal", 0.5))
        credibility = self._clamp01(credibility)
        threat = float(getattr(impression, "identity_threat", 0.0))
        threat = self._clamp01(threat)

        # Political salience can amplify distrust on hostile content.
        pol_threat = 0.0
        try:
            gsr = getattr(context, "gsr", None)
            if gsr is not None:
                pol_sal = float(getattr(gsr.ensure_topic(content.topic), "political_salience", 0.0))
                if pol_sal > 0.0:
                    lean = float(getattr(self.identity, "political_lean", 0.0))
                    part = float(getattr(self.identity, "partisanship", 0.0))
                    alignment = float(impression.stance_signal) * lean
                    pol_threat = pol_sal * max(0.0, -alignment) * max(0.0, min(1.0, part))
        except Exception:
            pol_threat = 0.0

        # Small, naturalistic adjustments; credibility and alignment build trust, threat erodes it.
        delta = (0.015 * (alignment - 0.5)) + (0.01 * (credibility - 0.5)) - (0.02 * threat)
        if pol_threat > 0.0:
            delta -= 0.02 * pol_threat

        if impression.intake_mode == IntakeMode.PHYSICAL:
            delta *= 1.5

        try:
            gsr.update_trust(self.id, content.author_id, delta)
        except Exception:
            pass

    def _apply_political_context(self, context: "WorldContext", impression: Impression) -> None:
        gsr = getattr(context, "gsr", None)
        if gsr is None:
            return
        try:
            pol_sal = float(getattr(gsr.ensure_topic(impression.topic), "political_salience", 0.0))
        except Exception:
            pol_sal = 0.0
        if pol_sal <= 0.0:
            return

        try:
            lean = float(getattr(self.identity, "political_lean", 0.0))
            part = float(getattr(self.identity, "partisanship", 0.0))
        except Exception:
            return

        alignment = float(impression.stance_signal) * lean
        pol_threat = pol_sal * max(0.0, -alignment) * max(0.0, min(1.0, part))
        if pol_threat > 0.0:
            try:
                impression.identity_threat = max(float(getattr(impression, "identity_threat", 0.0)), pol_threat)
            except Exception:
                pass

        # Keep network edge trust in sync when possible (directional: viewer -> author)
        try:
            graph = getattr(context, "network", None)
            graph = getattr(graph, "graph", None)
            if graph:
                graph.update_edge_trust(self.id, content.author_id, delta)
        except Exception:
            pass

    def _should_defer_belief_updates(self, context: "WorldContext") -> bool:
        """
        Phase-contract hook:
        - If context supports deferral and we're not in consolidation, queue deltas.
        """
        in_consolidation = bool(getattr(context, "in_consolidation", False))
        has_queue = callable(getattr(context, "queue_belief_delta", None))
        return has_queue and (not in_consolidation)

    def _apply_or_queue_belief_delta(self, context: "WorldContext", delta: BeliefDelta) -> bool:
        """
        Returns True if the delta was queued (deferred), False if applied immediately.
        """
        if self._should_defer_belief_updates(context):
            context.queue_belief_delta(self.id, delta)
            return True

        # Legal to apply only during CONSOLIDATE if contract is enabled.
        self.beliefs.apply_delta(delta)
        return False

    def perceive(
        self,
        content: ContentItem,
        context: "WorldContext",
        is_physical: bool = False,
        stimulus_id: Optional[str] = None,
    ):
        """
        Perception pipeline (contract-aware):
          1) Evaluate content -> Impression
          2) Store impression (working memory)
          3) Log exposure (always)
          4) Sample consumption
             - if not consumed: stop
             - if consumed: log consumption, compute belief delta
          5) Phase contract:
             - belief deltas are queued unless CONSOLIDATE is active
        """
        impression = self.attention.evaluate(content, is_physical=is_physical)

        # mark self-source for downstream logic
        try:
            if content.author_id == self.id:
                setattr(impression, "is_self_source", True)
        except Exception:
            pass

        # apply political identity context (may raise identity_threat)
        self._apply_political_context(context, impression)

        self._remember_impression(impression)

        # --- Exposure (always) ---
        context.analytics.log_exposure(
            viewer_id=self.id,
            source_id=content.author_id,
            topic=content.topic,
            is_physical=is_physical,
            timestamp=context.clock.t,
            content_id=content.id,
            intake_mode=impression.intake_mode.value,
            media_type=impression.media_type.value if impression.media_type else None,
        )

        consumed_prob = self._clamp01(float(getattr(impression, "consumed_prob", 1.0)))
        if self.rng.random() >= consumed_prob:
            return  # exposed but not consumed

        # Spend time for actual consumption (opportunity cost)
        try:
            cost = float(getattr(impression, "attention_cost_minutes", 0.0))
        except Exception:
            cost = 0.0
        if cost > 0.0:
            spend = getattr(context, "spend_time", None)
            if callable(spend):
                if not spend(self.id, cost):
                    return

        # --- Consumption (explicit) ---
        context.analytics.log_consumption(
            viewer_id=self.id,
            content_id=content.id,
            topic=content.topic,
            timestamp=context.clock.t,
            media_type=impression.media_type.value if impression.media_type else None,
            intake_mode=impression.intake_mode.value,
        )

        # Record for daily dream
        self.daily_impressions_consumed.append(impression)

        # --- Belief delta compute (no direct mutation here under contract) ---
        prior = self.beliefs.get(content.topic)
        old_stance = prior.stance if prior else 0.0

        belief_delta = self.belief_update_engine.update(
            viewer=self,
            content_author_id=content.author_id,
            impression=impression,
            gsr=context.gsr,
        )

        deferred = self._apply_or_queue_belief_delta(context, belief_delta)

        # Trust update based on consumption (after delta compute to keep influence stable)
        self._update_trust_from_impression(context, content, impression, old_stance)

        # If deferred, we cannot legally compute crossings/new stance yet (state unchanged).
        # Kernel CONSOLIDATE will apply and log belief updates.
        if deferred:
            return

        # Immediate-apply path (only when contract deferral is disabled or we are consolidating)
        after = self.beliefs.get(content.topic)
        new_stance = after.stance if after else old_stance

        if context.analytics.crossing_detector.check(old_stance, new_stance):
            attribution = context.analytics.attribution_engine.assign_credit(
                agent_id=self.id,
                topic=content.topic,
                history=context.analytics.exposure_history,
            )
            from gsocialsim.analytics.attribution import BeliefCrossingEvent

            crossing_event = BeliefCrossingEvent(
                timestamp=context.clock.t,
                agent_id=self.id,
                topic=content.topic,
                old_stance=old_stance,
                new_stance=new_stance,
                attribution=attribution,
            )
            context.analytics.log_belief_crossing(crossing_event)

        context.analytics.log_belief_update(
            timestamp=context.clock.t,
            agent_id=self.id,
            delta=belief_delta,
        )

    def learn(self, action_key: str, reward_vector: RewardVector):
        self.policy.learn(action_key, reward_vector)

    def act(self, tick: int, context: Optional["WorldContext"] = None) -> Optional[Interaction]:
        # Action is gated by time budget if available
        spend = getattr(context, "spend_time", None) if context is not None else None

        interaction = self.policy.generate_interaction(self, tick)
        if interaction:
            attention_costs = {
                InteractionVerb.CREATE: 5.0,
                InteractionVerb.LIKE: 1.0,
                InteractionVerb.FORWARD: 1.0,
                InteractionVerb.COMMENT: 3.0,
                InteractionVerb.REPLY: 3.0,
            }
            cost = attention_costs.get(interaction.verb, 1.0)
            if callable(spend) and cost > 0.0:
                if not spend(self.id, cost):
                    return None
            self.daily_actions.append(interaction)

            reward = RewardVector()
            topic = None

            if interaction.verb == InteractionVerb.LIKE:
                reward.affiliation = 0.2
                topic = interaction.target_stimulus_id
            elif interaction.verb == InteractionVerb.FORWARD:
                reward.status = 0.3
                topic = interaction.target_stimulus_id

            if topic:
                action_key = f"{interaction.verb.value}_{topic}"
                self.learn(action_key, reward)

        return interaction

    def dream(self, world_context: "WorldContext") -> None:
        """
        Daily consolidation ("dreaming / reflection").
        """
        if not self.daily_impressions_consumed:
            return

        self.identity.consolidate_from_impressions(
            self.daily_impressions_consumed,
            rng=self.rng,
            max_samples=30,
        )

        counts: dict[str, int] = {}
        sums: dict[str, float] = {}
        for imp in self.daily_impressions_consumed:
            t = str(getattr(imp, "topic", ""))
            counts[t] = counts.get(t, 0) + 1
            sums[t] = sums.get(t, 0.0) + float(getattr(imp, "stance_signal", 0.0))

        for topic, c in counts.items():
            self.beliefs.nudge_salience(topic, 0.02 * min(10, c))
            self.beliefs.nudge_knowledge(topic, 0.01 * min(10, c))

            # Reflection: small stance drift toward the mean of consumed signals.
            belief = self.beliefs.get(topic)
            if belief is None:
                continue
            mean_signal = sums.get(topic, 0.0) / max(1, c)
            openness = 1.0 - float(getattr(self.identity, "identity_rigidity", 0.5))
            openness = max(0.0, min(1.0, openness))
            step = 0.02 * openness
            drift = (mean_signal - belief.stance) * step
            if drift != 0.0:
                self.beliefs.apply_delta(BeliefDelta(topic_id=topic, stance_delta=drift, confidence_delta=0.0))

        try:
            world_context.analytics.log_dream(
                timestamp=world_context.clock.t,
                agent_id=self.id,
                consolidated=len(self.daily_impressions_consumed),
                topic_counts=counts,
                actions=len(self.daily_actions),
            )
        except Exception:
            pass

    def consolidate_daily(self, world_context):
        """
        End-of-day boundary.
        """
        self.dream(world_context)
        self.budgets.regen_daily()

        self.daily_impressions_consumed.clear()
        self.daily_actions.clear()
