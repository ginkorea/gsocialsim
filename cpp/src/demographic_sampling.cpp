#include "demographic_sampling.h"
#include "identity_space.h"
#include <algorithm>
#include <cmath>

// Sample segment from weighted mix
std::string DemographicSampler::sample_segment(const SegmentMix& mix) {
    if (mix.size() == 0) {
        return "general";  // fallback
    }

    std::uniform_real_distribution<double> dist(0.0, 1.0);
    double roll = dist(rng_);

    double cumulative = 0.0;
    for (size_t i = 0; i < mix.size(); ++i) {
        cumulative += mix.weights[i];
        if (roll < cumulative) {
            return mix.segment_ids[i];
        }
    }

    return mix.segment_ids.back();  // fallback to last
}

// Generate demographics from segment
AgentDemographics DemographicSampler::generate_demographics(
    const PopulationSegment& segment,
    const std::string& cell_id) {

    AgentDemographics demo;

    demo.home_cell_id = cell_id;

    // Age
    demo.age = sample_age_from_cohort(segment.age_cohort);
    demo.age_cohort = segment.age_cohort;

    // Geography
    demo.geography_type = segment.primary_geography;

    // Education
    demo.education_level = segment.education_level;

    // Income
    demo.income_bracket = segment.income_bracket;
    // Sample income within bracket
    if (segment.income_bracket == "low") {
        demo.income_annual = static_cast<int>(sample_normal_clamped(35000, 10000, 15000, 45000));
    } else if (segment.income_bracket == "middle") {
        demo.income_annual = static_cast<int>(sample_normal_clamped(70000, 20000, 45000, 100000));
    } else if (segment.income_bracket == "upper_middle") {
        demo.income_annual = static_cast<int>(sample_normal_clamped(140000, 30000, 100000, 200000));
    } else {  // high
        demo.income_annual = static_cast<int>(sample_normal_clamped(300000, 100000, 200000, 1000000));
    }

    // Race
    demo.race_ethnicity = sample_race(segment.percent_white);

    // Gender
    demo.gender = sample_gender(segment.percent_female);

    // Religion
    demo.religion = segment.dominant_religion;
    // Add variance to religiosity
    if (demo.religion == "atheist") {
        demo.religiosity = sample_uniform(0.0, 0.2);
    } else if (demo.religion == "evangelical") {
        demo.religiosity = sample_normal_clamped(0.8, 0.15, 0.4, 1.0);
    } else {
        demo.religiosity = sample_normal_clamped(0.5, 0.2, 0.0, 1.0);
    }

    // Political ideology (add individual variance)
    demo.political_ideology = sample_normal_clamped(
        segment.political_ideology, 0.15, -1.0, 1.0);
    demo.political_label = ideology_to_label(demo.political_ideology);

    // Institutional trust (add variance)
    demo.institutional_trust = sample_normal_clamped(
        segment.institutional_trust, 0.1, 0.0, 1.0);

    // Polarization (add variance)
    demo.polarization = sample_normal_clamped(
        segment.polarization, 0.1, 0.0, 1.0);

    // Media diet
    demo.media_diet = segment.media_diet_type;

    // Attention budget (add variance)
    demo.attention_budget = sample_normal_clamped(
        segment.attention_budget, 0.2, 0.2, 2.0);

    // Copy media biases from segment (could add variance later)
    demo.consume_bias = segment.consume_bias;
    demo.interact_bias = segment.interact_bias;

    // Occupation (simplified - could be more sophisticated)
    if (segment.education_level == "graduate") {
        demo.occupation = "professional";
    } else if (segment.education_level == "bachelors") {
        demo.occupation = "white_collar";
    } else if (segment.education_level == "some_college") {
        demo.occupation = "service";
    } else {
        demo.occupation = "blue_collar";
    }

    // Union membership
    demo.union_membership = (segment.id == "union_households") ? "member" : "none";

    // Social identity flags
    demo.parent = (demo.age >= 25) && (sample_uniform(0.0, 1.0) < 0.6);
    demo.veteran = (demo.age >= 40) && (sample_uniform(0.0, 1.0) < 0.10);
    demo.small_business_owner = (segment.id == "small_business_owners");

    // Segment assignment
    demo.primary_segment_id = segment.id;
    demo.segment_fit_score = 0.85 + sample_uniform(-0.1, 0.1);  // High fit with variance

    return demo;
}

// Generate demographics and resolve identity coordinates
AgentDemographics DemographicSampler::generate_demographics(
    const PopulationSegment& segment,
    const std::string& cell_id,
    const IdentitySpace& identity_space) {

    AgentDemographics demo = generate_demographics(segment, cell_id);
    demo.country_id = identity_space.config().country_id;
    demo.identity_coords = identity_space.resolve(demo);
    return demo;
}

// Generate psychographics from segment
AgentPsychographics DemographicSampler::generate_psychographics(
    const PopulationSegment& segment) {

    AgentPsychographics psycho;

    // Big 5 personality (add variance around segment stereotypes)
    // These are rough stereotypes for different segments
    if (segment.political_ideology < -0.5) {
        // Left-leaning: higher openness, lower conscientiousness
        psycho.openness = sample_normal_clamped(0.7, 0.15, 0.0, 1.0);
        psycho.conscientiousness = sample_normal_clamped(0.4, 0.15, 0.0, 1.0);
        psycho.agreeableness = sample_normal_clamped(0.6, 0.15, 0.0, 1.0);
    } else if (segment.political_ideology > 0.5) {
        // Right-leaning: lower openness, higher conscientiousness
        psycho.openness = sample_normal_clamped(0.3, 0.15, 0.0, 1.0);
        psycho.conscientiousness = sample_normal_clamped(0.7, 0.15, 0.0, 1.0);
        psycho.agreeableness = sample_normal_clamped(0.5, 0.15, 0.0, 1.0);
    } else {
        // Moderate: average on all
        psycho.openness = sample_normal_clamped(0.5, 0.15, 0.0, 1.0);
        psycho.conscientiousness = sample_normal_clamped(0.5, 0.15, 0.0, 1.0);
        psycho.agreeableness = sample_normal_clamped(0.5, 0.15, 0.0, 1.0);
    }

    // Extraversion and neuroticism: uniform random
    psycho.extraversion = sample_normal_clamped(0.5, 0.2, 0.0, 1.0);
    psycho.neuroticism = sample_normal_clamped(0.5, 0.2, 0.0, 1.0);

    // Social media behavior (based on age cohort and attention budget)
    if (segment.age_cohort == "gen_z" || segment.age_cohort == "millennial") {
        psycho.posting_frequency = sample_normal_clamped(2.0, 1.0, 0.1, 10.0);
        psycho.engagement_propensity = sample_normal_clamped(0.6, 0.15, 0.0, 1.0);
        psycho.virality_seeking = sample_normal_clamped(0.6, 0.2, 0.0, 1.0);
    } else {
        psycho.posting_frequency = sample_normal_clamped(0.5, 0.3, 0.0, 5.0);
        psycho.engagement_propensity = sample_normal_clamped(0.3, 0.15, 0.0, 1.0);
        psycho.virality_seeking = sample_normal_clamped(0.3, 0.2, 0.0, 1.0);
    }

    // Outrage susceptibility (higher for polarized segments)
    psycho.outrage_susceptibility = sample_normal_clamped(
        segment.polarization * 0.8, 0.15, 0.0, 1.0);

    // Influence dynamics (from segment)
    psycho.susceptibility = segment.susceptibility + sample_uniform(-0.1, 0.1);
    psycho.susceptibility = std::clamp(psycho.susceptibility, 0.0, 1.0);

    psycho.identity_rigidity = segment.identity_rigidity + sample_uniform(-0.1, 0.1);
    psycho.identity_rigidity = std::clamp(psycho.identity_rigidity, 0.0, 1.0);

    psycho.bounded_confidence_tau = 1.5;  // default, could vary by segment

    psycho.trust_in_sources_base = segment.institutional_trust + sample_uniform(-0.1, 0.1);
    psycho.trust_in_sources_base = std::clamp(psycho.trust_in_sources_base, 0.0, 1.0);

    // Social graph position (will be computed after network creation)
    psycho.follower_count = 0;
    psycho.following_count = 0;
    psycho.centrality_score = 0.0;
    psycho.verified_status = false;
    psycho.influencer_status = false;

    return psycho;
}

// Generate beliefs from segment baseline
std::unordered_map<TopicId, Belief> DemographicSampler::generate_beliefs(
    const PopulationSegment& segment) {

    std::unordered_map<TopicId, Belief> beliefs;

    for (const auto& [topic, dist] : segment.baseline_beliefs) {
        Belief belief;

        // Sample stance from distribution (mean ± variance)
        belief.stance = sample_normal_clamped(
            dist.mean, std::sqrt(dist.variance), -1.0, 1.0);

        // Set core_value to the segment baseline (rebound anchor)
        belief.core_value = dist.mean;

        // Confidence based on inverse of variance
        belief.confidence = 1.0 - dist.variance;
        belief.confidence = std::clamp(belief.confidence, 0.1, 1.0);

        // Salience based on polarization and variance (extreme = salient)
        belief.salience = std::abs(dist.mean) * (1.0 - dist.variance);
        belief.salience = std::clamp(belief.salience, 0.1, 1.0);

        // Knowledge: moderate baseline
        belief.knowledge = 0.5;

        // Initialize dynamics state
        belief.momentum = dist.momentum;
        belief.evidence_accumulator = 0.0;
        belief.exposure_count = 0;

        beliefs[topic] = belief;
    }

    return beliefs;
}

// ============================================================================
// Helper Methods
// ============================================================================

int DemographicSampler::sample_age_from_cohort(const std::string& cohort) {
    if (cohort == "gen_z") {
        return static_cast<int>(sample_uniform(18, 28));
    } else if (cohort == "millennial") {
        return static_cast<int>(sample_uniform(28, 44));
    } else if (cohort == "gen_x") {
        return static_cast<int>(sample_uniform(44, 60));
    } else {  // boomer_plus
        return static_cast<int>(sample_uniform(60, 85));
    }
}

std::string DemographicSampler::sample_race(double percent_white) {
    double roll = sample_uniform(0.0, 1.0);
    if (roll < percent_white) {
        return "white";
    } else {
        // Sample from other races (simplified)
        double remaining = 1.0 - percent_white;
        double roll2 = sample_uniform(0.0, remaining);

        // Rough US demographics for non-white
        if (roll2 < remaining * 0.35) return "black";
        if (roll2 < remaining * 0.70) return "hispanic";
        if (roll2 < remaining * 0.90) return "asian";
        return "other";
    }
}

std::string DemographicSampler::sample_gender(double percent_female) {
    double roll = sample_uniform(0.0, 1.0);
    if (roll < percent_female) {
        return "female";
    } else if (roll < percent_female + (1.0 - percent_female) * 0.98) {
        return "male";
    } else {
        return "non_binary";
    }
}

std::string DemographicSampler::ideology_to_label(double ideology) {
    if (ideology < -0.7) return "progressive";
    if (ideology < -0.4) return "liberal";
    if (ideology < 0.4) return "moderate";
    if (ideology < 0.7) return "conservative";
    return "reactionary";
}

double DemographicSampler::sample_normal_clamped(
    double mean, double stddev, double min_val, double max_val) {

    std::normal_distribution<double> dist(mean, stddev);
    double value = dist(rng_);
    return std::clamp(value, min_val, max_val);
}

double DemographicSampler::sample_uniform(double min_val, double max_val) {
    std::uniform_real_distribution<double> dist(min_val, max_val);
    return dist(rng_);
}
