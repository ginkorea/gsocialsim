#include "stimulus_ingestion.h"

void StimulusIngestionEngine::register_data_source(std::shared_ptr<DataSource> source) {
    if (!source) return;
    data_sources_.push_back(std::move(source));
}

const Stimulus* StimulusIngestionEngine::get_stimulus(const std::string& stimulus_id) const {
    auto it = stimuli_store_.find(stimulus_id);
    if (it == stimuli_store_.end()) return nullptr;
    return &it->second;
}

const std::unordered_map<std::string, Stimulus>& StimulusIngestionEngine::stimuli_store() const {
    return stimuli_store_;
}

std::vector<Stimulus> StimulusIngestionEngine::tick(int current_tick) {
    std::vector<Stimulus> newly_added;
    for (const auto& source : data_sources_) {
        if (!source) continue;
        auto stimuli = source->get_stimuli(current_tick);
        for (const auto& stimulus : stimuli) {
            stimuli_store_[stimulus.id] = stimulus;
            newly_added.push_back(stimulus);
        }
    }
    return newly_added;
}
