from __future__ import annotations

from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.stimuli.stimulus import MediaType


class AttentionSystem:
    """
    Generates Impressions from ContentItems.

    New behavior (still deterministic):
      - Attach media_type to impressions
      - Provide consumed_prob and interact_prob based on media_type and intake_mode

    NOTE: We are not sampling here (no RNG). Sampling/gating belongs in Agent.perceive()
    so it can be deterministic per-agent and logged properly.
    """

    # Baseline: "more people read news, more people interact with social"
    _BASE_CONSUME = {
        MediaType.NEWS: 0.85,
        MediaType.SOCIAL_POST: 0.65,
        MediaType.VIDEO: 0.60,
        MediaType.MEME: 0.55,
        MediaType.LONGFORM: 0.50,
        MediaType.FORUM_THREAD: 0.45,
        MediaType.UNKNOWN: 0.60,
    }

    _BASE_INTERACT = {
        MediaType.NEWS: 0.08,
        MediaType.SOCIAL_POST: 0.28,
        MediaType.VIDEO: 0.18,
        MediaType.MEME: 0.22,
        MediaType.LONGFORM: 0.10,
        MediaType.FORUM_THREAD: 0.16,
        MediaType.UNKNOWN: 0.15,
    }

    # Intake mode modifiers (seek/physical tends to increase consumption; deep focus maxes it)
    _INTAKE_CONSUME_MULT = {
        IntakeMode.SCROLL: 1.00,
        IntakeMode.SEEK: 1.15,
        IntakeMode.PHYSICAL: 1.20,
        IntakeMode.DEEP_FOCUS: 1.40,
    }

    _INTAKE_INTERACT_MULT = {
        IntakeMode.SCROLL: 1.00,
        IntakeMode.SEEK: 0.90,        # seeking is often info-driven, less performative
        IntakeMode.PHYSICAL: 0.75,    # physical “interaction” is modeled separately later
        IntakeMode.DEEP_FOCUS: 0.60,  # deep focus is processing-heavy, not engagement-heavy
    }

    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def evaluate(self, content: ContentItem, is_physical: bool = False) -> Impression:
        # Intake mode selection is still backward compatible.
        intake_mode = IntakeMode.PHYSICAL if is_physical else IntakeMode.SCROLL

        # Determine media type robustly.
        mt = getattr(content, "media_type", MediaType.UNKNOWN)
        if not isinstance(mt, MediaType):
            try:
                mt = MediaType.from_any(mt)
            except Exception:
                mt = MediaType.UNKNOWN

        base_consume = self._BASE_CONSUME.get(mt, self._BASE_CONSUME[MediaType.UNKNOWN])
        base_interact = self._BASE_INTERACT.get(mt, self._BASE_INTERACT[MediaType.UNKNOWN])

        consume_mult = self._INTAKE_CONSUME_MULT.get(intake_mode, 1.0)
        interact_mult = self._INTAKE_INTERACT_MULT.get(intake_mode, 1.0)

        consumed_prob = self._clamp01(base_consume * consume_mult)
        interact_prob = self._clamp01(base_interact * interact_mult)

        imp = Impression(
            intake_mode=intake_mode,
            content_id=content.id,
            topic=content.topic,
            stance_signal=content.stance,

            # Placeholder perceptual fields (LLM later)
            emotional_valence=0.0,
            arousal=0.0,
            credibility_signal=0.5,
            identity_threat=0.0,
            social_proof=0.0,
            relationship_strength_source=0.0,

            # New fields
            media_type=mt,
            consumed_prob=consumed_prob,
            interact_prob=interact_prob,
        )
        imp.clamp()
        return imp
