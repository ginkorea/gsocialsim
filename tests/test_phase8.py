import unittest
from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.agents.reward_weights import RewardWeights
from src.gsocialsim.types import AgentId, TopicId

class TestPhase8(unittest.TestCase):

    def test_bandit_learner(self):
        """
        Verify that an agent learns to prefer actions that align with its personality.
        """
        print("\n--- Test: Reinforcement Learning (Bandit) ---")
        kernel = WorldKernel(seed=606)
        
        # Agent with personality that strongly values affiliation
        agent = Agent(id=AgentId("learner"), seed=607)
        agent.personality = RewardWeights(affiliation=1.0, status=0.0)
        
        # Agent has two topics to talk about
        good_topic = TopicId("T_good")
        bad_topic = TopicId("T_bad")
        agent.beliefs.update(good_topic, 1, 1, 1, 1)
        agent.beliefs.update(bad_topic, 1, 1, 1, 1)
        agent.budgets.action_budget = 1000 # Give plenty of budget

        kernel.agents.add_agent(agent)
        
        # Mock the decision to act to make the test deterministic
        agent.policy.should_act = lambda agent: True
        
        # Mock the reward generation to give affiliation reward only for the good topic
        original_learn = agent.learn
        def mock_learn(topic, reward_vector):
            # The bandit uses epsilon-greedy, so we need to run it for a bit to learn
            if topic == good_topic:
                reward_vector.affiliation = 1.0
            else:
                reward_vector.affiliation = -1.0 # Give negative reward for the bad topic
            original_learn(topic, reward_vector)
        agent.learn = mock_learn

        # Run the simulation for many steps to allow for learning
        for i in range(100): # More than enough to learn
            content = agent.act(kernel.clock.t + i)
            if content:
                from src.gsocialsim.policy.bandit_learner import RewardVector
                agent.learn(content.topic, RewardVector())
        
        # After learning, disable exploration (epsilon=0) to check exploitation
        agent.policy.epsilon = 0.0
        post_counts = {good_topic: 0, bad_topic: 0}
        for i in range(100):
            content = agent.act(kernel.clock.t + i)
            if content:
                post_counts[content.topic] += 1
        
        self.assertGreater(post_counts[good_topic], post_counts[bad_topic], "Agent should have learned to prefer the rewarding topic.")
        self.assertEqual(post_counts[bad_topic], 0, "Agent should not choose the negatively rewarded topic in exploitation mode.")
        print(f"Verified: Agent learned to prefer the good topic. Posts (good/bad): {post_counts['T_good']}/{post_counts['T_bad']}")

if __name__ == '__main__':
    unittest.main()
