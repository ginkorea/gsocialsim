from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING, Optional, Set
import itertools
import random

from gsocialsim.agents.budget_state import BudgetKind
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.types import TopicId

if TYPE_CHECKING:
    from gsocialsim.kernel.world_kernel import WorldContext
    from gsocialsim.stimuli.interaction import Interaction
    from gsocialsim.stimuli.stimulus import Stimulus

_event_counter = itertools.count()


class EventPhase(IntEnum):
    """
    Deterministic ordering within the same simulation tick.
    Lower runs earlier.
    """
    INGEST = 10
    PERCEIVE = 20
    INTERACT_PERCEIVE = 30
    ACT = 40
    ALLOCATE_ATTENTION = 50
    DEEP_FOCUS = 60
    DAY_BOUNDARY = 90


def _stimulus_topic_id(stimulus: "Stimulus") -> TopicId:
    raw = getattr(stimulus, "metadata", None) or {}
    t = raw.get("topic")

    if t is None:
        return TopicId("T_Original")

    if isinstance(t, str):
        t = t.strip()
        return TopicId(t if t else "T_Original")

    return TopicId(str(t))


def _stimulus_stance(stimulus: "Stimulus") -> float:
    raw = getattr(stimulus, "stance_hint", None)
    if raw is None:
        raw = getattr(stimulus, "metadata", None) or {}
        raw = raw.get("stance")
    try:
        v = float(raw) if raw is not None else 0.0
    except Exception:
        v = 0.0
    if raw is None:
        # Deterministic small bias per stimulus when stance is unspecified
        topic = _stimulus_topic_id(stimulus)
        seed = hash(f"{stimulus.id}:{topic}") & 0xFFFFFFFF
        rng = random.Random(seed)
        v = rng.uniform(-0.35, 0.35)
    return max(-1.0, min(1.0, v))


def _stimulus_identity_threat(stimulus: "Stimulus") -> Optional[float]:
    raw = getattr(stimulus, "metadata", None) or {}
    for key in ("identity_threat", "threat"):
        if key in raw:
            try:
                v = float(raw.get(key))
                return max(0.0, min(1.0, v))
            except Exception:
                return None
    return None


def _stimulus_political_salience(stimulus: "Stimulus") -> Optional[float]:
    raw_val = getattr(stimulus, "political_salience", None)
    if raw_val is None:
        raw = getattr(stimulus, "metadata", None) or {}
        raw_val = raw.get("political_salience")
    try:
        v = float(raw_val) if raw_val is not None else None
    except Exception:
        v = None
    if v is None:
        return None
    return max(0.0, min(1.0, v))


def _get_followers(context: "WorldContext", author_id: str) -> Set[str]:
    try:
        return set(context.network.graph.get_followers(author_id))
    except Exception:
        return set()


def _subs_recipients(context: "WorldContext", stimulus: "Stimulus", topic: TopicId) -> Set[str]:
    subs = getattr(context, "subscriptions", None)
    if subs is None:
        return set()

    def _try_get(sub_type: str, target_id: Optional[str]) -> Set[str]:
        if not target_id:
            return set()

        fn = getattr(subs, "get_subscribers", None)
        if callable(fn):
            try:
                return set(fn(sub_type, target_id))
            except Exception:
                pass

        m = getattr(subs, "subscribers_by_target", None)
        if isinstance(m, dict):
            for key in ((sub_type, target_id), (str(sub_type), target_id)):
                try:
                    v = m.get(key)
                    if v:
                        return set(v)
                except Exception:
                    continue
        return set()

    recipients: Set[str] = set()
    recipients |= _try_get("topic", str(topic))
    recipients |= _try_get("creator", getattr(stimulus, "creator_id", None))
    recipients |= _try_get("outlet", getattr(stimulus, "outlet_id", None))
    recipients |= _try_get("community", getattr(stimulus, "community_id", None))
    return recipients


def _select_stimulus_recipients(context: "WorldContext", stimulus: "Stimulus", topic: TopicId) -> Set[str]:
    has_subs = getattr(context, "subscriptions", None) is not None
    recipients: Set[str] = set()

    if has_subs:
        recipients |= _subs_recipients(context, stimulus, topic)

    recipients |= _get_followers(context, getattr(stimulus, "source", ""))

    if not has_subs:
        return set(context.agents.agents.keys())

    return recipients


def _mark_perceived(agent, tick: int) -> None:
    try:
        setattr(agent, "last_perception_tick", tick)
    except Exception:
        pass


def _queue_or_apply_belief_delta(context: "WorldContext", agent_id: str, agent, delta) -> None:
    """
    Phase-contract enforcement:
      - If not in consolidation and context supports queuing, queue.
      - Otherwise apply immediately.

    Note: WorldKernel CONSOLIDATE(t) is the canonical place to apply queued deltas. :contentReference[oaicite:3]{index=3}
    """
    in_consolidation = bool(getattr(context, "in_consolidation", False))
    queue_fn = getattr(context, "queue_belief_delta", None)

    if (not in_consolidation) and callable(queue_fn):
        queue_fn(agent_id, delta)
        try:
            context.analytics.log_belief_delta_queued(timestamp=context.clock.t, agent_id=agent_id, delta=delta)
        except Exception:
            pass
        return

    # If we are consolidating (or no queue available), apply.
    try:
        agent.beliefs.apply_delta(delta)
    except Exception:
        pass

    try:
        context.analytics.log_belief_update(timestamp=context.clock.t, agent_id=agent_id, delta=delta)
    except Exception:
        pass


@dataclass(order=True)
class Event(ABC):
    timestamp: int = field(compare=True)
    phase: int = field(default=int(EventPhase.ACT), compare=True)
    tie_breaker: int = field(init=False, compare=True)

    def __post_init__(self):
        self.tie_breaker = next(_event_counter)

    @abstractmethod
    def apply(self, context: "WorldContext"):
        pass


@dataclass(order=True)
class StimulusIngestionEvent(Event):
    phase: int = field(default=int(EventPhase.INGEST), init=False, compare=True)

    def apply(self, context: "WorldContext"):
        new_stimuli = context.stimulus_engine.tick(self.timestamp)
        if new_stimuli:
            for stimulus in new_stimuli:
                context.scheduler.schedule(
                    StimulusPerceptionEvent(
                        timestamp=self.timestamp,
                        stimulus_id=stimulus.id,
                    )
                )
        context.scheduler.schedule(StimulusIngestionEvent(timestamp=self.timestamp + 1))


@dataclass(order=True)
class StimulusPerceptionEvent(Event):
    phase: int = field(default=int(EventPhase.PERCEIVE), init=False, compare=True)
    stimulus_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        stimulus = context.stimulus_engine.get_stimulus(self.stimulus_id)
        if not stimulus:
            return

        topic = _stimulus_topic_id(stimulus)
        try:
            pol = _stimulus_political_salience(stimulus)
            if pol is not None and context.gsr is not None:
                current = float(getattr(context.gsr.ensure_topic(topic), "political_salience", 0.0))
                context.gsr.set_political_salience(topic, max(current, pol))
        except Exception:
            pass

        temp_content = ContentItem(
            id=stimulus.id,
            author_id=stimulus.source,
            topic=topic,
            stance=_stimulus_stance(stimulus),
            content_text=getattr(stimulus, "content_text", None),
            identity_threat=_stimulus_identity_threat(stimulus),
            media_type=getattr(stimulus, "media_type", None),
            outlet_id=getattr(stimulus, "outlet_id", None),
            community_id=getattr(stimulus, "community_id", None),
            provenance={"stimulus_id": stimulus.id, "source": stimulus.source},
        )

        recipients = _select_stimulus_recipients(context, stimulus, topic)
        for agent_id in recipients:
            agent = context.agents.get(agent_id)
            if agent:
                _mark_perceived(agent, self.timestamp)
                agent.perceive(temp_content, context, stimulus_id=stimulus.id)


@dataclass(order=True)
class AgentActionEvent(Event):
    phase: int = field(default=int(EventPhase.ACT), init=False, compare=True)
    agent_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        interaction = agent.act(tick=self.timestamp)
        if interaction:
            context.analytics.log_interaction(self.timestamp, interaction)
            context.scheduler.schedule(
                InteractionPerceptionEvent(timestamp=self.timestamp, interaction=interaction)
            )

        context.scheduler.schedule(AgentActionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))


@dataclass(order=True)
class InteractionPerceptionEvent(Event):
    phase: int = field(default=int(EventPhase.INTERACT_PERCEIVE), init=False, compare=True)
    interaction: "Interaction" = field(compare=False)

    def apply(self, context: "WorldContext"):
        from gsocialsim.policy.bandit_learner import RewardVector
        from gsocialsim.stimuli.interaction import InteractionVerb

        author = context.agents.get(self.interaction.agent_id)
        if not author:
            return

        followers = _get_followers(context, author.id)
        reward = RewardVector()
        topic: TopicId | None = None

        if self.interaction.verb == InteractionVerb.CREATE:
            content = self.interaction.original_content
            topic = content.topic
            reward.affiliation = 0.1 * len(followers)

            for follower_id in followers:
                follower = context.agents.get(follower_id)
                if follower:
                    _mark_perceived(follower, self.timestamp)
                    follower.perceive(content, context)

        elif self.interaction.verb == InteractionVerb.LIKE:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = _stimulus_topic_id(stimulus)
                reward.affiliation = 0.2

        elif self.interaction.verb == InteractionVerb.FORWARD:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = _stimulus_topic_id(stimulus)
                reward.status = 0.3

        if topic and author:
            action_key = f"{self.interaction.verb.value}_{topic}"
            author.learn(action_key, reward)


@dataclass(order=True)
class AllocateAttentionEvent(Event):
    phase: int = field(default=int(EventPhase.ALLOCATE_ATTENTION), init=False, compare=True)
    agent_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        # Reactive gate: only consider deep focus if agent perceived this tick.
        if getattr(agent, "last_perception_tick", None) != self.timestamp:
            context.scheduler.schedule(AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))
            return

        high_salience_impressions = []
        for impression in agent.recent_impressions.values():
            b = agent.beliefs.get(impression.topic)
            if b and b.salience > 0.5:
                high_salience_impressions.append(impression)

        if (
            high_salience_impressions
            and agent.budgets.deep_focus_budget >= 1
            and agent.budgets.attention_minutes >= 10
        ):
            impression_to_focus = agent.rng.choice(high_salience_impressions)
            context.scheduler.schedule(
                DeepFocusEvent(
                    timestamp=self.timestamp,
                    agent_id=self.agent_id,
                    content_id=impression_to_focus.content_id,
                    original_impression=impression_to_focus,
                )
            )

        context.scheduler.schedule(AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))


@dataclass(order=True)
class DeepFocusEvent(Event):
    """
    Contract-friendly DeepFocus:
      - may compute deltas here
      - must NOT apply belief state here unless we're in CONSOLIDATE
    """
    phase: int = field(default=int(EventPhase.DEEP_FOCUS), init=False, compare=True)
    agent_id: str = field(compare=False)
    content_id: str = field(compare=False)
    original_impression: Impression = field(compare=False)

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        if not (agent.budgets.spend(BudgetKind.ATTENTION, 10) and agent.budgets.spend(BudgetKind.DEEP_FOCUS, 1)):
            print(f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] failed Deep Focus due to insufficient budget.")
            return

        print(f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] engaged in Deep Focus on '{self.content_id}'")

        amplified_impression = Impression(
            intake_mode=IntakeMode.DEEP_FOCUS,
            content_id=self.content_id,
            topic=self.original_impression.topic,
            stance_signal=self.original_impression.stance_signal,
            emotional_valence=self.original_impression.emotional_valence + 0.3,
            arousal=self.original_impression.arousal + 0.3,
            credibility_signal=min(1.0, self.original_impression.credibility_signal + 0.2),
            identity_threat=self.original_impression.identity_threat,
            social_proof=self.original_impression.social_proof,
            relationship_strength_source=self.original_impression.relationship_strength_source,
        )

        # Note: content_author_id should be the original author, but in this legacy path
        # we only have content_id; keep behavior stable with prior code.
        content_source_id = self.original_impression.content_id

        belief_delta = agent.belief_update_engine.update(
            viewer=agent,
            content_author_id=content_source_id,
            impression=amplified_impression,
            gsr=context.gsr,
        )

        # Contract enforcement:
        _queue_or_apply_belief_delta(context, self.agent_id, agent, belief_delta)


@dataclass(order=True)
class DayBoundaryEvent(Event):
    phase: int = field(default=int(EventPhase.DAY_BOUNDARY), init=False, compare=True)

    def apply(self, context: "WorldContext"):
        for agent in context.agents.agents.values():
            agent.consolidate_daily(context)
        context.scheduler.schedule(DayBoundaryEvent(timestamp=self.timestamp + context.clock.ticks_per_day))
