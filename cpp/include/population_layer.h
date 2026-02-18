#pragma once

#include <string>
#include <unordered_map>
#include <vector>

#include "types.h"

// -----------------------------
// Module: Population Layer
// Aggregate micro-agents into population cells with segmented demographics
// Designed for CUDA optimization (flat arrays, contiguous memory)
// -----------------------------

// Belief distribution for population segments
struct BeliefDistribution {
    double mean = 0.0;         // [-1, +1] average stance
    double variance = 0.1;     // [0, 1] spread
    double momentum = 0.0;     // Population-level velocity
    double core_value = 0.0;   // Rebound anchor

    BeliefDistribution() = default;
    BeliefDistribution(double m, double v, double mom, double core)
        : mean(m), variance(v), momentum(mom), core_value(core) {}
};

// Population segment (demographic/identity group)
struct PopulationSegment {
    std::string id;

    // Demographics (for segment characterization)
    std::string age_cohort;              // "gen_z", "millennial", "gen_x", "boomer_plus"
    std::string primary_geography;       // "urban_core", "suburban", "small_town", "rural"
    std::string education_level;         // "high_school", "some_college", "bachelors", "graduate"
    std::string income_bracket;          // "low", "middle", "upper_middle", "high"
    double percent_white = 0.5;          // [0,1] racial composition
    double percent_female = 0.5;         // [0,1] gender composition
    std::string dominant_religion;       // "atheist", "evangelical", "catholic", "mainline_protestant", etc.

    // Psychographics
    double political_ideology = 0.0;     // [-1, +1] left to right
    std::string political_label;         // "progressive", "liberal", "moderate", "conservative", "reactionary"
    double institutional_trust = 0.5;    // [0,1] trust in institutions
    std::string media_diet_type;         // "traditional", "social_native", "alt_media", "podcast_heavy", "mixed"

    // Identity traits (existing)
    std::vector<double> identity_vector;  // 8-dimensional
    double identity_rigidity = 0.5;
    double attention_budget = 1.0;
    double susceptibility = 0.5;
    double polarization = 0.0;

    // Baseline beliefs (topic -> distribution)
    std::unordered_map<TopicId, BeliefDistribution> baseline_beliefs;

    // Media consumption biases
    std::unordered_map<MediaType, double> consume_bias;
    std::unordered_map<MediaType, double> interact_bias;

    PopulationSegment() = default;
    explicit PopulationSegment(const std::string& segment_id) : id(segment_id) {
        identity_vector.resize(8, 0.0);
    }
};

// Segment mix within a cell (weights sum to 1.0)
struct SegmentMix {
    std::vector<std::string> segment_ids;  // Ordered list of segment IDs
    std::vector<double> weights;           // Corresponding weights [0,1], sum=1.0

    SegmentMix() = default;

    void add_segment(const std::string& id, double weight) {
        segment_ids.push_back(id);
        weights.push_back(weight);
    }

    void normalize() {
        double sum = 0.0;
        for (double w : weights) sum += w;
        if (sum > 0.0) {
            for (double& w : weights) w /= sum;
        }
    }

    size_t size() const { return segment_ids.size(); }
};

// Exposure event for population aggregation
struct PopulationExposure {
    int tick = 0;
    std::string cell_id;
    ActorId source;
    TopicId topic;
    double stance = 0.0;
    double strength = 1.0;  // Influence strength
    std::string channel;    // "broadcast", "dm", "physical", etc.

    PopulationExposure() = default;
    PopulationExposure(int t, const std::string& cid, const ActorId& src,
                       const TopicId& top, double st, double str, const std::string& ch)
        : tick(t), cell_id(cid), source(src), topic(top), stance(st), strength(str), channel(ch) {}
};

// Population cell (hex grid cell with segment mix)
struct PopulationCell {
    std::string cell_id;
    int population = 0;
    SegmentMix segment_mix;

    // Current beliefs (topic -> distribution)
    std::unordered_map<TopicId, BeliefDistribution> beliefs;

    // Exposure accumulator (cleared after update)
    std::vector<PopulationExposure> exposure_accumulator;

    PopulationCell() = default;
    explicit PopulationCell(const std::string& cid, int pop = 0)
        : cell_id(cid), population(pop) {}

    void add_exposure(const PopulationExposure& exp) {
        exposure_accumulator.push_back(exp);
    }

    void clear_exposures() {
        exposure_accumulator.clear();
    }
};

// Population reach estimate
struct PopulationReach {
    std::string cell_id;
    int exposed = 0;
    int consumed = 0;
    int engaged = 0;

    PopulationReach() = default;
    PopulationReach(const std::string& cid, int exp, int cons, int eng)
        : cell_id(cid), exposed(exp), consumed(cons), engaged(eng) {}
};

// ============================================================================
// CUDA-Ready Arrays (Struct-of-Arrays layout for GPU optimization)
// ============================================================================

// Flat array representation of population cells for CUDA
struct PopulationCellArrays {
    // Parallel arrays indexed by cell_index
    std::vector<std::string> cell_ids;
    std::vector<int> populations;

    // Segment mix (variable length, use offset + count)
    std::vector<int> segment_mix_offsets;    // Start index in segment_ids array
    std::vector<int> segment_mix_counts;     // Number of segments per cell
    std::vector<int> segment_ids_flat;       // Flattened segment IDs (as indices)
    std::vector<double> segment_weights_flat; // Flattened segment weights

    // Beliefs (variable length per cell, use offset + count)
    std::vector<int> belief_offsets;         // Start index in beliefs array
    std::vector<int> belief_counts;          // Number of topics per cell
    std::vector<int> belief_topic_ids_flat;  // Flattened topic IDs (as indices)
    std::vector<double> belief_means_flat;
    std::vector<double> belief_variances_flat;
    std::vector<double> belief_momentum_flat;
    std::vector<double> belief_core_values_flat;

    size_t num_cells() const { return cell_ids.size(); }
};

// ============================================================================
// Population Update Engine (CPU + optional CUDA)
// ============================================================================

class PopulationUpdateEngine {
public:
    bool cuda_enabled = false;

    PopulationUpdateEngine() = default;

    // Apply exposures to a single cell (CPU version)
    void update_cell(
        PopulationCell& cell,
        const std::unordered_map<std::string, PopulationSegment>& segments);

    // Apply exposures to all cells (CPU batch)
    void update_all_cells_cpu(
        std::unordered_map<std::string, PopulationCell>& cells,
        const std::unordered_map<std::string, PopulationSegment>& segments);

    // Apply exposures to all cells (CUDA batch)
    // NOTE: CUDA implementation will be in population_cuda.cu (Phase 5)
    void update_all_cells_cuda(
        PopulationCellArrays& cell_arrays,
        const std::vector<PopulationSegment>& segments);

private:
    // Helper: Compute weighted belief update from exposures
    BeliefDistribution compute_belief_update(
        const BeliefDistribution& current,
        const std::vector<PopulationExposure>& exposures,
        const TopicId& topic,
        const SegmentMix& segment_mix,
        const std::unordered_map<std::string, PopulationSegment>& segments);
};

// ============================================================================
// Population Layer (Main Interface)
// ============================================================================

class PopulationLayer {
public:
    PopulationLayer() = default;

    // Initialize from GeoWorld
    void initialize_from_geo(const class GeoWorld& geo);

    // Initialize segments with default profiles
    void initialize_default_segments();

    // Record an exposure event
    void record_exposure(const PopulationExposure& exposure);

    // Update all cells with accumulated exposures
    void update_all_cells();

    // Estimate reach for a piece of content
    PopulationReach estimate_reach(const Content& content) const;

    // Get cell by ID
    PopulationCell* get_cell(const std::string& cell_id);

    // Get segment by ID
    PopulationSegment* get_segment(const std::string& segment_id);

    // Export to flat arrays for CUDA
    PopulationCellArrays export_to_arrays() const;

    // Import from flat arrays (after CUDA update)
    void import_from_arrays(const PopulationCellArrays& arrays);

    // Stats
    size_t num_cells() const { return cells_.size(); }
    size_t num_segments() const { return segments_.size(); }
    size_t total_population() const;

private:
    std::unordered_map<std::string, PopulationCell> cells_;
    std::unordered_map<std::string, PopulationSegment> segments_;
    PopulationUpdateEngine update_engine_;

    // Segment ID to index mapping (for CUDA)
    std::unordered_map<std::string, int> segment_id_to_index_;
    std::vector<std::string> segment_index_to_id_;

    // Topic ID to index mapping (for CUDA)
    std::unordered_map<TopicId, int> topic_id_to_index_;
    std::vector<TopicId> topic_index_to_id_;
};
