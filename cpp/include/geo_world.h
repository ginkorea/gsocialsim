#pragma once

#include <random>
#include <string>
#include <unordered_map>
#include <vector>

#include "types.h"

struct GeoLocation {
    std::string cell_id;
    double lat = 0.0;
    double lon = 0.0;
    std::string country;
    std::string admin1;
    std::string admin2;
};

struct GeoPopulationSampler {
    int h3_resolution = 6;
    double min_population = 1.0;
    double max_population = 1.0e12;
    std::unordered_map<std::string, double> cell_weights;
    std::unordered_map<std::string, GeoLocation> cell_meta;
    std::vector<std::string> cells;
    std::vector<double> cdf;
    double total_weight = 0.0;

    void load_h3_population_csv(const std::string& path);
    std::string sample_cell(std::mt19937& rng) const;
    GeoLocation cell_location(const std::string& cell_id) const;
};

struct GeoWorld {
    bool enable_life_cycle = true;
    int h3_resolution = 6;
    int agent_scale = 10;
    std::string population_csv_path = "data/geo/h3_population.csv";

    GeoPopulationSampler population;
    std::unordered_map<AgentId, GeoLocation> agent_home;
    std::unordered_map<AgentId, double> agent_social_factor;

    void load_population_csv();
    void ensure_agent(const AgentId& agent_id, std::mt19937& rng);
    double proximity(const AgentId& a, const AgentId& b) const;
};
