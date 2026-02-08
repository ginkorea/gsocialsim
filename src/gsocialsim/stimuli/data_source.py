from abc import ABC, abstractmethod
from typing import List, Dict, Any
import csv

from gsocialsim.stimuli.stimulus import Stimulus


class DataSource(ABC):
    """Abstract base class for any source of external data."""

    @abstractmethod
    def get_stimuli(self, tick: int) -> List[Stimulus]:
        """Returns a list of all stimuli that should be injected at a given tick."""
        raise NotImplementedError


class CsvDataSource(DataSource):
    """
    A concrete data source that reads from a CSV file.

    Expected columns:
      - id
      - tick
      - source
      - content_text
    Optional columns:
      - topic   (if present, will be stored in stimulus.metadata["topic"])
    """

    def __init__(self, file_path: str):
        self.stimuli_by_tick: Dict[int, List[Stimulus]] = {}

        with open(file_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                tick = int(row["tick"])

                # Optional topic support
                topic = row.get("topic")
                if isinstance(topic, str):
                    topic = topic.strip() or None

                stimulus = Stimulus(
                    id=row["id"],
                    source=row["source"],
                    tick=tick,
                    content_text=row["content_text"],
                    metadata={"topic": topic},
                )

                self.stimuli_by_tick.setdefault(tick, []).append(stimulus)

        print(
            f"Loaded {sum(len(s) for s in self.stimuli_by_tick.values())} stimuli from {file_path}"
        )

    def get_stimuli(self, tick: int) -> List[Stimulus]:
        return self.stimuli_by_tick.get(tick, [])
