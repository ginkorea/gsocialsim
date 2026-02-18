#include "cross_border.h"
#include <cmath>
#include <algorithm>

// ============================================================================
// Language Barrier Model
// ============================================================================

double compute_language_accessibility(
    const std::string& content_language,
    const std::string& origin_country,
    const std::string& viewer_country,
    bool requires_translation,
    double translation_quality,
    const GlobalGeoHierarchy& geo)
{
    // Same country: full accessibility
    if (origin_country == viewer_country) {
        return 1.0;
    }

    // Check if countries share a language
    double lang_compat = geo.get_language_compatibility(origin_country, viewer_country);

    if (lang_compat >= 0.9) {
        // Shared official language (e.g., US-UK both English)
        return 1.0;
    }

    if (lang_compat >= 0.7) {
        // Shared common language (high proficiency)
        return 0.85;
    }

    // No shared language -- translation needed
    if (requires_translation && translation_quality > 0.0) {
        // Translation quality degrades meaning preservation
        // Good translation (0.9): 0.9 * 0.7 = 0.63
        // Poor translation (0.4): 0.4 * 0.7 = 0.28
        return std::clamp(translation_quality * 0.7, 0.0, 0.85);
    }

    // Check English as lingua franca
    const Country* viewer_c = const_cast<GlobalGeoHierarchy&>(geo).get_country(viewer_country);
    if (viewer_c && content_language == "en" && viewer_c->english_proficiency > 0.3) {
        // English content in non-English country: scaled by proficiency
        return std::clamp(viewer_c->english_proficiency * 0.8, 0.0, 0.85);
    }

    // No shared language and no translation: very low accessibility
    return 0.05;
}

// ============================================================================
// Per-Country Credibility
// ============================================================================

double get_content_country_credibility(
    const InternationalContent& content,
    const std::string& viewer_country_id,
    const GlobalGeoHierarchy& geo)
{
    // Check explicit per-country credibility/resonance
    auto it = content.cultural_resonance.find(viewer_country_id);
    if (it != content.cultural_resonance.end()) {
        return std::clamp(it->second, 0.0, 1.0);
    }

    // Derive from geopolitical relationship
    double tension = geo.get_geopolitical_tension(content.origin_country, viewer_country_id);

    // State-sponsored content gets extra credibility penalty in high-tension countries
    double base_credibility = 1.0 - (tension * 0.6);

    if (content.is_state_sponsored) {
        // State propaganda from a hostile state: severe credibility hit
        double state_tension = geo.get_geopolitical_tension(
            content.sponsoring_state.empty() ? content.origin_country : content.sponsoring_state,
            viewer_country_id);
        base_credibility *= (1.0 - state_tension * 0.5);
    }

    return std::clamp(base_credibility, 0.05, 1.0);
}

// ============================================================================
// CrossBorderFactors Computation
// ============================================================================

CrossBorderFactors compute_cross_border_factors(
    const InternationalContent& content,
    const std::string& viewer_country_id,
    double viewer_institutional_trust,
    const GlobalGeoHierarchy& geo)
{
    CrossBorderFactors factors;

    // Same country: near-unity factors
    if (content.origin_country == viewer_country_id) {
        factors.reach_mult = 1.0;
        factors.credibility_mult = 1.0;

        // State-sponsored content in own country still gets slight credibility boost
        // (propaganda is most effective at home)
        return factors;
    }

    // --- REACH ---
    // Reach is driven by: cultural distance, language barriers, platform penetration

    // 1. Cultural distance decay (sharp exponential)
    double cultural_distance = geo.get_cultural_distance(
        content.origin_country, viewer_country_id);
    double cultural_reach = std::exp(-2.0 * cultural_distance);

    // 2. Language accessibility
    double lang_access = compute_language_accessibility(
        content.original_language,
        content.origin_country,
        viewer_country_id,
        content.requires_translation,
        content.translation_quality,
        geo);

    // 3. Amplification budget boosts reach (paid promotion)
    double amplification_boost = 1.0;
    if (content.amplification_budget > 0.0) {
        // Diminishing returns: budget of 1.0 gives ~1.3x boost
        amplification_boost = 1.0 + 0.3 * (1.0 - std::exp(-content.amplification_budget));
    }

    // 4. Inauthentic accounts boost apparent reach but cap at 1.0
    double inauthenticity_boost = 1.0;
    if (content.uses_inauthentic_accounts) {
        inauthenticity_boost = 1.2; // 20% extra apparent reach
    }

    factors.reach_mult = std::clamp(
        cultural_reach * lang_access * amplification_boost * inauthenticity_boost,
        0.0, 1.0);

    // --- CREDIBILITY ---
    // Credibility is driven by: geopolitical tension, state affiliation,
    // viewer institutional trust, content source reputation

    // 1. Per-country credibility (from resonance map or derived)
    double base_cred = get_content_country_credibility(content, viewer_country_id, geo);

    // 2. Viewer's institutional trust modulates foreign source credibility
    // High institutional trust -> more skeptical of foreign propaganda
    // Low institutional trust -> more susceptible to alternative narratives
    double trust_modulation;
    if (content.is_state_sponsored || content.source_type == InternationalContent::SourceType::STATE_PROPAGANDA) {
        // State propaganda: high institutional trust agents are MORE skeptical
        trust_modulation = 1.0 - (viewer_institutional_trust * 0.4);
    } else if (content.source_type == InternationalContent::SourceType::INTERNATIONAL_MEDIA) {
        // Established international media: institutional trust helps credibility
        trust_modulation = 0.7 + (viewer_institutional_trust * 0.3);
    } else if (content.source_type == InternationalContent::SourceType::MULTILATERAL_ORG) {
        // UN/WHO etc: strongly modulated by institutional trust
        trust_modulation = 0.5 + (viewer_institutional_trust * 0.5);
    } else {
        // Default: mild trust modulation
        trust_modulation = 0.8 + (viewer_institutional_trust * 0.2);
    }

    // 3. Microtargeted content that looks organic may bypass skepticism
    double targeting_cred = 1.0;
    if (content.is_microtargeted && !content.is_state_sponsored) {
        targeting_cred = 1.05; // Slightly more persuasive
    }

    factors.credibility_mult = std::clamp(
        base_cred * trust_modulation * targeting_cred,
        0.0, 1.0);

    return factors;
}

// Simplified overload with Agent reference
CrossBorderFactors compute_cross_border_factors(
    const InternationalContent& content,
    const Agent& viewer,
    const GlobalGeoHierarchy& geo)
{
    return compute_cross_border_factors(
        content,
        viewer.demographics.country_id,
        viewer.demographics.institutional_trust,
        geo);
}
