#pragma once

#include <optional>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

#include "types.h"

class NetworkGraph {
public:
    void add_edge(const AgentId& follower, const AgentId& followed, std::optional<double> trust = std::nullopt);
    std::vector<AgentId> get_followers(const AgentId& agent_id) const;
    std::vector<AgentId> get_following(const AgentId& agent_id) const;
    const std::unordered_set<AgentId>& get_followers_ref(const AgentId& agent_id) const;
    const std::unordered_set<AgentId>& get_following_ref(const AgentId& agent_id) const;
    std::optional<double> get_edge_trust(const AgentId& follower, const AgentId& followed) const;
    std::optional<double> update_edge_trust(const AgentId& follower, const AgentId& followed, double delta);

private:
    std::unordered_map<AgentId, std::unordered_set<AgentId>> following_;
    std::unordered_map<AgentId, std::unordered_set<AgentId>> followers_;
    struct PairHash {
        size_t operator()(const std::pair<AgentId, AgentId>& p) const {
            return std::hash<std::string>{}(p.first) ^ (std::hash<std::string>{}(p.second) << 1);
        }
    };
    std::unordered_map<std::pair<AgentId, AgentId>, double, PairHash> edge_trust_;
    static const std::unordered_set<AgentId>& empty_set();
};

class NetworkLayer {
public:
    NetworkGraph graph;
};
