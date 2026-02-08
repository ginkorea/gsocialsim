#!/usr/bin/env python3
"""
apply_phase_scheduler_patch.py

Drop this file in your repo root (gsocialsim) and run:
  python apply_phase_scheduler_patch.py

It writes a unified diff patch to a temp file and applies it using:
  1) git apply
  2) patch -p1  (fallback)

This implements:
- EventPhase + phase ordering
- Scheduler ordering: (timestamp, phase, tie_breaker)
- Agent.last_perception_tick set on perceive()
- AllocateAttentionEvent reactive gate (must have perceived this tick)
- Updates test_event_system expectations for phase ordering

If it fails, it prints stderr so you can see what mismatched.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

PATCH_TEXT = r"""diff --git a/src/gsocialsim/kernel/event_scheduler.py b/src/gsocialsim/kernel/event_scheduler.py
index 1f3c1a2..0d7a4b1 100644
--- a/src/gsocialsim/kernel/event_scheduler.py
+++ b/src/gsocialsim/kernel/event_scheduler.py
@@ -1,23 +1,24 @@
 import heapq
 from typing import List
 from gsocialsim.kernel.events import Event
 
 class EventScheduler:
     """A priority queue to manage and dispatch events in chronological order."""
     def __init__(self):
-        # The queue now stores tuples: (timestamp, tie_breaker, event_object)
-        self._queue: List[tuple[int, int, Event]] = []
+        # The queue stores tuples: (timestamp, phase, tie_breaker, event_object)
+        self._queue: List[tuple[int, int, int, Event]] = []
 
     def schedule(self, event: Event):
         """Add an event to the queue as a tuple for robust sorting."""
-        entry = (event.timestamp, event.tie_breaker, event)
+        entry = (event.timestamp, int(event.phase), event.tie_breaker, event)
         heapq.heappush(self._queue, entry)
 
     def get_next_event(self) -> Event | None:
         """Pop the next event from the queue."""
         if not self._queue:
             return None
-        # The event object is the third item in the tuple
-        return heapq.heappop(self._queue)[2]
+        # The event object is the fourth item in the tuple
+        return heapq.heappop(self._queue)[3]
 
     def is_empty(self) -> bool:
         return len(self._queue) == 0
diff --git a/src/gsocialsim/kernel/events.py b/src/gsocialsim/kernel/events.py
index 0b4f3aa..d6f4f73 100644
--- a/src/gsocialsim/kernel/events.py
+++ b/src/gsocialsim/kernel/events.py
@@ -1,19 +1,34 @@
 from __future__ import annotations
 from abc import ABC, abstractmethod
 from dataclasses import dataclass, field
 from typing import TYPE_CHECKING
 import itertools
+from enum import IntEnum
 
 from gsocialsim.agents.budget_state import BudgetKind
 from gsocialsim.stimuli.content_item import ContentItem
 from gsocialsim.agents.impression import Impression, IntakeMode
 from gsocialsim.types import TopicId
 
 if TYPE_CHECKING:
     from gsocialsim.kernel.world_kernel import WorldContext
     from gsocialsim.stimuli.interaction import Interaction
     from gsocialsim.stimuli.stimulus import Stimulus
 
 _event_counter = itertools.count()
 
+class EventPhase(IntEnum):
+    """
+    Ordering within the same simulation tick.
+    Smaller runs earlier.
+    """
+    INGEST = 10
+    PERCEIVE = 20
+    INTERACT_PERCEIVE = 30
+    ACT = 40
+    ALLOCATE_ATTENTION = 50
+    DEEP_FOCUS = 60
+
 @dataclass(order=True)
 class Event(ABC):
     timestamp: int = field(compare=True)
+    phase: int = field(default=int(EventPhase.ACT), compare=True)
     tie_breaker: int = field(init=False, compare=True)
     def __post_init__(self): self.tie_breaker = next(_event_counter)
     @abstractmethod
     def apply(self, context: "WorldContext"):
         pass
 
 @dataclass(order=True)
 class StimulusIngestionEvent(Event):
+    phase: int = field(default=int(EventPhase.INGEST), compare=True)
     def apply(self, context: "WorldContext"):
         new_stimuli = context.stimulus_engine.tick(self.timestamp)
         if new_stimuli:
             for stimulus in new_stimuli:
                 context.scheduler.schedule(StimulusPerceptionEvent(timestamp=self.timestamp, stimulus_id=stimulus.id))
         context.scheduler.schedule(StimulusIngestionEvent(timestamp=self.timestamp + 1))
 
 @dataclass(order=True)
 class StimulusPerceptionEvent(Event):
+    phase: int = field(default=int(EventPhase.PERCEIVE), compare=True)
     stimulus_id: str = field(compare=False)
     def apply(self, context: "WorldContext"):
         stimulus = context.stimulus_engine.get_stimulus(self.stimulus_id)
         if not stimulus: return
         
         temp_content = ContentItem(id=stimulus.id, author_id=stimulus.source, topic=TopicId(f"stim_{stimulus.id}"), stance=0.0)
         for agent in context.agents.agents.values():
             agent.perceive(temp_content, context, stimulus_id=stimulus.id)
 
 @dataclass(order=True)
 class AgentActionEvent(Event):
+    phase: int = field(default=int(EventPhase.ACT), compare=True)
     agent_id: str = field(compare=False)
     def apply(self, context: "WorldContext"):
         agent = context.agents.get(self.agent_id)
         if not agent: return
 
@@ -35,11 +50,12 @@ class AgentActionEvent(Event):
         context.scheduler.schedule(AgentActionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))
 
 @dataclass(order=True)
 class InteractionPerceptionEvent(Event):
+    phase: int = field(default=int(EventPhase.INTERACT_PERCEIVE), compare=True)
     interaction: "Interaction" = field(compare=False)
 
     def apply(self, context: "WorldContext"):
         from gsocialsim.policy.bandit_learner import RewardVector
         from gsocialsim.stimuli.interaction import InteractionVerb
@@ -90,6 +106,7 @@ class InteractionPerceptionEvent(Event):
             author.learn(action_key, reward)
 
 @dataclass(order=True)
 class DeepFocusEvent(Event):
+    phase: int = field(default=int(EventPhase.DEEP_FOCUS), compare=True)
     agent_id: str = field(compare=False)
     content_id: str = field(compare=False)
     original_impression: Impression = field(compare=False) # Store the impression that led to deep focus
 
@@ -141,10 +158,26 @@ class DeepFocusEvent(Event):
             print(f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] failed Deep Focus due to insufficient budget.")
 
 @dataclass(order=True)
 class AllocateAttentionEvent(Event):
+    phase: int = field(default=int(EventPhase.ALLOCATE_ATTENTION), compare=True)
     agent_id: str = field(compare=False)
     def apply(self, context: "WorldContext"):
         agent = context.agents.get(self.agent_id)
         if not agent: return
 
+        # Deep focus should be reactive: only consider deep focus if the agent perceived
+        # something at this same tick. Otherwise, just schedule next allocation tick.
+        if getattr(agent, "last_perception_tick", None) != self.timestamp:
+            context.scheduler.schedule(
+                AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id)
+            )
+            return
+
         # PRD: Triggered by salience thresholds. Consumes deep_focus_budget.
         # For this phase: if a recent impression has high salience, trigger deep focus.
         high_salience_impressions = []
         for impression in agent.recent_impressions.values():
             if agent.beliefs.get(impression.topic) and agent.beliefs.get(impression.topic).salience > 0.5: # Example threshold
                 high_salience_impressions.append(impression)
         
         if high_salience_impressions and agent.budgets.deep_focus_budget >= 1 and agent.budgets.attention_minutes >= 10:
             # Choose one high-salience impression to deep focus on
             impression_to_focus = agent.rng.choice(high_salience_impressions)
             context.scheduler.schedule(DeepFocusEvent(timestamp=self.timestamp, agent_id=self.agent_id, content_id=impression_to_focus.content_id, original_impression=impression_to_focus))
         
         # Schedule next attention allocation event (e.g., for next tick)
         context.scheduler.schedule(AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))
 
 @dataclass(order=True)
 class DayBoundaryEvent(Event):
     def apply(self, context: "WorldContext"):
         for agent in context.agents.agents.values():
             agent.consolidate_daily(context)
         context.scheduler.schedule(DayBoundaryEvent(timestamp=self.timestamp + context.clock.ticks_per_day))
diff --git a/src/gsocialsim/agents/agent.py b/src/gsocialsim/agents/agent.py
index 3f9f9c1..c5adf63 100644
--- a/src/gsocialsim/agents/agent.py
+++ b/src/gsocialsim/agents/agent.py
@@ -1,6 +1,6 @@
 from dataclasses import dataclass, field
 from typing import Optional, TYPE_CHECKING
 from collections import deque
 import random
 
@@ -33,6 +33,8 @@ class Agent:
     policy: BanditLearner = field(default_factory=BanditLearner)
     # Store the most recent impressions, keyed by content_id
     recent_impressions: dict[str, Impression] = field(default_factory=dict)
+    # Tracks whether the agent perceived anything during a given tick
+    last_perception_tick: Optional[int] = None
 
     def __post_init__(self):
         self.rng = random.Random(self.seed)
         self.budgets._rng = self.rng
 
     def perceive(self, content: ContentItem, context: "WorldContext", is_physical: bool = False, stimulus_id: Optional[str] = None):
+        self.last_perception_tick = context.clock.t
         impression = self.attention.evaluate(content, is_physical=is_physical)
         # Store the impression for potential deep focus/later action
         if impression.content_id:
             self.recent_impressions[impression.content_id] = impression
diff --git a/tests/test_event_system.py b/tests/test_event_system.py
index 8b1c3c0..6a9bb7d 100644
--- a/tests/test_event_system.py
+++ b/tests/test_event_system.py
@@ -1,12 +1,13 @@
 import unittest
 from unittest.mock import Mock
 from gsocialsim.kernel.event_scheduler import EventScheduler
 from gsocialsim.kernel.events import (
     Event,
     StimulusIngestionEvent,
     DayBoundaryEvent,
     AgentActionEvent,
+    EventPhase,
 )
 
 class TestEventSystem(unittest.TestCase):
 
     def test_event_scheduler_tie_breaking(self):
@@ -14,35 +15,44 @@ class TestEventSystem(unittest.TestCase):
         Verify that the EventScheduler correctly orders and dispatches
         different event types that are scheduled for the exact same timestamp.
         """
         print("
 --- Test: Event Scheduler Tie-Breaking ---")
         scheduler = EventScheduler()
         
         # Schedule three different event types for the same timestamp (t=0)
-        # Their tie-breaker values will be 0, 1, 2 respectively.
+        # Now ordering is by (timestamp, phase, tie_breaker).
         e1 = StimulusIngestionEvent(timestamp=0)
         e2 = DayBoundaryEvent(timestamp=0)
         e3 = AgentActionEvent(timestamp=0, agent_id="A1")
 
         scheduler.schedule(e1)
         scheduler.schedule(e2)
         scheduler.schedule(e3)
 
         # Retrieve the events.
-        # They should come out in the order they were added
-        # because the tie-breaker maintains insertion order for same-timestamp events.
+        # They should come out ordered by phase first:
+        #   INGEST (StimulusIngestionEvent) -> ACT (AgentActionEvent) -> default (DayBoundaryEvent uses ACT default unless set)
+        # DayBoundaryEvent is a system boundary event; if you later give it a specific phase,
+        # update this test accordingly.
         out1 = scheduler.get_next_event()
         out2 = scheduler.get_next_event()
         out3 = scheduler.get_next_event()
 
         self.assertIsInstance(out1, StimulusIngestionEvent, "First event should be StimulusIngestionEvent")
-        self.assertIsInstance(out2, DayBoundaryEvent, "Second event should be DayBoundaryEvent")
-        self.assertIsInstance(out3, AgentActionEvent, "Third event should be AgentActionEvent")
-        print("Verified: Events with the same timestamp are dispatched in a stable, predictable order.")
+        # AgentActionEvent has ACT phase
+        self.assertIsInstance(out2, AgentActionEvent, "Second event should be AgentActionEvent (ACT phase)")
+        # DayBoundaryEvent currently inherits default phase (ACT). If you later set DayBoundaryEvent phase,
+        # this should be updated.
+        self.assertIsInstance(out3, DayBoundaryEvent, "Third event should be DayBoundaryEvent")
+        print("Verified: Events with the same timestamp are dispatched in a stable, phase-driven order.")
 
     def test_event_apply_calls(self):
         """
         Verify that calling apply() on an event triggers its logic.
         """
"""

def _run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr

def main() -> int:
    repo_root = Path.cwd()
    tmp_patch = repo_root / ".tmp_phase_scheduler.patch"
    tmp_patch.write_text(PATCH_TEXT, encoding="utf-8")

    try:
        # Prefer git apply if available
        if shutil.which("git"):
            code, out, err = _run(["git", "apply", str(tmp_patch)])
            if code == 0:
                print("OK: applied patch with git apply")
                return 0
            print("git apply failed, trying patch -p1")
            if out.strip():
                print(out)
            if err.strip():
                print(err, file=sys.stderr)

        if shutil.which("patch"):
            code, out, err = _run(["patch", "-p1", "-i", str(tmp_patch)])
            if code == 0:
                print("OK: applied patch with patch -p1")
                return 0
            if out.strip():
                print(out)
            if err.strip():
                print(err, file=sys.stderr)

        print("ERROR: could not apply patch (no git/patch or patch did not match).", file=sys.stderr)
        print(f"Patch file left at: {tmp_patch}", file=sys.stderr)
        return 2

    finally:
        # Keep it around if something failed so you can inspect; delete on success
        pass

if __name__ == "__main__":
    raise SystemExit(main())
