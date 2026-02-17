#include "global_social_reality.h"

#include <algorithm>

static inline double clamp01(double v) {
    if (v < 0.0) return 0.0;
    if (v > 1.0) return 1.0;
    return v;
}

std::pair<AgentId, AgentId> GlobalSocialReality::make_key(const AgentId& u, const AgentId& v) const {
    if (u == v) return {u, v};
    return (u < v) ? std::make_pair(u, v) : std::make_pair(v, u);
}

RelationshipVector& GlobalSocialReality::get_relationship(const AgentId& u, const AgentId& v) {
    auto key = make_key(u, v);
    auto it = relations_.find(key);
    if (it != relations_.end()) {
        return it->second;
    }
    RelationshipVector vec;
    if (u == v) {
        vec.affinity = 1.0;
        vec.trust = 1.0;
        vec.intimacy = 1.0;
        vec.conflict = 0.0;
        vec.reciprocity = 1.0;
        vec.status_delta = 0.0;
    }
    auto res = relations_.emplace(key, vec);
    return res.first->second;
}

void GlobalSocialReality::set_relationship(const AgentId& u, const AgentId& v, const RelationshipVector& vec) {
    relations_[make_key(u, v)] = vec;
}

double GlobalSocialReality::update_trust(const AgentId& u, const AgentId& v, double delta) {
    auto& rel = get_relationship(u, v);
    rel.trust = clamp01(rel.trust + delta);
    return rel.trust;
}

TopicReality& GlobalSocialReality::ensure_topic(const TopicId& topic) {
    auto it = topics_.find(topic);
    if (it != topics_.end()) return it->second;
    TopicReality tr;
    tr.truth = default_truth;
    tr.salience = 0.0;
    tr.volatility = default_volatility;
    auto res = topics_.emplace(topic, tr);
    return res.first->second;
}

double GlobalSocialReality::truth(const TopicId& topic) {
    return ensure_topic(topic).truth;
}

void GlobalSocialReality::set_truth(const TopicId& topic, double value) {
    ensure_topic(topic).truth = clamp01(value);
}

double GlobalSocialReality::salience(const TopicId& topic) {
    return ensure_topic(topic).salience;
}

void GlobalSocialReality::set_salience(const TopicId& topic, double value) {
    ensure_topic(topic).salience = clamp01(value);
}

void GlobalSocialReality::bump_salience(const TopicId& topic, double delta) {
    auto& tr = ensure_topic(topic);
    tr.salience = clamp01(tr.salience + delta);
}

void GlobalSocialReality::decay() {
    for (auto& kv : topics_) {
        kv.second.salience = clamp01(kv.second.salience * (1.0 - kv.second.volatility));
    }
}

double GlobalSocialReality::political_salience_value(const TopicId& topic) {
    return ensure_topic(topic).political_salience;
}

void GlobalSocialReality::set_political_salience(const TopicId& topic, double value) {
    ensure_topic(topic).political_salience = clamp01(value);
}

double GlobalSocialReality::observe_truth(
    const TopicId& topic,
    std::mt19937* rng,
    double noise_std,
    double attention_gain
) {
    auto& tr = ensure_topic(topic);
    double std = std::max(1e-6, noise_std / std::max(1e-6, attention_gain));
    std::normal_distribution<double> dist(0.0, std);
    if (rng) {
        return clamp01(tr.truth + dist(*rng));
    }
    std::mt19937 local_rng(std::random_device{}());
    return clamp01(tr.truth + dist(local_rng));
}

double GlobalSocialReality::observe_salience(
    const TopicId& topic,
    std::mt19937* rng,
    double noise_std
) {
    auto& tr = ensure_topic(topic);
    std::normal_distribution<double> dist(0.0, std::max(1e-6, noise_std));
    if (rng) {
        return clamp01(tr.salience + dist(*rng));
    }
    std::mt19937 local_rng(std::random_device{}());
    return clamp01(tr.salience + dist(local_rng));
}
