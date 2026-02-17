#include "geo_world.h"

#include <algorithm>
#include <cmath>
#include <fstream>
#include <random>

#include "utils.h"

static inline double clamp01(double v) {
    if (v < 0.0) return 0.0;
    if (v > 1.0) return 1.0;
    return v;
}

void GeoPopulationSampler::load_h3_population_csv(const std::string& path) {
    cell_weights.clear();
    cell_meta.clear();
    cells.clear();
    cdf.clear();
    total_weight = 0.0;

    std::ifstream infile(path);
    if (!infile.is_open()) {
        return;
    }

    std::string header_line;
    if (!std::getline(infile, header_line)) {
        return;
    }
    auto headers = split_csv_row(header_line);
    std::unordered_map<std::string, size_t> idx;
    for (size_t i = 0; i < headers.size(); ++i) {
        std::string key = headers[i];
        for (auto& c : key) c = static_cast<char>(std::tolower(c));
        idx[key] = i;
    }

    auto get = [&](const std::vector<std::string>& row, const std::string& key) -> std::string {
        auto it = idx.find(key);
        if (it == idx.end()) return "";
        return it->second < row.size() ? row[it->second] : "";
    };

    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;
        auto row = split_csv_row(line);
        std::string cell = get(row, "h3_cell");
        if (cell.empty()) cell = get(row, "cell");
        if (cell.empty()) continue;
        double w = 0.0;
        try {
            std::string w_raw = get(row, "population");
            if (w_raw.empty()) w_raw = get(row, "weight");
            if (w_raw.empty()) w_raw = get(row, "pop");
            w = std::stod(w_raw);
        } catch (...) {
            continue;
        }
        if (w <= 0.0 || w < min_population || w > max_population) continue;
        cell_weights[cell] = cell_weights[cell] + w;
        total_weight += w;

        GeoLocation meta;
        meta.cell_id = cell;
        meta.country = get(row, "country");
        meta.admin1 = get(row, "admin1");
        meta.admin2 = get(row, "admin2");
        cell_meta[cell] = meta;
    }

    cells.reserve(cell_weights.size());
    cdf.reserve(cell_weights.size());
    double acc = 0.0;
    for (const auto& kv : cell_weights) {
        cells.push_back(kv.first);
        acc += kv.second;
        cdf.push_back(acc);
    }
    total_weight = acc;
}

std::string GeoPopulationSampler::sample_cell(std::mt19937& rng) const {
    if (cells.empty() || total_weight <= 0.0) return "UNKNOWN";
    std::uniform_real_distribution<double> dist(0.0, total_weight);
    double r = dist(rng);
    auto it = std::lower_bound(cdf.begin(), cdf.end(), r);
    size_t idx = it == cdf.end() ? cdf.size() - 1 : static_cast<size_t>(it - cdf.begin());
    return cells[idx];
}

GeoLocation GeoPopulationSampler::cell_location(const std::string& cell_id) const {
    auto it = cell_meta.find(cell_id);
    if (it != cell_meta.end()) return it->second;
    GeoLocation loc;
    loc.cell_id = cell_id;
    return loc;
}

void GeoWorld::load_population_csv() {
    population.h3_resolution = h3_resolution;
    population.load_h3_population_csv(population_csv_path);
}

void GeoWorld::ensure_agent(const AgentId& agent_id, std::mt19937& rng) {
    if (agent_home.find(agent_id) != agent_home.end()) return;
    std::string cell = population.sample_cell(rng);
    GeoLocation loc = population.cell_location(cell);
    agent_home[agent_id] = loc;
    std::uniform_real_distribution<double> dist(0.2, 1.0);
    agent_social_factor[agent_id] = dist(rng);
}

double GeoWorld::proximity(const AgentId& a, const AgentId& b) const {
    if (a == b) return 1.0;
    auto ita = agent_home.find(a);
    auto itb = agent_home.find(b);
    if (ita == agent_home.end() || itb == agent_home.end()) return 0.0;
    if (ita->second.cell_id == itb->second.cell_id) return 1.0;
    if (!ita->second.country.empty() && ita->second.country == itb->second.country) {
        return 0.2;
    }
    return 0.0;
}
