import unittest
import io
from contextlib import redirect_stdout
import random

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import AgentId, ContentId, TopicId, ActorId
from gsocialsim.social.relationship_vector import RelationshipVector

class TestPhase3(unittest.TestCase):

    def setUp(self):
        """Set up a world with three agents: a viewer, a trusted author, and an untrusted author."""
        self.kernel = WorldKernel(seed=101)
        self.kernel.physical_world.enable_life_cycle = False
        
        self.viewer = Agent(id=AgentId("viewer"), seed=102)
        self.trusted_author = Agent(id=AgentId("trusted_author"), seed=103)
        self.untrusted_author = Agent(id=AgentId("untrusted_author"), seed=104)

        self.kernel.agents.add_agent(self.viewer)
        self.kernel.agents.add_agent(self.trusted_author)
        self.kernel.agents.add_agent(self.untrusted_author)
        # Ensure deterministic consumption and sufficient attention budget
        self.viewer.rng = random.Random(0)
        self.viewer.rng.random = lambda: 0.0
        self.viewer.budgets.attention_bank_minutes = 1000.0
        self.viewer.budgets.reset_for_tick()

        # Establish trust relationships
        # Viewer -> Trusted Author: High trust
        high_trust_vector = RelationshipVector(trust=0.9)
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.trusted_author.id, high_trust_vector)

        # Viewer -> Untrusted Author: Low trust
        low_trust_vector = RelationshipVector(trust=0.1)
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.untrusted_author.id, low_trust_vector)

        self.topic = TopicId("T3")

    def test_influence_is_scaled_by_trust(self):
        """
        Verify that belief updates are stronger from a trusted source than an untrusted one.
        """
        print("\n--- Test: Influence Scaled by Trust ---")
        # Viewer starts with a neutral belief
        self.viewer.beliefs.update(self.topic, stance=0.0, confidence=0.5, salience=0, knowledge=0)
        initial_stance = self.viewer.beliefs.get(self.topic).stance
        print(f"Viewer starts with belief: Stance={initial_stance:.2f}")

        # --- Case 1: Exposure to content from a TRUSTED author ---
        trusted_content = ContentItem(id=ContentId("C_trust"), author_id=self.trusted_author.id, topic=self.topic, stance=1.0)
        
        self.viewer.perceive(trusted_content, self.kernel.world_context)
        t = self.kernel.clock.t
        self.kernel.world_context.begin_phase(t, "CONSOLIDATE")
        self.kernel._consolidate(t)
        belief_after_trusted = self.viewer.beliefs.get(self.topic)
        
        print(f"After trusted content, viewer belief is: Stance={belief_after_trusted.stance:.4f}")
        # Change = (1.0 - 0.0) * 0.10 * 0.9 (trust) = 0.09
        self.assertAlmostEqual(belief_after_trusted.stance, 0.09)
        stance_change_trusted = belief_after_trusted.stance - initial_stance

        # --- Case 2: Reset and expose to content from an UNTRUSTED author ---
        self.viewer.beliefs.update(self.topic, stance=0.0, confidence=0.5, salience=0, knowledge=0) # Reset stance
        initial_stance_untrusted = self.viewer.beliefs.get(self.topic).stance
        untrusted_content = ContentItem(id=ContentId("C_untrust"), author_id=self.untrusted_author.id, topic=self.topic, stance=1.0)
        
        self.viewer.perceive(untrusted_content, self.kernel.world_context)
        t = self.kernel.clock.t
        self.kernel.world_context.begin_phase(t, "CONSOLIDATE")
        self.kernel._consolidate(t)
        belief_after_untrusted = self.viewer.beliefs.get(self.topic)

        print(f"After untrusted content, viewer belief is: Stance={belief_after_untrusted.stance:.4f}")
        # Change = (1.0 - 0.0) * 0.10 * 0.1 (trust) = 0.01
        self.assertAlmostEqual(belief_after_untrusted.stance, 0.01)
        stance_change_untrusted = belief_after_untrusted.stance - initial_stance_untrusted

        # --- Verification ---
        self.assertGreater(stance_change_trusted, stance_change_untrusted)
        print(f"Verified: Stance change from trusted source ({stance_change_trusted:.4f}) > from untrusted source ({stance_change_untrusted:.4f})")

    def test_new_belief_confidence_scaled_by_trust(self):
        """
        Verify that confidence in a newly formed belief is scaled by the source's trust.
        """
        print("\n--- Test: New Belief Confidence Scaled by Trust ---")
        # Viewer starts with no belief on the topic
        self.assertIsNone(self.viewer.beliefs.get(self.topic))

        # --- Case 1: Exposure to content from a TRUSTED author ---
        trusted_content = ContentItem(id=ContentId("C_trust"), author_id=self.trusted_author.id, topic=self.topic, stance=0.7)
        self.viewer.perceive(trusted_content, self.kernel.world_context)
        t = self.kernel.clock.t
        self.kernel.world_context.begin_phase(t, "CONSOLIDATE")
        self.kernel._consolidate(t)
        belief_from_trusted = self.viewer.beliefs.get(self.topic)
        
        print(f"New belief from trusted source: Confidence={belief_from_trusted.confidence:.4f}")
        # New confidence = 0.1 * 0.9 (trust) = 0.09
        self.assertAlmostEqual(belief_from_trusted.confidence, 0.09)

        # --- Case 2: Reset and expose to content from an UNTRUSTED author ---
        self.viewer.beliefs.topics.pop(self.topic) # Reset belief
        self.assertIsNone(self.viewer.beliefs.get(self.topic))
        untrusted_content = ContentItem(id=ContentId("C_untrust"), author_id=self.untrusted_author.id, topic=self.topic, stance=0.7)
        self.viewer.perceive(untrusted_content, self.kernel.world_context)
        t = self.kernel.clock.t
        self.kernel.world_context.begin_phase(t, "CONSOLIDATE")
        self.kernel._consolidate(t)
        belief_from_untrusted = self.viewer.beliefs.get(self.topic)

        print(f"New belief from untrusted source: Confidence={belief_from_untrusted.confidence:.4f}")
        # New confidence = 0.1 * 0.1 (trust) = 0.01
        self.assertAlmostEqual(belief_from_untrusted.confidence, 0.01)

        # --- Verification ---
        self.assertGreater(belief_from_trusted.confidence, belief_from_untrusted.confidence)
        print("Verified: Confidence in new belief is higher from a trusted source.")

if __name__ == '__main__':
    unittest.main()
