#pragma once

#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "data_source.h"
#include "types.h"

class StimulusIngestionEngine {
public:
    void register_data_source(std::shared_ptr<DataSource> source);
    const Stimulus* get_stimulus(const std::string& stimulus_id) const;
    std::vector<Stimulus> tick(int current_tick);

private:
    std::vector<std::shared_ptr<DataSource>> data_sources_;
    std::unordered_map<std::string, Stimulus> stimuli_store_;
};
