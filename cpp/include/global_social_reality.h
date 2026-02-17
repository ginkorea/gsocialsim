#pragma once

#include <map>
#include <random>
#include <string>
#include <unordered_map>
#include <utility>

#include "relationship_vector.h"
#include "types.h"

struct TopicReality {
    double truth = 0.5;
    double salience = 0.0;
    double institutional_stance = 0.0;
    double volatility = 0.02;
    double political_salience = 0.0;
};

class GlobalSocialReality {
public:
    RelationshipVector& get_relationship(const AgentId& u, const AgentId& v);
    void set_relationship(const AgentId& u, const AgentId& v, const RelationshipVector& vec);
    double update_trust(const AgentId& u, const AgentId& v, double delta);

    TopicReality& ensure_topic(const TopicId& topic);
    double truth(const TopicId& topic);
    void set_truth(const TopicId& topic, double value);
    double salience(const TopicId& topic);
    void set_salience(const TopicId& topic, double value);
    void bump_salience(const TopicId& topic, double delta);
    void decay();
    double political_salience_value(const TopicId& topic);
    void set_political_salience(const TopicId& topic, double value);

    double observe_truth(
        const TopicId& topic,
        std::mt19937* rng = nullptr,
        double noise_std = 0.08,
        double attention_gain = 1.0
    );
    double observe_salience(
        const TopicId& topic,
        std::mt19937* rng = nullptr,
        double noise_std = 0.05
    );

    double default_truth = 0.5;
    double default_volatility = 0.02;

private:
    std::pair<AgentId, AgentId> make_key(const AgentId& u, const AgentId& v) const;
    std::map<std::pair<AgentId, AgentId>, RelationshipVector> relations_;
    std::unordered_map<TopicId, TopicReality> topics_;
};
