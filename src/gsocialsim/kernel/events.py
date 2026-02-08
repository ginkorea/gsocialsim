from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
import itertools

if TYPE_CHECKING:
    from src.gsocialsim.kernel.world_kernel import WorldContext
    from src.gsocialsim.stimuli.interaction import Interaction

_event_counter = itertools.count()

@dataclass(order=True)
class Event(ABC):
    timestamp: int = field(compare=True)
    tie_breaker: int = field(init=False, compare=True)
    def __post_init__(self): self.tie_breaker = next(_event_counter)
    @abstractmethod
    def apply(self, context: WorldContext): pass

@dataclass(order=True)
class StimulusIngestionEvent(Event):
    def apply(self, context: WorldContext):
        new_stimuli = context.stimulus_engine.tick(self.timestamp)
        if new_stimuli:
            for stimulus in new_stimuli:
                context.scheduler.schedule(StimulusPerceptionEvent(timestamp=self.timestamp, stimulus_id=stimulus.id))
        context.scheduler.schedule(StimulusIngestionEvent(timestamp=self.timestamp + 1))

@dataclass(order=True)
class StimulusPerceptionEvent(Event):
    stimulus_id: str = field(compare=False)
    def apply(self, context: WorldContext):
        stimulus = context.stimulus_engine.get_stimulus(self.stimulus_id)
        if not stimulus: return
        from src.gsocialsim.stimuli.content_item import ContentItem
        from src.gsocialsim.types import TopicId
        temp_content = ContentItem(id=stimulus.id, author_id=stimulus.source, topic=TopicId(f"stim_{stimulus.id}"), stance=0.0)
        for agent in context.agents.agents.values():
            agent.perceive(temp_content, context, stimulus_id=stimulus.id)

@dataclass(order=True)
class AgentActionEvent(Event):
    agent_id: str = field(compare=False)
    def apply(self, context: WorldContext):
        agent = context.agents.get(self.agent_id)
        if not agent: return
        interaction = agent.act(tick=self.timestamp)
        if interaction:
            context.analytics.log_interaction(self.timestamp, interaction)
            context.scheduler.schedule(InteractionPerceptionEvent(timestamp=self.timestamp, interaction=interaction))
        context.scheduler.schedule(AgentActionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))

@dataclass(order=True)
class InteractionPerceptionEvent(Event):
    interaction: Interaction = field(compare=False)
    def apply(self, context: WorldContext):
        from src.gsocialsim.policy.bandit_learner import RewardVector
        from src.gsocialsim.stimuli.interaction import InteractionVerb
        author = context.agents.get(self.interaction.agent_id)
        if not author: return
        followers = context.network.graph.get_followers(author.id)
        if not followers: return
        
        reward = RewardVector()
        topic = None

        if self.interaction.verb == InteractionVerb.CREATE:
            content = self.interaction.original_content
            topic = content.topic
            reward.affiliation = 0.1 * len(followers)
            for follower_id in followers:
                follower = context.agents.get(follower_id)
                if follower: follower.perceive(content, context)
        elif self.interaction.verb == InteractionVerb.LIKE:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = f"stim_{stimulus.id}"
                reward.affiliation = 0.2
        elif self.interaction.verb == InteractionVerb.FORWARD:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = f"stim_{stimulus.id}"
                reward.status = 0.3

        if topic and author:
            action_key = f"{self.interaction.verb.value}_{topic}"
            author.learn(action_key, reward)

@dataclass(order=True)
class DayBoundaryEvent(Event):
    def apply(self, context: WorldContext):
        for agent in context.agents.agents.values():
            agent.consolidate_daily(context)
        context.scheduler.schedule(DayBoundaryEvent(timestamp=self.timestamp + context.clock.ticks_per_day))