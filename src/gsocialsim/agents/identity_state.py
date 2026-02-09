from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set, Iterable, Optional
import random

from gsocialsim.agents.impression import Impression


@dataclass
class IdentityState:
    identity_vector: List[float] = field(default_factory=lambda: [0.0] * 8)
    identity_rigidity: float = 0.5
    ingroup_labels: Set[str] = field(default_factory=set)
    taboo_boundaries: Set[str] = field(default_factory=set)

    def is_threatening(self, content_text: str) -> bool:
        """A simple check to see if content text contains taboo keywords."""
        if not content_text:
            return False
        for taboo in self.taboo_boundaries:
            if taboo in content_text.lower():
                return True
        return False

    @staticmethod
    def _clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

    @staticmethod
    def _topic_to_dim(topic: str, dims: int) -> int:
        # Deterministic mapping to a dimension (stable across runs).
        return abs(hash(topic)) % max(1, dims)

    def consolidate_from_impressions(
        self,
        impressions: Iterable[Impression],
        rng: random.Random,
        *,
        max_samples: int = 30,
    ) -> None:
        """
        "Dreaming/reflection" identity consolidation.

        Design intent:
        - Identity shifts are slow, bounded, and mediated by rigidity.
        - Threatening/intense content increases rigidity (defensive consolidation).
        - Repeated, salient topic exposure nudges identity_vector directions.

        This is not LLM-driven yet; it's a deterministic scaffold that later becomes
        partially LLM-driven without changing call sites.
        """
        imps = list(impressions)
        if not imps:
            return

        dims = len(self.identity_vector) if self.identity_vector else 8
        if not self.identity_vector:
            self.identity_vector = [0.0] * dims

        # Weighted sample of impressions for consolidation.
        def weight(imp: Impression) -> float:
            # Emphasize identity threat + arousal + social proof.
            it = float(getattr(imp, "identity_threat", 0.0))
            ar = float(getattr(imp, "arousal", 0.0))
            sp = float(getattr(imp, "social_proof", 0.0))
            return 0.2 + 0.5 * it + 0.3 * ar + 0.2 * sp

        pool = imps[:]
        weights = [max(0.0001, weight(x)) for x in pool]
        k = min(max_samples, len(pool))

        chosen: List[Impression] = []
        for _ in range(k):
            if not pool:
                break
            idx = rng.choices(range(len(pool)), weights=weights, k=1)[0]
            chosen.append(pool.pop(idx))
            weights.pop(idx)

        # Aggregate consolidation signals.
        total_w = 0.0
        threat_w = 0.0
        stance_push = [0.0] * dims

        for imp in chosen:
            topic = str(getattr(imp, "topic", ""))
            dim = self._topic_to_dim(topic, dims)

            w = max(0.0001, weight(imp))
            total_w += w

            it = float(getattr(imp, "identity_threat", 0.0))
            threat_w += w * it

            # stance_signal nudges identity direction for that topic-dimension
            s = float(getattr(imp, "stance_signal", 0.0))
            stance_push[dim] += w * s

        if total_w <= 0.0:
            return

        avg_threat = threat_w / total_w

        # Rigidity update: bounded, slow.
        # High threat -> more rigid; calm days -> slight relaxation.
        rigidity_delta = (avg_threat - 0.25) * 0.05  # small
        self.identity_rigidity = self._clamp(self.identity_rigidity + rigidity_delta, 0.05, 0.95)

        # Identity vector update: damped by rigidity (more rigid = smaller movement)
        # Step size is intentionally small.
        step = 0.03 * (1.0 - self.identity_rigidity)
        for i in range(dims):
            delta = (stance_push[i] / total_w) * step
            self.identity_vector[i] = self._clamp(self.identity_vector[i] + delta, -1.0, 1.0)

        # Optional: very light ingroup formation placeholder
        # If a dimension becomes strong, add a synthetic label.
        # (Later, LLM can generate semantically meaningful labels.)
        strong_dims = [i for i, v in enumerate(self.identity_vector) if abs(v) > 0.75]
        for i in strong_dims:
            label = f"ingroup_dim_{i}"
            if label not in self.ingroup_labels and rng.random() < 0.10:
                self.ingroup_labels.add(label)
