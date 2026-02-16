from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from gsocialsim.social.global_social_reality import GlobalSocialReality


@dataclass
class WorldContext:
    """
    Shared simulation context passed into Events and Agents.

    Phase Contract (non-negotiable):
      INGEST(t) -> ACT_BATCH(t) -> PERCEIVE_BATCH(t) -> CONSOLIDATE(t)

    Contract enforcement surface:
      - begin_phase(...) sets in_consolidation flag.
      - belief deltas computed during ACT/PERCEIVE are queued here.
      - kernel applies queued deltas only during CONSOLIDATE(t).
    """

    # Core pointers
    kernel: Optional[Any] = None
    clock: Optional[Any] = None
    agents: Optional[Any] = None

    # Optional subsystem pointers (some may exist, some may be unused by the contract kernel)
    scheduler: Optional[Any] = None
    network: Optional[Any] = None
    stimulus_engine: Optional[Any] = None
    physical_world: Optional[Any] = None
    attention_system: Optional[Any] = None
    evolutionary_system: Optional[Any] = None
    analytics: Optional[Any] = None
    gsr: GlobalSocialReality | None = None

    # Future subsystems
    subscriptions: Optional[Any] = None

    # ----------------------------
    # Phase contract state surface
    # ----------------------------
    current_tick: int = 0
    current_phase: str = "INIT"  # "INGEST" | "ACT" | "PERCEIVE" | "CONSOLIDATE"
    in_consolidation: bool = False

    # World-side per-tick buffers (contract surface)
    stimuli_by_tick: Dict[int, List[Any]] = field(default_factory=dict)
    posted_by_tick: Dict[int, List[Any]] = field(default_factory=dict)

    # Belief deferral queue: list[(agent_id, belief_delta)]
    deferred_belief_deltas: List[Tuple[str, Any]] = field(default_factory=list)

    def begin_phase(self, tick: int, phase: str) -> None:
        self.current_tick = tick
        self.current_phase = phase
        self.in_consolidation = (phase == "CONSOLIDATE")

    def clear_tick_buffers(self, tick: int) -> None:
        """
        Prevent unbounded growth for long runs.
        Keeps only current tick buffers if you call this each tick.
        """
        self.stimuli_by_tick.pop(tick, None)
        self.posted_by_tick.pop(tick, None)

    def queue_belief_delta(self, agent_id: str, delta: Any) -> None:
        self.deferred_belief_deltas.append((agent_id, delta))

    def pop_all_belief_deltas(self) -> List[Tuple[str, Any]]:
        out = list(self.deferred_belief_deltas)
        self.deferred_belief_deltas.clear()
        return out
