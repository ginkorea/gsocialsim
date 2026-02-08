# tests/test_phase10.py
import statistics
import unittest

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.policy.bandit_learner import RewardVector


class TestPhase10(unittest.TestCase):
    def _expected_value_for_action(self, agent: Agent, action_key: str) -> float:
        """
        Current BanditLearner stores:
          - action_counts[action_key]
          - action_rewards[action_key] as a RewardVector SUM (not average)

        Expected scalar value (as used in exploitation) is:
          (sum_reward_vector.weighted_sum(personality) / count)
        """
        policy = agent.policy
        cnt = policy.action_counts.get(action_key, 0)
        if cnt <= 0:
            return 0.0
        sum_vec = policy.action_rewards[action_key]
        return sum_vec.weighted_sum(agent.personality) / cnt

    def test_evolutionary_pressure(self):
        """
        Current model behavior check (not evolutionary selection yet):
        Under a status-rewarding environment, agents with higher 'status' personality
        weight should learn a higher expected value for the SAME action key.

        IMPORTANT: BanditLearner keys actions as "<verb>_<topic>", e.g. "create_T".
        So we train on that exact key.
        """
        print("\n--- Test: Selection Pressure via Learning (Current Model) ---")
        _ = WorldKernel(seed=707)  # kernel not strictly required for this test, but fine to construct

        topic = "T"
        action_key = f"create_{topic}"

        # Create an initial population with random personalities
        agents: list[Agent] = []
        for i in range(20):
            agent = Agent(id=AgentId(f"agent_{i}"), seed=708 + i)
            agent.personality = RewardWeights(
                affiliation=agent.rng.random(),
                status=agent.rng.random(),
            )
            # Ensure there is at least one topic so "create_T" is a plausible action
            agent.beliefs.update(topic, 1, 1, 1, 1)
            agents.append(agent)

        initial_avg_status = statistics.mean(a.personality.status for a in agents)
        print(f"Initial average 'status' personality weight: {initial_avg_status:.2f}")

        # Environment: reward is an affine function of personality.status
        # high status -> positive reward, low status -> negative reward
        for _ in range(500):
            for agent in agents:
                reward_val = agent.personality.status * 0.1 - 0.05
                agent.learn(action_key, RewardVector(status=reward_val))

        # Compare learned values between high-status and low-status subsets
        agents_sorted = sorted(agents, key=lambda a: a.personality.status)
        low = agents_sorted[:5]
        high = agents_sorted[-5:]

        low_vals = [self._expected_value_for_action(a, action_key) for a in low]
        high_vals = [self._expected_value_for_action(a, action_key) for a in high]

        low_mean = statistics.mean(low_vals)
        high_mean = statistics.mean(high_vals)

        print(f"Mean learned value (low-status 5):  {low_mean:.4f}")
        print(f"Mean learned value (high-status 5): {high_mean:.4f}")

        self.assertGreater(
            high_mean,
            low_mean,
            "Under a status-rewarding environment, higher-status agents should learn a higher value for action 'create_T'."
        )


if __name__ == "__main__":
    unittest.main()
