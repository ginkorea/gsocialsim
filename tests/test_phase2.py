import unittest
import io
from contextlib import redirect_stdout

from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.stimuli.content_item import ContentItem
from src.gsocialsim.types import AgentId, ContentId, TopicId, ActorId

class TestPhase2(unittest.TestCase):

    def setUp(self):
        """Set up a standard world and agent for tests."""
        self.seed = 42
        self.kernel = WorldKernel(seed=self.seed)
        self.agent = Agent(id=AgentId("agent_001"), seed=self.seed + 1)
        self.kernel.agents.add_agent(self.agent)
        self.topic = TopicId("T1")

    def test_agent_forms_new_belief(self):
        """
        Verify that an agent with no prior belief forms a new one
        after being exposed to content.
        """
        print("\n--- Test: Agent Forms New Belief ---")
        # Agent starts with no belief on the topic
        self.assertIsNone(self.agent.beliefs.get(self.topic))
        print(f"Agent '{self.agent.id}' starts with no belief on topic '{self.topic}'.")

        # Create a piece of content
        content = ContentItem(
            id=ContentId("C1"),
            author_id=ActorId("author_01"),
            topic=self.topic,
            stance=0.8
        )
        print(f"Agent perceives content '{content.id}' with stance {content.stance}.")

        # Capture the log output
        f = io.StringIO()
        with redirect_stdout(f):
            # Agent perceives the content
            self.agent.perceive(content, self.kernel.world_context)
        log_output = f.getvalue()

        # Check the agent's belief state
        new_belief = self.agent.beliefs.get(self.topic)
        self.assertIsNotNone(new_belief)
        self.assertAlmostEqual(new_belief.stance, 0.8) # Stance is adopted directly
        self.assertAlmostEqual(new_belief.confidence, 0.1) # Confidence starts low
        print(f"Agent's new belief: Stance={new_belief.stance:.2f}, Confidence={new_belief.confidence:.2f}")

        # Check if the event was logged
        self.assertIn("LOG:", log_output)
        self.assertIn(f"Agent['{self.agent.id}']", log_output)
        self.assertIn(f"Topic='{self.topic}'", log_output)
        self.assertIn("StanceΔ=0.8000", log_output)
        print("Belief formation was logged successfully.")

    def test_agent_updates_existing_belief(self):
        """
        Verify that an agent with an existing belief modifies it
        after being exposed to new content.
        """
        print("\n--- Test: Agent Updates Existing Belief ---")
        # Agent starts with a contrary belief
        self.agent.beliefs.update(
            topic_id=self.topic,
            stance=-0.5,
            confidence=0.5,
            salience=0.0,
            knowledge=0.0
        )
        initial_belief = self.agent.beliefs.get(self.topic)
        print(f"Agent '{self.agent.id}' starts with belief: Stance={initial_belief.stance:.2f}, Confidence={initial_belief.confidence:.2f}")

        # Create a piece of content with an opposing stance
        content = ContentItem(
            id=ContentId("C2"),
            author_id=ActorId("author_02"),
            topic=self.topic,
            stance=1.0
        )
        print(f"Agent perceives content '{content.id}' with stance {content.stance}.")

        # Capture log output
        f = io.StringIO()
        with redirect_stdout(f):
            self.agent.perceive(content, self.kernel.world_context)
        log_output = f.getvalue()

        # Check the agent's belief state
        updated_belief = self.agent.beliefs.get(self.topic)
        self.assertIsNotNone(updated_belief)

        # The new stance should be 5% closer to the content's stance (1.0)
        # Original stance = -0.5. Difference = 1.0 - (-0.5) = 1.5.
        # Change = 1.5 * 0.05 = 0.075.
        # New stance = -0.5 + 0.075 = -0.425
        self.assertAlmostEqual(updated_belief.stance, -0.425)
        
        # Confidence should increase by a small, fixed amount (0.01)
        # New confidence = 0.5 + 0.01 = 0.51
        self.assertAlmostEqual(updated_belief.confidence, 0.51)
        print(f"Agent's updated belief: Stance={updated_belief.stance:.2f}, Confidence={updated_belief.confidence:.2f}")

        # Check if the event was logged correctly
        self.assertIn("LOG:", log_output)
        self.assertIn(f"StanceΔ={0.075:.4f}", log_output)
        self.assertIn(f"ConfΔ={0.01:.4f}", log_output)
        print("Belief update was logged successfully.")

if __name__ == '__main__':
    unittest.main()
