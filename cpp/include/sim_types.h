#pragma once

#include <string>

struct Belief {
    double stance = 0.0;
    double confidence = 0.0;
    double salience = 0.5;
    double knowledge = 0.5;
};

struct Impression {
    double stance_signal = 0.0;
    double consumed_prob = 1.0;
    double attention_cost = 1.0;
    double identity_threat = 0.0;
    double primal_activation = 0.0;
    double credibility_signal = 0.5;
};

struct Content {
    std::string id;
    std::string author_id;
    std::string topic;
    double stance = 0.0;
    std::string media_type;
    double identity_threat = 0.0;
    double primal_activation = 0.0;
    double credibility_signal = 0.5;
};
