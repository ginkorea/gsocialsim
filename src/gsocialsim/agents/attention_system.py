from src.gsocialsim.stimuli.content_item import ContentItem
from src.gsocialsim.agents.impression import Impression, IntakeMode

class AttentionSystem:
    """
    Phase 6: Differentiates between physical and online perception.
    """
    def evaluate(self, content: ContentItem, is_physical: bool = False) -> Impression:
        # For now, we assume a simple 'scroll' intake and a direct 1-to-1 mapping
        # of content stance to the impression's stance signal.
        intake_mode = IntakeMode.PHYSICAL if is_physical else IntakeMode.SCROLL
        return Impression(
            intake_mode=intake_mode,
            content_id=content.id,
            topic=content.topic,
            stance_signal=content.stance
        )
