#pragma once

#include <deque>
#include <optional>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

#include "feed_queue.h"
#include "types.h"

struct WorldContext;

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

class Agent {
public:
    AgentId id;
    std::mt19937 rng;

    double agent_weight = 1.0;
    ActivityPreferences activity;
    IdentityState identity;
    EmotionState emotion;
    RewardWeights personality;

    double time_remaining = 0.0;
    std::unordered_map<TopicId, Belief> beliefs;
    std::deque<ContentId> recent_impressions;
    size_t max_recent_impressions = 200;

    FeedPriorityQueue feed_queue;

    AttentionSystem attention;
    BeliefUpdateEngine belief_engine;
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

    void enqueue_content(const Content& content, int tick, int current_tick, double engagement);
    std::optional<FeedItem> dequeue_next_content();

    void dream();
    void consolidate_daily();

private:
    bool spend_time(double minutes);
    void remember_impression(const Impression& imp);
    void apply_belief_delta(const BeliefDelta& delta);
    void nudge_salience(const TopicId& topic, double delta);
    void nudge_knowledge(const TopicId& topic, double delta);
};
