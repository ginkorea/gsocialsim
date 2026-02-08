from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
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

    IMPORTANT:
      In this codebase TopicId may be a typing alias / NewType and not a runtime
      type suitable for isinstance(..., TopicId). So we do NOT type-check it.

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
        )
        for agent in context.agents.agents.values():
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

        followers = context.network.graph.get_followers(author.id)
        if not followers:
            return

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

            # Re-process the original impression with amplified effect
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

            # Apply the deep impression directly to the agent's belief
            content_source_id = self.original_impression.content_id  # Using content_id as source for simplicity

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
