from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional
import random

from gsocialsim.agents.agent import Agent
from gsocialsim.agents.identity_state import IdentityState
from gsocialsim.agents.emotion_state import EmotionState
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.types import AgentId, TopicId


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

    agent = Agent(id=agent_id, seed=seed)
    agent.personality = big5_to_reward_weights(big5)

    # Identity state
    agent.identity = IdentityState(
        identity_vector=[local_rng.gauss(0.0, 0.2) for _ in range(8)],
        identity_rigidity=_identity_rigidity_from_big5(big5),
        political_lean=_sample_political_lean(local_rng),
        partisanship=_partisanship_from_big5(big5),
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
        agent.beliefs.update(
            topic_id=topic,
            stance=_stance_from_big5(local_rng, big5),
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
