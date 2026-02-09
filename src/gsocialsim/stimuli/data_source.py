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
                creator_id = _clean_opt_str(get(row, "creator_id"))
                outlet_id = _clean_opt_str(get(row, "outlet_id"))
                community_id = _clean_opt_str(get(row, "community_id"))

                # Keep metadata flexible and compatible with existing code paths.
                metadata: Dict[str, Any] = {"topic": topic}
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
                    metadata=metadata,
                )

                self.stimuli_by_tick.setdefault(tick, []).append(stimulus)

        print(
            f"Loaded {sum(len(s) for s in self.stimuli_by_tick.values())} stimuli from {file_path}"
        )

    def get_stimuli(self, tick: int) -> List[Stimulus]:
        return self.stimuli_by_tick.get(tick, [])
