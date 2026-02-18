# Agent Demographics & Identity Extension Plan

## Problem Statement

Currently, agents have simplified identity models (8D identity_vector, identity_rigidity, basic_trust). To match the richness of the new population microsegments, **individual agents and influencers need detailed demographic and psychographic profiles**.

This enables:
- **Realistic matching**: Assign agents to appropriate population segments
- **Homophily modeling**: Influence strength based on demographic similarity
- **Targeted content**: Influencers can target specific demographics
- **Analytics**: Track influence patterns by demographic characteristics
- **Realism**: Agents behave according to their full identity profile

---

## Current Agent Identity Model (Minimal)

From `cpp/include/types.h` and `cpp/include/agent.h`:

```cpp
struct Agent {
    AgentId id;
    ActorType type;  // HUMAN, BOT, INSTITUTION, MEDIA_OUTLET

    // Minimal identity
    std::vector<double> identity_vector;  // 8D
    double identity_rigidity;
    double basic_trust;

    // Beliefs (topics only, no demographic context)
    std::unordered_map<TopicId, Belief> beliefs;

    // No demographics, no psychographics
};
```

---

## Proposed Extended Agent Identity Model

### New Agent Struct Extension

```cpp
struct AgentDemographics {
    // Core demographics
    int age;                              // Actual age (18-90)
    std::string age_cohort;               // "gen_z", "millennial", "gen_x", "boomer_plus"
    std::string geography_type;           // "urban_core", "suburban", "small_town", "rural"
    std::string home_cell_id;             // H3 cell ID for geographic location

    std::string education_level;          // "high_school", "some_college", "bachelors", "graduate"
    std::string income_bracket;           // "low", "middle", "upper_middle", "high"
    int income_annual;                    // Actual income (for targeted ads, etc.)

    std::string race_ethnicity;           // "white", "black", "hispanic", "asian", "other", "multiracial"
    std::string gender;                   // "male", "female", "non_binary"

    std::string religion;                 // "atheist", "evangelical", "catholic", "mainline_protestant",
                                          // "muslim", "jewish", "hindu", "buddhist", "other", "spiritual"
    double religiosity;                   // [0,1] how religious (0=secular, 1=very devout)

    // Political/ideological
    double political_ideology;            // [-1, +1] left to right
    std::string political_label;          // "progressive", "liberal", "moderate", "conservative", "reactionary"
    double institutional_trust;           // [0,1] trust in government, media, science
    double polarization;                  // [0,1] how extreme/tribal

    // Media consumption profile
    std::string media_diet;               // "traditional", "social_native", "alt_media", "podcast_heavy", "mixed"
    double attention_budget;              // [0,2] media consumption capacity
    std::unordered_map<MediaType, double> consume_bias;    // Consumption multipliers
    std::unordered_map<MediaType, double> interact_bias;   // Engagement multipliers

    // Social identity
    std::string occupation;               // "student", "teacher", "engineer", "tradesperson", etc.
    std::string union_membership;         // "none", "member", "household"
    bool small_business_owner;
    bool parent;
    bool veteran;

    // Segment assignment
    std::string primary_segment_id;       // Best-matching population segment
    double segment_fit_score;             // [0,1] how well agent matches segment
};

struct AgentPsychographics {
    // Personality traits (Big 5)
    double openness;                      // [0,1]
    double conscientiousness;             // [0,1]
    double extraversion;                  // [0,1]
    double agreeableness;                 // [0,1]
    double neuroticism;                   // [0,1]

    // Social media behavior
    double posting_frequency;             // Posts per day
    double engagement_propensity;         // [0,1] likelihood to comment/share
    double virality_seeking;              // [0,1] desire for viral content
    double outrage_susceptibility;        // [0,1] clickbait vulnerability

    // Influence dynamics
    double susceptibility;                // [0,1] (from segment)
    double identity_rigidity;             // [0,1] (already exists)
    double bounded_confidence_tau;        // Threshold for rejecting divergent views
    double trust_in_sources_base;         // [0,1] default trust level

    // Social graph position
    int follower_count;
    int following_count;
    double centrality_score;              // Network centrality (computed)
    bool verified_status;
    bool influencer_status;               // >10k followers
};

// Extended Agent struct
struct Agent {
    // Existing fields
    AgentId id;
    ActorType type;
    std::vector<double> identity_vector;  // 8D (keep for compatibility)

    // NEW: Full demographic and psychographic profile
    AgentDemographics demographics;
    AgentPsychographics psychographics;

    // Beliefs (unchanged)
    std::unordered_map<TopicId, Belief> beliefs;

    // Methods
    void assign_to_segment(const PopulationSegment& segment);
    double compute_similarity(const Agent& other) const;
    double compute_influence_weight(const Agent& source) const;
};
```

---

## Implementation Plan

### Phase 1: Extend Agent Struct (1 day)

**Files to modify:**
- `cpp/include/types.h` - Add `AgentDemographics` and `AgentPsychographics` structs
- `cpp/include/agent.h` - Add fields to `Agent` struct

**Backwards compatibility:**
- Keep existing `identity_vector` and `identity_rigidity` fields
- Map new fields to old fields for existing code

### Phase 2: Agent Generation with Realistic Demographics (2 days)

**Files to modify:**
- `cpp/src/main.cpp` - Agent initialization logic

**Approach: Stratified Sampling**

```cpp
void initialize_agents_with_demographics(
    int num_agents,
    const GeoWorld& geo,
    const PopulationLayer& population,
    std::vector<Agent>& agents) {

    // Step 1: Determine geographic distribution
    // Assign each agent to a cell based on cell population weights
    std::vector<std::string> agent_cell_assignments =
        assign_agents_to_cells(num_agents, geo);

    // Step 2: For each agent, sample demographics from their cell's segment mix
    for (int i = 0; i < num_agents; ++i) {
        Agent agent;
        agent.id = generate_agent_id();

        std::string cell_id = agent_cell_assignments[i];
        PopulationCell* cell = population.get_cell(cell_id);

        // Sample a segment from the cell's segment mix
        std::string segment_id = sample_segment(cell->segment_mix);
        PopulationSegment* segment = population.get_segment(segment_id);

        // Generate demographics consistent with segment
        agent.demographics = generate_demographics_from_segment(*segment, cell_id);
        agent.psychographics = generate_psychographics_from_segment(*segment);

        // Initialize beliefs from segment baseline
        agent.beliefs = initialize_beliefs_from_segment(*segment);

        // Assign segment
        agent.demographics.primary_segment_id = segment_id;
        agent.demographics.segment_fit_score = compute_fit_score(agent, *segment);

        agents.push_back(agent);
    }
}
```

**Sampling logic examples:**

```cpp
AgentDemographics generate_demographics_from_segment(
    const PopulationSegment& segment,
    const std::string& cell_id) {

    AgentDemographics demo;
    demo.home_cell_id = cell_id;

    // Age: Sample from segment's age cohort
    if (segment.age_cohort == "gen_z") {
        demo.age = sample_uniform(18, 27);
    } else if (segment.age_cohort == "millennial") {
        demo.age = sample_uniform(28, 43);
    } // ... etc
    demo.age_cohort = segment.age_cohort;

    // Geography
    demo.geography_type = segment.primary_geography;

    // Education
    demo.education_level = segment.education_level;

    // Income: Sample from segment's income distribution
    if (segment.income_bracket == "middle") {
        demo.income_annual = sample_normal(70000, 20000);
    }
    demo.income_bracket = segment.income_bracket;

    // Race: Sample from segment's racial composition
    double race_roll = sample_uniform(0.0, 1.0);
    if (race_roll < segment.percent_white) {
        demo.race_ethnicity = "white";
    } else {
        // Sample from remaining distribution
        // ...
    }

    // Gender
    double gender_roll = sample_uniform(0.0, 1.0);
    demo.gender = (gender_roll < segment.percent_female) ? "female" : "male";

    // Religion
    demo.religion = segment.dominant_religion;
    demo.religiosity = sample_from_segment_religion_distribution(segment);

    // Political ideology
    demo.political_ideology = segment.political_ideology + sample_normal(0.0, 0.15);
    demo.political_ideology = clamp(demo.political_ideology, -1.0, 1.0);
    demo.political_label = ideology_to_label(demo.political_ideology);

    // Institutional trust
    demo.institutional_trust = segment.institutional_trust + sample_normal(0.0, 0.1);
    demo.institutional_trust = clamp(demo.institutional_trust, 0.0, 1.0);

    // Polarization
    demo.polarization = segment.polarization + sample_normal(0.0, 0.1);
    demo.polarization = clamp(demo.polarization, 0.0, 1.0);

    // Media diet
    demo.media_diet = segment.media_diet_type;
    demo.attention_budget = segment.attention_budget + sample_normal(0.0, 0.2);
    demo.attention_budget = clamp(demo.attention_budget, 0.2, 2.0);

    // Copy media biases from segment
    demo.consume_bias = segment.consume_bias;
    demo.interact_bias = segment.interact_bias;

    // Occupation (sample from segment-appropriate occupations)
    demo.occupation = sample_occupation(segment);

    // Social identity tags
    demo.parent = (demo.age >= 25) && (sample_uniform(0.0, 1.0) < 0.6);
    demo.veteran = (segment.id == "rural_traditionalists") && (sample_uniform(0.0, 1.0) < 0.15);
    demo.small_business_owner = (segment.id == "small_business_owners");

    return demo;
}
```

### Phase 3: Homophily-Based Influence Weighting (1 day)

**Files to modify:**
- `cpp/src/belief_dynamics.cpp` - Add demographic similarity to influence calculation

**Homophily model:**

```cpp
double Agent::compute_similarity(const Agent& other) const {
    double similarity_score = 0.0;
    double total_weight = 0.0;

    // Age similarity (closer ages = higher similarity)
    double age_diff = std::abs(demographics.age - other.demographics.age);
    double age_similarity = std::exp(-age_diff / 20.0);  // Decay with 20-year half-life
    similarity_score += 0.1 * age_similarity;
    total_weight += 0.1;

    // Geography match
    if (demographics.geography_type == other.demographics.geography_type) {
        similarity_score += 0.15;
    }
    total_weight += 0.15;

    // Education match
    if (demographics.education_level == other.demographics.education_level) {
        similarity_score += 0.1;
    }
    total_weight += 0.1;

    // Race match (strong homophily)
    if (demographics.race_ethnicity == other.demographics.race_ethnicity) {
        similarity_score += 0.2;
    }
    total_weight += 0.2;

    // Gender match
    if (demographics.gender == other.demographics.gender) {
        similarity_score += 0.05;
    }
    total_weight += 0.05;

    // Religion match (very strong homophily)
    if (demographics.religion == other.demographics.religion) {
        similarity_score += 0.15;
    }
    total_weight += 0.15;

    // Political ideology similarity (strongest)
    double ideology_diff = std::abs(demographics.political_ideology -
                                    other.demographics.political_ideology);
    double ideology_similarity = std::exp(-ideology_diff / 0.5);  // Sharp decay
    similarity_score += 0.25 * ideology_similarity;
    total_weight += 0.25;

    return similarity_score / total_weight;  // Normalize to [0,1]
}

double Agent::compute_influence_weight(const Agent& source) const {
    // Base trust from belief dynamics
    double base_trust = basic_trust;  // or from trust network

    // Homophily amplification
    double similarity = compute_similarity(source);

    // In-group vs out-group modulation
    double homophily_boost;
    if (similarity > 0.7) {
        // Strong in-group: amplify influence
        homophily_boost = 1.0 + (similarity - 0.7) * 2.0;  // Up to 1.6x
    } else if (similarity < 0.3) {
        // Strong out-group: attenuate influence
        homophily_boost = 0.3 + similarity;  // Down to 0.3x
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

    // Institutional trust modulates elite influence
    if (source.type == ActorType::INSTITUTION ||
        source.type == ActorType::MEDIA_OUTLET) {
        base_trust *= demographics.institutional_trust;
    }

    return base_trust * homophily_boost * status_boost;
}
```

**Integration into belief dynamics:**

Modify `BeliefDynamicsEngine::compute_update()` to use `compute_influence_weight()`:

```cpp
BeliefDelta BeliefDynamicsEngine::compute_update(
    Belief& current,
    const Impression& impression,
    const Agent& target,      // NEW: target agent
    const Agent& source,      // NEW: source agent
    bool is_self_source,
    double proximity) {

    // Existing trust calculation
    double base_trust = impression.credibility_signal;

    // NEW: Modulate by demographic similarity (homophily)
    double homophily_weight = target.compute_influence_weight(source);
    double effective_trust = base_trust * homophily_weight;

    // Continue with existing dynamics...
    // Trust gate, bounded confidence, etc.
}
```

### Phase 4: Targeted Content & Microtargeting (2 days)

**Enable influencers/bots to target specific demographics:**

```cpp
struct ContentTargeting {
    // Demographic filters
    std::optional<std::string> target_age_cohort;
    std::optional<std::string> target_geography;
    std::optional<std::string> target_education;
    std::optional<std::string> target_income;
    std::optional<std::string> target_race;
    std::optional<std::string> target_gender;
    std::optional<std::string> target_religion;

    // Psychographic filters
    std::optional<double> min_political_ideology;   // [-1, +1]
    std::optional<double> max_political_ideology;
    std::optional<std::string> target_segment;

    // Behavioral filters
    std::optional<double> min_engagement_propensity;
    std::optional<double> min_susceptibility;

    bool matches(const Agent& agent) const {
        if (target_age_cohort && agent.demographics.age_cohort != *target_age_cohort)
            return false;
        if (target_geography && agent.demographics.geography_type != *target_geography)
            return false;
        // ... check all filters
        if (min_political_ideology &&
            agent.demographics.political_ideology < *min_political_ideology)
            return false;
        if (max_political_ideology &&
            agent.demographics.political_ideology > *max_political_ideology)
            return false;

        return true;  // All filters passed
    }
};

// Extend Content struct
struct Content {
    // ... existing fields ...

    // NEW: Targeting specification
    std::optional<ContentTargeting> targeting;
};

// In network delivery
std::vector<ContentId> BroadcastFeedNetwork::build_candidates(
    AgentId viewer_id,
    WorldContext& context) {

    Agent* viewer = context.agents.get(viewer_id);
    std::vector<ContentId> candidates;

    for (const auto& content_id : candidate_pool) {
        Content* content = context.content_store.get(content_id);

        // NEW: Check targeting filters
        if (content->targeting) {
            if (!content->targeting->matches(*viewer)) {
                continue;  // Skip this content for this viewer
            }
        }

        candidates.push_back(content_id);
    }

    return candidates;
}
```

### Phase 5: Analytics & Reporting (1 day)

**New analytics queries:**

```cpp
// Influence patterns by demographic
struct InfluenceAnalytics {
    std::unordered_map<std::string, int> reach_by_age_cohort;
    std::unordered_map<std::string, int> reach_by_segment;
    std::unordered_map<std::string, int> reach_by_ideology;

    double cross_ideological_exposure_rate;  // % of content from opposite ideology
    double echo_chamber_score;                // % of content from same segment
    double homophily_coefficient;             // Network clustering by demographics
};

// Belief shift by demographic
struct BeliefShiftAnalytics {
    std::unordered_map<std::string, double> avg_belief_change_by_segment;
    std::unordered_map<std::string, double> polarization_by_segment;

    // Cross-tab: Which segments are most influenced by which sources?
    std::map<std::pair<std::string, std::string>, double> influence_matrix;
    // Key: (source_segment, target_segment) -> influence strength
};
```

---

## Example: Agent Generation with Full Demographics

```cpp
// Generate 1000 agents for simulation

std::vector<Agent> agents;
initialize_agents_with_demographics(1000, geo_world, population, agents);

// Example agent 1: Progressive Activist
// demographics.age = 28
// demographics.age_cohort = "millennial"
// demographics.geography_type = "urban_core"
// demographics.education_level = "bachelors"
// demographics.race_ethnicity = "black"
// demographics.gender = "female"
// demographics.religion = "atheist"
// demographics.political_ideology = -0.85
// demographics.institutional_trust = 0.25
// demographics.attention_budget = 1.6
// demographics.primary_segment_id = "progressive_activists"
// beliefs["climate_change"].stance = -0.87
// beliefs["social_justice"].stance = -0.91

// Example agent 2: MAGA Base
// demographics.age = 52
// demographics.age_cohort = "gen_x"
// demographics.geography_type = "small_town"
// demographics.education_level = "high_school"
// demographics.race_ethnicity = "white"
// demographics.gender = "male"
// demographics.religion = "evangelical"
// demographics.political_ideology = 0.88
// demographics.institutional_trust = 0.08
// demographics.attention_budget = 1.4
// demographics.primary_segment_id = "maga_base"
// beliefs["immigration"].stance = 0.91
// beliefs["election_integrity"].stance = 0.85
```

---

## Benefits of Full Agent Demographics

1. **Realistic Influence Networks**
   - Homophily: Similar demographics = stronger influence
   - Cross-cutting exposure tracked explicitly

2. **Targeted Campaigns**
   - Bots/influencers can microtarget (e.g., "white males 30-50 in rural areas")
   - Measure differential impact by demographic

3. **Echo Chamber Quantification**
   - Measure % of content consumed from in-group vs out-group
   - Track ideological segregation in real-time

4. **Realistic Belief Dynamics**
   - Age effects (older = more rigid)
   - Education effects (college+ = more critical thinking)
   - Race effects (identity-based solidarity)

5. **Policy Research**
   - Test interventions on specific demographics
   - Measure disinformation spread by segment
   - Model voting behavior by demographic bloc

6. **Validation Against Real Data**
   - Compare simulation belief distributions to actual polling data by demographic
   - Validate influence patterns against social science research

---

## Data Requirements

To fully implement this, we need:

1. **Census data** (for realistic cell demographics)
   - Already have H3 population data
   - Add age, race, education, income distributions per cell

2. **Polling data** (for baseline beliefs)
   - Pew Research, Gallup, etc.
   - Beliefs by demographic cross-tabs

3. **Social media research** (for media consumption patterns)
   - Platform usage by age, education, etc.
   - Engagement patterns by demographic

4. **Network research** (for homophily coefficients)
   - Actual in-group preference rates from literature

---

## Implementation Timeline

- **Phase 1** (Extend Agent Struct): 1 day
- **Phase 2** (Agent Generation): 2 days
- **Phase 3** (Homophily Weighting): 1 day
- **Phase 4** (Targeted Content): 2 days
- **Phase 5** (Analytics): 1 day

**Total: ~1 week**

---

## Open Questions

1. Should we model **intersectionality** explicitly? (e.g., Black women have unique experience vs Black men + women separately)

2. Should **segment assignment be dynamic**? (Can agents shift from "Moderate" to "Progressive Activist" over time?)

3. How do we handle **anonymous/pseudonymous agents**? (Demographics unknown but inferred from behavior?)

4. Should we add **network formation homophily**? (Agents preferentially follow similar others?)

5. Do we need **cohort effects** vs **age effects**? (Are Boomers conservative because they're old, or because of their generation's experiences?)

---

**Ready to implement once approved!**
