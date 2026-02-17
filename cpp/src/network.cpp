#include "network.h"

static inline double clamp01(double v) {
    if (v < 0.0) return 0.0;
    if (v > 1.0) return 1.0;
    return v;
}

const std::unordered_set<AgentId>& NetworkGraph::empty_set() {
    static const std::unordered_set<AgentId> empty;
    return empty;
}

void NetworkGraph::add_edge(const AgentId& follower, const AgentId& followed, std::optional<double> trust) {
    following_[follower].insert(followed);
    followers_[followed].insert(follower);
    double trust_val = 0.5;
    if (trust.has_value()) {
        trust_val = clamp01(trust.value());
    }
    edge_trust_[{follower, followed}] = trust_val;
}

std::vector<AgentId> NetworkGraph::get_followers(const AgentId& agent_id) const {
    auto it = followers_.find(agent_id);
    if (it == followers_.end()) return {};
    return std::vector<AgentId>(it->second.begin(), it->second.end());
}

std::vector<AgentId> NetworkGraph::get_following(const AgentId& agent_id) const {
    auto it = following_.find(agent_id);
    if (it == following_.end()) return {};
    return std::vector<AgentId>(it->second.begin(), it->second.end());
}

const std::unordered_set<AgentId>& NetworkGraph::get_followers_ref(const AgentId& agent_id) const {
    auto it = followers_.find(agent_id);
    if (it == followers_.end()) return empty_set();
    return it->second;
}

const std::unordered_set<AgentId>& NetworkGraph::get_following_ref(const AgentId& agent_id) const {
    auto it = following_.find(agent_id);
    if (it == following_.end()) return empty_set();
    return it->second;
}

std::optional<double> NetworkGraph::get_edge_trust(const AgentId& follower, const AgentId& followed) const {
    auto it = edge_trust_.find({follower, followed});
    if (it == edge_trust_.end()) return std::nullopt;
    return it->second;
}

std::optional<double> NetworkGraph::update_edge_trust(const AgentId& follower, const AgentId& followed, double delta) {
    auto it = edge_trust_.find({follower, followed});
    if (it == edge_trust_.end()) return std::nullopt;
    it->second = clamp01(it->second + delta);
    return it->second;
}
