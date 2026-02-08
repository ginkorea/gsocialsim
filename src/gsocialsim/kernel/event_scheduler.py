import heapq
from typing import List
from gsocialsim.kernel.events import Event

class EventScheduler:
    """A priority queue to manage and dispatch events in chronological order."""
    def __init__(self):
        # The queue now stores tuples: (timestamp, tie_breaker, event_object)
        self._queue: List[tuple[int, int, Event]] = []

    def schedule(self, event: Event):
        """Add an event to the queue as a tuple for robust sorting."""
        entry = (event.timestamp, event.tie_breaker, event)
        heapq.heappush(self._queue, entry)

    def pop_due(self, timestamp: int):
        """Pop and return all events scheduled exactly at `timestamp` (in phase/order priority)."""
        due = []
        while self._queue and self._queue[0][0] == timestamp:
            _, _, event = heapq.heappop(self._queue)
            due.append(event)
        return due

    def get_next_event(self) -> Event | None:
        """Pop the next event from the queue."""
        if not self._queue:
            return None
        # The event object is the third item in the tuple
        return heapq.heappop(self._queue)[2]

    def is_empty(self) -> bool:
        return len(self._queue) == 0
