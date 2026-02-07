from dataclasses import dataclass, field
from typing import Dict
from collections import defaultdict
import random
import math

from src.gsocialsim.policy.action_policy import ActionPolicy
from src.gsocialsim.agents.reward_weights import RewardWeights
from src.gsocialsim.types import TopicId
from src.gsocialsim.stimuli.content_item import ContentItem

@dataclass
class RewardVector:
    status: float = 0.0
    affiliation: float = 0.0
    # ... other reward types ...

    def weighted_sum(self, weights: RewardWeights) -> float:
        return self.status * weights.status + self.affiliation * weights.affiliation

class BanditLearner(ActionPolicy):
    """
    An epsilon-greedy contextual bandit that learns which topics to post about.
    """
    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon
        self.action_counts: Dict[TopicId, int] = defaultdict(int)
        self.action_rewards: Dict[TopicId, float] = defaultdict(float)

    def generate_action(self, agent: "Agent", tick: int) -> Optional["ContentItem"]:
        if not agent.beliefs.topics:
            return None

        if agent.rng.random() < self.epsilon:
            # Explore: choose a random topic
            topic_id = agent.rng.choice(list(agent.beliefs.topics.keys()))
        else:
            # Exploit: choose the best-known topic
            avg_rewards = {
                t: self.action_rewards[t] / self.action_counts[t]
                for t in self.action_counts if self.action_counts[t] > 0
            }
            if not avg_rewards: # Handle case where no actions have been tried
                 topic_id = agent.rng.choice(list(agent.beliefs.topics.keys()))
            else:
                topic_id = max(avg_rewards, key=avg_rewards.get)

        belief = agent.beliefs.get(topic_id)
        return ContentItem(
            id=f"C_{agent.id}_{tick}",
            author_id=agent.id,
            topic=topic_id,
            stance=belief.stance
        )

    def learn(self, topic: TopicId, reward: float):
        self.action_counts[topic] += 1
        self.action_rewards[topic] += reward
