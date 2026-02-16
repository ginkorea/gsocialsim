import unittest
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import AgentId, TopicId
import random

class TestPhase7(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=505)
        self.viewer = Agent(id=AgentId("viewer"), seed=506)
        self.source1 = Agent(id=AgentId("source1"), seed=507)
        self.source2 = Agent(id=AgentId("source2"), seed=508)
        self.kernel.agents.add_agent(self.viewer)
        self.kernel.agents.add_agent(self.source1)
        self.kernel.agents.add_agent(self.source2)
        self.viewer.rng = random.Random(0)
        self.viewer.rng.random = lambda: 0.0
        self.viewer.budgets.attention_bank_minutes = 1000.0
        self.viewer.budgets.reset_for_tick()
        
        self.topic = TopicId("T7_Attrib")
        self.viewer.beliefs.update(self.topic, -0.2, 0.5, 0, 0) # Start with a moderately negative belief

        # Set trust to 1.0 to ensure influence is strong enough to cross the threshold
        from gsocialsim.social.relationship_vector import RelationshipVector
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.source1.id, RelationshipVector(trust=1.0))
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.source2.id, RelationshipVector(trust=1.0))


    def test_belief_crossing_and_attribution(self):
        """
        Verify that a belief crossing event is logged and that attribution
        is correctly assigned to the influencing sources.
        """
        print("\n--- Test: Belief Crossing and Attribution ---")
        
        # Capture log output across all relevant perceptions
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            # Exposure 1
            content1 = ContentItem("c1", self.source1.id, self.topic, 0.8)
            self.viewer.perceive(content1, self.kernel.world_context)
            
            # Exposure 2 (this one should trigger the crossing)
            content2 = ContentItem("c2", self.source2.id, self.topic, 1.0)
            self.viewer.perceive(content2, self.kernel.world_context)

            t = self.kernel.clock.t
            self.kernel.world_context.begin_phase(t, "CONSOLIDATE")
            self.kernel._consolidate(t)
            
        log_output = f.getvalue()

        self.assertIn("BeliefCrossing", log_output, "Belief crossing event was not logged.")
        self.assertIn(f"Topic='{self.topic}'", log_output)
        
        # Verify attribution
        self.assertIn("Attribution=", log_output)
        self.assertIn(f"'{self.source1.id}'", log_output)
        self.assertIn(f"'{self.source2.id}'", log_output)
        print("Verified: Belief crossing and attribution logged correctly.")

if __name__ == '__main__':
    unittest.main()
