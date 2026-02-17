from __future__ import annotations

from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.stimuli.stimulus import MediaType


class AttentionSystem:
    """
    Generates Impressions from ContentItems.

    Deterministic behavior:
      - Attach media_type
      - Provide consumed_prob and interact_prob based on media_type and intake_mode

    Contract helper:
      - Attach a suggested attention_cost_minutes (dynamic attribute) to the Impression.
        This lets Agent.perceive() enforce per-tick attention budgets without changing
        the Impression dataclass yet.
    """

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

    _INTAKE_CONSUME_MULT = {
        IntakeMode.SCROLL: 1.00,
        IntakeMode.SEEK: 1.15,
        IntakeMode.PHYSICAL: 1.20,
        IntakeMode.DEEP_FOCUS: 1.40,
    }

    _INTAKE_INTERACT_MULT = {
        IntakeMode.SCROLL: 1.00,
        IntakeMode.SEEK: 0.90,
        IntakeMode.PHYSICAL: 0.75,
        IntakeMode.DEEP_FOCUS: 0.60,
    }

    # Contract-facing "time cost" hints (minutes) per content type under SCROLL
    _BASE_ATTENTION_COST_MIN = {
        MediaType.MEME: 0.5,
        MediaType.SOCIAL_POST: 1.0,
        MediaType.NEWS: 2.0,
        MediaType.VIDEO: 4.0,
        MediaType.FORUM_THREAD: 3.0,
        MediaType.LONGFORM: 6.0,
        MediaType.UNKNOWN: 1.5,
    }

    # Intake mode scales time cost
    _INTAKE_COST_MULT = {
        IntakeMode.SCROLL: 1.00,
        IntakeMode.SEEK: 1.25,        # seeking tends to spend more time
        IntakeMode.PHYSICAL: 1.50,    # offline engagement tends to take longer
        IntakeMode.DEEP_FOCUS: 3.00,  # deep focus is expensive
    }

    _PRIMAL_BASE_BY_MEDIA = {
        MediaType.VIDEO: 0.25,
        MediaType.MEME: 0.20,
        MediaType.SOCIAL_POST: 0.15,
        MediaType.NEWS: 0.10,
        MediaType.LONGFORM: 0.08,
        MediaType.FORUM_THREAD: 0.08,
        MediaType.UNKNOWN: 0.0,
    }

    _PRIMAL_TRIGGER_WEIGHT = {
        "self": 0.12,
        "personal": 0.12,
        "contrast": 0.10,
        "contrastable": 0.10,
        "tangible": 0.10,
        "start_end": 0.08,
        "beginning_end": 0.08,
        "memorable": 0.08,
        "visual": 0.12,
        "emotion": 0.12,
        "emotional": 0.12,
    }

    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def evaluate(self, content: ContentItem, is_physical: bool = False) -> Impression:
        intake_mode = IntakeMode.PHYSICAL if is_physical else IntakeMode.SCROLL

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

        # Optional primal activation (neuromarketing-style)
        triggers = getattr(content, "primal_triggers", []) or []
        intensity = getattr(content, "primal_intensity", None)
        primal_activation = 0.0
        if triggers or intensity is not None:
            base = float(self._PRIMAL_BASE_BY_MEDIA.get(mt, 0.0))
            trig = 0.0
            for t in triggers:
                trig += float(self._PRIMAL_TRIGGER_WEIGHT.get(str(t).strip().lower(), 0.05))
            if intensity is not None:
                try:
                    trig += 0.4 * float(intensity)
                except Exception:
                    pass
            primal_activation = self._clamp01(base + trig)

        # Identity threat can be supplied by content or inferred from a simple flag.
        identity_threat = 0.0
        try:
            if content.identity_threat is not None:
                identity_threat = float(content.identity_threat)
            elif getattr(content, "is_identity_threatening", False):
                identity_threat = 1.0
        except Exception:
            identity_threat = 0.0

        imp = Impression(
            intake_mode=intake_mode,
            content_id=content.id,
            topic=content.topic,
            stance_signal=content.stance,
            emotional_valence=0.0,
            arousal=0.0,
            credibility_signal=0.5,
            identity_threat=identity_threat,
            social_proof=0.0,
            relationship_strength_source=0.0,
            media_type=mt,
            consumed_prob=consumed_prob,
            interact_prob=interact_prob,
            primal_activation=primal_activation,
        )
        imp.clamp()

        # Attach contract helper: estimated attention time cost in minutes
        base_cost = float(self._BASE_ATTENTION_COST_MIN.get(mt, self._BASE_ATTENTION_COST_MIN[MediaType.UNKNOWN]))
        mult = float(self._INTAKE_COST_MULT.get(intake_mode, 1.0))
        attention_cost_minutes = max(0.0, base_cost * mult)

        # Dynamic attribute: safe with existing Impression dataclass
        try:
            setattr(imp, "attention_cost_minutes", attention_cost_minutes)
        except Exception:
            pass

        return imp
