import unittest
from unittest.mock import Mock, patch
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.kernel.events import DeepFocusEvent, AllocateAttentionEvent
from gsocialsim.agents.impression import Impression, IntakeMode

class TestAttentionSystem(unittest.TestCase):

    def test_salience_triggers_deep_focus(self):
        """
        Verify that a high-salience impression in an agent's memory
        correctly triggers the scheduling of a DeepFocusEvent.
        """
        print("\n--- Test: Salience Triggers Deep Focus ---")
        
        # --- Setup ---
        kernel = WorldKernel(seed=1001)
        kernel.physical_world.enable_life_cycle = False
        agent = Agent(id=AgentId("test_agent"), seed=1002)
        agent.budgets.deep_focus_budget = 5
        agent.budgets.attention_minutes = 100
        agent.budgets.attention_bank_minutes = 100
        kernel.agents.add_agent(agent)

        # 1. Create a belief with high salience
        high_salience_topic = TopicId("T_IMPORTANT")
        agent.beliefs.update(high_salience_topic, stance=0.5, confidence=0.5, salience=0.9, knowledge=0.5)

        # 2. Add an impression related to that topic to the agent's memory
        impression = Impression(
            intake_mode=IntakeMode.SCROLL,
            content_id="important_stimulus",
            topic=high_salience_topic,
            stance_signal=0.6
        )
        agent.recent_impressions["important_stimulus"] = impression
        agent.last_perception_tick = 1
        
        # --- Execution ---
        # Directly call the apply method of the event
        allocate_event = AllocateAttentionEvent(timestamp=1, agent_id=agent.id)
        allocate_event.apply(kernel.world_context)

        # --- Verification ---
        # Check the scheduler's queue for a DeepFocusEvent
        found_event = False
        while not kernel.scheduler.is_empty():
            event = kernel.scheduler.get_next_event()
            if isinstance(event, DeepFocusEvent):
                found_event = True
                self.assertEqual(event.agent_id, agent.id)
                self.assertEqual(event.content_id, "important_stimulus")
                break # Stop once we've found it

        self.assertTrue(found_event, "A DeepFocusEvent should have been scheduled for the high-salience topic.")
        print("Verified: High salience correctly schedules a DeepFocusEvent.")

if __name__ == '__main__':
    unittest.main()
