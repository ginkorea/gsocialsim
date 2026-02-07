from src.gsocialsim.stimuli.content_item import ContentItem
from src.gsocialsim.agents.impression import Impression, IntakeMode

class AttentionSystem:
    """
    Phase 2: A very simple system that directly translates a ContentItem
    into an Impression without any complex filtering or cognitive modeling.
    """
    def evaluate(self, content: ContentItem) -> Impression:
        # For now, we assume a simple 'scroll' intake and a direct 1-to-1 mapping
        # of content stance to the impression's stance signal.
        return Impression(
            intake_mode=IntakeMode.SCROLL,
            content_id=content.id,
            topic=content.topic,
            stance_signal=content.stance
        )
