#pragma once

#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "types.h"

// -----------------------------
// Module: Subscription Service
// Opt-in feed semantics for content delivery
// -----------------------------

enum class SubscriptionType {
    CREATOR = 0,   // Subscribe to a specific agent's content
    TOPIC,         // Subscribe to a topic category
    OUTLET,        // Subscribe to a media outlet
    COMMUNITY      // Subscribe to a community/group
};

struct Subscription {
    AgentId subscriber;
    SubscriptionType type;
    std::string target_id;  // CreatorId / TopicId / OutletId / CommunityId
    double strength;        // [0,1] opt-in intensity/weight
    int created_tick;

    Subscription() = default;
    Subscription(const AgentId& sub, SubscriptionType t, const std::string& target, double str, int tick)
        : subscriber(sub), type(t), target_id(target), strength(str), created_tick(tick) {}
};

class SubscriptionService {
public:
    SubscriptionService() = default;

    // Subscribe agent to a target (creator/topic/outlet/community)
    void subscribe(const AgentId& agent_id, SubscriptionType type, const std::string& target_id, double strength, int tick);

    // Unsubscribe agent from a target
    void unsubscribe(const AgentId& agent_id, SubscriptionType type, const std::string& target_id);

    // Get all subscriptions for an agent
    std::vector<Subscription> get_subscriptions(const AgentId& agent_id) const;

    // Check if agent is subscribed to a target
    bool is_subscribed(const AgentId& agent_id, SubscriptionType type, const std::string& target_id) const;

    // Get subscription strength (0.0 if not subscribed)
    double get_subscription_strength(const AgentId& agent_id, SubscriptionType type, const std::string& target_id) const;

    // Get all subscribers for a target
    std::unordered_set<AgentId> get_subscribers(SubscriptionType type, const std::string& target_id) const;

    // Get subscriber count for a target
    size_t subscriber_count(SubscriptionType type, const std::string& target_id) const;

    // Clear all subscriptions (for testing/reset)
    void clear();

    // Stats
    size_t total_subscriptions() const;
    size_t total_subscribers() const;

private:
    // Fast lookup: agent -> list of their subscriptions
    std::unordered_map<AgentId, std::vector<Subscription>> subs_by_agent_;

    // Fast lookup: (type, target) -> set of subscribers
    // Key format: "type:target_id"
    std::unordered_map<std::string, std::unordered_set<AgentId>> subscribers_by_target_;

    // Helper to create lookup key
    static std::string make_key(SubscriptionType type, const std::string& target_id);
};
