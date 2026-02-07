import unittest
from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.types import AgentId, TopicId

class TestPhase5(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=303)
        self.agent = Agent(id=AgentId("budget_agent"), seed=304)
        # Give the agent a belief so it has something to post about
        self.agent.beliefs.update(TopicId("T5"), 1.0, 1.0, 1.0, 1.0)
        self.agent.budgets.action_budget = 2.0 # Start with a known budget
        self.kernel.agents.add_agent(self.agent)

    def test_budget_depletion_and_regeneration(self):
        """
        Verify that an agent stops acting when its budget is depleted
        and resumes after the daily budget regeneration.
        """
        print("\n--- Test: Budget Depletion and Regeneration ---")
        
        # Give the agent a small, fixed budget
        self.agent.budgets.action_budget = 2.0
        print(f"Agent starts with action_budget = {self.agent.budgets.action_budget}")

        # Mock the policy to make the test deterministic
        self.agent.policy.should_act = lambda agent: True

        # --- Depletion Phase ---
        # Agent should now post on every tick until budget is gone
        posts_in_first_day = 0
        for _ in range(2): # Should run exactly twice
            content = self.agent.act(self.kernel.clock.t)
            if content:
                posts_in_first_day += 1
        
        self.assertEqual(posts_in_first_day, 2, "Agent should have posted exactly twice before running out of budget.")
        self.assertEqual(self.agent.budgets.action_budget, 0, "Agent's action budget should be zero.")
        print("Agent successfully depleted its action budget and stopped posting.")

        # --- Regeneration Phase ---
        # Run the kernel long enough to cross a day boundary
        ticks_to_new_day = self.kernel.clock.ticks_per_day - self.kernel.clock.tick_of_day
        self.kernel.step(ticks_to_new_day + 1)
        
        self.assertGreater(self.agent.budgets.action_budget, 0, "Agent's action budget should have been regenerated.")
        print(f"After daily cycle, agent budget regenerated to: {self.agent.budgets.action_budget:.2f}")

        # Verify agent can act again
        can_act_again = False
        for _ in range(300):
             if self.agent.act(self.kernel.clock.t):
                 can_act_again = True
                 break
        
        self.assertTrue(can_act_again, "Agent should be able to act again after budget regeneration.")
        print("Agent can act again. Budget system is working.")

if __name__ == '__main__':
    unittest.main()
