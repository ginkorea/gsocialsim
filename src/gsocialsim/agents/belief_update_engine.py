from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.agents.belief_state import TopicId
from gsocialsim.social.global_social_reality import GlobalSocialReality
from gsocialsim.types import ActorId

if TYPE_CHECKING:
    from gsocialsim.agents.agent import Agent


@dataclass
class BeliefDelta:
    topic_id: TopicId
    stance_delta: float = 0.0
    confidence_delta: float = 0.0


class BeliefUpdateEngine:
    """
    Pure delta generator.

    Phase contract note:
    - This engine must not mutate belief state.
    - It only returns a BeliefDelta; application is handled elsewhere (CONSOLIDATE).
    """

    @staticmethod
    def _clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

    def update(
        self,
        viewer: "Agent",
        content_author_id: ActorId,
        impression: Impression,
        gsr: GlobalSocialReality,
    ) -> BeliefDelta:
        topic_id = impression.topic
        current_belief = viewer.beliefs.get(topic_id)

        # Relationship trust (0..1 assumed)
        rel = gsr.get_relationship(viewer.id, content_author_id)
        trust = float(getattr(rel, "trust", 0.0))
        trust = self._clamp(trust, 0.0, 1.0)

        multiplier = 10.0 if impression.intake_mode == IntakeMode.PHYSICAL else 1.0
        # In-person interaction tends to raise perceived trust.
        trust_effect = min(1.0, trust + 0.15) if impression.intake_mode == IntakeMode.PHYSICAL else trust

        # Credibility modulates influence strength but keeps default stable at 1.0.
        credibility = float(getattr(impression, "credibility_signal", 0.5))
        credibility = self._clamp(credibility, 0.0, 1.0)
        credibility_mult = 0.5 + credibility  # 0.5..1.5, default=1.0

        # Self-source reinforcement (pondering / self-radicalization)
        is_self_source = bool(getattr(impression, "is_self_source", False))
        if is_self_source:
            multiplier *= 1.2

        # Threat signal can come from impression or test hook
        identity_threat = float(getattr(impression, "identity_threat", 0.0))
        is_threatening = bool(getattr(impression, "_is_threatening_hack", False)) or identity_threat > 0.5

        if current_belief is None:
            # Initialize beliefs conservatively (still scaled by trust)
            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=float(impression.stance_signal) * trust_effect * multiplier,
                confidence_delta=(0.1 * trust_effect * multiplier) + (0.03 * trust_effect if is_self_source else 0.0),
            )

        stance_difference = float(impression.stance_signal) - float(current_belief.stance)

        # Confirmation bias: aligned content solidifies confidence
        is_confirming = (stance_difference > 0 and current_belief.stance > 0) or (
            stance_difference < 0 and current_belief.stance < 0
        )

        # Backfire: if opposed and threatening, reverse influence and harden confidence
        is_opposed = abs(stance_difference) > 1.0

        base_influence = 0.10
        stance_change = stance_difference * base_influence * trust_effect * multiplier * credibility_mult
        confidence_change = 0.02 * trust_effect * multiplier * credibility_mult

        if is_confirming:
            stance_change *= 1.1
            confidence_change += 0.04 * trust_effect * multiplier

        if is_self_source:
            confidence_change += 0.03 * trust_effect

        if is_threatening and is_opposed:
            # push away from the threatening content and harden the belief
            stance_change = -stance_difference * base_influence * trust_effect * multiplier * 0.6
            confidence_change += 0.05 * trust_effect * multiplier
        elif is_opposed:
            # Non-hostile disagreement: allow some change if trust/credibility are high.
            openness = 1.0 - float(getattr(viewer.identity, "identity_rigidity", 0.5))
            openness = self._clamp(openness, 0.0, 1.0)
            persuasive = trust_effect * credibility_mult
            if persuasive >= 0.7:
                confidence_change -= 0.01 * (0.3 + 0.7 * openness)

        return BeliefDelta(
            topic_id=topic_id,
            stance_delta=stance_change,
            confidence_delta=confidence_change,
        )
