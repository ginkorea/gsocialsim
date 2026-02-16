from typing import Dict, List
from gsocialsim.stimuli.data_source import DataSource
from gsocialsim.stimuli.stimulus import Stimulus

class StimulusIngestionEngine:
    def __init__(self):
        self._data_sources: List[DataSource] = []
        self._stimuli_store: Dict[str, Stimulus] = {}

    def register_data_source(self, source: DataSource):
        self._data_sources.append(source)

    def get_stimulus(self, stimulus_id: str) -> Stimulus | None:
        return self._stimuli_store.get(stimulus_id)

    def tick(self, current_tick: int) -> List[Stimulus]:
        """ Polls all data sources and adds new stimuli to the world. """
        newly_added = []
        for source in self._data_sources:
            new_stimuli = source.get_stimuli(current_tick)
            for stimulus in new_stimuli:
                self._stimuli_store[stimulus.id] = stimulus
                newly_added.append(stimulus)
        return newly_added
