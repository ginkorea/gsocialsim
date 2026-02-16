import unittest
from gsocialsim.agents.agent import Agent
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.types import AgentId, TopicId
from gsocialsim.policy.bandit_learner import RewardVector

class TestLearningPolicy(unittest.TestCase):

    def test_personality_driven_learning(self):
        """
        Verify that agents with different personalities learn to prefer
        different actions based on the rewards they receive.
        """
        print("\n--- Test: Personality-Driven Learning (Bandit) ---")
        
        # --- Setup ---
        # Agent Affiliation: High affiliation weight, low status
        agent_aff = Agent(id=AgentId("AffiliationSeeker"), seed=809)
        agent_aff.personality = RewardWeights(affiliation=1.0, status=0.1)

        # Agent Status: High status weight, low affiliation
        agent_status = Agent(id=AgentId("StatusSeeker"), seed=810)
        agent_status.personality = RewardWeights(affiliation=0.1, status=1.0)

        for agent in [agent_aff, agent_status]:
            agent.budgets.action_bank = 1000.0
            agent.budgets.attention_bank_minutes = 1000.0
            agent.budgets.reset_for_tick()
            agent.beliefs.update(TopicId("T1"), 0.1, 0.1, 0.1, 0.1)

        # Provide recent impressions so LIKE/FORWARD actions are available
        agent_aff.recent_impressions["stim_1"] = None
        agent_status.recent_impressions["stim_1"] = None

        # Seed learning: LIKE yields affiliation, FORWARD yields status
        like_key = "like_stim_1"
        forward_key = "forward_stim_1"

        for _ in range(50):
            agent_aff.learn(like_key, RewardVector(affiliation=1.0))
            agent_aff.learn(forward_key, RewardVector(status=0.2))

            agent_status.learn(like_key, RewardVector(affiliation=0.2))
            agent_status.learn(forward_key, RewardVector(status=1.0))

        # Exploitation only
        agent_aff.policy.epsilon = 0.0
        agent_status.policy.epsilon = 0.0

        interaction_aff = agent_aff.act(tick=0)
        interaction_status = agent_status.act(tick=0)

        self.assertIsNotNone(interaction_aff)
        self.assertIsNotNone(interaction_status)
        self.assertEqual(interaction_aff.verb.name, "LIKE", "AffiliationSeeker should prefer LIKE.")
        self.assertEqual(interaction_status.verb.name, "FORWARD", "StatusSeeker should prefer FORWARD.")

        print("Verified: Agents successfully learned personality-driven behaviors.")

if __name__ == '__main__':
    unittest.main()
