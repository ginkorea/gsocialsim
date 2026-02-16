import heapq
from typing import List, Optional

from gsocialsim.kernel.events import Event


class EventScheduler:
    """
    A priority queue to manage and dispatch events in deterministic order.

    Ordering:
      1) timestamp
      2) phase (lower runs earlier)
      3) tie_breaker (monotonic insertion order)
    """

    def __init__(self):
        # (timestamp, phase, tie_breaker, event)
        self._queue: List[tuple[int, int, int, Event]] = []

    def schedule(self, event: Event) -> None:
        """Add an event to the queue as a tuple for robust sorting."""
        phase = int(getattr(event, "phase", 0))
        entry = (event.timestamp, phase, event.tie_breaker, event)
        heapq.heappush(self._queue, entry)

    def pop_due(self, timestamp: int) -> list[Event]:
        """Pop and return all events scheduled exactly at `timestamp` (already phase-ordered)."""
        due: list[Event] = []
        while self._queue and self._queue[0][0] == timestamp:
            _, _, _, event = heapq.heappop(self._queue)
            due.append(event)
        return due

    def get_next_event(self) -> Optional[Event]:
        """Pop the next event from the queue."""
        if not self._queue:
            return None
        return heapq.heappop(self._queue)[3]

    def is_empty(self) -> bool:
        return len(self._queue) == 0
