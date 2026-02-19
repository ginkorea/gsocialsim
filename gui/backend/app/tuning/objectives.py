import numpy as np
from typing import Any


def compute_objective(name: str, tick_history: list[dict], state: dict | None) -> float:
    if name == "polarization":
        return _polarization(tick_history, state)
    elif name == "crossing_rate":
        return _crossing_rate(tick_history)
    elif name == "consumption_rate":
        return _consumption_rate(tick_history)
    elif name == "mean_belief_shift":
        return _mean_belief_shift(tick_history, state)
    elif name == "influence_gini":
        return _influence_gini(tick_history)
    else:
        return 0.0


def _polarization(tick_history: list[dict], state: dict | None) -> float:
    if tick_history:
        leans = tick_history[-1].get("leans", [])
    elif state and "agents" in state:
        leans = [a["political_lean"] for a in state["agents"]]
    else:
        return 0.0
    if not leans:
        return 0.0
    arr = np.array(leans)
    return float(np.var(arr))


def _crossing_rate(tick_history: list[dict]) -> float:
    if not tick_history:
        return 0.0
    total_deltas = sum(t.get("belief_deltas", 0) for t in tick_history)
    n_ticks = len(tick_history)
    return total_deltas / max(n_ticks, 1)


def _consumption_rate(tick_history: list[dict]) -> float:
    if not tick_history:
        return 0.0
    last = tick_history[-1]
    impressions = last.get("impressions", 0)
    consumed = last.get("consumed", 0)
    return consumed / max(impressions, 1)


def _mean_belief_shift(tick_history: list[dict], state: dict | None) -> float:
    if not tick_history or len(tick_history) < 2:
        return 0.0
    first_leans = tick_history[0].get("leans", [])
    last_leans = tick_history[-1].get("leans", [])
    if not first_leans or len(first_leans) != len(last_leans):
        return 0.0
    shifts = [abs(b - a) for a, b in zip(first_leans, last_leans)]
    return float(np.mean(shifts))


def _influence_gini(tick_history: list[dict]) -> float:
    # Approximate Gini coefficient of impressions distribution
    if not tick_history:
        return 0.0
    impressions_per_tick = [t.get("impressions", 0) for t in tick_history]
    arr = np.array(impressions_per_tick, dtype=float)
    if arr.sum() == 0:
        return 0.0
    arr = np.sort(arr)
    n = len(arr)
    index = np.arange(1, n + 1)
    return float((2 * np.sum(index * arr) - (n + 1) * np.sum(arr)) / (n * np.sum(arr)))
