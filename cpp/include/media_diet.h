#pragma once

#include "country.h"
#include <cmath>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>

// ============================================================================
// Phase 2: Media Diet -- Budget Conservation & Saturation
// ============================================================================
//
// A media diet defines how an agent allocates finite attention across media
// sources from different countries. The core constraint is **budget
// conservation**: all allocations must sum to exactly 1.0.
//
//   origin_share + residence_share + sum(international_shares) = 1.0
//
// For domestic agents (non-diaspora), origin_share == residence_share and
// there is no split. Diaspora agents split attention between origin and
// residence country media, plus optional international sources.
//
// **Saturation model**: Media consumption from a single source has
// diminishing returns. An agent consuming 80% of media from one source
// doesn't get 80% of the information -- they hit saturation. Effective
// information intake follows:
//
//   effective(share) = 1 - exp(-k * share)   where k controls saturation rate
//
// This means a 50/50 split gives more total information than 100/0.
//
// Invariants:
//   - Budget sums to 1.0 (within epsilon)
//   - All shares in [0, 1]
//   - Effective intake per source <= raw share
//   - Total effective intake < 1.0 (saturation always loses some)
//   - Domestic agent: origin_share >= 0.8

struct MediaSource {
    std::string country_id;       // Media origin country
    std::string source_type;      // "domestic", "origin", "residence", "international"
    double share = 0.0;           // [0, 1] -- fraction of attention budget
};

struct MediaDiet {
    std::string agent_country_id;          // Agent's country of residence
    std::string origin_country_id;         // Origin country (same as agent_country for non-diaspora)
    bool is_diaspora = false;

    // Budget allocation
    double origin_share = 0.0;             // Media from origin country
    double residence_share = 0.0;          // Media from residence country
    std::unordered_map<std::string, double> international_shares;  // Other country media

    // Saturation parameter
    double saturation_k = 3.0;             // Higher = faster saturation

    // Create a domestic (non-diaspora) media diet
    static MediaDiet create_domestic(const std::string& country_id, double intl_share = 0.05);

    // Create a diaspora media diet from a DiasporaSegment
    static MediaDiet create_from_diaspora(const DiasporaSegment& segment);

    // Validate budget conservation: all shares sum to 1.0
    bool validate() const;

    // Normalize shares to sum to 1.0 (fixes floating point drift)
    void normalize();

    // Get the raw share for media from a given country
    double get_share(const std::string& country_id) const;

    // Get the effective (post-saturation) intake for a given country's media
    double get_effective_intake(const std::string& country_id) const;

    // Get total effective intake across all sources (always < 1.0 due to saturation)
    double get_total_effective_intake() const;

    // Get all sources as a flat list
    std::vector<MediaSource> get_sources() const;

    // Adjust shares after an event (e.g., crisis in origin country increases origin media)
    void shift_toward(const std::string& country_id, double delta);
};

// ============================================================================
// Media Diet Factory
// ============================================================================

// Generate media diets for all agents in a country, accounting for diaspora
class MediaDietFactory {
public:
    // Create default domestic diet for a country
    static MediaDiet create_default_domestic(const std::string& country_id);

    // Create diaspora diet with dual media consumption
    static MediaDiet create_diaspora_diet(
        const DiasporaSegment& segment,
        double origin_weight_override = -1.0);

    // Apply saturation curve: effective = 1 - exp(-k * share)
    static double saturation_curve(double share, double k = 3.0);
};
