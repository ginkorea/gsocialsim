from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator
from contextlib import contextmanager
import time


@dataclass
class PerfStats:
    total: float = 0.0
    count: int = 0
    max: float = 0.0
    min: float = 1.0e30

    def add(self, duration: float, count: int = 1) -> None:
        self.total += duration
        self.count += count
        if duration > self.max:
            self.max = duration
        if duration < self.min:
            self.min = duration


class PerfTracker:
    def __init__(self, enabled: bool = False, level: str = "basic") -> None:
        self.enabled = bool(enabled)
        self.level = str(level)
        self.stats: Dict[str, PerfStats] = {}

    def set_enabled(self, enabled: bool, level: str | None = None) -> None:
        self.enabled = bool(enabled)
        if level is not None:
            self.level = str(level)

    @contextmanager
    def time(self, name: str, count: int = 1) -> Iterator[None]:
        if not self.enabled:
            yield
            return
        start = time.perf_counter()
        try:
            yield
        finally:
            dur = time.perf_counter() - start
            stat = self.stats.get(name)
            if stat is None:
                stat = PerfStats()
                self.stats[name] = stat
            stat.add(dur, count=count)

    def report(self, top: int = 20) -> str:
        if not self.stats:
            return "TIMING REPORT: no data collected."
        rows = sorted(self.stats.items(), key=lambda kv: kv[1].total, reverse=True)
        lines = ["TIMING REPORT (top by total time):"]
        for name, s in rows[:top]:
            avg = s.total / s.count if s.count else 0.0
            lines.append(
                f"{name}: total={s.total:.4f}s count={s.count} avg={avg:.6f}s max={s.max:.6f}s"
            )
        return "\n".join(lines)
