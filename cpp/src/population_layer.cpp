#include "population_layer.h"

#include <algorithm>
#include <cmath>
#include <stdexcept>

#include "geo_world.h"

// Helper: Clamp value to range
static double clamp(double x, double lo, double hi) {
    return std::max(lo, std::min(hi, x));
}

// ============================================================================
// PopulationUpdateEngine Implementation
// ============================================================================

void PopulationUpdateEngine::update_cell(
    PopulationCell& cell,
    const std::unordered_map<std::string, PopulationSegment>& segments) {

    if (cell.exposure_accumulator.empty()) {
        return;
    }

    // Group exposures by topic
    std::unordered_map<TopicId, std::vector<PopulationExposure>> exposures_by_topic;
    for (const auto& exp : cell.exposure_accumulator) {
        exposures_by_topic[exp.topic].push_back(exp);
    }

    // Update belief for each topic
    for (const auto& [topic, exposures] : exposures_by_topic) {
        // Get or create current belief
        auto it = cell.beliefs.find(topic);
        BeliefDistribution current;
        if (it != cell.beliefs.end()) {
            current = it->second;
        }

        // Compute updated belief
        BeliefDistribution updated = compute_belief_update(
            current, exposures, topic, cell.segment_mix, segments);

        // Store updated belief
        cell.beliefs[topic] = updated;
    }

    // Clear exposures after processing
    cell.clear_exposures();
}

void PopulationUpdateEngine::update_all_cells_cpu(
    std::unordered_map<std::string, PopulationCell>& cells,
    const std::unordered_map<std::string, PopulationSegment>& segments) {

    for (auto& [cell_id, cell] : cells) {
        update_cell(cell, segments);
    }
}

void PopulationUpdateEngine::update_all_cells_cuda(
    PopulationCellArrays& cell_arrays,
    const std::vector<PopulationSegment>& segments) {

    // TODO: CUDA implementation in Phase 5 (population_cuda.cu)
    // For now, throw error if called
    (void)cell_arrays;
    (void)segments;
    throw std::runtime_error("CUDA support not yet implemented (Phase 5)");
}

BeliefDistribution PopulationUpdateEngine::compute_belief_update(
    const BeliefDistribution& current,
    const std::vector<PopulationExposure>& exposures,
    const TopicId& topic,
    const SegmentMix& segment_mix,
    const std::unordered_map<std::string, PopulationSegment>& segments) {

    BeliefDistribution updated = current;

    if (exposures.empty()) {
        return updated;
    }

    // Aggregate influence from all exposures
    double total_influence = 0.0;
    double total_weight = 0.0;

    for (const auto& exp : exposures) {
        double stance_diff = exp.stance - current.mean;
        double influence = stance_diff * exp.strength;

        total_influence += influence;
        total_weight += exp.strength;
    }

    if (total_weight < 1e-6) {
        return updated;
    }

    // Average influence
    double avg_influence = total_influence / total_weight;

    // Compute segment-weighted susceptibility
    double avg_susceptibility = 0.0;
    double avg_identity_rigidity = 0.0;

    for (size_t i = 0; i < segment_mix.size(); ++i) {
        const std::string& seg_id = segment_mix.segment_ids[i];
        double weight = segment_mix.weights[i];

        auto it = segments.find(seg_id);
        if (it != segments.end()) {
            avg_susceptibility += weight * it->second.susceptibility;
            avg_identity_rigidity += weight * it->second.identity_rigidity;
        }
    }

    // Apply population-level dynamics (simplified from individual dynamics)

    // 1. Inertia & Momentum
    double inertia_rho = 0.85;
    updated.momentum = inertia_rho * current.momentum + 0.10 * avg_influence * avg_susceptibility;

    // 2. Rebound force toward core value
    double rebound_k = 0.05;
    double rebound_force = -rebound_k * (current.mean - current.core_value);

    // 3. Stance update
    double learning_rate = 0.10 * (1.0 - avg_identity_rigidity);
    double stance_delta = learning_rate * updated.momentum + rebound_force;
    updated.mean = clamp(current.mean + stance_delta, -1.0, 1.0);

    // 4. Variance update (exposure increases certainty slightly)
    double variance_reduction = 0.01 * total_weight;
    updated.variance = std::max(0.05, current.variance - variance_reduction);

    return updated;
}

// ============================================================================
// PopulationLayer Implementation
// ============================================================================

void PopulationLayer::initialize_from_geo(const GeoWorld& geo) {
    if (!geo.enable_life_cycle || !geo.population_loaded) {
        return;
    }

    // Get cell IDs from GeoWorld
    const auto& cell_agents = geo.cell_agents;

    for (const auto& [cell_id, agent_ids] : cell_agents) {
        // Create cell
        int population = static_cast<int>(agent_ids.size());
        PopulationCell cell(cell_id, population);

        // Initialize with default segment mix (single segment for now)
        cell.segment_mix.add_segment("general", 1.0);

        cells_[cell_id] = cell;
    }
}

void PopulationLayer::initialize_default_segments() {
    // Define 5 canonical segments

    // 1. Progressive Urban
    {
        PopulationSegment seg("progressive_urban");
        seg.identity_rigidity = 0.4;
        seg.susceptibility = 0.6;
        seg.polarization = 0.5;
        seg.identity_vector = {-0.7, 0.6, 0.5, 0.7, 0.8, 0.4, 0.3, -0.5};
        segments_["progressive_urban"] = seg;
    }

    // 2. Conservative Rural
    {
        PopulationSegment seg("conservative_rural");
        seg.identity_rigidity = 0.7;
        seg.susceptibility = 0.4;
        seg.polarization = 0.6;
        seg.identity_vector = {0.7, -0.6, -0.5, -0.4, 0.3, 0.7, 0.6, 0.5};
        segments_["conservative_rural"] = seg;
    }

    // 3. Moderate Suburban
    {
        PopulationSegment seg("moderate_suburban");
        seg.identity_rigidity = 0.5;
        seg.susceptibility = 0.5;
        seg.polarization = 0.3;
        seg.identity_vector = {0.1, 0.0, 0.2, -0.1, 0.1, 0.3, 0.2, 0.0};
        segments_["moderate_suburban"] = seg;
    }

    // 4. Young Urban
    {
        PopulationSegment seg("young_urban");
        seg.identity_rigidity = 0.3;
        seg.susceptibility = 0.7;
        seg.polarization = 0.4;
        seg.identity_vector = {-0.5, 0.7, 0.6, 0.5, 0.9, 0.2, 0.4, -0.3};
        segments_["young_urban"] = seg;
    }

    // 5. General Population
    {
        PopulationSegment seg("general");
        seg.identity_rigidity = 0.5;
        seg.susceptibility = 0.5;
        seg.polarization = 0.4;
        seg.identity_vector = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
        segments_["general"] = seg;
    }

    // Build index mappings for CUDA
    int idx = 0;
    for (const auto& [seg_id, seg] : segments_) {
        segment_id_to_index_[seg_id] = idx;
        segment_index_to_id_.push_back(seg_id);
        idx++;
    }
}

void PopulationLayer::record_exposure(const PopulationExposure& exposure) {
    auto it = cells_.find(exposure.cell_id);
    if (it != cells_.end()) {
        it->second.add_exposure(exposure);
    }
}

void PopulationLayer::update_all_cells() {
    if (update_engine_.cuda_enabled) {
        // Export to arrays, update on GPU, import back
        auto arrays = export_to_arrays();
        // TODO: Call CUDA kernel in Phase 5
        // update_engine_.update_all_cells_cuda(arrays, segment_vector);
        // import_from_arrays(arrays);

        // For now, fall back to CPU
        update_engine_.update_all_cells_cpu(cells_, segments_);
    } else {
        // CPU update
        update_engine_.update_all_cells_cpu(cells_, segments_);
    }
}

PopulationReach PopulationLayer::estimate_reach(const Content& content) const {
    PopulationReach total_reach("all", 0, 0, 0);

    // Simple heuristic: estimate based on cell populations and content properties
    for (const auto& [cell_id, cell] : cells_) {
        // Exposure probability based on social proof
        double exposure_prob = 0.1 + 0.5 * content.social_proof;
        int exposed = static_cast<int>(cell.population * exposure_prob);

        // Consumption probability (segment-weighted)
        double avg_consume = 0.5; // Simplified
        int consumed = static_cast<int>(exposed * avg_consume);

        // Engagement probability
        double engage_prob = 0.2;
        int engaged = static_cast<int>(consumed * engage_prob);

        total_reach.exposed += exposed;
        total_reach.consumed += consumed;
        total_reach.engaged += engaged;
    }

    return total_reach;
}

PopulationCell* PopulationLayer::get_cell(const std::string& cell_id) {
    auto it = cells_.find(cell_id);
    return it != cells_.end() ? &it->second : nullptr;
}

PopulationSegment* PopulationLayer::get_segment(const std::string& segment_id) {
    auto it = segments_.find(segment_id);
    return it != segments_.end() ? &it->second : nullptr;
}

size_t PopulationLayer::total_population() const {
    size_t total = 0;
    for (const auto& [cell_id, cell] : cells_) {
        total += cell.population;
    }
    return total;
}

PopulationCellArrays PopulationLayer::export_to_arrays() const {
    PopulationCellArrays arrays;

    // Reserve space
    arrays.cell_ids.reserve(cells_.size());
    arrays.populations.reserve(cells_.size());
    arrays.segment_mix_offsets.reserve(cells_.size());
    arrays.segment_mix_counts.reserve(cells_.size());
    arrays.belief_offsets.reserve(cells_.size());
    arrays.belief_counts.reserve(cells_.size());

    int segment_offset = 0;
    int belief_offset = 0;

    for (const auto& [cell_id, cell] : cells_) {
        // Cell metadata
        arrays.cell_ids.push_back(cell_id);
        arrays.populations.push_back(cell.population);

        // Segment mix
        arrays.segment_mix_offsets.push_back(segment_offset);
        arrays.segment_mix_counts.push_back(static_cast<int>(cell.segment_mix.size()));

        for (size_t i = 0; i < cell.segment_mix.size(); ++i) {
            const std::string& seg_id = cell.segment_mix.segment_ids[i];
            int seg_idx = segment_id_to_index_.at(seg_id);
            arrays.segment_ids_flat.push_back(seg_idx);
            arrays.segment_weights_flat.push_back(cell.segment_mix.weights[i]);
            segment_offset++;
        }

        // Beliefs
        arrays.belief_offsets.push_back(belief_offset);
        arrays.belief_counts.push_back(static_cast<int>(cell.beliefs.size()));

        for (const auto& [topic, dist] : cell.beliefs) {
            // Get or create topic index
            auto it = topic_id_to_index_.find(topic);
            int topic_idx;
            if (it == topic_id_to_index_.end()) {
                topic_idx = static_cast<int>(topic_index_to_id_.size());
                const_cast<std::unordered_map<TopicId, int>&>(topic_id_to_index_)[topic] = topic_idx;
                const_cast<std::vector<TopicId>&>(topic_index_to_id_).push_back(topic);
            } else {
                topic_idx = it->second;
            }

            arrays.belief_topic_ids_flat.push_back(topic_idx);
            arrays.belief_means_flat.push_back(dist.mean);
            arrays.belief_variances_flat.push_back(dist.variance);
            arrays.belief_momentum_flat.push_back(dist.momentum);
            arrays.belief_core_values_flat.push_back(dist.core_value);
            belief_offset++;
        }
    }

    return arrays;
}

void PopulationLayer::import_from_arrays(const PopulationCellArrays& arrays) {
    // Import updated beliefs back from flat arrays
    for (size_t cell_idx = 0; cell_idx < arrays.num_cells(); ++cell_idx) {
        const std::string& cell_id = arrays.cell_ids[cell_idx];
        auto it = cells_.find(cell_id);
        if (it == cells_.end()) continue;

        PopulationCell& cell = it->second;

        // Import beliefs
        int belief_offset = arrays.belief_offsets[cell_idx];
        int belief_count = arrays.belief_counts[cell_idx];

        for (int i = 0; i < belief_count; ++i) {
            int idx = belief_offset + i;
            int topic_idx = arrays.belief_topic_ids_flat[idx];
            const TopicId& topic = topic_index_to_id_[topic_idx];

            BeliefDistribution dist;
            dist.mean = arrays.belief_means_flat[idx];
            dist.variance = arrays.belief_variances_flat[idx];
            dist.momentum = arrays.belief_momentum_flat[idx];
            dist.core_value = arrays.belief_core_values_flat[idx];

            cell.beliefs[topic] = dist;
        }
    }
}
