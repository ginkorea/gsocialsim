import unittest

from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.types import AgentId, TopicId
from src.gsocialsim.kernel.events import DeepFocusEvent, AllocateAttentionEvent
from src.gsocialsim.stimuli.content_item import ContentItem


class TestAttentionSystem(unittest.TestCase):
    def setUp(self):
        self.kernel = WorldKernel(seed=1000)
        self.agent = Agent(id=AgentId("test_agent"), seed=1001)

        # Budgets to spend
        self.agent.budgets.deep_focus_budget = 5
        self.agent.budgets.attention_minutes = 100

        # Belief: high salience so AllocateAttentionEvent deterministically chooses deep focus
        self.high_salience_topic = TopicId("T_Focus_High")
        self.agent.beliefs.update(
            self.high_salience_topic,
            stance=0.0,
            confidence=0.1,
            salience=0.8,
            knowledge=0.1,
        )

        self.kernel.agents.add_agent(self.agent)
        self.kernel.start()  # kernel boot may seed events

        # IMPORTANT: isolate this unit test from whatever the kernel seeds at T=0
        # so we don't accidentally "eat ourselves" by popping/rescheduling the same earliest event.
        self.kernel.world_context.scheduler._queue.clear()

    def test_deep_focus_event_scheduling_and_cost(self):
        print("\n--- Test: Deep Focus Event Scheduling and Cost ---")
        initial_deep_focus_budget = self.agent.budgets.deep_focus_budget
        initial_attention_budget = self.agent.budgets.attention_minutes

        # --- Ensure agent has a recent impression with high salience for DeepFocusEvent to pick ---
        content_id = "stim_test1"
        stimulus_content = ContentItem(
            id=content_id,
            author_id="SourceX",
            topic=self.high_salience_topic,
            stance=0.5,
        )

        # Directly populate recent_impressions for the agent
        self.agent.perceive(stimulus_content, self.kernel.world_context, stimulus_id=content_id)
        self.assertIn(content_id, self.agent.recent_impressions)
        print(f"Agent has recent impression for '{content_id}'.")

        # --- Trigger AllocateAttentionEvent, expecting it to schedule a DeepFocusEvent ---
        allocate_event = AllocateAttentionEvent(timestamp=1, agent_id=self.agent.id)
        allocate_event.apply(self.kernel.world_context)

        # --- Verify DeepFocusEvent was scheduled WITHOUT popping/rescheduling ---
        # Scheduler stores tuples like (timestamp, tie_breaker, event).
        deep_focus_event = next(
            (
                entry[2]
                for entry in self.kernel.world_context.scheduler._queue
                if isinstance(entry[2], DeepFocusEvent) and entry[2].agent_id == self.agent.id
            ),
            None,
        )

        self.assertIsNotNone(deep_focus_event, "DeepFocusEvent should have been scheduled.")

        # Apply the deep focus event to test its effects
        deep_focus_event.apply(self.kernel.world_context)

        # --- Verify budgets were spent ---
        self.assertEqual(
            self.agent.budgets.deep_focus_budget,
            initial_deep_focus_budget - 1,
            "Deep focus budget should have decreased by 1.",
        )
        self.assertEqual(
            self.agent.budgets.attention_minutes,
            initial_attention_budget - 10,
            "Attention minutes should have decreased by 10.",
        )
        print("Verified: DeepFocusEvent scheduled, applied, and budgets correctly spent.")


if __name__ == "__main__":
    unittest.main()
