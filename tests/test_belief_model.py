import unittest
from unittest.mock import patch
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.relationship_vector import RelationshipVector
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.agents.belief_update_engine import BeliefUpdateEngine

class TestBeliefModel(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=909)
        self.kernel.physical_world.enable_life_cycle = False
        self.viewer = Agent(id=AgentId("viewer"), seed=910)
        self.source = Agent(id=AgentId("source"), seed=911)
        self.topic = TopicId("T_Bias")
        self.kernel.agents.add_agent(self.viewer)
        self.kernel.agents.add_agent(self.source)
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.source.id, RelationshipVector(trust=1.0))

    def test_confirmation_bias(self):
        print("\n--- Test: Confirmation Bias ---")
        impression = Impression(IntakeMode.SCROLL, "c1", self.topic, 0.3)
        engine = self.viewer.belief_update_engine

        # Baseline (opposing) - multiplier should be 1.0
        self.viewer.beliefs.update(self.topic, stance=-0.1, confidence=0.5, salience=0, knowledge=0)
        with patch.object(engine, 'update', wraps=engine.update) as spy:
            delta_base = spy(self.viewer, self.source.id, impression, self.kernel.world_context.gsr)
            # We can't directly inspect the multiplier, so we check the output
            expected_base_change = (0.3 - (-0.1)) * 0.10 * 1.0 # stance_diff * base_influence * multiplier
            self.assertAlmostEqual(delta_base.stance_delta, expected_base_change)
            print(f"Baseline stance change (no bias): {delta_base.stance_delta:.4f}")

        # Confirmation (aligned) - multiplier should be 1.5
        self.viewer.beliefs.update(self.topic, stance=0.1, confidence=0.5, salience=0, knowledge=0)
        with patch.object(engine, 'update', wraps=engine.update) as spy:
            delta_confirm = spy(self.viewer, self.source.id, impression, self.kernel.world_context.gsr)
            expected_confirm_change = (0.3 - 0.1) * 0.10 * 1.5 # stance_diff * base_influence * multiplier
            self.assertAlmostEqual(delta_confirm.stance_delta, expected_confirm_change)
            print(f"Confirming stance change (with bias): {delta_confirm.stance_delta:.4f}")
        
        print("Verified: Confirmation bias logic is applying the correct multiplier.")

    def test_backfire_effect(self):
        print("\n--- Test: Backfire Effect ---")
        self.viewer.beliefs.update(self.topic, stance=0.8, confidence=0.9, salience=0, knowledge=0)
        impression_threatening = Impression(IntakeMode.SCROLL, "c2", self.topic, -0.8)
        setattr(impression_threatening, '_is_threatening_hack', True)

        initial_stance = self.viewer.beliefs.get(self.topic).stance
        delta = self.viewer.belief_update_engine.update(self.viewer, self.source.id, impression_threatening, self.kernel.world_context.gsr)
        
        self.assertGreater(delta.stance_delta, 0, "Stance delta should be positive (repulsion).")
        print("Verified: Backfire effect works.")

if __name__ == '__main__':
    unittest.main()
