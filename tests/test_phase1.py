import unittest
import datetime
from src.gsocialsim.kernel.world_kernel import WorldKernel, AgentPopulation
from src.gsocialsim.kernel.sim_clock import SimClock
from src.gsocialsim.agents.agent import Agent

class TestPhase1(unittest.TestCase):

    def test_world_kernel_initialization_and_clock_advance(self):
        print("""
--- Test: WorldKernel Initialization and Clock Advance ---""")
        seed = 42
        kernel = WorldKernel(seed=seed)

        self.assertIsInstance(kernel.clock, SimClock)
        self.assertEqual(kernel.clock.t, 0)
        self.assertEqual(kernel.clock.day, 0)
        self.assertIsInstance(kernel.agents, AgentPopulation)
        self.assertEqual(len(kernel.agents.agents), 0)

        initial_datetime = kernel.clock.get_datetime(datetime.datetime(2026, 1, 1))
        print(f"Initial simulation datetime: {initial_datetime}")

        ticks_to_advance = 100
        kernel.step(ticks_to_advance)

        self.assertEqual(kernel.clock.t, ticks_to_advance)
        self.assertEqual(kernel.clock.day, 0) # 100 minutes is less than a day (1440 min)
        self.assertEqual(kernel.clock.tick_of_day, 100)

        advanced_datetime = kernel.clock.get_datetime(datetime.datetime(2026, 1, 1))
        print(f"Simulation datetime after {ticks_to_advance} ticks: {advanced_datetime}")
        self.assertEqual(advanced_datetime, initial_datetime + datetime.timedelta(minutes=ticks_to_advance))
        print("Clock advanced successfully.")

    def test_agent_creation_and_population_management(self):
        print("""
--- Test: Agent Creation and Population Management ---""")
        seed = 123
        kernel = WorldKernel(seed=seed)

        agent1 = Agent(id="agent_001", seed=seed + 1)
        agent2 = Agent(id="agent_002", seed=seed + 2)

        agent1.beliefs.update("T1", 0, 0, 0, 0) # Give a belief to prevent IndexError
        agent2.beliefs.update("T1", 0, 0, 0, 0)
        kernel.agents.add_agent(agent1)
        kernel.agents.add_agent(agent2)

        self.assertEqual(len(kernel.agents.agents), 2)
        self.assertIn("agent_001", kernel.agents.agents)
        self.assertIn("agent_002", kernel.agents.agents)
        self.assertEqual(kernel.agents.get("agent_001"), agent1)
        print(f"Agent 'agent_001' created and added to population. Initial identity vector: {agent1.identity.identity_vector[0:3]}...")
        print(f"Agent 'agent_002' created and added to population. Initial belief topics: {agent2.beliefs.topics}")

        # Verify that agent states are initialized (even if empty)
        self.assertIsInstance(agent1.identity, type(Agent(id='temp', seed=0).identity))
        self.assertIsInstance(agent1.beliefs, type(Agent(id='temp', seed=0).beliefs))
        self.assertIsInstance(agent1.emotion, type(Agent(id='temp', seed=0).emotion))
        self.assertIsInstance(agent1.budgets, type(Agent(id='temp', seed=0).budgets))
        self.assertIsInstance(agent1.personality, type(Agent(id='temp', seed=0).personality))
        print("Agent states (identity, beliefs, emotion, budgets, personality) are initialized.")

        # Run a few steps and ensure agent state doesn't change (as no logic implemented)
        initial_agent1_identity_vector = list(agent1.identity.identity_vector)
        initial_agent2_belief_topics = dict(agent2.beliefs.topics)

        kernel.step(50)
        self.assertEqual(agent1.identity.identity_vector, initial_agent1_identity_vector)
        self.assertEqual(agent2.beliefs.topics, initial_agent2_belief_topics)
        print("Agent states remained unchanged after simulation steps (as expected for Phase 1).")

    def test_daily_budget_regeneration_initialization(self):
        print("""
--- Test: Daily Budget Regeneration Initialization ---""")
        agent_id = "test_budget_agent"
        agent_seed = 99
        agent = Agent(id=agent_id, seed=agent_seed)

        # Before regeneration, budgets are 0 (default)
        self.assertEqual(agent.budgets.attention_minutes, 0.0)
        self.assertEqual(agent.budgets.action_budget, 0.0)

        # Manually call regen_daily to test initial functionality
        agent.budgets.regen_daily()
        print(f"Budgets after first regeneration: Attention={agent.budgets.attention_minutes:.2f}, Action={agent.budgets.action_budget:.2f}")

        # Budgets should now be non-zero due to random generation
        self.assertGreater(agent.budgets.attention_minutes, 0)
        self.assertGreater(agent.budgets.action_budget, 0)
        print("Budgets regenerated successfully.")

if __name__ == '__main__':
    unittest.main()
