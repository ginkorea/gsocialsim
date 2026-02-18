#include "subscription_service.h"

#include <algorithm>
#include <sstream>

// Helper to create lookup key for subscribers_by_target_
std::string SubscriptionService::make_key(SubscriptionType type, const std::string& target_id) {
    std::ostringstream oss;
    oss << static_cast<int>(type) << ":" << target_id;
    return oss.str();
}

void SubscriptionService::subscribe(const AgentId& agent_id, SubscriptionType type,
                                     const std::string& target_id, double strength, int tick) {
    // Clamp strength to [0, 1]
    strength = std::max(0.0, std::min(1.0, strength));

    // Check if already subscribed
    auto& agent_subs = subs_by_agent_[agent_id];
    for (auto& sub : agent_subs) {
        if (sub.type == type && sub.target_id == target_id) {
            // Update existing subscription
            sub.strength = strength;
            sub.created_tick = tick;
            return;
        }
    }

    // Add new subscription
    agent_subs.emplace_back(agent_id, type, target_id, strength, tick);

    // Update reverse index
    std::string key = make_key(type, target_id);
    subscribers_by_target_[key].insert(agent_id);
}

void SubscriptionService::unsubscribe(const AgentId& agent_id, SubscriptionType type,
                                       const std::string& target_id) {
    // Remove from agent's subscription list
    auto it = subs_by_agent_.find(agent_id);
    if (it != subs_by_agent_.end()) {
        auto& subs = it->second;
        subs.erase(
            std::remove_if(subs.begin(), subs.end(),
                [&](const Subscription& sub) {
                    return sub.type == type && sub.target_id == target_id;
                }),
            subs.end()
        );

        // Clean up if no subscriptions left
        if (subs.empty()) {
            subs_by_agent_.erase(it);
        }
    }

    // Remove from reverse index
    std::string key = make_key(type, target_id);
    auto it2 = subscribers_by_target_.find(key);
    if (it2 != subscribers_by_target_.end()) {
        it2->second.erase(agent_id);

        // Clean up if no subscribers left
        if (it2->second.empty()) {
            subscribers_by_target_.erase(it2);
        }
    }
}

std::vector<Subscription> SubscriptionService::get_subscriptions(const AgentId& agent_id) const {
    auto it = subs_by_agent_.find(agent_id);
    if (it != subs_by_agent_.end()) {
        return it->second;
    }
    return {};
}

bool SubscriptionService::is_subscribed(const AgentId& agent_id, SubscriptionType type,
                                         const std::string& target_id) const {
    auto it = subs_by_agent_.find(agent_id);
    if (it != subs_by_agent_.end()) {
        for (const auto& sub : it->second) {
            if (sub.type == type && sub.target_id == target_id) {
                return true;
            }
        }
    }
    return false;
}

double SubscriptionService::get_subscription_strength(const AgentId& agent_id, SubscriptionType type,
                                                       const std::string& target_id) const {
    auto it = subs_by_agent_.find(agent_id);
    if (it != subs_by_agent_.end()) {
        for (const auto& sub : it->second) {
            if (sub.type == type && sub.target_id == target_id) {
                return sub.strength;
            }
        }
    }
    return 0.0;
}

std::unordered_set<AgentId> SubscriptionService::get_subscribers(SubscriptionType type,
                                                                  const std::string& target_id) const {
    std::string key = make_key(type, target_id);
    auto it = subscribers_by_target_.find(key);
    if (it != subscribers_by_target_.end()) {
        return it->second;
    }
    return {};
}

size_t SubscriptionService::subscriber_count(SubscriptionType type, const std::string& target_id) const {
    std::string key = make_key(type, target_id);
    auto it = subscribers_by_target_.find(key);
    if (it != subscribers_by_target_.end()) {
        return it->second.size();
    }
    return 0;
}

void SubscriptionService::clear() {
    subs_by_agent_.clear();
    subscribers_by_target_.clear();
}

size_t SubscriptionService::total_subscriptions() const {
    size_t total = 0;
    for (const auto& [agent_id, subs] : subs_by_agent_) {
        total += subs.size();
    }
    return total;
}

size_t SubscriptionService::total_subscribers() const {
    return subs_by_agent_.size();
}
