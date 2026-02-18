#include "agent.h"
#include "identity_space.h"
#include <cmath>
#include <algorithm>

// ============================================================================
// Agent Demographics: Homophily and Influence Weighting
// ============================================================================

// Compute demographic similarity between agents using dimensional identity space
double Agent::compute_similarity(const Agent& other) const {
    // Use the dimensional identity space engine if available
    if (identity_space) {
        // Use cached coordinates if available, otherwise resolve on the fly
        const AgentIdentityCoords& coords_a = demographics.identity_coords.empty()
            ? identity_space->resolve(demographics)
            : demographics.identity_coords;
        const AgentIdentityCoords& coords_b = other.demographics.identity_coords.empty()
            ? identity_space->resolve(other.demographics)
            : other.demographics.identity_coords;

        return identity_space->compute_similarity(coords_a, coords_b, demographics, other.demographics);
    }

    // Fallback: create a temporary default identity space
    static const IdentitySpace default_space(IdentitySpace::create_default("USA"));
    auto coords_a = default_space.resolve(demographics);
    auto coords_b = default_space.resolve(other.demographics);
    return default_space.compute_similarity(coords_a, coords_b, demographics, other.demographics);
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
