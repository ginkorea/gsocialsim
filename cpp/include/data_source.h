#pragma once

#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "types.h"

class DataSource {
public:
    virtual ~DataSource() = default;
    virtual std::vector<Stimulus> get_stimuli(int tick) = 0;
};

class CsvDataSource final : public DataSource {
public:
    explicit CsvDataSource(const std::string& file_path);

    std::vector<Stimulus> get_stimuli(int tick) override;

private:
    std::unordered_map<int, std::vector<Stimulus>> stimuli_by_tick_;
};
