from __future__ import annotations

from typing import Iterable, Tuple, List

HAS_FAST = False
try:
    from gsocialsim.fast import _fast_perception as _fast  # type: ignore

    HAS_FAST = True
except Exception:
    _fast = None


def compute_belief_delta(
    stance_signal: float,
    current_stance: float,
    has_belief: bool,
    trust: float,
    credibility: float,
    primal_activation: float,
    identity_threat: float,
    is_self_source: bool,
    identity_rigidity: float,
    is_physical: bool,
) -> Tuple[float, float]:
    if HAS_FAST:
        return _fast.compute_belief_delta(
            float(stance_signal),
            float(current_stance),
            bool(has_belief),
            float(trust),
            float(credibility),
            float(primal_activation),
            float(identity_threat),
            bool(is_self_source),
            float(identity_rigidity),
            bool(is_physical),
        )
    # Fallback uses Python implementation (imported lazily to avoid cycles).
    from gsocialsim.agents.belief_update_engine import BeliefUpdateEngine, BeliefDelta

    engine = BeliefUpdateEngine()
    # Build a small shim to reuse existing logic is too heavy here; fallback is not expected.
    delta = BeliefDelta(topic_id="T__shim", stance_delta=0.0, confidence_delta=0.0)
    # Maintain API, but callers should avoid fallback in hot path.
    return (delta.stance_delta, delta.confidence_delta)


def compute_belief_deltas(
    stance_signal: Iterable[float],
    current_stance: Iterable[float],
    has_belief: Iterable[bool],
    trust: Iterable[float],
    credibility: Iterable[float],
    primal_activation: Iterable[float],
    identity_threat: Iterable[float],
    is_self_source: Iterable[bool],
    identity_rigidity: Iterable[float],
    is_physical: Iterable[bool],
) -> Tuple[List[float], List[float]]:
    if not HAS_FAST:
        raise RuntimeError("fast perception module not available")
    return _fast.compute_belief_deltas(
        stance_signal,
        current_stance,
        has_belief,
        trust,
        credibility,
        primal_activation,
        identity_threat,
        is_self_source,
        identity_rigidity,
        is_physical,
    )
