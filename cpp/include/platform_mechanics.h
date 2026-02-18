#pragma once

#include <unordered_map>

#include "types.h"

// -----------------------------
// Module: Platform Mechanics
// Defines platform-specific behavior and policies
// -----------------------------

struct PlatformMechanics {
    // Visibility and ranking parameters
    double visibility_threshold = 0.0;   // Min score to be shown
    double engagement_boost = 1.0;       // Multiplier for high-engagement content
    double recency_weight = 0.4;         // Weight for recency in ranking
    double engagement_weight = 0.45;     // Weight for engagement in ranking
    double proximity_weight = 0.1;       // Weight for proximity in ranking
    double mutual_weight = 0.05;         // Weight for mutual connections in ranking

    // Format costs (time in minutes to produce content)
    std::unordered_map<MediaType, double> format_costs;

    // Ranking weights per media type (multipliers)
    std::unordered_map<MediaType, double> ranking_weights;

    // Media-specific consumption biases
    std::unordered_map<MediaType, double> consume_bias;

    // Media-specific interaction biases
    std::unordered_map<MediaType, double> interact_bias;

    PlatformMechanics() {
        // Default format costs (minutes to create)
        format_costs[MediaType::MEME] = 2.0;
        format_costs[MediaType::SOCIAL_POST] = 3.0;
        format_costs[MediaType::NEWS] = 15.0;
        format_costs[MediaType::VIDEO] = 30.0;
        format_costs[MediaType::FORUM_THREAD] = 10.0;
        format_costs[MediaType::LONGFORM] = 45.0;

        // Default ranking weights (neutral)
        ranking_weights[MediaType::MEME] = 1.0;
        ranking_weights[MediaType::SOCIAL_POST] = 1.0;
        ranking_weights[MediaType::NEWS] = 1.0;
        ranking_weights[MediaType::VIDEO] = 1.0;
        ranking_weights[MediaType::FORUM_THREAD] = 1.0;
        ranking_weights[MediaType::LONGFORM] = 1.0;

        // Default consume bias (from agent.cpp)
        consume_bias[MediaType::NEWS] = 0.85;
        consume_bias[MediaType::SOCIAL_POST] = 0.65;
        consume_bias[MediaType::VIDEO] = 0.60;
        consume_bias[MediaType::MEME] = 0.55;
        consume_bias[MediaType::LONGFORM] = 0.50;
        consume_bias[MediaType::FORUM_THREAD] = 0.45;

        // Default interact bias
        interact_bias[MediaType::SOCIAL_POST] = 0.28;
        interact_bias[MediaType::MEME] = 0.22;
        interact_bias[MediaType::VIDEO] = 0.18;
        interact_bias[MediaType::FORUM_THREAD] = 0.16;
        interact_bias[MediaType::LONGFORM] = 0.10;
        interact_bias[MediaType::NEWS] = 0.08;
    }

    // Get format cost for a media type
    double get_format_cost(MediaType mt) const {
        auto it = format_costs.find(mt);
        return it != format_costs.end() ? it->second : 5.0;
    }

    // Get ranking weight for a media type
    double get_ranking_weight(MediaType mt) const {
        auto it = ranking_weights.find(mt);
        return it != ranking_weights.end() ? it->second : 1.0;
    }

    // Get consume bias for a media type
    double get_consume_bias(MediaType mt) const {
        auto it = consume_bias.find(mt);
        return it != consume_bias.end() ? it->second : 0.5;
    }

    // Get interact bias for a media type
    double get_interact_bias(MediaType mt) const {
        auto it = interact_bias.find(mt);
        return it != interact_bias.end() ? it->second : 0.1;
    }
};
