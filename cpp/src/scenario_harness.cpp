#include "scenario_harness.h"
#include <chrono>
#include <cmath>

// ============================================================================
// ScenarioHarness Implementation
// ============================================================================

void ScenarioHarness::register_scenario(const std::string& name, ScenarioFn fn) {
    scenarios_.push_back({name, fn});
}

std::vector<ScenarioResult> ScenarioHarness::run_all() {
    std::vector<ScenarioResult> results;
    results.reserve(scenarios_.size());

    for (const auto& [name, fn] : scenarios_) {
        ScenarioResult result;
        result.name = name;

        auto start = std::chrono::high_resolution_clock::now();
        try {
            std::string reason;
            result.passed = fn(reason);
            result.failure_reason = reason;
        } catch (const std::exception& e) {
            result.passed = false;
            result.failure_reason = std::string("Exception: ") + e.what();
        }
        auto end = std::chrono::high_resolution_clock::now();
        result.duration_ms = std::chrono::duration<double, std::milli>(end - start).count();

        results.push_back(result);
    }

    return results;
}

void ScenarioHarness::print_results(const std::vector<ScenarioResult>& results) const {
    int passed = 0, failed = 0;
    for (const auto& r : results) {
        if (r.passed) {
            std::cout << "  PASS  " << r.name << " (" << r.duration_ms << "ms)\n";
            ++passed;
        } else {
            std::cout << "  FAIL  " << r.name << " -- " << r.failure_reason
                      << " (" << r.duration_ms << "ms)\n";
            ++failed;
        }
    }
    std::cout << "\n  " << passed << " passed, " << failed << " failed, "
              << results.size() << " total\n";
}

void ScenarioHarness::register_all_builtin() {
    // CrossBorderFactors
    register_scenario("cross_border_same_country", scenarios::cross_border_same_country);
    register_scenario("cross_border_high_tension", scenarios::cross_border_high_tension);
    register_scenario("cross_border_untranslated_foreign", scenarios::cross_border_untranslated_foreign);
    register_scenario("cross_border_language_barrier", scenarios::cross_border_language_barrier);
    register_scenario("cross_border_state_propaganda", scenarios::cross_border_state_propaganda);

    // MediaDiet
    register_scenario("media_diet_budget_conservation", scenarios::media_diet_budget_conservation);
    register_scenario("media_diet_saturation_diminishing", scenarios::media_diet_saturation_diminishing);
    register_scenario("media_diet_diaspora_split", scenarios::media_diet_diaspora_split);
    register_scenario("media_diet_shift_preserves_budget", scenarios::media_diet_shift_preserves_budget);

    // ActorCapabilities
    register_scenario("actor_caps_credibility_bounds", scenarios::actor_caps_credibility_bounds);
    register_scenario("actor_caps_production_bounded", scenarios::actor_caps_production_bounded);
    register_scenario("actor_caps_state_vs_media", scenarios::actor_caps_state_vs_media);
    register_scenario("actor_caps_validate_profiles", scenarios::actor_caps_validate_profiles);

    // End-to-end
    register_scenario("scenario_russian_interference", scenarios::scenario_russian_interference);
    register_scenario("scenario_international_media_coverage", scenarios::scenario_international_media_coverage);
    register_scenario("scenario_diaspora_media_consumption", scenarios::scenario_diaspora_media_consumption);
}

// ============================================================================
// Helper: Build a minimal GlobalGeoHierarchy for testing
// ============================================================================

namespace {

GlobalGeoHierarchy build_test_geo() {
    GlobalGeoHierarchy geo;

    // USA
    Country usa;
    usa.country_id = "USA";
    usa.name = "United States";
    usa.official_languages = {"en"};
    usa.common_languages = {"en", "es"};
    usa.english_proficiency = 1.0;
    usa.political_system = PoliticalSystem::PRESIDENTIAL_DEMOCRACY;
    usa.total_population = 331000000;
    usa.urban_percentage = 0.83;
    usa.internet_penetration = 0.90;
    usa.social_media_penetration = 0.72;
    usa.cultural_distance = {
        {"GBR", 0.15}, {"RUS", 0.70}, {"CHN", 0.80},
        {"IND", 0.55}, {"BRA", 0.45}, {"FRA", 0.30}
    };
    usa.geopolitical_tension = {
        {"RUS", 0.80}, {"CHN", 0.75}, {"IND", 0.15},
        {"GBR", 0.05}, {"BRA", 0.10}, {"FRA", 0.10}
    };
    geo.add_country(usa);

    // Russia
    Country rus;
    rus.country_id = "RUS";
    rus.name = "Russia";
    rus.official_languages = {"ru"};
    rus.common_languages = {"ru"};
    rus.english_proficiency = 0.15;
    rus.political_system = PoliticalSystem::AUTHORITARIAN;
    rus.total_population = 144000000;
    rus.urban_percentage = 0.75;
    rus.internet_penetration = 0.80;
    rus.social_media_penetration = 0.55;
    rus.cultural_distance = {
        {"USA", 0.70}, {"GBR", 0.65}, {"CHN", 0.50},
        {"IND", 0.55}, {"BRA", 0.60}, {"FRA", 0.55}
    };
    rus.geopolitical_tension = {
        {"USA", 0.80}, {"GBR", 0.75}, {"CHN", 0.25},
        {"IND", 0.20}, {"BRA", 0.15}, {"FRA", 0.60}
    };
    geo.add_country(rus);

    // UK
    Country gbr;
    gbr.country_id = "GBR";
    gbr.name = "United Kingdom";
    gbr.official_languages = {"en"};
    gbr.common_languages = {"en"};
    gbr.english_proficiency = 1.0;
    gbr.political_system = PoliticalSystem::PARLIAMENTARY_DEMOCRACY;
    gbr.total_population = 67000000;
    gbr.urban_percentage = 0.84;
    gbr.internet_penetration = 0.95;
    gbr.social_media_penetration = 0.78;
    gbr.cultural_distance = {
        {"USA", 0.15}, {"RUS", 0.65}, {"FRA", 0.25},
        {"IND", 0.50}
    };
    gbr.geopolitical_tension = {
        {"USA", 0.05}, {"RUS", 0.75}, {"FRA", 0.15},
        {"IND", 0.10}
    };
    geo.add_country(gbr);

    // India
    Country ind;
    ind.country_id = "IND";
    ind.name = "India";
    ind.official_languages = {"hi", "en"};
    ind.common_languages = {"hi", "en", "bn", "te", "ta"};
    ind.english_proficiency = 0.30;
    ind.political_system = PoliticalSystem::PARLIAMENTARY_DEMOCRACY;
    ind.total_population = 1400000000;
    ind.urban_percentage = 0.35;
    ind.internet_penetration = 0.50;
    ind.social_media_penetration = 0.35;
    ind.cultural_distance = {
        {"USA", 0.55}, {"RUS", 0.55}, {"GBR", 0.50}, {"CHN", 0.60}
    };
    ind.geopolitical_tension = {
        {"USA", 0.15}, {"RUS", 0.20}, {"GBR", 0.10}, {"CHN", 0.65}
    };
    geo.add_country(ind);

    // Indian-American diaspora
    DiasporaSegment indian_american;
    indian_american.segment_id = "indian_american";
    indian_american.base_archetype = SegmentArchetype::EDUCATED_PROFESSIONAL_ELITE;
    indian_american.origin_country = "IND";
    indian_american.residence_country = "USA";
    indian_american.origin_identity_strength = 0.70;
    indian_american.residence_identity_strength = 0.80;
    indian_american.origin_media_consumption = 0.40;
    indian_american.residence_media_consumption = 0.80;
    indian_american.languages = {"hi", "en"};
    indian_american.transnational_topics = {"immigration", "h1b_visas", "india_us_relations"};
    indian_american.population_estimate = 4900000;
    indian_american.primary_geography = "urban_core";
    geo.add_diaspora_segment(indian_american);

    return geo;
}

} // anonymous namespace

// ============================================================================
// CrossBorderFactors Scenarios
// ============================================================================

namespace scenarios {

bool cross_border_same_country(std::string& reason) {
    auto geo = build_test_geo();

    InternationalContent content;
    content.content_id = "us_news_1";
    content.origin_country = "USA";
    content.original_language = "en";
    content.source_type = InternationalContent::SourceType::INTERNATIONAL_MEDIA;
    content.requires_translation = false;
    content.translation_quality = 0.0;
    content.is_microtargeted = false;
    content.is_state_sponsored = false;
    content.amplification_budget = 0.0;
    content.uses_inauthentic_accounts = false;

    auto factors = compute_cross_border_factors(content, "USA", 0.5, geo);

    // Invariant: same-country reach >= 0.9
    if (factors.reach_mult < 0.9) {
        reason = "reach_mult " + std::to_string(factors.reach_mult) + " < 0.9 for same country";
        return false;
    }
    // Invariant: same-country credibility >= 0.8
    if (factors.credibility_mult < 0.8) {
        reason = "credibility_mult " + std::to_string(factors.credibility_mult) + " < 0.8 for same country";
        return false;
    }
    return true;
}

bool cross_border_high_tension(std::string& reason) {
    auto geo = build_test_geo();

    // Russian content targeting US (tension = 0.80)
    InternationalContent content;
    content.content_id = "ru_content_1";
    content.origin_country = "RUS";
    content.original_language = "en"; // English-language Russian media
    content.source_type = InternationalContent::SourceType::STATE_PROPAGANDA;
    content.requires_translation = false;
    content.translation_quality = 0.0;
    content.is_microtargeted = false;
    content.is_state_sponsored = true;
    content.sponsoring_state = "RUS";
    content.amplification_budget = 0.0;
    content.uses_inauthentic_accounts = false;

    auto factors = compute_cross_border_factors(content, "USA", 0.5, geo);

    // Invariant: high tension + state sponsored -> credibility <= 0.5
    if (factors.credibility_mult > 0.5) {
        reason = "credibility_mult " + std::to_string(factors.credibility_mult)
                 + " > 0.5 for high-tension state propaganda";
        return false;
    }
    // Both in [0, 1]
    if (factors.reach_mult < 0.0 || factors.reach_mult > 1.0) {
        reason = "reach_mult out of [0,1]";
        return false;
    }
    if (factors.credibility_mult < 0.0 || factors.credibility_mult > 1.0) {
        reason = "credibility_mult out of [0,1]";
        return false;
    }
    return true;
}

bool cross_border_untranslated_foreign(std::string& reason) {
    auto geo = build_test_geo();

    // Russian content in Russian targeting US (no translation)
    InternationalContent content;
    content.content_id = "ru_russian_lang";
    content.origin_country = "RUS";
    content.original_language = "ru";
    content.source_type = InternationalContent::SourceType::STATE_PROPAGANDA;
    content.requires_translation = false;  // No translation available
    content.translation_quality = 0.0;
    content.is_microtargeted = false;
    content.is_state_sponsored = false;
    content.amplification_budget = 0.0;
    content.uses_inauthentic_accounts = false;

    auto factors = compute_cross_border_factors(content, "USA", 0.5, geo);

    // Invariant: untranslated foreign language -> reach_mult <= 0.15
    if (factors.reach_mult > 0.15) {
        reason = "reach_mult " + std::to_string(factors.reach_mult)
                 + " > 0.15 for untranslated foreign language";
        return false;
    }
    return true;
}

bool cross_border_language_barrier(std::string& reason) {
    auto geo = build_test_geo();

    // Test language accessibility helper
    // English content US->UK: should be high
    double us_uk = compute_language_accessibility("en", "USA", "GBR", false, 0.0, geo);
    if (us_uk < 0.9) {
        reason = "US->UK English accessibility " + std::to_string(us_uk) + " < 0.9";
        return false;
    }

    // Russian content RUS->USA: should be very low (no translation)
    double rus_usa = compute_language_accessibility("ru", "RUS", "USA", false, 0.0, geo);
    if (rus_usa > 0.15) {
        reason = "RUS->USA Russian accessibility " + std::to_string(rus_usa) + " > 0.15";
        return false;
    }

    // Russian content with good translation: moderate
    double rus_usa_translated = compute_language_accessibility("ru", "RUS", "USA", true, 0.85, geo);
    if (rus_usa_translated < 0.3 || rus_usa_translated > 0.7) {
        reason = "RUS->USA translated accessibility " + std::to_string(rus_usa_translated)
                 + " not in [0.3, 0.7]";
        return false;
    }

    // Same country: always 1.0
    double same = compute_language_accessibility("en", "USA", "USA", false, 0.0, geo);
    if (std::abs(same - 1.0) > 0.001) {
        reason = "Same country accessibility " + std::to_string(same) + " != 1.0";
        return false;
    }

    return true;
}

bool cross_border_state_propaganda(std::string& reason) {
    auto geo = build_test_geo();

    // State propaganda vs regular international media: propaganda should have lower credibility
    InternationalContent propaganda;
    propaganda.content_id = "ru_prop";
    propaganda.origin_country = "RUS";
    propaganda.original_language = "en";
    propaganda.source_type = InternationalContent::SourceType::STATE_PROPAGANDA;
    propaganda.requires_translation = false;
    propaganda.is_state_sponsored = true;
    propaganda.sponsoring_state = "RUS";
    propaganda.amplification_budget = 0.0;
    propaganda.uses_inauthentic_accounts = false;
    propaganda.is_microtargeted = false;
    propaganda.translation_quality = 0.0;

    InternationalContent regular;
    regular.content_id = "ru_media";
    regular.origin_country = "RUS";
    regular.original_language = "en";
    regular.source_type = InternationalContent::SourceType::INTERNATIONAL_MEDIA;
    regular.requires_translation = false;
    regular.is_state_sponsored = false;
    regular.amplification_budget = 0.0;
    regular.uses_inauthentic_accounts = false;
    regular.is_microtargeted = false;
    regular.translation_quality = 0.0;

    auto prop_factors = compute_cross_border_factors(propaganda, "USA", 0.5, geo);
    auto reg_factors = compute_cross_border_factors(regular, "USA", 0.5, geo);

    // State propaganda should have lower credibility than regular media
    if (prop_factors.credibility_mult >= reg_factors.credibility_mult) {
        reason = "Propaganda credibility " + std::to_string(prop_factors.credibility_mult)
                 + " >= regular " + std::to_string(reg_factors.credibility_mult);
        return false;
    }

    return true;
}

// ============================================================================
// MediaDiet Scenarios
// ============================================================================

bool media_diet_budget_conservation(std::string& reason) {
    // Domestic diet
    auto domestic = MediaDiet::create_domestic("USA", 0.08);
    if (!domestic.validate()) {
        reason = "Domestic diet fails validation";
        return false;
    }

    // Factory domestic
    auto factory_domestic = MediaDietFactory::create_default_domestic("USA");
    if (!factory_domestic.validate()) {
        reason = "Factory domestic diet fails validation";
        return false;
    }

    // Diaspora diet from segment
    DiasporaSegment seg;
    seg.segment_id = "indian_american";
    seg.origin_country = "IND";
    seg.residence_country = "USA";
    seg.origin_media_consumption = 0.40;
    seg.residence_media_consumption = 0.80;

    auto diaspora = MediaDiet::create_from_diaspora(seg);
    if (!diaspora.validate()) {
        reason = "Diaspora diet fails validation (sum=" +
                 std::to_string(diaspora.origin_share + diaspora.residence_share) + ")";
        return false;
    }

    return true;
}

bool media_diet_saturation_diminishing(std::string& reason) {
    double k = 3.0;

    // Saturation curve properties
    double at_zero = MediaDietFactory::saturation_curve(0.0, k);
    double at_quarter = MediaDietFactory::saturation_curve(0.25, k);
    double at_half = MediaDietFactory::saturation_curve(0.50, k);
    double at_full = MediaDietFactory::saturation_curve(1.00, k);

    // At 0: should be 0
    if (std::abs(at_zero) > 0.001) {
        reason = "saturation(0) = " + std::to_string(at_zero) + " != 0";
        return false;
    }

    // Monotonically increasing
    if (!(at_quarter < at_half && at_half < at_full)) {
        reason = "Saturation not monotonically increasing";
        return false;
    }

    // Diminishing returns: effective < raw share for share > 0
    // at_half should be < 0.5 (but with k=3 it's actually > 0.5)
    // The key invariant is marginal return decreases
    double marginal_first = at_quarter / 0.25;
    double marginal_second = (at_half - at_quarter) / 0.25;
    if (marginal_second >= marginal_first) {
        reason = "Marginal returns not decreasing: first=" +
                 std::to_string(marginal_first) + " second=" +
                 std::to_string(marginal_second);
        return false;
    }

    // Split advantage: two sources at 0.5 each give more than one at 1.0
    double split_total = 2.0 * at_half;
    if (split_total <= at_full) {
        reason = "Split not better: 2*sat(0.5)=" + std::to_string(split_total)
                 + " <= sat(1.0)=" + std::to_string(at_full);
        return false;
    }

    return true;
}

bool media_diet_diaspora_split(std::string& reason) {
    DiasporaSegment seg;
    seg.segment_id = "indian_american";
    seg.origin_country = "IND";
    seg.residence_country = "USA";
    seg.origin_media_consumption = 0.40;
    seg.residence_media_consumption = 0.80;

    auto diet = MediaDiet::create_from_diaspora(seg);

    // Should have both origin and residence shares
    if (diet.origin_share <= 0.0) {
        reason = "Diaspora origin_share is 0";
        return false;
    }
    if (diet.residence_share <= 0.0) {
        reason = "Diaspora residence_share is 0";
        return false;
    }

    // Residence should be larger (0.80 vs 0.40 raw)
    if (diet.residence_share <= diet.origin_share) {
        reason = "Diaspora residence_share " + std::to_string(diet.residence_share)
                 + " <= origin_share " + std::to_string(diet.origin_share);
        return false;
    }

    // Budget must be conserved
    if (!diet.validate()) {
        reason = "Diaspora diet budget not conserved";
        return false;
    }

    return true;
}

bool media_diet_shift_preserves_budget(std::string& reason) {
    auto diet = MediaDietFactory::create_default_domestic("USA");

    // Shift toward international content
    diet.shift_toward("_global", 0.1);

    if (!diet.validate()) {
        reason = "Budget not conserved after shift";
        return false;
    }

    // All shares should still be in [0, 1]
    if (diet.residence_share < 0.0 || diet.residence_share > 1.0) {
        reason = "residence_share out of bounds after shift";
        return false;
    }

    return true;
}

// ============================================================================
// ActorCapabilities Scenarios
// ============================================================================

bool actor_caps_credibility_bounds(std::string& reason) {
    auto caps = ActorCapabilityFactory::state_media_profile();

    // Set some per-country overrides
    caps.credibility_overrides["USA"] = 0.10;
    caps.credibility_overrides["RUS"] = 0.70;

    // Credibility in USA should be between floor and ceiling
    double usa_cred = caps.get_credibility("USA");
    if (usa_cred < caps.credibility_floor || usa_cred > caps.credibility_ceiling) {
        reason = "USA credibility " + std::to_string(usa_cred) + " outside [" +
                 std::to_string(caps.credibility_floor) + ", " +
                 std::to_string(caps.credibility_ceiling) + "]";
        return false;
    }

    // Russia credibility should be between floor and ceiling
    double rus_cred = caps.get_credibility("RUS");
    if (rus_cred < caps.credibility_floor || rus_cred > caps.credibility_ceiling) {
        reason = "RUS credibility " + std::to_string(rus_cred) + " outside bounds";
        return false;
    }

    // Unknown country should get default (midpoint, clamped)
    double unknown_cred = caps.get_credibility("XYZ");
    if (unknown_cred < caps.credibility_floor || unknown_cred > caps.credibility_ceiling) {
        reason = "Unknown country credibility outside bounds";
        return false;
    }

    return true;
}

bool actor_caps_production_bounded(std::string& reason) {
    InternationalActor actor;
    actor.actor_id = "test_actor";
    actor.actor_type = InternationalActor::ActorType::FOREIGN_STATE_MEDIA;
    actor.active_countries = {"USA", "GBR", "DEU", "FRA"};

    auto caps = ActorCapabilityFactory::state_media_profile();

    int production = compute_actor_production(actor, caps, 0);

    // Production should be positive
    if (production <= 0) {
        reason = "Production " + std::to_string(production) + " <= 0";
        return false;
    }

    // Production should be bounded (not infinite)
    if (production > 500) {
        reason = "Production " + std::to_string(production) + " > 500 (unreasonably high)";
        return false;
    }

    return true;
}

bool actor_caps_state_vs_media(std::string& reason) {
    auto state = ActorCapabilityFactory::state_media_profile();
    auto media = ActorCapabilityFactory::international_media_profile();

    // State media should have higher targeting precision (microtargeting)
    if (state.targeting_precision <= media.targeting_precision) {
        reason = "State targeting " + std::to_string(state.targeting_precision)
                 + " <= media " + std::to_string(media.targeting_precision);
        return false;
    }

    // State media should have lower credibility ceiling
    if (state.credibility_ceiling >= media.credibility_ceiling) {
        reason = "State credibility ceiling " + std::to_string(state.credibility_ceiling)
                 + " >= media " + std::to_string(media.credibility_ceiling);
        return false;
    }

    // International media should have higher content quality
    if (media.content_quality <= state.content_quality) {
        reason = "Media quality " + std::to_string(media.content_quality)
                 + " <= state " + std::to_string(state.content_quality);
        return false;
    }

    // State media can use inauthentic accounts, media cannot
    if (!state.can_use_inauthentic_accounts) {
        reason = "State media should be able to use inauthentic accounts";
        return false;
    }
    if (media.can_use_inauthentic_accounts) {
        reason = "International media should not use inauthentic accounts";
        return false;
    }

    return true;
}

bool actor_caps_validate_profiles(std::string& reason) {
    // All factory profiles should pass validation
    auto profiles = {
        ActorCapabilityFactory::international_media_profile(),
        ActorCapabilityFactory::state_media_profile(),
        ActorCapabilityFactory::multilateral_org_profile(),
        ActorCapabilityFactory::regional_org_profile(),
        ActorCapabilityFactory::global_ngo_profile(),
        ActorCapabilityFactory::multinational_corp_profile(),
        ActorCapabilityFactory::global_celebrity_profile()
    };

    int idx = 0;
    for (const auto& profile : profiles) {
        if (!profile.validate()) {
            reason = "Profile #" + std::to_string(idx) + " fails validation";
            return false;
        }
        ++idx;
    }

    return true;
}

// ============================================================================
// End-to-End Scenarios
// ============================================================================

bool scenario_russian_interference(std::string& reason) {
    auto geo = build_test_geo();

    // Setup: RT creates English-language content targeting US audiences
    InternationalContent rt_content;
    rt_content.content_id = "rt_election_1";
    rt_content.origin_country = "RUS";
    rt_content.original_language = "en";
    rt_content.source_type = InternationalContent::SourceType::STATE_PROPAGANDA;
    rt_content.requires_translation = false;
    rt_content.translation_quality = 0.0;
    rt_content.is_microtargeted = true;
    rt_content.is_state_sponsored = true;
    rt_content.sponsoring_state = "RUS";
    rt_content.amplification_budget = 1.5;
    rt_content.uses_inauthentic_accounts = true;
    rt_content.cultural_distance_decay = 2.0;

    // Test with different viewer profiles

    // High institutional trust viewer (educated professional)
    auto high_trust = compute_cross_border_factors(rt_content, "USA", 0.8, geo);

    // Low institutional trust viewer (susceptible target)
    auto low_trust = compute_cross_border_factors(rt_content, "USA", 0.2, geo);

    // In Russia itself
    InternationalContent rt_domestic = rt_content;
    rt_domestic.origin_country = "RUS";
    auto in_russia = compute_cross_border_factors(rt_domestic, "RUS", 0.5, geo);

    // Invariant 1: State propaganda should have low credibility in US
    if (high_trust.credibility_mult > 0.4) {
        reason = "RT credibility too high for high-trust US viewer: " +
                 std::to_string(high_trust.credibility_mult);
        return false;
    }

    // Invariant 2: Low institutional trust increases susceptibility to propaganda
    if (low_trust.credibility_mult <= high_trust.credibility_mult) {
        reason = "Low-trust viewer should be more susceptible: low=" +
                 std::to_string(low_trust.credibility_mult) + " high=" +
                 std::to_string(high_trust.credibility_mult);
        return false;
    }

    // Invariant 3: Same-country reach should be high
    if (in_russia.reach_mult < 0.9) {
        reason = "RT in Russia reach too low: " + std::to_string(in_russia.reach_mult);
        return false;
    }

    // Invariant 4: Amplification should increase reach
    InternationalContent no_amplification = rt_content;
    no_amplification.amplification_budget = 0.0;
    no_amplification.uses_inauthentic_accounts = false;
    auto no_amp = compute_cross_border_factors(no_amplification, "USA", 0.5, geo);

    if (high_trust.reach_mult <= no_amp.reach_mult) {
        // Note: reach comparison should be against same trust level
        auto with_amp = compute_cross_border_factors(rt_content, "USA", 0.5, geo);
        if (with_amp.reach_mult <= no_amp.reach_mult) {
            reason = "Amplification should increase reach: with=" +
                     std::to_string(with_amp.reach_mult) + " without=" +
                     std::to_string(no_amp.reach_mult);
            return false;
        }
    }

    return true;
}

bool scenario_international_media_coverage(std::string& reason) {
    auto geo = build_test_geo();

    // BBC covering international event
    InternationalContent bbc_content;
    bbc_content.content_id = "bbc_intl_1";
    bbc_content.origin_country = "GBR";
    bbc_content.original_language = "en";
    bbc_content.source_type = InternationalContent::SourceType::INTERNATIONAL_MEDIA;
    bbc_content.requires_translation = false;
    bbc_content.translation_quality = 0.0;
    bbc_content.is_microtargeted = false;
    bbc_content.is_state_sponsored = false;
    bbc_content.amplification_budget = 0.3;
    bbc_content.uses_inauthentic_accounts = false;

    // BBC in UK (home country)
    auto in_uk = compute_cross_border_factors(bbc_content, "GBR", 0.6, geo);

    // BBC in USA (close cultural ally, shared language)
    auto in_usa = compute_cross_border_factors(bbc_content, "USA", 0.6, geo);

    // BBC in Russia (hostile, different language but content in English)
    auto in_russia = compute_cross_border_factors(bbc_content, "RUS", 0.4, geo);

    // BBC in India (moderate distance, some English proficiency)
    auto in_india = compute_cross_border_factors(bbc_content, "IND", 0.5, geo);

    // Invariant 1: Home country should have highest factors
    if (in_uk.effective() < in_usa.effective()) {
        reason = "BBC should be most effective at home: UK=" +
                 std::to_string(in_uk.effective()) + " USA=" +
                 std::to_string(in_usa.effective());
        return false;
    }

    // Invariant 2: USA (close ally, same language) > Russia (hostile, diff language)
    if (in_usa.effective() <= in_russia.effective()) {
        reason = "BBC more effective in USA than Russia: USA=" +
                 std::to_string(in_usa.effective()) + " RUS=" +
                 std::to_string(in_russia.effective());
        return false;
    }

    // Invariant 3: All factors in [0, 1]
    for (const auto& f : {in_uk, in_usa, in_russia, in_india}) {
        if (f.reach_mult < 0.0 || f.reach_mult > 1.0 ||
            f.credibility_mult < 0.0 || f.credibility_mult > 1.0) {
            reason = "Factor out of [0,1]";
            return false;
        }
    }

    return true;
}

bool scenario_diaspora_media_consumption(std::string& reason) {
    // Indian-American diaspora media diet
    DiasporaSegment seg;
    seg.segment_id = "indian_american";
    seg.origin_country = "IND";
    seg.residence_country = "USA";
    seg.origin_media_consumption = 0.40;
    seg.residence_media_consumption = 0.80;

    auto diet = MediaDiet::create_from_diaspora(seg);

    // Invariant 1: Budget conservation
    if (!diet.validate()) {
        reason = "Diaspora diet budget not conserved";
        return false;
    }

    // Invariant 2: Both countries represented
    if (diet.get_share("IND") <= 0.0) {
        reason = "No Indian media in diaspora diet";
        return false;
    }
    if (diet.get_share("USA") <= 0.0) {
        reason = "No US media in diaspora diet";
        return false;
    }

    // Invariant 3: Saturation makes split more efficient than single-source
    double combined_effective = diet.get_total_effective_intake();
    double single_source = MediaDietFactory::saturation_curve(1.0, diet.saturation_k);
    if (combined_effective <= single_source) {
        reason = "Diaspora split should be more efficient: split=" +
                 std::to_string(combined_effective) + " single=" +
                 std::to_string(single_source);
        return false;
    }

    // Invariant 4: Shift toward origin preserves budget
    diet.shift_toward("IND", 0.1);
    if (!diet.validate()) {
        reason = "Budget broken after shift toward origin";
        return false;
    }

    return true;
}

} // namespace scenarios
