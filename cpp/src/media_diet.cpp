#include "media_diet.h"
#include <cmath>
#include <algorithm>
#include <numeric>

// ============================================================================
// MediaDiet Implementation
// ============================================================================

MediaDiet MediaDiet::create_domestic(const std::string& country_id, double intl_share) {
    MediaDiet diet;
    diet.agent_country_id = country_id;
    diet.origin_country_id = country_id;
    diet.is_diaspora = false;

    // Domestic agents consume mostly domestic media
    intl_share = std::clamp(intl_share, 0.0, 0.3); // Cap international at 30%
    diet.origin_share = 0.0;                         // Not applicable for domestic
    diet.residence_share = 1.0 - intl_share;
    if (intl_share > 0.001) {
        diet.international_shares["_global"] = intl_share;
    }

    return diet;
}

MediaDiet MediaDiet::create_from_diaspora(const DiasporaSegment& segment) {
    MediaDiet diet;
    diet.agent_country_id = segment.residence_country;
    diet.origin_country_id = segment.origin_country;
    diet.is_diaspora = true;

    // Diaspora media consumption from segment definition
    // These are raw consumption fractions, need to be normalized to sum to 1.0
    double origin_raw = segment.origin_media_consumption;   // e.g., 0.40
    double residence_raw = segment.residence_media_consumption; // e.g., 0.80
    double intl_raw = 0.05; // Small baseline international

    // Normalize to budget = 1.0
    double total = origin_raw + residence_raw + intl_raw;
    if (total > 0.0) {
        diet.origin_share = origin_raw / total;
        diet.residence_share = residence_raw / total;
        // Remainder goes to international
        double remainder = 1.0 - diet.origin_share - diet.residence_share;
        if (remainder > 0.001) {
            diet.international_shares["_global"] = remainder;
        }
    } else {
        // Fallback: even split
        diet.origin_share = 0.4;
        diet.residence_share = 0.55;
        diet.international_shares["_global"] = 0.05;
    }

    diet.normalize();
    return diet;
}

bool MediaDiet::validate() const {
    double total = residence_share;
    if (is_diaspora) {
        total += origin_share;
    }
    for (const auto& [_, share] : international_shares) {
        total += share;
    }
    // Budget conservation: must sum to 1.0 within epsilon
    return std::abs(total - 1.0) < 1e-6;
}

void MediaDiet::normalize() {
    double total = residence_share;
    if (is_diaspora) {
        total += origin_share;
    }
    for (const auto& [_, share] : international_shares) {
        total += share;
    }

    if (total <= 0.0) {
        // Degenerate case: reset to domestic default
        residence_share = 0.95;
        origin_share = 0.0;
        international_shares.clear();
        international_shares["_global"] = 0.05;
        return;
    }

    // Scale everything proportionally
    double scale = 1.0 / total;
    residence_share *= scale;
    if (is_diaspora) {
        origin_share *= scale;
    }
    for (auto& [_, share] : international_shares) {
        share *= scale;
    }
}

double MediaDiet::get_share(const std::string& country_id) const {
    if (country_id == agent_country_id) {
        return residence_share;
    }
    if (is_diaspora && country_id == origin_country_id) {
        return origin_share;
    }
    auto it = international_shares.find(country_id);
    if (it != international_shares.end()) {
        return it->second;
    }
    // Check for global international pool
    auto global_it = international_shares.find("_global");
    if (global_it != international_shares.end()) {
        // International sources share the global pool
        return global_it->second;
    }
    return 0.0;
}

double MediaDiet::get_effective_intake(const std::string& country_id) const {
    double share = get_share(country_id);
    return MediaDietFactory::saturation_curve(share, saturation_k);
}

double MediaDiet::get_total_effective_intake() const {
    double total = 0.0;
    total += MediaDietFactory::saturation_curve(residence_share, saturation_k);
    if (is_diaspora) {
        total += MediaDietFactory::saturation_curve(origin_share, saturation_k);
    }
    for (const auto& [_, share] : international_shares) {
        total += MediaDietFactory::saturation_curve(share, saturation_k);
    }
    return total;
}

std::vector<MediaSource> MediaDiet::get_sources() const {
    std::vector<MediaSource> sources;

    sources.push_back({agent_country_id, "residence", residence_share});

    if (is_diaspora && origin_share > 0.001) {
        sources.push_back({origin_country_id, "origin", origin_share});
    }

    for (const auto& [country, share] : international_shares) {
        if (share > 0.001) {
            sources.push_back({country, "international", share});
        }
    }

    return sources;
}

void MediaDiet::shift_toward(const std::string& country_id, double delta) {
    delta = std::clamp(delta, -0.3, 0.3); // Cap shift to prevent wild swings

    if (country_id == agent_country_id) {
        residence_share += delta;
    } else if (is_diaspora && country_id == origin_country_id) {
        origin_share += delta;
    } else {
        international_shares[country_id] += delta;
    }

    // Clamp all shares to [0, 1]
    residence_share = std::clamp(residence_share, 0.0, 1.0);
    origin_share = std::clamp(origin_share, 0.0, 1.0);
    for (auto& [_, share] : international_shares) {
        share = std::clamp(share, 0.0, 1.0);
    }

    // Re-normalize to maintain budget conservation
    normalize();
}

// ============================================================================
// MediaDietFactory Implementation
// ============================================================================

MediaDiet MediaDietFactory::create_default_domestic(const std::string& country_id) {
    MediaDiet diet;
    diet.agent_country_id = country_id;
    diet.origin_country_id = country_id;
    diet.is_diaspora = false;
    diet.residence_share = 0.92;
    diet.origin_share = 0.0;
    diet.international_shares["_global"] = 0.08;
    return diet;
}

MediaDiet MediaDietFactory::create_diaspora_diet(
    const DiasporaSegment& segment,
    double origin_weight_override)
{
    MediaDiet diet;
    diet.agent_country_id = segment.residence_country;
    diet.origin_country_id = segment.origin_country;
    diet.is_diaspora = true;

    double origin_raw = (origin_weight_override >= 0.0)
        ? origin_weight_override
        : segment.origin_media_consumption;
    double residence_raw = segment.residence_media_consumption;

    // Ensure some international exposure
    double intl_raw = std::max(0.03, 1.0 - origin_raw - residence_raw);

    double total = origin_raw + residence_raw + intl_raw;
    diet.origin_share = origin_raw / total;
    diet.residence_share = residence_raw / total;
    diet.international_shares["_global"] = intl_raw / total;

    diet.normalize();
    return diet;
}

double MediaDietFactory::saturation_curve(double share, double k) {
    // Diminishing returns: effective = 1 - exp(-k * share)
    // At share=0: effective=0
    // At share=1: effective = 1 - exp(-k) ~= 0.95 for k=3
    // At share=0.5: effective = 1 - exp(-1.5) ~= 0.78
    if (share <= 0.0) return 0.0;
    return 1.0 - std::exp(-k * share);
}
