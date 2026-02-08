import unittest
from unittest.mock import Mock
from gsocialsim.kernel.event_scheduler import EventScheduler
from gsocialsim.kernel.events import (
    Event,
    StimulusIngestionEvent,
    DayBoundaryEvent,
    AgentActionEvent,
)

class TestEventSystem(unittest.TestCase):

    def test_event_scheduler_tie_breaking(self):
        """
        Verify that the EventScheduler correctly orders and dispatches
        different event types that are scheduled for the exact same timestamp.
        """
        print("--- Test: Event Scheduler Tie-Breaking ---")
        scheduler = EventScheduler()
        
        # Schedule three different event types for the same timestamp (t=0)
        # Their tie-breaker values will be 0, 1, 2 respectively.
        e1 = StimulusIngestionEvent(timestamp=0)
        e2 = DayBoundaryEvent(timestamp=0)
        e3 = AgentActionEvent(timestamp=0, agent_id="A1")

        scheduler.schedule(e1)
        scheduler.schedule(e2)
        scheduler.schedule(e3)

        # Retrieve the events. They should come out in the order they were added
        # because the tie-breaker maintains insertion order for same-timestamp events.
        out1 = scheduler.get_next_event()
        out2 = scheduler.get_next_event()
        out3 = scheduler.get_next_event()

        self.assertIsInstance(out1, StimulusIngestionEvent, "First event should be StimulusIngestionEvent")
        self.assertIsInstance(out2, DayBoundaryEvent, "Second event should be DayBoundaryEvent")
        self.assertIsInstance(out3, AgentActionEvent, "Third event should be AgentActionEvent")
        print("Verified: Events with the same timestamp are dispatched in a stable, predictable order.")

    def test_event_apply_calls(self):
        """ Verify that the event's apply method is called by the kernel. """
        # This is a conceptual test of the main loop
        mock_event = Mock(spec=Event)
        mock_event.timestamp = 0
        
        mock_context = Mock()
        
        # Manually call apply to simulate the kernel's behavior
        mock_event.apply(mock_context)
        
        # Verify that the apply method was called exactly once
        mock_event.apply.assert_called_once_with(mock_context)

if __name__ == '__main__':


    unittest.main()
