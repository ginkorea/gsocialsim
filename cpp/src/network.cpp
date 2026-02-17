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

size_t NetworkGraph::mutual_following_count(const AgentId& a, const AgentId& b) const {
    const auto& fa = get_following_ref(a);
    const auto& fb = get_following_ref(b);
    if (fa.empty() || fb.empty()) return 0;
    const auto* small = &fa;
    const auto* large = &fb;
    if (fb.size() < fa.size()) {
        small = &fb;
        large = &fa;
    }
    size_t count = 0;
    for (const auto& id : *small) {
        if (large->find(id) != large->end()) {
            ++count;
        }
    }
    return count;
}

void NetworkGraph::compute_edge_mutual() {
    edge_mutual_.clear();
    for (const auto& kv : following_) {
        const auto& follower = kv.first;
        const auto& following = kv.second;
        for (const auto& followed : following) {
            size_t mutual = mutual_following_count(follower, followed);
            edge_mutual_[{follower, followed}] = static_cast<double>(mutual);
        }
    }
}

std::optional<double> NetworkGraph::get_edge_mutual(const AgentId& follower, const AgentId& followed) const {
    auto it = edge_mutual_.find({follower, followed});
    if (it == edge_mutual_.end()) return std::nullopt;
    return it->second;
}
