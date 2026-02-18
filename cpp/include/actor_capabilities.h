#pragma once

#include "country.h"
#include <cmath>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>

// ============================================================================
// Phase 3: Actor Capabilities Model
// ============================================================================
//
// International actors (BBC, RT, Al Jazeera, UN, Greenpeace, etc.) have
// different **capabilities** that determine what content they can produce,
// where it can reach, and how believable it is.
//
// ActorCapabilities formalizes these properties:
//
//   production_capacity  -- how much content per tick (bounded)
//   targeting_precision  -- how well actor can microtarget demographics
//   language_coverage    -- which languages actor produces content in
//   amplification_budget -- resources for paid promotion
//   credibility_floor    -- minimum credibility even in hostile countries
//   credibility_ceiling  -- maximum credibility even in friendly countries
//
// Capability constraints prevent unrealistic outcomes:
//   - RT cannot have high credibility in US (ceiling enforced)
//   - BBC cannot produce content in 50 languages (language_coverage bounded)
//   - Greenpeace cannot microtarget like a state actor (precision bounded)
//
// Invariants:
//   - production_capacity in [0, 100] content items per tick
//   - targeting_precision in [0, 1] where 1.0 = perfect demographic targeting
//   - credibility_floor <= credibility_ceiling
//   - credibility per country in [floor, ceiling]
//   - amplification_budget >= 0

struct ActorCapabilities {
    // Content production
    double production_capacity = 10.0;     // Max content items per tick
    double content_quality = 0.5;          // [0, 1] -- baseline quality of produced content

    // Targeting
    double targeting_precision = 0.3;      // [0, 1] -- ability to microtarget
    bool can_use_inauthentic_accounts = false;  // State actors / troll farms
    double astroturf_capacity = 0.0;       // [0, 1] -- ability to create fake grassroots

    // Language coverage
    std::vector<std::string> production_languages;  // Languages for content creation
    std::unordered_map<std::string, double> language_quality;  // Lang -> quality [0,1]

    // Financial resources
    double amplification_budget = 0.0;     // Resources for paid promotion per tick
    double budget_per_country_cap = 0.0;   // Max spend per country per tick

    // Credibility bounds (prevents unrealistic scenarios)
    double credibility_floor = 0.05;       // Min credibility anywhere
    double credibility_ceiling = 0.95;     // Max credibility anywhere

    // Per-country credibility overrides (between floor and ceiling)
    std::unordered_map<std::string, double> credibility_overrides;

    // Influence reach
    double global_reach_base = 0.1;        // [0, 1] -- base reach without targeting
    std::unordered_map<std::string, double> per_country_reach;  // Country-specific reach

    // Get effective credibility for a country (clamped to [floor, ceiling])
    double get_credibility(const std::string& country_id) const;

    // Get effective reach for a country
    double get_reach(const std::string& country_id) const;

    // Check if actor can produce content in a given language
    bool can_produce_in(const std::string& language) const;

    // Get content quality in a specific language (may be lower than base)
    double get_language_quality(const std::string& language) const;

    // Validate all bounds
    bool validate() const;
};

// ============================================================================
// Actor Capability Profiles (Factory)
// ============================================================================

class ActorCapabilityFactory {
public:
    // Create capability profile based on actor type
    static ActorCapabilities create_for_actor(const InternationalActor& actor);

    // Preset profiles for common actor types
    static ActorCapabilities international_media_profile();    // BBC, CNN, Reuters
    static ActorCapabilities state_media_profile();            // RT, CGTN, PressTV
    static ActorCapabilities multilateral_org_profile();       // UN, WHO, IMF
    static ActorCapabilities regional_org_profile();           // EU, African Union
    static ActorCapabilities global_ngo_profile();             // Greenpeace, HRW
    static ActorCapabilities multinational_corp_profile();     // Apple, BP
    static ActorCapabilities global_celebrity_profile();       // Pope, Greta
};

// ============================================================================
// Content Generation from Actor Capabilities
// ============================================================================

// Determine how many content items an actor produces in a given tick
// Accounts for production capacity, language constraints, and budget
int compute_actor_production(
    const InternationalActor& actor,
    const ActorCapabilities& caps,
    int tick);

// Compute the effective targeting score for content delivered to a country
// Accounts for targeting precision, available data, and country-specific factors
double compute_targeting_effectiveness(
    const ActorCapabilities& caps,
    const std::string& target_country,
    const GlobalGeoHierarchy& geo);
