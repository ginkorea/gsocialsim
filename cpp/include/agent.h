#pragma once

#include <deque>
#include <optional>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

#include "belief_dynamics.h"
#include "feed_queue.h"
#include "identity_space.h"
#include "types.h"

struct WorldContext;
class IdentitySpace;

struct ActivityPreferences {
    double read_propensity = 0.5;
    double write_propensity = 0.5;
    double react_propensity = 0.5;
    double reflect_propensity = 0.3;
};

struct PlannedAction {
    AgentId agent_id;
    std::optional<Interaction> interaction;
    double cost_minutes = 0.0;
    std::optional<RewardVector> reward;
    std::optional<std::string> action_key;
};

struct PerceptionPlan {
    AgentId agent_id;
    Content content;
    Impression impression;
    double proximity = 0.0;
    std::optional<ContentId> stimulus_id;
    bool exposed = false;
    bool consumed_roll = false;
    bool has_belief = false;
    double attention_cost = 0.0;
    double exposure_cost = 0.0;
    double consumption_extra_cost = 0.0;
    std::optional<BeliefDelta> delta;
    double old_stance = 0.0;
};

class AttentionSystem {
public:
    Impression evaluate(const Content& content, double proximity = 0.0) const;
};

// Legacy BeliefUpdateEngine (deprecated in favor of BeliefDynamicsEngine)
class BeliefUpdateEngine {
public:
    BeliefDelta update(
        const Belief* current,
        const Impression& impression,
        double trust,
        double identity_rigidity,
        bool is_self_source,
        double proximity
    ) const;
};

class BanditPolicy {
public:
    std::optional<Interaction> generate_interaction(class Agent& agent, int tick);
    void learn(const std::string& action_key, const RewardVector& reward);
};

// ============================================================================
// Agent Demographics & Psychographics (Phase 6: Microsegments)
// ============================================================================

struct AgentDemographics {
    // Core demographics
    int age = 35;                              // Actual age (18-90)
    std::string age_cohort;                    // "gen_z", "millennial", "gen_x", "boomer_plus"
    std::string geography_type;                // "urban_core", "suburban", "small_town", "rural"
    std::string home_cell_id;                  // H3 cell ID for geographic location

    std::string education_level;               // "high_school", "some_college", "bachelors", "graduate"
    std::string income_bracket;                // "low", "middle", "upper_middle", "high"
    int income_annual = 50000;                 // Actual income (for targeting)

    std::string race_ethnicity;                // "white", "black", "hispanic", "asian", "other", "multiracial"
    std::string gender;                        // "male", "female", "non_binary"

    std::string religion;                      // "atheist", "evangelical", "catholic", "mainline_protestant", etc.
    double religiosity = 0.5;                  // [0,1] how religious (0=secular, 1=very devout)

    // Political/ideological
    double political_ideology = 0.0;           // [-1, +1] left to right
    std::string political_label;               // "progressive", "liberal", "moderate", "conservative", "reactionary"
    double institutional_trust = 0.5;          // [0,1] trust in government, media, science
    double polarization = 0.5;                 // [0,1] how extreme/tribal

    // Media consumption profile
    std::string media_diet;                    // "traditional", "social_native", "alt_media", "podcast_heavy", "mixed"
    double attention_budget = 1.0;             // [0,2] media consumption capacity
    std::unordered_map<MediaType, double> consume_bias;    // Consumption multipliers
    std::unordered_map<MediaType, double> interact_bias;   // Engagement multipliers

    // Social identity
    std::string occupation;                    // "student", "teacher", "engineer", "tradesperson", etc.
    std::string union_membership;              // "none", "member", "household"
    bool small_business_owner = false;
    bool parent = false;
    bool veteran = false;

    // Multi-dimensional political identity
    PoliticalIdentity political_identity;

    // Country context
    std::string country_id;                    // "USA", "IND", "BRA", etc.

    // Cached identity coordinates (resolved by IdentitySpace)
    AgentIdentityCoords identity_coords;

    // Segment assignment
    std::string primary_segment_id;            // Best-matching population segment
    double segment_fit_score = 0.0;            // [0,1] how well agent matches segment
};

struct AgentPsychographics {
    // Personality traits (Big 5)
    double openness = 0.5;                     // [0,1]
    double conscientiousness = 0.5;            // [0,1]
    double extraversion = 0.5;                 // [0,1]
    double agreeableness = 0.5;                // [0,1]
    double neuroticism = 0.5;                  // [0,1]

    // Social media behavior
    double posting_frequency = 1.0;            // Posts per day
    double engagement_propensity = 0.5;        // [0,1] likelihood to comment/share
    double virality_seeking = 0.5;             // [0,1] desire for viral content
    double outrage_susceptibility = 0.5;       // [0,1] clickbait vulnerability

    // Influence dynamics
    double susceptibility = 0.5;               // [0,1] (from segment)
    double identity_rigidity = 0.5;            // [0,1] resistance to belief change
    double bounded_confidence_tau = 1.5;       // Threshold for rejecting divergent views
    double trust_in_sources_base = 0.5;        // [0,1] default trust level

    // Social graph position
    int follower_count = 0;
    int following_count = 0;
    double centrality_score = 0.0;             // Network centrality (computed)
    bool verified_status = false;
    bool influencer_status = false;            // >10k followers
};

class Agent {
public:
    AgentId id;
    std::mt19937 rng;

    double agent_weight = 1.0;
    ActivityPreferences activity;
    IdentityState identity;
    EmotionState emotion;
    RewardWeights personality;

    // Phase 6: Full demographic and psychographic profiles
    AgentDemographics demographics;
    AgentPsychographics psychographics;

    // Dimensional identity similarity engine (set at init, owned by Country/Sim)
    const IdentitySpace* identity_space = nullptr;

    double time_remaining = 0.0;
    std::unordered_map<TopicId, Belief> beliefs;
    std::deque<ContentId> recent_impressions;
    size_t max_recent_impressions = 200;

    FeedPriorityQueue feed_queue;

    AttentionSystem attention;
    BeliefDynamicsEngine belief_engine;  // Phase 3: Advanced influence dynamics
    BanditPolicy policy;

    std::vector<Impression> daily_impressions_consumed;
    std::vector<Interaction> daily_actions;

    explicit Agent(const AgentId& agent_id, uint32_t seed);

    void reset_time(double minutes);
    void reflect();

    PlannedAction plan_action(int tick);
    PerceptionPlan plan_perception(
        const Content& content,
        double trust = 0.5,
        double proximity = 0.0,
        bool compute_delta = true,
        const std::optional<ContentId>& stimulus_id = std::nullopt
    );

    bool apply_planned_action(const PlannedAction& plan, WorldContext* context = nullptr);
    void apply_perception_plan(const PerceptionPlan& plan, WorldContext* context = nullptr);
    void apply_perception_plan_local(
        const PerceptionPlan& plan,
        double& remaining_minutes,
        std::vector<std::pair<AgentId, BeliefDelta>>* out_deltas = nullptr
    );

    void enqueue_content(
        const Content& content,
        int tick,
        int current_tick,
        double engagement,
        double proximity = 0.0,
        double mutual_score = 0.0);
    void enqueue_content(
        const Content* content,
        int tick,
        int current_tick,
        double engagement,
        double proximity = 0.0,
        double mutual_score = 0.0);
    std::optional<FeedItem> dequeue_next_content();
    void clear_feed();

    void dream();
    void consolidate_daily();

    void apply_belief_delta(const BeliefDelta& delta);

    // Phase 6: Homophily and demographic influence
    double compute_similarity(const Agent& other) const;
    double compute_influence_weight(const Agent& source) const;

private:
    bool spend_time(double minutes);
    void remember_impression(const Impression& imp);
    void nudge_salience(const TopicId& topic, double delta);
    void nudge_knowledge(const TopicId& topic, double delta);
};
