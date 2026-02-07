import unittest
import io
from contextlib import redirect_stdout

from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.types import AgentId, TopicId

class TestPhase4(unittest.TestCase):

    def setUp(self):
        """
        Set up a world with a simple influence chain: A -> B -> C
        Agent A follows B, Agent B follows C.
        """
        self.kernel = WorldKernel(seed=202)
        
        self.agent_A = Agent(id=AgentId("A"), seed=203)
        self.agent_B = Agent(id=AgentId("B"), seed=204)
        self.agent_C = Agent(id=AgentId("C"), seed=205)

        self.kernel.agents.add_agent(self.agent_A)
        self.kernel.agents.add_agent(self.agent_B)
        self.kernel.agents.add_agent(self.agent_C)

        # A follows B
        self.kernel.world_context.network.graph.add_edge(
            follower=self.agent_A.id,
            followed=self.agent_B.id
        )
        # B follows C
        self.kernel.world_context.network.graph.add_edge(
            follower=self.agent_B.id,
            followed=self.agent_C.id
        )
        
        self.agent_A.budgets.action_budget = 10
        self.agent_B.budgets.action_budget = 10
        self.agent_C.budgets.action_budget = 10

    def test_autonomous_influence_chain(self):
        """
        Verify that a belief can propagate autonomously from C to B to A.
        """
        print("\n--- Test: Autonomous Influence Chain ---")
        # Seed Agent C with a strong, confident belief.
        self.topic = TopicId("T4_Chain")
        self.agent_C.beliefs.update(self.topic, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)
        print(f"Initial state: A.stance=N/A, B.stance=N/A, C.stance={self.agent_C.beliefs.get(self.topic).stance:.2f}")

        # Ensure A and B start with no belief
        self.assertIsNone(self.agent_A.beliefs.get(self.topic))
        self.assertIsNone(self.agent_B.beliefs.get(self.topic))

        # Run the simulation for enough ticks for actions to occur and propagate
        # With a 1% action chance, 300 ticks should be sufficient for C and then B to post.
        f = io.StringIO()
        with redirect_stdout(f):
            self.kernel.step(300)
        log_output = f.getvalue()

        # --- Verification ---
        print("\n--- Verifying Final States ---")
        belief_A = self.agent_A.beliefs.get(self.topic)
        belief_B = self.agent_B.beliefs.get(self.topic)
        belief_C = self.agent_C.beliefs.get(self.topic)

        # 1. C's belief should be unchanged (it's the source)
        self.assertAlmostEqual(belief_C.stance, 1.0)
        print(f"Final C Stance: {belief_C.stance:.4f} (Correct)")

        # 2. B must have been influenced by C
        self.assertIsNotNone(belief_B, "Agent B was not influenced, no belief formed.")
        self.assertGreater(belief_B.stance, 0, "Agent B's stance should have moved towards C's.")
        print(f"Final B Stance: {belief_B.stance:.4f} (Influenced by C)")
        
        # 3. A must have been influenced by B
        self.assertIsNotNone(belief_A, "Agent A was not influenced, no belief formed.")
        self.assertGreater(belief_A.stance, 0, "Agent A's stance should have moved towards B's.")
        print(f"Final A Stance: {belief_A.stance:.4f} (Influenced by B)")

        # 4. The influence on A should be less than on B, as it's second-hand
        self.assertLess(belief_A.stance, belief_B.stance, "A's stance should be less extreme than B's.")
        print("Verified: Influence propagated autonomously and diluted down the chain.")

        # 5. Check logs for the chain of events
        self.assertIn(f"Agent['B'] BeliefUpdate: Topic='{self.topic}'", log_output, "Log shows no belief update for B")
        self.assertIn(f"Agent['A'] BeliefUpdate: Topic='{self.topic}'", log_output, "Log shows no belief update for A")
        print("Verified: Log files show updates for both A and B.")

if __name__ == '__main__':
    unittest.main()
