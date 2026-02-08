# src/gsocialsim/kernel/world_context.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from gsocialsim.social.global_social_reality import GlobalSocialReality


@dataclass
class WorldContext:
    """
    Shared simulation context passed into Events and Agents.
    Keep this intentionally lightweight: it's a container for pointers to
    subsystems (scheduler, network, physical_world, etc).

    The WorldKernel is responsible for wiring these references in __post_init__.
    """

    # Core pointers
    kernel: Optional[Any] = None
    clock: Optional[Any] = None
    agents: Optional[Any] = None

    # Required by many Events
    scheduler: Optional[Any] = None

    # Optional subsystems (present in later phases)
    network: Optional[Any] = None
    stimulus_engine: Optional[Any] = None
    physical_world: Optional[Any] = None
    attention_system: Optional[Any] = None
    evolutionary_system: Optional[Any] = None
    analytics: Optional[Any] = None
    gsr: GlobalSocialReality | None = None
