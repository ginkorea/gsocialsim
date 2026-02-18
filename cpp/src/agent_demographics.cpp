#include "agent.h"
#include <cmath>
#include <algorithm>

// ============================================================================
// Agent Demographics: Homophily and Influence Weighting
// ============================================================================

// Compute demographic similarity between agents
double Agent::compute_similarity(const Agent& other) const {
    double similarity_score = 0.0;
    double total_weight = 0.0;

    // 1. Age similarity (closer ages = higher similarity)
    double age_diff = std::abs(demographics.age - other.demographics.age);
    double age_similarity = std::exp(-age_diff / 20.0);  // 20-year half-life
    similarity_score += 0.10 * age_similarity;
    total_weight += 0.10;

    // 2. Geography match
    if (demographics.geography_type == other.demographics.geography_type) {
        similarity_score += 0.15;
    }
    total_weight += 0.15;

    // 3. Education match
    if (demographics.education_level == other.demographics.education_level) {
        similarity_score += 0.10;
    }
    total_weight += 0.10;

    // 4. Race match (strong homophily)
    if (demographics.race_ethnicity == other.demographics.race_ethnicity) {
        similarity_score += 0.20;
    }
    total_weight += 0.20;

    // 5. Gender match
    if (demographics.gender == other.demographics.gender) {
        similarity_score += 0.05;
    }
    total_weight += 0.05;

    // 6. Religion match (very strong homophily)
    if (demographics.religion == other.demographics.religion) {
        similarity_score += 0.15;
    }
    total_weight += 0.15;

    // 7. Political ideology similarity (strongest factor)
    double ideology_diff = std::abs(demographics.political_ideology -
                                     other.demographics.political_ideology);
    double ideology_similarity = std::exp(-ideology_diff / 0.5);  // Sharp decay
    similarity_score += 0.25 * ideology_similarity;
    total_weight += 0.25;

    // Normalize to [0,1]
    return similarity_score / total_weight;
}

// Compute influence weight from source to this agent
double Agent::compute_influence_weight(const Agent& source) const {
    // Base trust (from social network or default)
    double base_trust = psychographics.trust_in_sources_base;

    // Homophily amplification
    double similarity = compute_similarity(source);

    // In-group vs out-group modulation
    double homophily_boost;
    if (similarity > 0.7) {
        // Strong in-group: amplify influence (up to 1.6x)
        homophily_boost = 1.0 + (similarity - 0.7) * 2.0;
    } else if (similarity < 0.3) {
        // Strong out-group: attenuate influence (down to 0.3x)
        homophily_boost = 0.3 + similarity;
    } else {
        // Neutral: no modulation
        homophily_boost = 1.0;
    }

    // Verified/influencer status boost
    double status_boost = 1.0;
    if (source.psychographics.verified_status) {
        status_boost += 0.2;
    }
    if (source.psychographics.influencer_status) {
        status_boost += 0.3;
    }

    // Institutional trust modulates elite/institution influence
    // (Note: ActorType would need to be accessible; this is a placeholder)
    // if (source.type == ActorType::INSTITUTION || source.type == ActorType::MEDIA_OUTLET) {
    //     base_trust *= demographics.institutional_trust;
    // }

    return base_trust * homophily_boost * status_boost;
}
