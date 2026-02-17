from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import csv

from gsocialsim.stimuli.stimulus import Stimulus, MediaType


class DataSource(ABC):
    """Abstract base class for any source of external data."""

    @abstractmethod
    def get_stimuli(self, tick: int) -> List[Stimulus]:
        """Returns a list of all stimuli that should be injected at a given tick."""
        raise NotImplementedError


def _clean_opt_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        return v if v else None
    # defensive: coerce non-strings to string
    s = str(v).strip()
    return s if s else None


class CsvDataSource(DataSource):
    """
    A concrete data source that reads from a CSV file.

    Required columns:
      - id
      - tick
      - source
      - content_text

    Optional columns:
      - topic
      - stance           (float in [-1, 1])
      - identity_threat  (float in [0, 1])
      - political_salience (float in [0, 1])
      - primal_triggers  (csv list: e.g. "self,contrast,visual")
      - primal_intensity (float in [0, 1])
      - media_type       (news, social_post, video, meme, longform, forum_thread)
      - creator_id       (for subscription targeting)
      - outlet_id        (for subscription targeting)
      - community_id     (for subscription targeting)

    Notes:
      - All optional fields are safe: missing columns are simply treated as None.
      - The Stimulus class also mirrors some values into stimulus.metadata to keep the
        CSV format flexible and backward compatible.
    """

    def __init__(self, file_path: str):
        self.stimuli_by_tick: Dict[int, List[Stimulus]] = {}

        with open(file_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)

            # Normalize header names defensively (CSV authors make mistakes).
            # We keep original keys but also allow case-insensitive matching.
            fieldnames = reader.fieldnames or []
            lower_to_actual = {fn.lower(): fn for fn in fieldnames}

            def get(row: Dict[str, Any], key: str) -> Any:
                actual = lower_to_actual.get(key.lower(), key)
                return row.get(actual)

            for row in reader:
                tick_raw = get(row, "tick")
                if tick_raw is None:
                    continue
                tick = int(tick_raw)

                stimulus_id = str(get(row, "id"))
                source = str(get(row, "source"))
                content_text = str(get(row, "content_text"))

                topic = _clean_opt_str(get(row, "topic"))
                media_type_raw = _clean_opt_str(get(row, "media_type"))
                stance_raw = get(row, "stance")
                stance_val = None
                if stance_raw is not None and str(stance_raw).strip() != "":
                    try:
                        stance_val = float(stance_raw)
                    except Exception:
                        stance_val = None
                threat_raw = get(row, "identity_threat")
                threat_val = None
                if threat_raw is not None and str(threat_raw).strip() != "":
                    try:
                        threat_val = float(threat_raw)
                    except Exception:
                        threat_val = None
                pol_raw = get(row, "political_salience")
                pol_val = None
                if pol_raw is not None and str(pol_raw).strip() != "":
                    try:
                        pol_val = float(pol_raw)
                    except Exception:
                        pol_val = None
                primal_raw = get(row, "primal_triggers")
                primal_triggers = None
                if primal_raw is not None and str(primal_raw).strip() != "":
                    tokens = [t.strip().lower() for t in str(primal_raw).replace("|", ",").split(",")]
                    primal_triggers = [t for t in tokens if t]
                primal_intensity_raw = get(row, "primal_intensity")
                primal_intensity_val = None
                if primal_intensity_raw is not None and str(primal_intensity_raw).strip() != "":
                    try:
                        primal_intensity_val = float(primal_intensity_raw)
                    except Exception:
                        primal_intensity_val = None
                creator_id = _clean_opt_str(get(row, "creator_id"))
                outlet_id = _clean_opt_str(get(row, "outlet_id"))
                community_id = _clean_opt_str(get(row, "community_id"))

                # Keep metadata flexible and compatible with existing code paths.
                metadata: Dict[str, Any] = {"topic": topic}
                if stance_val is not None:
                    metadata["stance"] = stance_val
                if threat_val is not None:
                    metadata["identity_threat"] = threat_val
                if pol_val is not None:
                    metadata["political_salience"] = pol_val
                if primal_triggers is not None:
                    metadata["primal_triggers"] = primal_triggers
                if primal_intensity_val is not None:
                    metadata["primal_intensity"] = primal_intensity_val
                if media_type_raw is not None:
                    metadata["media_type"] = media_type_raw
                if creator_id is not None:
                    metadata["creator_id"] = creator_id
                if outlet_id is not None:
                    metadata["outlet_id"] = outlet_id
                if community_id is not None:
                    metadata["community_id"] = community_id

                stimulus = Stimulus(
                    id=stimulus_id,
                    source=source,
                    tick=tick,
                    content_text=content_text,
                    media_type=MediaType.from_any(media_type_raw),
                    creator_id=creator_id,
                    outlet_id=outlet_id,
                    community_id=community_id,
                    topic_hint=topic,
                    stance_hint=stance_val,
                    political_salience=pol_val,
                    primal_triggers=primal_triggers,
                    primal_intensity=primal_intensity_val,
                    metadata=metadata,
                )

                self.stimuli_by_tick.setdefault(tick, []).append(stimulus)

        print(
            f"Loaded {sum(len(s) for s in self.stimuli_by_tick.values())} stimuli from {file_path}"
        )

    def get_stimuli(self, tick: int) -> List[Stimulus]:
        return self.stimuli_by_tick.get(tick, [])
