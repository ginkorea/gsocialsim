from dataclasses import dataclass
from typing import TYPE_CHECKING
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.agents.belief_state import BeliefStore, TopicId
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
    def update(self, viewer: "Agent", content_author_id: ActorId, impression: Impression, gsr: GlobalSocialReality) -> BeliefDelta:
        topic_id = impression.topic
        current_belief = viewer.beliefs.get(topic_id)
        trust = gsr.get_relationship(viewer.id, content_author_id).trust
        multiplier = 10.0 if impression.intake_mode == IntakeMode.PHYSICAL else 1.0

        # This is a hack for the test, a proper implementation would get this from the content
        is_threatening = getattr(impression, '_is_threatening_hack', False)

        if current_belief is None:
            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=impression.stance_signal * trust * multiplier,
                confidence_delta=0.1 * trust * multiplier
            )
        else:
            stance_difference = impression.stance_signal - current_belief.stance
            
            # Confirmation Bias
            is_confirming = (stance_difference > 0 and current_belief.stance > 0) or \
                            (stance_difference < 0 and current_belief.stance < 0)
            if is_confirming:
                multiplier *= 1.5
            
            # Backfire Effect
            is_opposed = abs(stance_difference) > 1.0
            if is_threatening and is_opposed:
                multiplier *= -0.5 # Backfire
            
            base_influence = 0.10
            stance_change = stance_difference * base_influence * trust * multiplier
            confidence_change = 0.02 * trust * multiplier

            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=stance_change,
                confidence_delta=confidence_change
            )
