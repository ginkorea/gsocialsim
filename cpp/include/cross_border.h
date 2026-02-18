#pragma once

#include "country.h"
#include "agent.h"
#include <cmath>
#include <string>
#include <algorithm>

// ============================================================================
// Phase 1: Cross-Border Factors -- Reach vs Credibility Decomposition
// ============================================================================
//
// The old compute_cross_border_reach() merged cultural distance, language
// barriers, and geopolitical tension into a single scalar. This made it
// impossible to reason about *why* content didn't penetrate: was it because
// nobody saw it (reach) or nobody believed it (credibility)?
//
// CrossBorderFactors decomposes the cross-border effect into two independent
// multipliers:
//
//   reach_mult      -- probability that content is *seen* by the viewer
//                      (cultural distance decay, language barriers, platform
//                       penetration)
//
//   credibility_mult -- how *believable* the content is once seen
//                       (geopolitical tension, state affiliation penalty,
//                        source reputation, institutional trust of viewer)
//
// Effective influence = base_influence * reach_mult * credibility_mult
//
// Invariants:
//   - Same-country: reach_mult >= 0.9, credibility_mult >= 0.8
//   - Cross-border: reach_mult <= 1.0, credibility_mult <= 1.0
//   - High tension (>= 0.7): credibility_mult <= 0.5
//   - Untranslated foreign language: reach_mult <= 0.15
//   - Both multipliers in [0, 1]

struct CrossBorderFactors {
    double reach_mult = 1.0;       // [0, 1] -- fraction of audience that sees content
    double credibility_mult = 1.0; // [0, 1] -- believability once seen

    // Effective combined factor
    double effective() const { return reach_mult * credibility_mult; }
};

// Compute cross-border reach and credibility factors for content delivery
CrossBorderFactors compute_cross_border_factors(
    const InternationalContent& content,
    const std::string& viewer_country_id,
    double viewer_institutional_trust,
    const GlobalGeoHierarchy& geo);

// Simplified overload when you have an Agent reference
CrossBorderFactors compute_cross_border_factors(
    const InternationalContent& content,
    const Agent& viewer,
    const GlobalGeoHierarchy& geo);

// ============================================================================
// Per-country credibility lookup for international content
// ============================================================================

// Get the credibility of an international content piece as perceived in a
// specific country. Returns content.cultural_resonance for that country if
// available, otherwise derives from geopolitical tension and state affiliation.
double get_content_country_credibility(
    const InternationalContent& content,
    const std::string& viewer_country_id,
    const GlobalGeoHierarchy& geo);

// ============================================================================
// Language barrier model
// ============================================================================

// Compute language accessibility factor [0, 1].
// 1.0 = native language, 0.0 = completely inaccessible.
// Factors: shared language, translation quality, English proficiency overlap.
double compute_language_accessibility(
    const std::string& content_language,
    const std::string& origin_country,
    const std::string& viewer_country,
    bool requires_translation,
    double translation_quality,
    const GlobalGeoHierarchy& geo);
