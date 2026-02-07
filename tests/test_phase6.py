import unittest
from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.types import AgentId, TopicId
from src.gsocialsim.physical.physical_world import Place, Schedule

class TestPhase6(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=404)
        self.agent_A = Agent(id=AgentId("A"), seed=405)
        self.agent_B = Agent(id=AgentId("B"), seed=406)
        self.kernel.agents.add_agent(self.agent_A)
        self.kernel.agents.add_agent(self.agent_B)
        
        # Agents do NOT follow each other online
        self.topic = TopicId("T6_Phys")
        self.agent_B.beliefs.update(self.topic, 1.0, 1.0, 1.0, 1.0)

    def test_physical_influence(self):
        """
        Verify that agents who are not connected online can only influence
        each other when they are physically co-located, and that this
        influence is significantly amplified.
        """
        print("\n--- Test: Physical Layer Influence ---")
        
        # --- Run 1: No physical proximity ---
        # Agent A should not be influenced as they are not connected to B
        self.kernel.step(100)
        self.assertIsNone(self.agent_A.beliefs.get(self.topic), "Agent A should not have been influenced yet.")
        print("Verified: No influence without social connection (online or physical).")

        # --- Run 2: With physical proximity ---
        # Define a workplace and a schedule that makes them meet
        workplace = Place(id="office", size=10)
        self.kernel.world_context.physical_world.places["office"] = workplace
        
        # Meet at tick 500 of the day
        schedule_A = Schedule(daily_plan={500: "office"})
        schedule_B = Schedule(daily_plan={500: "office"})
        self.kernel.world_context.physical_world.schedules[self.agent_A.id] = schedule_A
        self.kernel.world_context.physical_world.schedules[self.agent_B.id] = schedule_B
        
        # Run the simulation past their meeting time
        self.kernel.step(501 - self.kernel.clock.t) # Step until tick 501

        belief_A = self.agent_A.beliefs.get(self.topic)
        self.assertIsNotNone(belief_A, "Agent A should have been influenced by physical proximity.")
        
        # Default trust is 0.5. Physical multiplier is 10.
        # Stance = 1.0 (from B) * 0.5 (trust) = 0.5. With multiplier -> 5.0, capped at 1.0.
        # Confidence = 0.1 * 0.5 (trust) = 0.05. With multiplier -> 0.5
        # The exact values are less important than the fact that it's a huge jump.
        self.assertGreater(belief_A.stance, 0.99, "Physical influence should be extremely strong.")
        self.assertGreater(belief_A.confidence, 0.49, "Confidence from physical influence should be high.")
        print(f"Verified: Physical co-location led to strong influence. New stance: {belief_A.stance:.2f}")

if __name__ == '__main__':
    unittest.main()
