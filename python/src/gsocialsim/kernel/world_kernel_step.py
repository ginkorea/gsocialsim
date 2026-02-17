from __future__ import annotations

"""
Deprecated compatibility shim.

Older versions of the project used a manual per-tick loop in this module.
The authoritative runtime is now event-driven via WorldKernel.step().

If anything still imports WorldKernelStep or calls step() from here, it will
delegate to the WorldKernel implementation to keep day boundary ("dream") behavior correct.
"""

from dataclasses import dataclass
from typing import Optional

from gsocialsim.kernel.world_kernel import WorldKernel


@dataclass
class WorldKernelStep:
    kernel: WorldKernel

    def step(self, num_ticks: int = 1) -> None:
        self.kernel.step(num_ticks=num_ticks)
