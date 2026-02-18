#include "actor_capabilities.h"
#include <cmath>
#include <algorithm>

// ============================================================================
// ActorCapabilities Implementation
// ============================================================================

double ActorCapabilities::get_credibility(const std::string& country_id) const {
    double cred = credibility_floor; // Start at floor

    auto it = credibility_overrides.find(country_id);
    if (it != credibility_overrides.end()) {
        cred = it->second;
    } else {
        // Default: midpoint between floor and ceiling
        cred = (credibility_floor + credibility_ceiling) / 2.0;
    }

    return std::clamp(cred, credibility_floor, credibility_ceiling);
}

double ActorCapabilities::get_reach(const std::string& country_id) const {
    auto it = per_country_reach.find(country_id);
    if (it != per_country_reach.end()) {
        return std::clamp(it->second, 0.0, 1.0);
    }
    return std::clamp(global_reach_base, 0.0, 1.0);
}

bool ActorCapabilities::can_produce_in(const std::string& language) const {
    for (const auto& lang : production_languages) {
        if (lang == language) return true;
    }
    return false;
}

double ActorCapabilities::get_language_quality(const std::string& language) const {
    auto it = language_quality.find(language);
    if (it != language_quality.end()) {
        return std::clamp(it->second, 0.0, 1.0);
    }
    // If language not explicitly listed, check if it's a production language
    if (can_produce_in(language)) {
        return content_quality; // Use base quality
    }
    return 0.0; // Cannot produce in this language
}

bool ActorCapabilities::validate() const {
    if (production_capacity < 0.0 || production_capacity > 100.0) return false;
    if (content_quality < 0.0 || content_quality > 1.0) return false;
    if (targeting_precision < 0.0 || targeting_precision > 1.0) return false;
    if (astroturf_capacity < 0.0 || astroturf_capacity > 1.0) return false;
    if (amplification_budget < 0.0) return false;
    if (credibility_floor < 0.0 || credibility_floor > 1.0) return false;
    if (credibility_ceiling < 0.0 || credibility_ceiling > 1.0) return false;
    if (credibility_floor > credibility_ceiling) return false;
    if (global_reach_base < 0.0 || global_reach_base > 1.0) return false;

    // Validate per-country credibility overrides
    for (const auto& [_, cred] : credibility_overrides) {
        if (cred < 0.0 || cred > 1.0) return false;
    }

    return true;
}

// ============================================================================
// Actor Capability Factory
// ============================================================================

ActorCapabilities ActorCapabilityFactory::create_for_actor(const InternationalActor& actor) {
    switch (actor.actor_type) {
        case InternationalActor::ActorType::INTERNATIONAL_MEDIA:
            return international_media_profile();
        case InternationalActor::ActorType::FOREIGN_STATE_MEDIA:
            return state_media_profile();
        case InternationalActor::ActorType::INTERNATIONAL_ORG:
            return multilateral_org_profile();
        case InternationalActor::ActorType::REGIONAL_ORG:
            return regional_org_profile();
        case InternationalActor::ActorType::GLOBAL_NGO:
            return global_ngo_profile();
        case InternationalActor::ActorType::MULTINATIONAL_CORP:
            return multinational_corp_profile();
        case InternationalActor::ActorType::GLOBAL_CELEBRITY:
            return global_celebrity_profile();
    }
    // Fallback
    return international_media_profile();
}

ActorCapabilities ActorCapabilityFactory::international_media_profile() {
    ActorCapabilities caps;

    // High production, high quality, moderate reach
    caps.production_capacity = 50.0;       // High output (BBC, CNN, Reuters)
    caps.content_quality = 0.75;           // Professional journalism
    caps.targeting_precision = 0.3;        // Some audience awareness, not microtargeting
    caps.can_use_inauthentic_accounts = false;
    caps.astroturf_capacity = 0.0;

    caps.production_languages = {"en"};    // Caller should override per actor
    caps.language_quality = {{"en", 0.95}};

    caps.amplification_budget = 0.5;       // Moderate paid promotion
    caps.budget_per_country_cap = 0.1;

    caps.credibility_floor = 0.20;         // Even in hostile countries, some credibility
    caps.credibility_ceiling = 0.90;       // High but not perfect

    caps.global_reach_base = 0.15;         // Moderate global baseline

    return caps;
}

ActorCapabilities ActorCapabilityFactory::state_media_profile() {
    ActorCapabilities caps;

    // High production (state-funded), lower quality, high targeting
    caps.production_capacity = 80.0;       // State funding = high output
    caps.content_quality = 0.45;           // Mixed quality (some good, some propaganda)
    caps.targeting_precision = 0.75;       // State actors invest in microtargeting
    caps.can_use_inauthentic_accounts = true;
    caps.astroturf_capacity = 0.6;         // Can create fake grassroots campaigns

    caps.production_languages = {"en", "ru"};  // Override per actor
    caps.language_quality = {{"ru", 0.95}, {"en", 0.70}};

    caps.amplification_budget = 2.0;       // Large budget for promotion
    caps.budget_per_country_cap = 0.5;

    caps.credibility_floor = 0.05;         // Very low in hostile countries
    caps.credibility_ceiling = 0.70;       // Never fully credible internationally
    // Home country credibility set via overrides

    caps.global_reach_base = 0.08;         // Lower organic reach (people avoid state media)

    return caps;
}

ActorCapabilities ActorCapabilityFactory::multilateral_org_profile() {
    ActorCapabilities caps;

    // Low production, high quality, high credibility
    caps.production_capacity = 5.0;        // Slow, deliberate output
    caps.content_quality = 0.85;           // Expert reports, data-driven
    caps.targeting_precision = 0.1;        // Not targeting, broadcasting
    caps.can_use_inauthentic_accounts = false;
    caps.astroturf_capacity = 0.0;

    caps.production_languages = {"en", "fr", "es", "ar", "zh", "ru"};  // UN official languages
    caps.language_quality = {
        {"en", 0.95}, {"fr", 0.90}, {"es", 0.90},
        {"ar", 0.85}, {"zh", 0.85}, {"ru", 0.85}
    };

    caps.amplification_budget = 0.2;       // Modest budget
    caps.budget_per_country_cap = 0.05;

    caps.credibility_floor = 0.15;         // Even skeptics acknowledge UN exists
    caps.credibility_ceiling = 0.85;       // High but modulated by institutional trust

    caps.global_reach_base = 0.10;         // Moderate -- mediated through national press

    return caps;
}

ActorCapabilities ActorCapabilityFactory::regional_org_profile() {
    ActorCapabilities caps;

    caps.production_capacity = 8.0;
    caps.content_quality = 0.70;
    caps.targeting_precision = 0.15;
    caps.can_use_inauthentic_accounts = false;
    caps.astroturf_capacity = 0.0;

    caps.production_languages = {"en", "fr"};
    caps.language_quality = {{"en", 0.90}, {"fr", 0.85}};

    caps.amplification_budget = 0.3;
    caps.budget_per_country_cap = 0.1;

    caps.credibility_floor = 0.10;
    caps.credibility_ceiling = 0.80;

    caps.global_reach_base = 0.05;         // Limited to region

    return caps;
}

ActorCapabilities ActorCapabilityFactory::global_ngo_profile() {
    ActorCapabilities caps;

    caps.production_capacity = 15.0;
    caps.content_quality = 0.70;
    caps.targeting_precision = 0.4;        // NGOs know their audience
    caps.can_use_inauthentic_accounts = false;
    caps.astroturf_capacity = 0.0;

    caps.production_languages = {"en"};
    caps.language_quality = {{"en", 0.90}};

    caps.amplification_budget = 0.8;       // Donor-funded campaigns
    caps.budget_per_country_cap = 0.2;

    caps.credibility_floor = 0.10;         // Some countries hostile to foreign NGOs
    caps.credibility_ceiling = 0.80;

    caps.global_reach_base = 0.08;

    return caps;
}

ActorCapabilities ActorCapabilityFactory::multinational_corp_profile() {
    ActorCapabilities caps;

    caps.production_capacity = 20.0;
    caps.content_quality = 0.60;           // Polished but commercial
    caps.targeting_precision = 0.8;        // Corporations excel at ad targeting
    caps.can_use_inauthentic_accounts = false;
    caps.astroturf_capacity = 0.3;         // Some astroturfing capability

    caps.production_languages = {"en"};
    caps.language_quality = {{"en", 0.90}};

    caps.amplification_budget = 5.0;       // Large marketing budgets
    caps.budget_per_country_cap = 1.0;

    caps.credibility_floor = 0.10;
    caps.credibility_ceiling = 0.60;       // People are skeptical of corporate messaging

    caps.global_reach_base = 0.12;

    return caps;
}

ActorCapabilities ActorCapabilityFactory::global_celebrity_profile() {
    ActorCapabilities caps;

    caps.production_capacity = 3.0;        // Low volume, high impact
    caps.content_quality = 0.50;           // Variable quality
    caps.targeting_precision = 0.2;        // Broadcasting, not targeting
    caps.can_use_inauthentic_accounts = false;
    caps.astroturf_capacity = 0.0;

    caps.production_languages = {"en"};
    caps.language_quality = {{"en", 0.95}};

    caps.amplification_budget = 0.1;       // Don't need paid promotion
    caps.budget_per_country_cap = 0.05;

    caps.credibility_floor = 0.05;
    caps.credibility_ceiling = 0.75;       // Celebrity credibility is fragile

    caps.global_reach_base = 0.30;         // High organic reach (followers)

    return caps;
}

// ============================================================================
// Content Generation
// ============================================================================

int compute_actor_production(
    const InternationalActor& actor,
    const ActorCapabilities& caps,
    int /* tick */)
{
    // Base production from capacity
    double base = caps.production_capacity;

    // Scale by number of active countries (more countries = spread thinner)
    double country_scaling = 1.0;
    if (actor.active_countries.size() > 5) {
        // Diminishing returns: 10 countries doesn't mean 10x production
        country_scaling = 1.0 + 0.3 * std::log(static_cast<double>(actor.active_countries.size()) / 5.0);
    }

    // Language constraint: can only produce in known languages
    double lang_scaling = std::min(1.0, static_cast<double>(caps.production_languages.size()) / 3.0);

    return static_cast<int>(std::max(1.0, base * country_scaling * lang_scaling));
}

double compute_targeting_effectiveness(
    const ActorCapabilities& caps,
    const std::string& target_country,
    const GlobalGeoHierarchy& geo)
{
    // Base targeting precision
    double precision = caps.targeting_precision;

    // Targeting is harder in countries with less internet penetration
    const Country* country = const_cast<GlobalGeoHierarchy&>(geo).get_country(target_country);
    if (country) {
        precision *= country->internet_penetration;
        precision *= country->social_media_penetration;
    }

    // Inauthentic accounts can boost targeting effectiveness
    if (caps.can_use_inauthentic_accounts) {
        precision = std::min(1.0, precision * 1.3);
    }

    return std::clamp(precision, 0.0, 1.0);
}
