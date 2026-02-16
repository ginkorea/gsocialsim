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

        # Test hook: threateningness can be attached by tests or future perception models
        is_threatening = bool(getattr(impression, "_is_threatening_hack", False))

        if current_belief is None:
            # Initialize beliefs conservatively (still scaled by trust)
            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=float(impression.stance_signal) * trust * multiplier,
                confidence_delta=0.1 * trust * multiplier,
            )

        stance_difference = float(impression.stance_signal) - float(current_belief.stance)

        # Confirmation bias: move more when confirming
        is_confirming = (stance_difference > 0 and current_belief.stance > 0) or (
            stance_difference < 0 and current_belief.stance < 0
        )
        if is_confirming:
            multiplier *= 1.5

        # Backfire: if opposed and threatening, reverse influence slightly
        is_opposed = abs(stance_difference) > 1.0
        if is_threatening and is_opposed:
            multiplier *= -0.5

        base_influence = 0.10
        stance_change = stance_difference * base_influence * trust * multiplier
        confidence_change = 0.02 * trust * multiplier

        return BeliefDelta(
            topic_id=topic_id,
            stance_delta=stance_change,
            confidence_delta=confidence_change,
        )
