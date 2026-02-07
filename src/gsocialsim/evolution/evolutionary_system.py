from dataclasses import dataclass
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.agents.reward_weights import RewardWeights
import random

@dataclass
class Fitness:
    """Represents an agent's success in the environment."""
    # For now, fitness is simply the agent's total affiliation reward
    total_reward: float = 0.0

class EvolutionarySystem:
    def __init__(self, exit_threshold: float = -10.0, mutation_rate: float = 0.1):
        self.exit_threshold = exit_threshold
        self.mutation_rate = mutation_rate

    def should_exit(self, agent: Agent) -> bool:
        """Determines if an agent's fitness is too low."""
        # A simple model: if total reward drops too low, exit
        total_reward = sum(agent.policy.action_rewards.values())
        return total_reward < self.exit_threshold

    def reproduce(self, parent: Agent, newborn_id: str, seed: int) -> Agent:
        """Creates a new agent by inheriting and mutating a parent's personality."""
        # Inherit personality (reward weights)
        new_weights = RewardWeights(
            status=parent.personality.status,
            affiliation=parent.personality.affiliation,
            # ... copy other weights
        )

        # Mutate
        rng = random.Random(seed)
        if rng.random() < self.mutation_rate:
            new_weights.affiliation += rng.gauss(0, 0.1)
        if rng.random() < self.mutation_rate:
            new_weights.status += rng.gauss(0, 0.1)

        newborn = Agent(id=newborn_id, seed=seed)
        newborn.personality = new_weights
        newborn.beliefs.update("T", 0, 0.1, 0.1, 0) # Give newborn a default belief to be viable
        return newborn
