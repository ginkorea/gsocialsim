#pragma once

#include <string>
#include <unordered_map>
#include <vector>

#include "types.h"

// -----------------------------
// Module: Delivery Record
// Tracks content delivery metrics per agent per tick
// -----------------------------

struct DeliveryRecord {
    int tick = 0;
    AgentId viewer;
    std::string layer_id;
    IntakeMode intake_mode = IntakeMode::SCROLL;

    // Content delivery funnel
    std::vector<ContentId> eligible;  // All content that could be shown
    std::vector<ContentId> shown;     // Content actually shown to user
    std::vector<ContentId> seen;      // Content user actually consumed

    // Media type breakdown
    std::unordered_map<MediaType, int> media_breakdown;

    DeliveryRecord() = default;
    DeliveryRecord(int t, const AgentId& v, const std::string& layer, IntakeMode mode)
        : tick(t), viewer(v), layer_id(layer), intake_mode(mode) {}

    // Add content to eligible list
    void add_eligible(const ContentId& cid, MediaType mt) {
        eligible.push_back(cid);
        media_breakdown[mt]++;
    }

    // Mark content as shown
    void add_shown(const ContentId& cid) {
        shown.push_back(cid);
    }

    // Mark content as seen/consumed
    void add_seen(const ContentId& cid) {
        seen.push_back(cid);
    }

    // Get conversion metrics
    double shown_rate() const {
        return eligible.empty() ? 0.0 : static_cast<double>(shown.size()) / eligible.size();
    }

    double seen_rate() const {
        return shown.empty() ? 0.0 : static_cast<double>(seen.size()) / shown.size();
    }

    double overall_conversion() const {
        return eligible.empty() ? 0.0 : static_cast<double>(seen.size()) / eligible.size();
    }
};
