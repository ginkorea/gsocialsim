from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, Optional, Set
import itertools

from gsocialsim.agents.budget_state import BudgetKind
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.types import TopicId

if TYPE_CHECKING:
    from gsocialsim.kernel.world_kernel import WorldContext
    from gsocialsim.stimuli.interaction import Interaction
    from gsocialsim.stimuli.stimulus import Stimulus

_event_counter = itertools.count()


def _stimulus_topic_id(stimulus: "Stimulus") -> TopicId:
    """
    Map a stimulus to a TopicId that agents can actually reason about.

    Rules:
      - If stimulus.metadata["topic"] is a non-empty string: use it.
      - If missing/empty: fall back to "T_Original" to preserve phase behavior.
      - If non-string: coerce to string (defensive).
    """
    raw = getattr(stimulus, "metadata", None) or {}
    t = raw.get("topic")

    if t is None:
        return TopicId("T_Original")

    if isinstance(t, str):
        t = t.strip()
        return TopicId(t if t else "T_Original")

    return TopicId(str(t))


def _get_followers(context: "WorldContext", author_id: str) -> Set[str]:
    """
    Backward compatible helper: return followers if the follow graph exists.
    """
    try:
        return set(context.network.graph.get_followers(author_id))
    except Exception:
        return set()


def _subs_recipients(context: "WorldContext", stimulus: "Stimulus", topic: TopicId) -> Set[str]:
    """
    Best-effort recipient selection from a subscription system, if present.

    We intentionally support multiple possible subscription service shapes to stay robust
    while we implement the real SubscriptionService next.

    Expected future shapes (any one of these):
      - context.subscriptions.get_subscribers(sub_type: str, target_id: str) -> Iterable[str]
      - context.subscriptions.subscribers_by_target[(sub_type, target_id)] -> set(agent_id)
      - context.subscriptions.subscribers_by_target[(sub_type.value, target_id)] -> set(agent_id)
    """
    subs = getattr(context, "subscriptions", None)
    if subs is None:
        return set()

    def _try_get(sub_type: str, target_id: Optional[str]) -> Set[str]:
        if not target_id:
            return set()

        # Method-based API
        fn = getattr(subs, "get_subscribers", None)
        if callable(fn):
            try:
                return set(fn(sub_type, target_id))
            except Exception:
                pass

        # Dict-based API
        m = getattr(subs, "subscribers_by_target", None)
        if isinstance(m, dict):
            # try common key shapes
            for key in ((sub_type, target_id), (str(sub_type), target_id)):
                try:
                    v = m.get(key)
                    if v:
                        return set(v)
                except Exception:
                    continue

        return set()

    recipients: Set[str] = set()

    # Topic subscriptions
    recipients |= _try_get("topic", str(topic))

    # Creator/outlet/community subscriptions (if present on stimulus)
    recipients |= _try_get("creator", getattr(stimulus, "creator_id", None))
    recipients |= _try_get("outlet", getattr(stimulus, "outlet_id", None))
    recipients |= _try_get("community", getattr(stimulus, "community_id", None))

    return recipients


def _select_stimulus_recipients(context: "WorldContext", stimulus: "Stimulus", topic: TopicId) -> Set[str]:
    """
    Full-capability intent: subscription-driven delivery, with follows as an additional source of eligibility.

    Backward compatibility:
      - If no subscription system exists yet, deliver to all agents (original behavior).
      - If subscription system exists but yields nobody, deliver to nobody (true gating).
    """
    has_subs = getattr(context, "subscriptions", None) is not None

    recipients: Set[str] = set()

    # Subscriptions if available
    if has_subs:
        recipients |= _subs_recipients(context, stimulus, topic)

    # Followers as a bridge / additional eligibility
    recipients |= _get_followers(context, getattr(stimulus, "source", ""))

    if not has_subs:
        # Legacy behavior: broadcast to all if we don't have subscriptions implemented yet.
        return set(context.agents.agents.keys())

    return recipients


@dataclass(order=True)
class Event(ABC):
    timestamp: int = field(compare=True)
    tie_breaker: int = field(init=False, compare=True)

    def __post_init__(self):
        self.tie_breaker = next(_event_counter)

    @abstractmethod
    def apply(self, context: "WorldContext"):
        pass


@dataclass(order=True)
class StimulusIngestionEvent(Event):
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
    stimulus_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        stimulus = context.stimulus_engine.get_stimulus(self.stimulus_id)
        if not stimulus:
            return

        topic = _stimulus_topic_id(stimulus)

        temp_content = ContentItem(
            id=stimulus.id,
            author_id=stimulus.source,
            topic=topic,
            stance=0.0,
            media_type=getattr(stimulus, "media_type", None),
            outlet_id=getattr(stimulus, "outlet_id", None),
            community_id=getattr(stimulus, "community_id", None),
            provenance={
                "stimulus_id": stimulus.id,
                "source": stimulus.source,
            },
        )

        recipients = _select_stimulus_recipients(context, stimulus, topic)
        for agent_id in recipients:
            agent = context.agents.get(agent_id)
            if agent:
                # Keep Agent.perceive signature unchanged for now.
                agent.perceive(temp_content, context, stimulus_id=stimulus.id)


@dataclass(order=True)
class AgentActionEvent(Event):
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
        context.scheduler.schedule(
            AgentActionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id)
        )


@dataclass(order=True)
class InteractionPerceptionEvent(Event):
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
class DeepFocusEvent(Event):
    agent_id: str = field(compare=False)
    content_id: str = field(compare=False)
    original_impression: Impression = field(compare=False)  # Store the impression that led to deep focus

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        if agent.budgets.spend(BudgetKind.ATTENTION, 10) and agent.budgets.spend(
            BudgetKind.DEEP_FOCUS, 1
        ):
            print(
                f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] engaged in Deep Focus on '{self.content_id}'"
            )

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

            content_source_id = self.original_impression.content_id

            belief_delta = agent.belief_update_engine.update(
                viewer=agent,
                content_author_id=content_source_id,
                impression=amplified_impression,
                gsr=context.gsr,
            )

            agent.beliefs.apply_delta(belief_delta)
            context.analytics.log_belief_update(
                timestamp=self.timestamp, agent_id=self.agent_id, delta=belief_delta
            )
        else:
            print(
                f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] failed Deep Focus due to insufficient budget."
            )


@dataclass(order=True)
class AllocateAttentionEvent(Event):
    agent_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        high_salience_impressions = []
        for impression in agent.recent_impressions.values():
            if agent.beliefs.get(impression.topic) and agent.beliefs.get(impression.topic).salience > 0.5:
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

        context.scheduler.schedule(
            AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id)
        )


@dataclass(order=True)
class DayBoundaryEvent(Event):
    def apply(self, context: "WorldContext"):
        for agent in context.agents.agents.values():
            agent.consolidate_daily(context)
        context.scheduler.schedule(
            DayBoundaryEvent(timestamp=self.timestamp + context.clock.ticks_per_day)
        )
