import io
import unittest
from contextlib import redirect_stdout
import random

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId, ContentId, ActorId
from gsocialsim.stimuli.content_item import ContentItem


class TestPhase6(unittest.TestCase):
    def setUp(self):
        self.kernel = WorldKernel(seed=505)

        self.agent_A = Agent(id=AgentId("agent_A"), seed=506)
        self.agent_B = Agent(id=AgentId("agent_B"), seed=507)

        # Seed B with a belief so it has something meaningful to communicate.
        self.topic = TopicId("T6_Physical")
        self.agent_B.beliefs.update(self.topic, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)

        self.kernel.agents.add_agent(self.agent_A)
        self.kernel.agents.add_agent(self.agent_B)
        self.agent_A.budgets.action_bank = 0.0
        self.agent_A.budgets.action_budget = 0.0
        self.agent_B.budgets.action_bank = 0.0
        self.agent_B.budgets.action_budget = 0.0
        self.agent_B.budgets.attention_bank_minutes = 1.0
        self.agent_A.rng = random.Random(0)
        self.agent_A.rng.random = lambda: 0.0
        self.agent_A.budgets.attention_bank_minutes = 1000.0
        self.agent_A.budgets.reset_for_tick()

    def test_physical_influence(self):
        """
        Current model: "physical proximity influence" is tested by delivering a perception
        with is_physical=True to simulate a co-located interaction.
        We do NOT depend on the kernel to autonomously schedule meetings yet.
        """
        print("\n--- Test: Physical Layer Influence ---")

        # --- Run 1: No proximity / no delivery ---
        self.kernel.step(1)
        self.assertIsNone(self.agent_A.beliefs.get(self.topic), "Agent A should not have been influenced yet.")
        print("Verified: No influence without an interaction delivery event.")

        # --- Run 2: With physical proximity ---
        content = ContentItem(
            id=ContentId("C_phys_1"),
            author_id=ActorId(str(self.agent_B.id)),
            topic=self.topic,
            stance=1.0,
        )

        f = io.StringIO()
        with redirect_stdout(f):
            # Key point: is_physical=True triggers the physical amplification path (if implemented).
            self.agent_A.perceive(content, self.kernel.world_context, is_physical=True)
            t = self.kernel.clock.t
            self.kernel.world_context.begin_phase(t, "CONSOLIDATE")
            self.kernel._consolidate(t)

        belief_A = self.agent_A.beliefs.get(self.topic)
        self.assertIsNotNone(belief_A, "Agent A should have been influenced by physical proximity.")
        print(f"Agent A formed belief via physical proximity: stance={belief_A.stance:.3f}, conf={belief_A.confidence:.3f}")

        # Keep this assertion loose but meaningful.
        self.assertGreater(
            belief_A.confidence, 0.0,
            "Physical influence should result in a non-zero confidence belief."
        )


if __name__ == "__main__":
    unittest.main()
