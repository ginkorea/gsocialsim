from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode

class AttentionSystem:
    """
    Generates Impressions from ContentItems, now with more detail.
    """
    def evaluate(self, content: ContentItem, is_physical: bool = False) -> Impression:
        # For now, we'll set default values for the new fields.
        # In an LLM phase, these would be derived from content_text.
        intake_mode = IntakeMode.PHYSICAL if is_physical else IntakeMode.SCROLL
        return Impression(
            intake_mode=intake_mode,
            content_id=content.id,
            topic=content.topic,
            stance_signal=content.stance,
            emotional_valence=0.0, # Placeholder
            arousal=0.0,         # Placeholder
            credibility_signal=0.5, # Placeholder
            identity_threat=0.0, # Placeholder
            social_proof=0.0,    # Placeholder
            relationship_strength_source=0.0 # Placeholder
        )