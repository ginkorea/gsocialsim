#pragma once

#include <random>
#include <string>
#include "agent.h"
#include "population_layer.h"

// Helper functions for generating agent demographics from population segments

class DemographicSampler {
public:
    explicit DemographicSampler(std::mt19937& rng) : rng_(rng) {}

    // Sample a segment from a cell's segment mix (weighted)
    std::string sample_segment(const SegmentMix& mix);

    // Generate full demographics for an agent based on their segment
    AgentDemographics generate_demographics(
        const PopulationSegment& segment,
        const std::string& cell_id);

    // Generate psychographics from segment
    AgentPsychographics generate_psychographics(const PopulationSegment& segment);

    // Initialize agent beliefs from segment baseline
    std::unordered_map<TopicId, Belief> generate_beliefs(const PopulationSegment& segment);

private:
    std::mt19937& rng_;

    // Helper: sample age within cohort
    int sample_age_from_cohort(const std::string& cohort);

    // Helper: sample race based on segment composition
    std::string sample_race(double percent_white);

    // Helper: sample gender based on segment composition
    std::string sample_gender(double percent_female);

    // Helper: convert political ideology to label
    std::string ideology_to_label(double ideology);

    // Helper: sample from normal distribution with clamp
    double sample_normal_clamped(double mean, double stddev, double min_val, double max_val);

    // Helper: sample uniform
    double sample_uniform(double min_val, double max_val);
};
