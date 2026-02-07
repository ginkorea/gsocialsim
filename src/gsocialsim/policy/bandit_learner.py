from collections import defaultdict
import random
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

from src.gsocialsim.policy.action_policy import ActionPolicy
from src.gsocialsim.agents.reward_weights import RewardWeights
from src.gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from src.gsocialsim.stimuli.content_item import ContentItem
from src.gsocialsim.types import TopicId

if TYPE_CHECKING:
    from src.gsocialsim.agents.agent import Agent

@dataclass
class RewardVector:
    status: float = 0.0
    affiliation: float = 0.0
    def weighted_sum(self, weights: RewardWeights) -> float:
        return self.status * weights.status + self.affiliation * weights.affiliation

class BanditLearner(ActionPolicy):
    def __init__(self, epsilon: float = 0.2):
        self.epsilon = epsilon
        self.action_counts: dict[str, int] = defaultdict(int)
        self.action_rewards: dict[str, float] = defaultdict(float)

    def generate_interaction(self, agent: "Agent", tick: int) -> Optional[Interaction]:
        if agent.rng.random() > 0.1: # 10% chance to act
            return None

        # Decide whether to interact with a remembered stimulus or create original content
        if agent.recent_exposures and agent.rng.random() < 0.7:
            # High chance to interact with something from memory
            target_id = agent.rng.choice(list(agent.recent_exposures))
            verb = agent.rng.choice([InteractionVerb.LIKE, InteractionVerb.FORWARD])
            return Interaction(agent_id=agent.id, verb=verb, target_stimulus_id=target_id)
        else:
            # Create original content
            if not agent.beliefs.topics: return None
            topic_id = agent.rng.choice(list(agent.beliefs.topics.keys()))
            belief = agent.beliefs.get(topic_id)
            content = ContentItem(
                id=f"C_{agent.id}_{tick}", author_id=agent.id,
                topic=topic_id, stance=belief.stance
            )
            return Interaction(agent_id=agent.id, verb=InteractionVerb.CREATE, original_content=content)

    def learn(self, action_key: str, reward: float):
        self.action_counts[action_key] += 1
        self.action_rewards[action_key] += reward
