#include "../include/agent.h"
#include "../include/demographic_sampling.h"
#include "../include/population_layer.h"
#include "../include/types.h"

#include <cassert>
#include <cmath>
#include <iostream>
#include <random>

// Test demographic sampling
void test_demographic_sampling() {
    std::mt19937 rng(42);
    DemographicSampler sampler(rng);

    // Create a test segment
    PopulationSegment seg("test_segment");
    seg.age_cohort = "millennial";
    seg.primary_geography = "urban_core";
    seg.education_level = "bachelors";
    seg.income_bracket = "middle";
    seg.percent_white = 0.6;
    seg.percent_female = 0.55;
    seg.dominant_religion = "atheist";
    seg.political_ideology = -0.7;
    seg.political_label = "liberal";
    seg.institutional_trust = 0.4;
    seg.media_diet_type = "social_native";
    seg.identity_rigidity = 0.5;
    seg.susceptibility = 0.6;
    seg.polarization = 0.6;
    seg.attention_budget = 1.3;

    // Generate demographics
    AgentDemographics demo = sampler.generate_demographics(seg, "cell_123");

    // Validate demographics
    assert(demo.age >= 28 && demo.age <= 44);  // millennial range
    assert(demo.age_cohort == "millennial");
    assert(demo.geography_type == "urban_core");
    assert(demo.education_level == "bachelors");
    assert(demo.income_bracket == "middle");
    assert(demo.income_annual >= 45000 && demo.income_annual <= 100000);
    assert(demo.home_cell_id == "cell_123");
    assert(demo.primary_segment_id == "test_segment");

    // Race should be sampled (white 60%, other 40%)
    assert(!demo.race_ethnicity.empty());

    // Gender should be sampled (female 55%, male ~45%)
    assert(demo.gender == "male" || demo.gender == "female" || demo.gender == "non_binary");

    // Political ideology should be near segment (-0.7 ± variance)
    assert(demo.political_ideology >= -1.0 && demo.political_ideology <= 1.0);
    assert(std::abs(demo.political_ideology - (-0.7)) < 0.4);  // Within reasonable variance

    std::cout << "✓ Demographic sampling test passed\n";
    std::cout << "  Generated: age=" << demo.age
              << ", race=" << demo.race_ethnicity
              << ", gender=" << demo.gender
              << ", ideology=" << demo.political_ideology << "\n";
}

// Test psychographic generation
void test_psychographic_generation() {
    std::mt19937 rng(42);
    DemographicSampler sampler(rng);

    PopulationSegment seg("progressive_segment");
    seg.age_cohort = "gen_z";
    seg.political_ideology = -0.8;
    seg.susceptibility = 0.7;
    seg.identity_rigidity = 0.5;
    seg.polarization = 0.7;
    seg.institutional_trust = 0.3;
    seg.attention_budget = 1.6;

    AgentPsychographics psycho = sampler.generate_psychographics(seg);

    // Validate psychographics
    assert(psycho.openness >= 0.0 && psycho.openness <= 1.0);
    assert(psycho.conscientiousness >= 0.0 && psycho.conscientiousness <= 1.0);
    assert(psycho.extraversion >= 0.0 && psycho.extraversion <= 1.0);
    assert(psycho.agreeableness >= 0.0 && psycho.agreeableness <= 1.0);
    assert(psycho.neuroticism >= 0.0 && psycho.neuroticism <= 1.0);

    // Young cohort should have higher posting frequency
    assert(psycho.posting_frequency > 0.5);
    assert(psycho.engagement_propensity > 0.3);

    // Susceptibility and rigidity should be near segment values
    assert(std::abs(psycho.susceptibility - 0.7) < 0.3);
    assert(std::abs(psycho.identity_rigidity - 0.5) < 0.3);

    std::cout << "✓ Psychographic generation test passed\n";
    std::cout << "  Big 5: O=" << psycho.openness
              << ", C=" << psycho.conscientiousness
              << ", E=" << psycho.extraversion << "\n";
}

// Test belief initialization
void test_belief_initialization() {
    std::mt19937 rng(42);
    DemographicSampler sampler(rng);

    PopulationSegment seg("test_segment");
    seg.baseline_beliefs["climate_change"] = BeliefDistribution(-0.8, 0.1, 0.0, -0.8);
    seg.baseline_beliefs["immigration"] = BeliefDistribution(0.5, 0.2, 0.0, 0.5);

    auto beliefs = sampler.generate_beliefs(seg);

    // Validate beliefs
    assert(beliefs.size() == 2);
    assert(beliefs.count("climate_change") > 0);
    assert(beliefs.count("immigration") > 0);

    // Climate belief should be near -0.8
    auto& climate = beliefs["climate_change"];
    assert(climate.stance >= -1.0 && climate.stance <= 1.0);
    assert(std::abs(climate.stance - (-0.8)) < 0.5);  // Within variance
    assert(climate.core_value == -0.8);  // Exact baseline
    assert(climate.confidence > 0.8);    // High confidence (low variance)

    // Immigration belief should be near 0.5
    auto& immigration = beliefs["immigration"];
    assert(std::abs(immigration.stance - 0.5) < 0.6);
    assert(immigration.core_value == 0.5);
    assert(immigration.confidence > 0.7);  // Moderate confidence

    std::cout << "✓ Belief initialization test passed\n";
    std::cout << "  Climate stance: " << climate.stance
              << " (core: " << climate.core_value << ")\n";
    std::cout << "  Immigration stance: " << immigration.stance
              << " (core: " << immigration.core_value << ")\n";
}

// Test homophily similarity
void test_homophily_similarity() {
    // Create two agents
    Agent agent1(AgentId("agent1"), 42);
    Agent agent2(AgentId("agent2"), 43);

    // Agent 1: Urban, young, liberal, white, female
    agent1.demographics.age = 30;
    agent1.demographics.age_cohort = "millennial";
    agent1.demographics.geography_type = "urban_core";
    agent1.demographics.education_level = "bachelors";
    agent1.demographics.race_ethnicity = "white";
    agent1.demographics.gender = "female";
    agent1.demographics.religion = "atheist";
    agent1.demographics.political_ideology = -0.7;

    // Agent 2: Similar to agent1 (high similarity)
    agent2.demographics.age = 32;
    agent2.demographics.age_cohort = "millennial";
    agent2.demographics.geography_type = "urban_core";
    agent2.demographics.education_level = "bachelors";
    agent2.demographics.race_ethnicity = "white";
    agent2.demographics.gender = "female";
    agent2.demographics.religion = "atheist";
    agent2.demographics.political_ideology = -0.6;

    double similarity = agent1.compute_similarity(agent2);

    // High similarity expected (all demographics match)
    assert(similarity > 0.8);
    std::cout << "✓ Homophily similarity test passed (similar agents)\n";
    std::cout << "  Similarity score: " << similarity << "\n";

    // Agent 3: Very different (low similarity)
    Agent agent3(AgentId("agent3"), 44);
    agent3.demographics.age = 65;
    agent3.demographics.age_cohort = "boomer_plus";
    agent3.demographics.geography_type = "rural";
    agent3.demographics.education_level = "high_school";
    agent3.demographics.race_ethnicity = "white";
    agent3.demographics.gender = "male";
    agent3.demographics.religion = "evangelical";
    agent3.demographics.political_ideology = 0.8;

    double low_similarity = agent1.compute_similarity(agent3);

    // Low similarity expected (different on most dimensions)
    assert(low_similarity < 0.5);
    std::cout << "✓ Homophily similarity test passed (different agents)\n";
    std::cout << "  Similarity score: " << low_similarity << "\n";
}

// Test influence weight calculation
void test_influence_weight() {
    Agent target(AgentId("target"), 42);
    Agent source_ingroup(AgentId("source_in"), 43);
    Agent source_outgroup(AgentId("source_out"), 44);

    // Target: moderate liberal
    target.demographics.age = 35;
    target.demographics.race_ethnicity = "white";
    target.demographics.gender = "female";
    target.demographics.religion = "atheist";
    target.demographics.political_ideology = -0.5;
    target.psychographics.trust_in_sources_base = 0.5;

    // In-group source: very similar
    source_ingroup.demographics.age = 37;
    source_ingroup.demographics.race_ethnicity = "white";
    source_ingroup.demographics.gender = "female";
    source_ingroup.demographics.religion = "atheist";
    source_ingroup.demographics.political_ideology = -0.6;
    source_ingroup.psychographics.verified_status = false;
    source_ingroup.psychographics.influencer_status = false;

    // Out-group source: very different
    source_outgroup.demographics.age = 65;
    source_outgroup.demographics.race_ethnicity = "white";
    source_outgroup.demographics.gender = "male";
    source_outgroup.demographics.religion = "evangelical";
    source_outgroup.demographics.political_ideology = 0.8;
    source_outgroup.psychographics.verified_status = false;
    source_outgroup.psychographics.influencer_status = false;

    double ingroup_weight = target.compute_influence_weight(source_ingroup);
    double outgroup_weight = target.compute_influence_weight(source_outgroup);

    // In-group should have higher influence
    assert(ingroup_weight > outgroup_weight);

    // In-group weight should be amplified (> base trust)
    assert(ingroup_weight > 0.5);

    // Out-group weight should be attenuated or at least not amplified
    // (may be ~= base trust if similarity is moderate)
    assert(outgroup_weight <= ingroup_weight);  // Key test: in-group > out-group

    std::cout << "✓ Influence weight test passed\n";
    std::cout << "  In-group weight: " << ingroup_weight << "\n";
    std::cout << "  Out-group weight: " << outgroup_weight << "\n";
    std::cout << "  Amplification ratio: " << (ingroup_weight / outgroup_weight) << "x\n";
}

// Test content targeting
void test_content_targeting() {
    Agent agent(AgentId("test_agent"), 42);

    // Set agent demographics
    agent.demographics.age_cohort = "millennial";
    agent.demographics.geography_type = "urban_core";
    agent.demographics.education_level = "bachelors";
    agent.demographics.race_ethnicity = "white";
    agent.demographics.gender = "female";
    agent.demographics.political_ideology = -0.6;
    agent.demographics.primary_segment_id = "suburban_liberals";
    agent.psychographics.engagement_propensity = 0.7;
    agent.psychographics.susceptibility = 0.6;

    // Test 1: Targeting that matches
    ContentTargeting target1;
    target1.target_age_cohort = "millennial";
    target1.target_gender = "female";
    target1.min_political_ideology = -1.0;
    target1.max_political_ideology = 0.0;

    assert(target1.matches(agent));
    std::cout << "✓ Content targeting test passed (matching criteria)\n";

    // Test 2: Targeting that doesn't match (wrong gender)
    ContentTargeting target2;
    target2.target_gender = "male";

    assert(!target2.matches(agent));
    std::cout << "✓ Content targeting test passed (non-matching criteria)\n";

    // Test 3: Targeting with segment filter
    ContentTargeting target3;
    target3.target_segment = "suburban_liberals";

    assert(target3.matches(agent));
    std::cout << "✓ Content targeting test passed (segment filter)\n";

    // Test 4: Targeting with behavioral filter
    ContentTargeting target4;
    target4.min_engagement_propensity = 0.8;  // Agent has 0.7, too low

    assert(!target4.matches(agent));
    std::cout << "✓ Content targeting test passed (behavioral filter)\n";
}

// Test segment mix sampling
void test_segment_mix_sampling() {
    std::mt19937 rng(42);
    DemographicSampler sampler(rng);

    SegmentMix mix;
    mix.add_segment("progressive_activists", 0.3);
    mix.add_segment("suburban_liberals", 0.5);
    mix.add_segment("urban_black_voters", 0.2);
    mix.normalize();

    // Sample 1000 times and check distribution
    std::unordered_map<std::string, int> counts;
    for (int i = 0; i < 1000; ++i) {
        std::string seg = sampler.sample_segment(mix);
        counts[seg]++;
    }

    // Check approximate proportions
    double prog_ratio = counts["progressive_activists"] / 1000.0;
    double lib_ratio = counts["suburban_liberals"] / 1000.0;
    double black_ratio = counts["urban_black_voters"] / 1000.0;

    assert(std::abs(prog_ratio - 0.3) < 0.1);  // Within 10% tolerance
    assert(std::abs(lib_ratio - 0.5) < 0.1);
    assert(std::abs(black_ratio - 0.2) < 0.1);

    std::cout << "✓ Segment mix sampling test passed\n";
    std::cout << "  Progressive: " << (prog_ratio * 100) << "%\n";
    std::cout << "  Liberal: " << (lib_ratio * 100) << "%\n";
    std::cout << "  Black voters: " << (black_ratio * 100) << "%\n";
}

int main() {
    std::cout << "Testing Agent Demographics System...\n\n";

    test_demographic_sampling();
    test_psychographic_generation();
    test_belief_initialization();
    test_homophily_similarity();
    test_influence_weight();
    test_content_targeting();
    test_segment_mix_sampling();

    std::cout << "\n✅ All agent demographics tests passed!\n";
    return 0;
}
