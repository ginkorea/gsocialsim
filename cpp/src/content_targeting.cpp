#include "types.h"
#include "agent.h"

// ContentTargeting::matches implementation
bool ContentTargeting::matches(const Agent& agent) const {
    // Check all demographic filters
    if (target_age_cohort && agent.demographics.age_cohort != *target_age_cohort) {
        return false;
    }

    if (target_geography && agent.demographics.geography_type != *target_geography) {
        return false;
    }

    if (target_education && agent.demographics.education_level != *target_education) {
        return false;
    }

    if (target_income && agent.demographics.income_bracket != *target_income) {
        return false;
    }

    if (target_race && agent.demographics.race_ethnicity != *target_race) {
        return false;
    }

    if (target_gender && agent.demographics.gender != *target_gender) {
        return false;
    }

    if (target_religion && agent.demographics.religion != *target_religion) {
        return false;
    }

    // Check psychographic filters
    if (min_political_ideology && agent.demographics.political_ideology < *min_political_ideology) {
        return false;
    }

    if (max_political_ideology && agent.demographics.political_ideology > *max_political_ideology) {
        return false;
    }

    if (target_segment && agent.demographics.primary_segment_id != *target_segment) {
        return false;
    }

    // Check behavioral filters
    if (min_engagement_propensity &&
        agent.psychographics.engagement_propensity < *min_engagement_propensity) {
        return false;
    }

    if (min_susceptibility && agent.psychographics.susceptibility < *min_susceptibility) {
        return false;
    }

    // All filters passed
    return true;
}
