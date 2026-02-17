#pragma once

#include <string>
#include <vector>

using AgentId = std::string;
using TopicId = std::string;
using ContentId = std::string;

struct Belief {
    double stance = 0.0;
    double confidence = 0.0;
    double salience = 0.5;
    double knowledge = 0.5;
};

struct Impression {
    TopicId topic;
    ContentId content_id;
    double stance_signal = 0.0;
    double consumed_prob = 1.0;
    double attention_cost = 1.0;
    double identity_threat = 0.0;
    double primal_activation = 0.0;
    double credibility_signal = 0.5;
};

struct Content {
    ContentId id;
    AgentId author_id;
    TopicId topic;
    double stance = 0.0;
    std::string media_type;
    double identity_threat = 0.0;
    double primal_activation = 0.0;
    double credibility_signal = 0.5;
};

struct BeliefDelta {
    TopicId topic_id;
    double stance_delta = 0.0;
    double confidence_delta = 0.0;
};

struct Stimulus {
    ContentId id;
    int tick = 0;
    AgentId source;
    TopicId topic;
    std::string media_type;
    double stance = 0.0;
    double identity_threat = 0.0;
    double primal_activation = 0.0;
    double credibility_signal = 0.5;
};
