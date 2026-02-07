from dataclasses import dataclass
from src.gsocialsim.agents.impression import Impression
from src.gsocialsim.agents.belief_state import BeliefStore, TopicId
from src.gsocialsim.social.global_social_reality import GlobalSocialReality
from src.gsocialsim.types import AgentId, ActorId

@dataclass
class BeliefDelta:
    """ Represents the calculated change to a single belief. """
    topic_id: TopicId
    stance_delta: float = 0.0
    confidence_delta: float = 0.0
    # Salience and knowledge deltas can be added later

class BeliefUpdateEngine:
    """
    Phase 3: An engine that uses social trust to modulate belief updates.
    """
    def update(
        self,
        viewer_id: AgentId,
        content_author_id: ActorId,
        belief_store: BeliefStore,
        impression: Impression,
        gsr: GlobalSocialReality,
    ) -> BeliefDelta:
        """
        Calculates belief change, scaling it by the trust between the viewer and author.
        """
        topic_id = impression.topic
        current_belief = belief_store.get(topic_id)
        
        # Get the trust from the viewer's perspective towards the author
        trust = gsr.get_relationship(viewer_id, content_author_id).trust

        if current_belief is None:
            # Agent has no opinion. New confidence is now scaled by trust.
            # A completely untrusted source (trust=0) will result in zero confidence.
            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=impression.stance_signal,
                confidence_delta=0.1 * trust # Confidence in new belief depends on trust
            )
        else:
            # Agent has an opinion.
            # The "nudge" towards the new stance is scaled by trust.
            # trust=1.0 -> 10% change, trust=0.5 -> 5% change, trust=0 -> 0% change
            base_influence_factor = 0.10
            stance_difference = impression.stance_signal - current_belief.stance
            stance_change = stance_difference * base_influence_factor * trust
            
            # Confidence increases slightly, also scaled by trust
            confidence_change = 0.02 * trust

            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=stance_change,
                confidence_delta=confidence_change
            )
