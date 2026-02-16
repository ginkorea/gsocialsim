import unittest
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId

class TestPhase5(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=303)
        self.agent = Agent(id=AgentId("budget_agent"), seed=304)
        # Give the agent a belief so it has something to post about
        self.agent.beliefs.update(TopicId("T5"), 1.0, 1.0, 1.0, 1.0)
        self.agent.budgets.action_bank = 2.0
        self.agent.budgets.attention_bank_minutes = 100.0
        self.agent.budgets.max_actions_per_tick = 1.0
        self.agent.budgets.reset_for_tick()
        self.kernel.agents.add_agent(self.agent)

    def test_budget_depletion_and_regeneration(self):
        """
        Verify that an agent stops acting when its budget is depleted
        and resumes after the daily budget regeneration.
        """
        print("\n--- Test: Budget Depletion and Regeneration ---")
        
        # Give the agent a small, fixed budget
        self.agent.budgets.action_bank = 2.0
        self.agent.budgets.attention_bank_minutes = 100.0
        self.agent.budgets.reset_for_tick()
        print(f"Agent starts with action_bank = {self.agent.budgets.action_bank}")

        # --- Depletion Phase ---
        # Agent should now post on every tick until budget is gone
        posts_in_first_day = 0
        # Tick 0
        if self.agent.act(self.kernel.clock.t):
            posts_in_first_day += 1
        # Tick 1
        self.agent.budgets.reset_for_tick()
        if self.agent.act(self.kernel.clock.t + 1):
            posts_in_first_day += 1

        self.agent.budgets.reset_for_tick()
        third = self.agent.act(self.kernel.clock.t + 2)

        self.assertEqual(posts_in_first_day, 2, "Agent should have posted exactly twice before running out of budget.")
        self.assertIsNone(third, "Agent should be out of action budget by the third tick.")
        print("Agent successfully depleted its action budget and stopped posting.")

        # --- Regeneration Phase ---
        # Run the kernel long enough to cross a day boundary
        ticks_to_new_day = self.kernel.clock.ticks_per_day - self.kernel.clock.tick_of_day
        self.kernel.step(ticks_to_new_day + 1)
        
        self.assertGreater(self.agent.budgets.action_bank, 0, "Agent's action bank should have been regenerated.")
        print(f"After daily cycle, agent budget regenerated to: {self.agent.budgets.action_bank:.2f}")

        # Verify agent can act again
        can_act_again = False
        for _ in range(3):
            self.agent.budgets.reset_for_tick()
            if self.agent.act(self.kernel.clock.t):
                can_act_again = True
                break
        
        self.assertTrue(can_act_again, "Agent should be able to act again after budget regeneration.")
        print("Agent can act again. Budget system is working.")

if __name__ == '__main__':
    unittest.main()
