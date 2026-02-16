from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional
import random

from gsocialsim.types import TopicId
from gsocialsim.social.global_social_reality import GlobalSocialReality


DIMENSIONS = ("economic", "social", "security", "environment", "culture")


@dataclass(frozen=True)
class PoliticalTopicSeed:
    topic: TopicId
    political_salience: float
    left_anchor: float
    right_anchor: float
    dimension_weights: Dict[str, float] = field(default_factory=dict)
    center_mean: float = 0.0
    spread: float = 0.25


# Heuristic, US-centric default set. Adjust to fit your scenario.
DEFAULT_POLITICAL_TOPICS: Dict[TopicId, PoliticalTopicSeed] = {
    "T_ECONOMY": PoliticalTopicSeed("T_ECONOMY", 0.65, -0.6, 0.6, {"economic": 1.0}),
    "T_Economy": PoliticalTopicSeed("T_Economy", 0.65, -0.6, 0.6, {"economic": 1.0}),
    "T_TAXES": PoliticalTopicSeed("T_TAXES", 0.75, -0.7, 0.7, {"economic": 1.0}),
    "T_HEALTHCARE": PoliticalTopicSeed("T_HEALTHCARE", 0.70, -0.6, 0.6, {"economic": 0.4, "social": 0.4}),
    "T_IMMIGRATION": PoliticalTopicSeed("T_IMMIGRATION", 0.80, -0.7, 0.7, {"social": 0.7, "security": 0.3}),
    "T_GUNS": PoliticalTopicSeed("T_GUNS", 0.85, -0.8, 0.8, {"social": 0.6, "security": 0.4}),
    "T_ABORTION": PoliticalTopicSeed("T_ABORTION", 0.90, -0.85, 0.85, {"social": 1.0}),
    "T_CLIMATE": PoliticalTopicSeed("T_CLIMATE", 0.80, -0.7, 0.7, {"environment": 1.0}),
    "T_ENERGY": PoliticalTopicSeed("T_ENERGY", 0.60, -0.5, 0.5, {"environment": 0.5, "economic": 0.5}),
    "T_EDUCATION": PoliticalTopicSeed("T_EDUCATION", 0.55, -0.5, 0.5, {"social": 0.6, "economic": 0.4}),
    "T_CRIME": PoliticalTopicSeed("T_CRIME", 0.70, -0.6, 0.6, {"security": 0.7, "social": 0.3}),
    "T_RACE": PoliticalTopicSeed("T_RACE", 0.80, -0.7, 0.7, {"social": 0.9}),
    "T_FOREIGN_POLICY": PoliticalTopicSeed("T_FOREIGN_POLICY", 0.60, -0.5, 0.5, {"security": 0.7, "economic": 0.3}),
    "T_Politics": PoliticalTopicSeed("T_Politics", 0.90, -0.8, 0.8, {"economic": 0.4, "social": 0.4, "security": 0.2}),
    "T_POLITICS": PoliticalTopicSeed("T_POLITICS", 0.90, -0.8, 0.8, {"economic": 0.4, "social": 0.4, "security": 0.2}),
    "T_Culture": PoliticalTopicSeed("T_Culture", 0.55, -0.4, 0.4, {"culture": 1.0}),
    "T_CULTURE": PoliticalTopicSeed("T_CULTURE", 0.55, -0.4, 0.4, {"culture": 1.0}),
    "T_Security": PoliticalTopicSeed("T_Security", 0.70, -0.6, 0.6, {"security": 1.0}),
    "T_SECURITY": PoliticalTopicSeed("T_SECURITY", 0.70, -0.6, 0.6, {"security": 1.0}),
}


def seed_political_topics(
    gsr: GlobalSocialReality,
    topics: Optional[Iterable[TopicId]] = None,
) -> None:
    """
    Seed political salience defaults into GlobalSocialReality.
    If topics is provided, only seeds those.
    """
    if topics is None:
        items = DEFAULT_POLITICAL_TOPICS.values()
    else:
        items = [DEFAULT_POLITICAL_TOPICS[t] for t in topics if t in DEFAULT_POLITICAL_TOPICS]

    for seed in items:
        gsr.set_political_salience(seed.topic, seed.political_salience)


def sample_political_stance(
    rng: random.Random,
    *,
    lean: float,
    dimensions: Optional[Dict[str, float]] = None,
    partisanship: float,
    seed: PoliticalTopicSeed,
) -> float:
    """
    Sample a stance given an agent political identity and a topic seed.
    lean: [-1,1], partisanship: [0,1]
    """
    lean = effective_lean(lean, dimensions, seed)
    partisanship = max(0.0, min(1.0, float(partisanship)))

    # Center-ish agents or low-partisanship: sample around center.
    if abs(lean) < 0.15 or partisanship < 0.25:
        return max(-1.0, min(1.0, rng.gauss(seed.center_mean, seed.spread)))

    # Mostly align with lean, with small cross-pressured chance.
    if rng.random() < (0.12 * (1.0 - partisanship)):
        anchor = seed.left_anchor if lean > 0 else seed.right_anchor
    else:
        anchor = seed.left_anchor if lean < 0 else seed.right_anchor

    # Higher partisanship -> tighter around the anchor.
    spread = seed.spread * (0.65 - 0.35 * partisanship)
    return max(-1.0, min(1.0, rng.gauss(anchor, spread)))


def effective_lean(
    lean: float,
    dimensions: Optional[Dict[str, float]],
    seed: PoliticalTopicSeed,
) -> float:
    """
    Compute a topic-specific effective lean using dimension weights.
    Falls back to 1D lean if dimensions or weights are missing.
    """
    lean = max(-1.0, min(1.0, float(lean)))
    if not dimensions or not seed.dimension_weights:
        return lean

    total = 0.0
    dot = 0.0
    for dim, w in seed.dimension_weights.items():
        if w == 0.0:
            continue
        v = float(dimensions.get(dim, 0.0))
        dot += v * float(w)
        total += abs(float(w))

    if total <= 0.0:
        return lean

    return max(-1.0, min(1.0, dot / total))


def overall_lean_from_dimensions(dimensions: Dict[str, float]) -> float:
    if not dimensions:
        return 0.0
    total = 0.0
    s = 0.0
    for v in dimensions.values():
        try:
            fv = float(v)
        except Exception:
            continue
        s += fv
        total += 1.0
    if total <= 0.0:
        return 0.0
    return max(-1.0, min(1.0, s / total))
