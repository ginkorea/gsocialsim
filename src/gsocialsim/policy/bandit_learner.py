from collections import defaultdict
import random
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

from src.gsocialsim.policy.action_policy import ActionPolicy
from src.gsocialsim.agents.reward_weights import RewardWeights
from src.gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from src.gsocialsim.stimuli.content_item import ContentItem

if TYPE_CHECKING:
    from src.gsocialsim.agents.agent import Agent

@dataclass
class RewardVector:
    status: float = 0.0
    affiliation: float = 0.0
    def __add__(self, other):
        return RewardVector(self.status + other.status, self.affiliation + other.affiliation)
    def weighted_sum(self, weights: RewardWeights) -> float:
        return self.status * weights.status + self.affiliation * weights.affiliation

class BanditLearner(ActionPolicy):
    def __init__(self, epsilon: float = 0.2):
        self.epsilon = epsilon
        self.action_counts: dict[str, int] = defaultdict(int)
        self.action_rewards: dict[str, RewardVector] = defaultdict(RewardVector)

    def _get_possible_actions(self, agent: "Agent", tick: int) -> list[Interaction]:
        actions = []
        for topic, belief in agent.beliefs.topics.items():
            content = ContentItem(id=f"C_{agent.id}_{tick}", author_id=agent.id, topic=topic, stance=belief.stance)
            actions.append(Interaction(agent_id=agent.id, verb=InteractionVerb.CREATE, original_content=content))
        for content_id in agent.recent_impressions.keys():
            actions.append(Interaction(agent_id=agent.id, verb=InteractionVerb.LIKE, target_stimulus_id=content_id))
            actions.append(Interaction(agent_id=agent.id, verb=InteractionVerb.FORWARD, target_stimulus_id=content_id))
        return actions

    def generate_interaction(self, agent: "Agent", tick: int) -> Optional[Interaction]:
        if agent.rng.random() > 0.2:
            return None
        possible_actions = self._get_possible_actions(agent, tick)
        if not possible_actions: return None

        if agent.rng.random() < self.epsilon:
            return agent.rng.choice(possible_actions)
        else:
            best_action = None
            max_expected_reward = -float('inf')
            for action in possible_actions:
                topic = action.original_content.topic if action.verb == InteractionVerb.CREATE else action.target_stimulus_id
                action_key = f"{action.verb.value}_{topic}"
                if self.action_counts[action_key] > 0:
                    avg_reward_vector = self.action_rewards[action_key]
                    expected_reward = avg_reward_vector.weighted_sum(agent.personality) / self.action_counts[action_key]
                    if expected_reward > max_expected_reward:
                        max_expected_reward = expected_reward
                        best_action = action
            return best_action if max_expected_reward > -float('inf') else agent.rng.choice(possible_actions)

    def learn(self, action_key: str, reward_vector: RewardVector):
        self.action_counts[action_key] += 1
        self.action_rewards[action_key] += reward_vector
