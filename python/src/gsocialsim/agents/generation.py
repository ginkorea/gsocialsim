from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional
import random

from gsocialsim.agents.agent import Agent
from gsocialsim.agents.identity_state import IdentityState
from gsocialsim.agents.agent import ActivityPreferences
from gsocialsim.agents.emotion_state import EmotionState
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.politics import (
    DEFAULT_POLITICAL_TOPICS,
    DIMENSIONS,
    sample_political_stance,
    overall_lean_from_dimensions,
)


@dataclass(frozen=True)
class Big5:
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float


@dataclass(frozen=True)
class MBTI:
    type_code: str  # e.g., "INTJ"


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def sample_big5(rng: random.Random) -> Big5:
    def sample(mean: float = 0.5, std: float = 0.15) -> float:
        return _clamp01(rng.gauss(mean, std))

    return Big5(
        openness=sample(),
        conscientiousness=sample(),
        extraversion=sample(),
        agreeableness=sample(),
        neuroticism=sample(),
    )


def sample_mbti(rng: random.Random, big5: Big5) -> MBTI:
    e = "E" if rng.random() < big5.extraversion else "I"
    n = "N" if rng.random() < big5.openness else "S"
    f = "F" if rng.random() < big5.agreeableness else "T"
    j = "J" if rng.random() < big5.conscientiousness else "P"
    return MBTI(type_code=f"{e}{n}{f}{j}")


def big5_to_reward_weights(big5: Big5) -> RewardWeights:
    status = _clamp01(0.3 + 0.7 * big5.extraversion + 0.2 * (1.0 - big5.agreeableness))
    affiliation = _clamp01(0.3 + 0.7 * big5.agreeableness + 0.2 * big5.extraversion)
    dominance = _clamp01(0.3 + 0.6 * big5.extraversion + 0.3 * (1.0 - big5.agreeableness))
    coherence = _clamp01(0.3 + 0.7 * big5.conscientiousness)
    novelty = _clamp01(0.3 + 0.7 * big5.openness)
    safety = _clamp01(0.3 + 0.7 * big5.neuroticism)
    effort_cost = -_clamp01(0.4 + 0.6 * big5.conscientiousness)
    return RewardWeights(
        status=status,
        affiliation=affiliation,
        dominance=dominance,
        coherence=coherence,
        novelty=novelty,
        safety=safety,
        effort_cost=effort_cost,
    )


def _stance_from_big5(rng: random.Random, big5: Big5) -> float:
    base = rng.gauss(0.0, 0.55)
    openness_scale = 0.5 + 0.5 * big5.openness
    return max(-1.0, min(1.0, base * openness_scale))


def _confidence_from_big5(big5: Big5) -> float:
    return _clamp01(0.15 + 0.45 * big5.conscientiousness + 0.25 * big5.neuroticism)


def _salience_from_big5(big5: Big5) -> float:
    return _clamp01(0.10 + 0.40 * big5.extraversion + 0.20 * big5.neuroticism)


def _knowledge_from_big5(big5: Big5) -> float:
    return _clamp01(0.10 + 0.40 * big5.openness + 0.20 * big5.conscientiousness)


def _identity_rigidity_from_big5(big5: Big5) -> float:
    rigidity = 0.2 + 0.6 * (0.5 * big5.neuroticism + 0.5 * (1.0 - big5.openness))
    return max(0.05, min(0.95, rigidity))


def _sample_political_lean(rng: random.Random) -> float:
    # Simple bimodal distribution with a moderate center mass.
    r = rng.random()
    if r < 0.45:
        mean = -0.6
    elif r < 0.90:
        mean = 0.6
    else:
        mean = 0.0
    return max(-1.0, min(1.0, rng.gauss(mean, 0.25)))


def _partisanship_from_big5(big5: Big5) -> float:
    base = 0.3 + 0.5 * (1.0 - big5.openness) + 0.2 * big5.neuroticism
    return _clamp01(base)


def _sample_political_dimensions(rng: random.Random, big5: Big5, base_lean: float) -> dict[str, float]:
    dims: dict[str, float] = {}
    # economic: conscientiousness -> more right; agreeableness -> more left
    econ = (big5.conscientiousness - 0.5) * 0.9 - (big5.agreeableness - 0.5) * 0.6
    econ += 0.4 * base_lean + rng.gauss(0.0, 0.2)
    # social: openness -> more left (negative), neuroticism -> more right (positive)
    social = (0.5 - big5.openness) * 0.9 + (big5.neuroticism - 0.5) * 0.3
    social += 0.5 * base_lean + rng.gauss(0.0, 0.2)
    # security: neuroticism -> more right, openness -> more left
    security = (big5.neuroticism - 0.5) * 0.7 + (0.5 - big5.openness) * 0.4
    security += 0.4 * base_lean + rng.gauss(0.0, 0.2)
    # environment: openness -> more left (negative)
    environment = (0.5 - big5.openness) * 0.9 + rng.gauss(0.0, 0.2)
    # culture: openness -> more left, agreeableness -> slightly left
    culture = (0.5 - big5.openness) * 0.7 + (0.5 - big5.agreeableness) * 0.2 + rng.gauss(0.0, 0.2)

    dims["economic"] = max(-1.0, min(1.0, econ))
    dims["social"] = max(-1.0, min(1.0, social))
    dims["security"] = max(-1.0, min(1.0, security))
    dims["environment"] = max(-1.0, min(1.0, environment))
    dims["culture"] = max(-1.0, min(1.0, culture))
    # ensure all known dims exist
    for d in DIMENSIONS:
        dims.setdefault(d, 0.0)
    return dims


def _sample_demographics(rng: random.Random) -> dict[str, str]:
    # Simple categorical sampling; adjust to target population distribution as needed.
    sex = rng.choices(["female", "male", "nonbinary"], weights=[0.49, 0.49, 0.02], k=1)[0]
    race = rng.choices(
        ["white", "black", "latino", "asian", "other"],
        weights=[0.60, 0.12, 0.18, 0.06, 0.04],
        k=1,
    )[0]
    age_group = rng.choices(
        ["18-29", "30-44", "45-64", "65+"],
        weights=[0.21, 0.26, 0.32, 0.21],
        k=1,
    )[0]
    return {"sex": sex, "race": race, "age_group": age_group}


def _sample_group_affiliations(rng: random.Random) -> dict[str, float]:
    groups = {}
    candidates = [
        "religious",
        "union",
        "military",
        "immigrant",
        "student",
        "parent",
        "community_org",
        "professional",
    ]
    for g in candidates:
        if rng.random() < 0.25:
            groups[g] = _clamp01(rng.gauss(0.6, 0.2))
    return groups


def _activity_preferences_from_big5(big5: Big5) -> ActivityPreferences:
    def clamp(x: float) -> float:
        return max(0.0, min(1.0, float(x)))

    read = 0.2 + 0.5 * big5.openness + 0.2 * big5.conscientiousness + 0.1 * big5.neuroticism
    write = 0.2 + 0.5 * big5.extraversion + 0.2 * big5.conscientiousness + 0.2 * (1.0 - big5.agreeableness)
    react = 0.2 + 0.6 * big5.extraversion + 0.2 * big5.agreeableness
    reflect = 0.2 + 0.6 * big5.openness + 0.2 * (1.0 - big5.extraversion) + 0.2 * big5.neuroticism
    return ActivityPreferences(
        read_propensity=clamp(read),
        write_propensity=clamp(write),
        react_propensity=clamp(react),
        reflect_propensity=clamp(reflect),
    )


def generate_agent(
    agent_id: AgentId,
    seed: int,
    topics: Iterable[TopicId],
    *,
    rng: Optional[random.Random] = None,
) -> Agent:
    local_rng = rng or random.Random(seed)
    big5 = sample_big5(local_rng)
    mbti = sample_mbti(local_rng, big5)
    base_lean = _sample_political_lean(local_rng)
    dims = _sample_political_dimensions(local_rng, big5, base_lean)
    overall_lean = overall_lean_from_dimensions(dims)

    agent = Agent(id=agent_id, seed=seed)
    agent.personality = big5_to_reward_weights(big5)
    agent.activity = _activity_preferences_from_big5(big5)

    # Identity state
    agent.identity = IdentityState(
        identity_vector=[local_rng.gauss(0.0, 0.2) for _ in range(8)],
        identity_rigidity=_identity_rigidity_from_big5(big5),
        political_lean=overall_lean,
        partisanship=_partisanship_from_big5(big5),
        political_dimensions=dims,
        demographics=_sample_demographics(local_rng),
        group_affiliations=_sample_group_affiliations(local_rng),
    )

    # Emotion state
    agent.emotion = EmotionState(
        valence=_clamp01(0.6 - 0.4 * big5.neuroticism) * 2.0 - 1.0,
        arousal=_clamp01(0.3 + 0.4 * big5.neuroticism),
        anger=_clamp01(0.2 + 0.4 * (1.0 - big5.agreeableness)),
        anxiety=_clamp01(0.2 + 0.6 * big5.neuroticism),
    )

    # Seed beliefs
    for topic in topics:
        if topic in DEFAULT_POLITICAL_TOPICS:
            stance = sample_political_stance(
                local_rng,
                lean=agent.identity.political_lean,
                dimensions=agent.identity.political_dimensions,
                partisanship=agent.identity.partisanship,
                seed=DEFAULT_POLITICAL_TOPICS[topic],
            )
        else:
            stance = _stance_from_big5(local_rng, big5)

        agent.beliefs.update(
            topic_id=topic,
            stance=stance,
            confidence=_confidence_from_big5(big5),
            salience=_salience_from_big5(big5),
            knowledge=_knowledge_from_big5(big5),
        )

    # Attach metadata for downstream use/debug
    try:
        setattr(agent, "big5", big5)
        setattr(agent, "mbti", mbti)
    except Exception:
        pass

    return agent


def generate_population(
    count: int,
    *,
    seed: int,
    topics: Iterable[TopicId],
    id_prefix: str = "agent",
) -> List[Agent]:
    rng = random.Random(seed)
    agents: List[Agent] = []
    for i in range(count):
        aid = AgentId(f"{id_prefix}_{i}")
        agents.append(generate_agent(aid, seed + i + 1, topics, rng=rng))
    return agents
