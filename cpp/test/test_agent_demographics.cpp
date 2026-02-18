#include "../include/agent.h"
#include "../include/demographic_sampling.h"
#include "../include/identity_space.h"
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

    // Political ideology should be near segment (-0.7 +/- variance)
    assert(demo.political_ideology >= -1.0 && demo.political_ideology <= 1.0);
    assert(std::abs(demo.political_ideology - (-0.7)) < 0.4);

    std::cout << "  Demographic sampling test passed\n";
    std::cout << "    Generated: age=" << demo.age
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

    std::cout << "  Psychographic generation test passed\n";
    std::cout << "    Big 5: O=" << psycho.openness
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
    assert(std::abs(climate.stance - (-0.8)) < 0.5);
    assert(climate.core_value == -0.8);
    assert(climate.confidence > 0.8);

    // Immigration belief should be near 0.5
    auto& immigration = beliefs["immigration"];
    assert(std::abs(immigration.stance - 0.5) < 0.6);
    assert(immigration.core_value == 0.5);
    assert(immigration.confidence > 0.7);

    std::cout << "  Belief initialization test passed\n";
    std::cout << "    Climate stance: " << climate.stance
              << " (core: " << climate.core_value << ")\n";
    std::cout << "    Immigration stance: " << immigration.stance
              << " (core: " << immigration.core_value << ")\n";
}

// Test dimensional religion distances
void test_religion_distances() {
    IdentitySpace space(IdentitySpace::create_default("USA"));

    // Build minimal demographics for religion tests
    auto make_demo = [](const std::string& religion, double religiosity) {
        AgentDemographics d;
        d.religion = religion;
        d.religiosity = religiosity;
        d.age = 35;
        d.geography_type = "suburban";
        d.education_level = "bachelors";
        d.race_ethnicity = "white";
        d.gender = "male";
        d.income_bracket = "middle";
        d.political_ideology = 0.0;
        return d;
    };

    // Resolve religion coords only
    auto get_religion_pos = [&](const std::string& religion, double religiosity) {
        auto demo = make_demo(religion, religiosity);
        auto coords = space.resolve(demo);
        return coords["religion"];
    };

    // Protestant-Catholic: close (tradition axis ~0.10 apart)
    auto protestant_pos = get_religion_pos("protestant", 0.55);
    auto catholic_pos = get_religion_pos("catholic", 0.60);
    double prot_cath_dist = protestant_pos.distance_to(catholic_pos);
    assert(prot_cath_dist < 0.15);
    std::cout << "    Protestant-Catholic dist: " << prot_cath_dist << " (< 0.15)\n";

    // Catholic-Hindu: distant
    auto hindu_pos = get_religion_pos("hindu", 0.60);
    double cath_hindu_dist = catholic_pos.distance_to(hindu_pos);
    assert(cath_hindu_dist > 0.50);
    std::cout << "    Catholic-Hindu dist: " << cath_hindu_dist << " (> 0.50)\n";

    // Devout evangelical vs atheist: very far
    auto devout_evan = get_religion_pos("evangelical", 0.90);
    auto atheist_pos = get_religion_pos("atheist", 0.05);
    double evan_atheist_dist = devout_evan.distance_to(atheist_pos);
    assert(evan_atheist_dist > 1.0);
    std::cout << "    Devout evangelical-Atheist dist: " << evan_atheist_dist << " (> 1.0)\n";

    // Atheist-Agnostic: close
    auto agnostic_pos = get_religion_pos("agnostic", 0.10);
    double atheist_agnostic_dist = atheist_pos.distance_to(agnostic_pos);
    assert(atheist_agnostic_dist < 0.10);
    std::cout << "    Atheist-Agnostic dist: " << atheist_agnostic_dist << " (< 0.10)\n";

    // Devout evangelical vs devout Hindu: far, but devotion partially compensates
    auto devout_hindu = get_religion_pos("hindu", 0.90);
    auto devout_evan2 = get_religion_pos("evangelical", 0.90);
    double evan_hindu_devout = devout_evan2.distance_to(devout_hindu);
    assert(evan_hindu_devout > 0.5);  // Still far despite shared devotion
    assert(evan_hindu_devout < evan_atheist_dist);  // But closer than evangelical-atheist
    std::cout << "    Devout evangelical-Devout Hindu dist: " << evan_hindu_devout
              << " (> 0.5, < evan-atheist)\n";

    std::cout << "  Religion distance test passed\n";
}

// Test country-specific race distances
void test_country_race_distances() {
    IdentitySpace us_space(IdentitySpace::create_default("USA"));
    IdentitySpace ind_space(IdentitySpace::create_default("IND"));

    // US: white-black distance
    auto make_us_demo = [](const std::string& race) {
        AgentDemographics d;
        d.race_ethnicity = race;
        d.age = 35;
        d.geography_type = "suburban";
        d.education_level = "bachelors";
        d.religion = "atheist";
        d.religiosity = 0.1;
        d.gender = "male";
        d.income_bracket = "middle";
        d.political_ideology = 0.0;
        return d;
    };

    auto us_white = make_us_demo("white");
    auto us_black = make_us_demo("black");
    auto us_hispanic = make_us_demo("hispanic");

    auto white_coords = us_space.resolve(us_white);
    auto black_coords = us_space.resolve(us_black);
    auto hispanic_coords = us_space.resolve(us_hispanic);

    double us_white_black = white_coords["race_ethnicity"].distance_to(black_coords["race_ethnicity"]);
    double us_white_hispanic = white_coords["race_ethnicity"].distance_to(hispanic_coords["race_ethnicity"]);

    // White-Black > White-Hispanic in US
    assert(us_white_black > us_white_hispanic);
    std::cout << "    US white-black dist: " << us_white_black << "\n";
    std::cout << "    US white-hispanic dist: " << us_white_hispanic << "\n";

    // India: upper_caste-dalit distance
    auto make_ind_demo = [](const std::string& caste) {
        AgentDemographics d;
        d.race_ethnicity = caste;
        d.age = 35;
        d.geography_type = "suburban";
        d.education_level = "bachelors";
        d.religion = "hindu";
        d.religiosity = 0.6;
        d.gender = "male";
        d.income_bracket = "middle";
        d.political_ideology = 0.0;
        return d;
    };

    auto ind_upper = make_ind_demo("upper_caste_hindu");
    auto ind_dalit = make_ind_demo("dalit");
    auto ind_muslim = make_ind_demo("muslim");

    auto upper_coords = ind_space.resolve(ind_upper);
    auto dalit_coords = ind_space.resolve(ind_dalit);
    auto muslim_coords = ind_space.resolve(ind_muslim);

    double ind_upper_dalit = upper_coords["race_ethnicity"].distance_to(dalit_coords["race_ethnicity"]);
    double ind_upper_muslim = upper_coords["race_ethnicity"].distance_to(muslim_coords["race_ethnicity"]);

    // Both should be significant distances
    assert(ind_upper_dalit > 0.5);
    assert(ind_upper_muslim > 0.5);
    std::cout << "    India upper_caste-dalit dist: " << ind_upper_dalit << "\n";
    std::cout << "    India upper_caste-muslim dist: " << ind_upper_muslim << "\n";

    std::cout << "  Country-specific race distance test passed\n";
}

// Test homophily similarity through the full dimensional system
void test_homophily_similarity() {
    IdentitySpace space(IdentitySpace::create_default("USA"));

    // Create two agents
    Agent agent1(AgentId("agent1"), 42);
    Agent agent2(AgentId("agent2"), 43);
    agent1.identity_space = &space;
    agent2.identity_space = &space;

    // Agent 1: Urban, young, liberal, white, female
    agent1.demographics.age = 30;
    agent1.demographics.age_cohort = "millennial";
    agent1.demographics.geography_type = "urban_core";
    agent1.demographics.education_level = "bachelors";
    agent1.demographics.income_bracket = "middle";
    agent1.demographics.race_ethnicity = "white";
    agent1.demographics.gender = "female";
    agent1.demographics.religion = "atheist";
    agent1.demographics.religiosity = 0.1;
    agent1.demographics.political_ideology = -0.7;

    // Agent 2: Very similar to agent1
    agent2.demographics.age = 32;
    agent2.demographics.age_cohort = "millennial";
    agent2.demographics.geography_type = "urban_core";
    agent2.demographics.education_level = "bachelors";
    agent2.demographics.income_bracket = "middle";
    agent2.demographics.race_ethnicity = "white";
    agent2.demographics.gender = "female";
    agent2.demographics.religion = "atheist";
    agent2.demographics.religiosity = 0.1;
    agent2.demographics.political_ideology = -0.6;

    // Resolve coordinates
    agent1.demographics.identity_coords = space.resolve(agent1.demographics);
    agent2.demographics.identity_coords = space.resolve(agent2.demographics);

    double similarity = agent1.compute_similarity(agent2);

    // High similarity expected
    assert(similarity > 0.85);
    std::cout << "    Similar agents similarity: " << similarity << " (> 0.85)\n";

    // Agent 3: Very different
    Agent agent3(AgentId("agent3"), 44);
    agent3.identity_space = &space;
    agent3.demographics.age = 65;
    agent3.demographics.age_cohort = "boomer_plus";
    agent3.demographics.geography_type = "rural";
    agent3.demographics.education_level = "high_school";
    agent3.demographics.income_bracket = "low";
    agent3.demographics.race_ethnicity = "white";
    agent3.demographics.gender = "male";
    agent3.demographics.religion = "evangelical";
    agent3.demographics.religiosity = 0.9;
    agent3.demographics.political_ideology = 0.8;
    agent3.demographics.identity_coords = space.resolve(agent3.demographics);

    double low_similarity = agent1.compute_similarity(agent3);

    // Low similarity expected
    assert(low_similarity < 0.30);
    std::cout << "    Different agents similarity: " << low_similarity << " (< 0.30)\n";

    std::cout << "  Homophily similarity test passed\n";
}

// Test geography distance ordering
void test_geography_distances() {
    IdentitySpace space(IdentitySpace::create_default("USA"));

    auto make_demo = [](const std::string& geo) {
        AgentDemographics d;
        d.geography_type = geo;
        d.age = 35;
        d.education_level = "bachelors";
        d.race_ethnicity = "white";
        d.religion = "atheist";
        d.religiosity = 0.1;
        d.gender = "male";
        d.income_bracket = "middle";
        d.political_ideology = 0.0;
        return d;
    };

    auto urban = space.resolve(make_demo("urban_core"));
    auto suburban = space.resolve(make_demo("suburban"));
    auto rural = space.resolve(make_demo("rural"));

    double urban_suburban = urban["geography"].distance_to(suburban["geography"]);
    double urban_rural = urban["geography"].distance_to(rural["geography"]);
    double suburban_rural = suburban["geography"].distance_to(rural["geography"]);

    // urban-suburban < urban-rural
    assert(urban_suburban < urban_rural);
    // suburban-rural < urban-rural
    assert(suburban_rural < urban_rural);

    std::cout << "    Urban-Suburban: " << urban_suburban << "\n";
    std::cout << "    Urban-Rural: " << urban_rural << "\n";
    std::cout << "    Suburban-Rural: " << suburban_rural << "\n";
    std::cout << "  Geography distance ordering test passed\n";
}

// Test influence weight calculation
void test_influence_weight() {
    IdentitySpace space(IdentitySpace::create_default("USA"));

    Agent target(AgentId("target"), 42);
    Agent source_ingroup(AgentId("source_in"), 43);
    Agent source_outgroup(AgentId("source_out"), 44);

    target.identity_space = &space;
    source_ingroup.identity_space = &space;
    source_outgroup.identity_space = &space;

    // Target: moderate liberal
    target.demographics.age = 35;
    target.demographics.race_ethnicity = "white";
    target.demographics.gender = "female";
    target.demographics.religion = "atheist";
    target.demographics.religiosity = 0.1;
    target.demographics.geography_type = "urban_core";
    target.demographics.education_level = "bachelors";
    target.demographics.income_bracket = "middle";
    target.demographics.political_ideology = -0.5;
    target.psychographics.trust_in_sources_base = 0.5;
    target.demographics.identity_coords = space.resolve(target.demographics);

    // In-group source: very similar
    source_ingroup.demographics.age = 37;
    source_ingroup.demographics.race_ethnicity = "white";
    source_ingroup.demographics.gender = "female";
    source_ingroup.demographics.religion = "atheist";
    source_ingroup.demographics.religiosity = 0.1;
    source_ingroup.demographics.geography_type = "urban_core";
    source_ingroup.demographics.education_level = "bachelors";
    source_ingroup.demographics.income_bracket = "middle";
    source_ingroup.demographics.political_ideology = -0.6;
    source_ingroup.psychographics.verified_status = false;
    source_ingroup.psychographics.influencer_status = false;
    source_ingroup.demographics.identity_coords = space.resolve(source_ingroup.demographics);

    // Out-group source: very different
    source_outgroup.demographics.age = 65;
    source_outgroup.demographics.race_ethnicity = "white";
    source_outgroup.demographics.gender = "male";
    source_outgroup.demographics.religion = "evangelical";
    source_outgroup.demographics.religiosity = 0.9;
    source_outgroup.demographics.geography_type = "rural";
    source_outgroup.demographics.education_level = "high_school";
    source_outgroup.demographics.income_bracket = "low";
    source_outgroup.demographics.political_ideology = 0.8;
    source_outgroup.psychographics.verified_status = false;
    source_outgroup.psychographics.influencer_status = false;
    source_outgroup.demographics.identity_coords = space.resolve(source_outgroup.demographics);

    double ingroup_weight = target.compute_influence_weight(source_ingroup);
    double outgroup_weight = target.compute_influence_weight(source_outgroup);

    // In-group should have higher influence
    assert(ingroup_weight > outgroup_weight);

    // In-group weight should be amplified (> base trust)
    assert(ingroup_weight > 0.5);

    std::cout << "    In-group weight: " << ingroup_weight << "\n";
    std::cout << "    Out-group weight: " << outgroup_weight << "\n";
    std::cout << "    Amplification ratio: " << (ingroup_weight / outgroup_weight) << "x\n";
    std::cout << "  Influence weight test passed\n";
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

    // Test 2: Targeting that doesn't match (wrong gender)
    ContentTargeting target2;
    target2.target_gender = "male";

    assert(!target2.matches(agent));

    // Test 3: Targeting with segment filter
    ContentTargeting target3;
    target3.target_segment = "suburban_liberals";

    assert(target3.matches(agent));

    // Test 4: Targeting with behavioral filter
    ContentTargeting target4;
    target4.min_engagement_propensity = 0.8;  // Agent has 0.7, too low

    assert(!target4.matches(agent));

    std::cout << "  Content targeting test passed\n";
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

    assert(std::abs(prog_ratio - 0.3) < 0.1);
    assert(std::abs(lib_ratio - 0.5) < 0.1);
    assert(std::abs(black_ratio - 0.2) < 0.1);

    std::cout << "  Segment mix sampling test passed\n";
    std::cout << "    Progressive: " << (prog_ratio * 100) << "%\n";
    std::cout << "    Liberal: " << (lib_ratio * 100) << "%\n";
    std::cout << "    Black voters: " << (black_ratio * 100) << "%\n";
}

// Test codepath uniformity: all categories go through exp(-dist/decay)
void test_codepath_uniformity() {
    IdentitySpace space(IdentitySpace::create_default("USA"));
    const auto& config = space.config();

    // Verify all dimensions have positive decay rates
    for (const auto& dim : config.dimensions) {
        assert(dim.decay_rate > 0.0);
        assert(dim.num_dims >= 1 && dim.num_dims <= 5);
    }

    // Verify that even age goes through the same codepath
    AgentDemographics demo_young;
    demo_young.age = 25;
    demo_young.geography_type = "urban_core";
    demo_young.education_level = "bachelors";
    demo_young.race_ethnicity = "white";
    demo_young.religion = "atheist";
    demo_young.religiosity = 0.1;
    demo_young.gender = "male";
    demo_young.income_bracket = "middle";
    demo_young.political_ideology = 0.0;

    AgentDemographics demo_old;
    demo_old.age = 75;
    demo_old.geography_type = "urban_core";
    demo_old.education_level = "bachelors";
    demo_old.race_ethnicity = "white";
    demo_old.religion = "atheist";
    demo_old.religiosity = 0.1;
    demo_old.gender = "male";
    demo_old.income_bracket = "middle";
    demo_old.political_ideology = 0.0;

    auto young_coords = space.resolve(demo_young);
    auto old_coords = space.resolve(demo_old);

    // Age should be resolved as a DimensionalPosition
    assert(young_coords.count("age") > 0);
    assert(old_coords.count("age") > 0);

    // Young = (25-18)/72 = 0.097, Old = (75-18)/72 = 0.792
    double expected_young = (25.0 - 18.0) / 72.0;
    double expected_old = (75.0 - 18.0) / 72.0;
    assert(std::abs(young_coords["age"].coords[0] - expected_young) < 0.01);
    assert(std::abs(old_coords["age"].coords[0] - expected_old) < 0.01);

    // Age distance through same codepath
    double age_dist = young_coords["age"].distance_to(old_coords["age"]);
    assert(age_dist > 0.5);  // Significant age gap

    std::cout << "    Age positions: young=" << young_coords["age"].coords[0]
              << ", old=" << old_coords["age"].coords[0] << "\n";
    std::cout << "    Age distance: " << age_dist << "\n";
    std::cout << "  Codepath uniformity test passed\n";
}

// Test auto-normalization of weights
void test_weight_normalization() {
    // Create a config with non-standard weights
    IdentitySpaceConfig config;
    config.country_id = "TEST";

    IdentityDimensionConfig dim1;
    dim1.name = "geography";
    dim1.num_dims = 1;
    dim1.weight = 50;  // Arbitrary high weight
    dim1.decay_rate = 0.50;
    dim1.positions = {
        {"urban_core", DimensionalPosition(0.0)},
        {"rural",      DimensionalPosition(1.0)},
    };

    IdentityDimensionConfig dim2;
    dim2.name = "education";
    dim2.num_dims = 1;
    dim2.weight = 50;  // Equal to geography
    dim2.decay_rate = 0.50;
    dim2.positions = {
        {"high_school", DimensionalPosition(0.0)},
        {"graduate",    DimensionalPosition(1.0)},
    };

    config.dimensions = {dim1, dim2};
    IdentitySpace space(config);

    // Two identical agents
    AgentDemographics demo_a;
    demo_a.age = 35;
    demo_a.geography_type = "urban_core";
    demo_a.education_level = "high_school";
    demo_a.race_ethnicity = "white";
    demo_a.religion = "atheist";
    demo_a.religiosity = 0.1;
    demo_a.gender = "male";
    demo_a.income_bracket = "middle";
    demo_a.political_ideology = 0.0;

    AgentDemographics demo_b = demo_a;

    auto coords_a = space.resolve(demo_a);
    auto coords_b = space.resolve(demo_b);

    double sim = space.compute_similarity(coords_a, coords_b, demo_a, demo_b);

    // Identical agents should have similarity ~1.0
    assert(sim > 0.99);
    std::cout << "    Identical agents (weights 50+50): " << sim << " (> 0.99)\n";

    // Different on both dimensions
    demo_b.geography_type = "rural";
    demo_b.education_level = "graduate";
    coords_b = space.resolve(demo_b);

    sim = space.compute_similarity(coords_a, coords_b, demo_a, demo_b);

    // Should still be in [0,1] regardless of weight sum
    assert(sim >= 0.0 && sim <= 1.0);
    std::cout << "    Max-different agents (weights 50+50): " << sim << " (in [0,1])\n";

    std::cout << "  Weight normalization test passed\n";
}

// Test generate_demographics with identity space resolution
void test_demographics_with_identity_resolution() {
    std::mt19937 rng(42);
    DemographicSampler sampler(rng);
    IdentitySpace space(IdentitySpace::create_default("USA"));

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

    AgentDemographics demo = sampler.generate_demographics(seg, "cell_123", space);

    // Should have identity coords resolved
    assert(!demo.identity_coords.empty());
    assert(demo.country_id == "USA");

    // Check that key dimensions are present
    assert(demo.identity_coords.count("age") > 0);
    assert(demo.identity_coords.count("geography") > 0);
    assert(demo.identity_coords.count("education") > 0);
    assert(demo.identity_coords.count("religion") > 0);
    assert(demo.identity_coords.count("race_ethnicity") > 0);
    assert(demo.identity_coords.count("political_ideology") > 0);

    std::cout << "    country_id: " << demo.country_id << "\n";
    std::cout << "    Resolved " << demo.identity_coords.size() << " dimension coords\n";
    std::cout << "  Demographics with identity resolution test passed\n";
}

// Test cross-country comparison
void test_cross_country_configs() {
    IdentitySpace us_space(IdentitySpace::create_default("USA"));
    IdentitySpace ind_space(IdentitySpace::create_default("IND"));
    IdentitySpace bra_space(IdentitySpace::create_default("BRA"));

    // Verify each country has a valid config
    assert(us_space.config().country_id == "USA");
    assert(ind_space.config().country_id == "IND");
    assert(bra_space.config().country_id == "BRA");

    // Verify dimension counts
    assert(us_space.config().dimensions.size() >= 8);
    assert(ind_space.config().dimensions.size() >= 9);  // India has language
    assert(bra_space.config().dimensions.size() >= 8);

    // Verify India has language dimension with positive weight
    bool india_has_language = false;
    for (const auto& dim : ind_space.config().dimensions) {
        if (dim.name == "language" && dim.weight > 0) {
            india_has_language = true;
        }
    }
    assert(india_has_language);

    std::cout << "    USA dims: " << us_space.config().dimensions.size() << "\n";
    std::cout << "    IND dims: " << ind_space.config().dimensions.size() << "\n";
    std::cout << "    BRA dims: " << bra_space.config().dimensions.size() << "\n";
    std::cout << "  Cross-country config test passed\n";
}

int main() {
    std::cout << "Testing Agent Demographics System (Dimensional Identity)\n\n";

    std::cout << "[1] Demographic Sampling\n";
    test_demographic_sampling();

    std::cout << "\n[2] Psychographic Generation\n";
    test_psychographic_generation();

    std::cout << "\n[3] Belief Initialization\n";
    test_belief_initialization();

    std::cout << "\n[4] Religion Distances (Dimensional)\n";
    test_religion_distances();

    std::cout << "\n[5] Country-Specific Race Distances\n";
    test_country_race_distances();

    std::cout << "\n[6] Geography Distances\n";
    test_geography_distances();

    std::cout << "\n[7] Homophily Similarity (Full Dimensional)\n";
    test_homophily_similarity();

    std::cout << "\n[8] Influence Weight\n";
    test_influence_weight();

    std::cout << "\n[9] Content Targeting\n";
    test_content_targeting();

    std::cout << "\n[10] Segment Mix Sampling\n";
    test_segment_mix_sampling();

    std::cout << "\n[11] Codepath Uniformity\n";
    test_codepath_uniformity();

    std::cout << "\n[12] Weight Auto-Normalization\n";
    test_weight_normalization();

    std::cout << "\n[13] Demographics with Identity Resolution\n";
    test_demographics_with_identity_resolution();

    std::cout << "\n[14] Cross-Country Configs\n";
    test_cross_country_configs();

    std::cout << "\nAll 14 agent demographics tests passed!\n";
    return 0;
}
