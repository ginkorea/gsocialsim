#include "identity_space.h"
#include "agent.h"
#include "country.h"
#include <algorithm>
#include <cmath>
#include <numeric>

// ============================================================================
// IdentitySpace Implementation
// ============================================================================

IdentitySpace::IdentitySpace(const IdentitySpaceConfig& config)
    : config_(config), weight_sum_(0.0) {
    for (const auto& dim : config_.dimensions) {
        weight_sum_ += dim.weight;
    }
}

AgentIdentityCoords IdentitySpace::resolve(const AgentDemographics& demo) const {
    AgentIdentityCoords coords;

    for (const auto& dim : config_.dimensions) {
        if (dim.name == "age") {
            // Age: normalized to [0,1] via (age - 18) / 72.0
            double pos = std::clamp((demo.age - 18.0) / 72.0, 0.0, 1.0);
            coords["age"] = DimensionalPosition(pos);
            continue;
        }

        if (dim.name == "political_ideology") {
            coords["political_ideology"] = resolve_political(demo);
            continue;
        }

        // Look up the label for this dimension from the agent's demographics
        std::string label;
        if (dim.name == "religion") {
            label = demo.religion;
        } else if (dim.name == "race_ethnicity") {
            label = demo.race_ethnicity;
        } else if (dim.name == "geography") {
            label = demo.geography_type;
        } else if (dim.name == "education") {
            label = demo.education_level;
        } else if (dim.name == "gender") {
            label = demo.gender;
        } else if (dim.name == "income") {
            label = demo.income_bracket;
        } else if (dim.name == "class_culture") {
            label = demo.occupation;
            // Map occupation to class culture labels
            if (label == "professional") label = "professional_elite";
            else if (label == "white_collar") label = "white_collar";
            else if (label == "service") label = "service_sector";
            else if (label == "blue_collar") label = "blue_collar";
        } else if (dim.name == "language") {
            // Language would come from a language field; skip if not present
            continue;
        }

        if (label.empty()) continue;

        auto it = dim.positions.find(label);
        if (it != dim.positions.end()) {
            DimensionalPosition pos = it->second;

            // Override y-coordinate if y_source is specified
            if (!dim.y_source.empty() && pos.coords.size() >= 2) {
                double y_val = get_agent_field(demo, dim.y_source);
                if (y_val >= 0.0) {
                    pos.coords[1] = y_val;
                }
            }

            coords[dim.name] = pos;
        } else {
            // Unknown label: place at origin
            coords[dim.name] = DimensionalPosition(std::vector<double>(static_cast<size_t>(dim.num_dims), 0.0));
        }
    }

    return coords;
}

double IdentitySpace::compute_similarity(
    const AgentIdentityCoords& a,
    const AgentIdentityCoords& b,
    const AgentDemographics& demo_a,
    const AgentDemographics& demo_b) const {

    if (weight_sum_ <= 0.0) return 0.5;

    double weighted_sum = 0.0;

    for (const auto& dim : config_.dimensions) {
        if (dim.weight <= 0.0) continue;

        auto it_a = a.find(dim.name);
        auto it_b = b.find(dim.name);

        double dim_similarity;
        if (it_a == a.end() || it_b == b.end()) {
            // Missing dimension: assume neutral similarity
            dim_similarity = 0.5;
        } else {
            double dist = it_a->second.distance_to(it_b->second);
            dim_similarity = std::exp(-dist / dim.decay_rate);
        }

        weighted_sum += dim.weight * dim_similarity;
    }

    return weighted_sum / weight_sum_;
}

double IdentitySpace::get_agent_field(const AgentDemographics& demo, const std::string& field_name) {
    if (field_name == "religiosity") return demo.religiosity;
    return -1.0; // Unknown field
}

DimensionalPosition IdentitySpace::resolve_political(const AgentDemographics& demo) {
    // Use PoliticalIdentity if available (non-zero), else derive from scalar
    const auto& pi = demo.political_identity;

    // Check if political_identity has been populated
    bool has_pi = (pi.economic_left_right != 0.0 ||
                   pi.social_progressive_traditional != 0.0 ||
                   pi.libertarian_authoritarian != 0.0 ||
                   pi.cosmopolitan_nationalist != 0.0 ||
                   pi.secular_religious != 0.0);

    if (has_pi) {
        return DimensionalPosition(std::vector<double>{
            pi.economic_left_right,
            pi.social_progressive_traditional,
            pi.libertarian_authoritarian,
            pi.cosmopolitan_nationalist,
            pi.secular_religious
        });
    }

    // Fallback: derive rough 5D position from scalar political_ideology [-1, +1]
    double ideo = demo.political_ideology;
    return DimensionalPosition(std::vector<double>{
        ideo,          // economic: left = -1, right = +1
        -ideo * 0.8,   // social: left = progressive (-), right = traditional (+)
        0.0,           // libertarian/authoritarian: unknown, default center
        ideo * 0.5,    // cosmopolitan/nationalist: mild correlation
        ideo * 0.4     // secular/religious: mild correlation
    });
}

// ============================================================================
// Factory: Country Default Configs
// ============================================================================

IdentitySpaceConfig IdentitySpace::create_default(const std::string& country_id) {
    if (country_id == "USA") return create_usa_default();
    if (country_id == "IND") return create_ind_default();
    if (country_id == "BRA") return create_bra_default();
    if (country_id == "GBR") return create_gbr_default();
    if (country_id == "FRA") return create_fra_default();
    // Default to USA for unknown countries
    return create_usa_default();
}

// ============================================================================
// Shared Dimension Defaults
// ============================================================================

IdentityDimensionConfig IdentitySpace::religion_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "religion";
    dim.num_dims = 2;
    dim.weight = 15;
    dim.decay_rate = 0.40;
    dim.y_source = "religiosity";
    dim.positions = {
        {"evangelical",  DimensionalPosition( 0.00, 0.85)},
        {"protestant",   DimensionalPosition(-0.05, 0.55)},
        {"catholic",     DimensionalPosition(-0.15, 0.60)},
        {"orthodox",     DimensionalPosition(-0.20, 0.65)},
        {"mormon",       DimensionalPosition( 0.10, 0.80)},
        {"jewish",       DimensionalPosition( 0.30, 0.50)},
        {"muslim",       DimensionalPosition( 0.40, 0.70)},
        {"hindu",        DimensionalPosition(-0.70, 0.60)},
        {"buddhist",     DimensionalPosition(-0.80, 0.50)},
        {"sikh",         DimensionalPosition(-0.60, 0.70)},
        {"jain",         DimensionalPosition(-0.75, 0.65)},
        {"atheist",      DimensionalPosition( 0.90, 0.05)},
        {"agnostic",     DimensionalPosition( 0.85, 0.10)},
        {"secular",      DimensionalPosition( 0.80, 0.15)},
    };
    return dim;
}

IdentityDimensionConfig IdentitySpace::geography_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "geography";
    dim.num_dims = 1;
    dim.weight = 15;
    dim.decay_rate = 0.50;
    dim.positions = {
        {"urban_core",  DimensionalPosition(0.00)},
        {"suburban",    DimensionalPosition(0.35)},
        {"small_town",  DimensionalPosition(0.65)},
        {"rural",       DimensionalPosition(1.00)},
    };
    return dim;
}

IdentityDimensionConfig IdentitySpace::education_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "education";
    dim.num_dims = 1;
    dim.weight = 8;
    dim.decay_rate = 0.50;
    dim.positions = {
        {"high_school",   DimensionalPosition(0.00)},
        {"some_college",  DimensionalPosition(0.35)},
        {"bachelors",     DimensionalPosition(0.70)},
        {"graduate",      DimensionalPosition(1.00)},
    };
    return dim;
}

IdentityDimensionConfig IdentitySpace::gender_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "gender";
    dim.num_dims = 1;
    dim.weight = 4;
    dim.decay_rate = 0.60;
    dim.positions = {
        {"male",       DimensionalPosition(0.00)},
        {"non_binary", DimensionalPosition(0.50)},
        {"female",     DimensionalPosition(1.00)},
    };
    return dim;
}

IdentityDimensionConfig IdentitySpace::income_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "income";
    dim.num_dims = 1;
    dim.weight = 3;
    dim.decay_rate = 0.50;
    dim.positions = {
        {"low",          DimensionalPosition(0.00)},
        {"middle",       DimensionalPosition(0.35)},
        {"upper_middle", DimensionalPosition(0.65)},
        {"high",         DimensionalPosition(1.00)},
    };
    return dim;
}

IdentityDimensionConfig IdentitySpace::age_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "age";
    dim.num_dims = 1;
    dim.weight = 10;
    dim.decay_rate = 0.28;
    // Age positions are computed dynamically in resolve()
    return dim;
}

IdentityDimensionConfig IdentitySpace::class_culture_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "class_culture";
    dim.num_dims = 1;
    dim.weight = 0; // Optional, disabled by default
    dim.decay_rate = 0.50;
    dim.positions = {
        {"agrarian",           DimensionalPosition(0.00)},
        {"blue_collar",        DimensionalPosition(0.25)},
        {"service_sector",     DimensionalPosition(0.50)},
        {"white_collar",       DimensionalPosition(0.75)},
        {"professional_elite", DimensionalPosition(1.00)},
    };
    return dim;
}

IdentityDimensionConfig IdentitySpace::political_ideology_dim_default() {
    IdentityDimensionConfig dim;
    dim.name = "political_ideology";
    dim.num_dims = 5;
    dim.weight = 25;
    dim.decay_rate = 0.30;
    // Positions computed dynamically from PoliticalIdentity or scalar fallback
    return dim;
}

// ============================================================================
// USA Default
// ============================================================================

IdentitySpaceConfig IdentitySpace::create_usa_default() {
    IdentitySpaceConfig config;
    config.country_id = "USA";

    // Race/Ethnicity -- US-specific 2D
    IdentityDimensionConfig race;
    race.name = "race_ethnicity";
    race.num_dims = 2;
    race.weight = 20;
    race.decay_rate = 0.30;
    race.positions = {
        {"white",       DimensionalPosition( 0.00,  0.00)},
        {"black",       DimensionalPosition(-0.80, -0.60)},
        {"hispanic",    DimensionalPosition(-0.30, -0.40)},
        {"asian",       DimensionalPosition( 0.20, -0.70)},
        {"multiracial", DimensionalPosition(-0.20, -0.20)},
        {"other",       DimensionalPosition( 0.00, -0.30)},
    };

    config.dimensions = {
        political_ideology_dim_default(),
        race,
        religion_dim_default(),
        geography_dim_default(),
        age_dim_default(),
        education_dim_default(),
        gender_dim_default(),
        income_dim_default(),
        class_culture_dim_default(),
    };

    return config;
}

// ============================================================================
// India Default
// ============================================================================

IdentitySpaceConfig IdentitySpace::create_ind_default() {
    IdentitySpaceConfig config;
    config.country_id = "IND";

    // Race/Ethnicity maps to caste/community in India
    IdentityDimensionConfig race;
    race.name = "race_ethnicity";
    race.num_dims = 2;
    race.weight = 20;
    race.decay_rate = 0.30;
    race.positions = {
        {"upper_caste_hindu", DimensionalPosition( 0.00,  0.00)},
        {"obc",               DimensionalPosition(-0.30,  0.10)},
        {"dalit",             DimensionalPosition(-0.70,  0.20)},
        {"muslim",            DimensionalPosition( 0.10, -0.80)},
        {"sikh",              DimensionalPosition( 0.20, -0.30)},
        {"christian",         DimensionalPosition( 0.15, -0.50)},
        {"tribal",            DimensionalPosition(-0.60,  0.50)},
    };

    // India: religion weight higher, language important
    auto religion = religion_dim_default();
    religion.weight = 20; // Religion more salient in India

    auto political = political_ideology_dim_default();
    political.weight = 20; // Politics slightly less dominant than US

    // Language dimension for India
    IdentityDimensionConfig language;
    language.name = "language";
    language.num_dims = 2;
    language.weight = 10; // Language matters in India
    language.decay_rate = 0.40;
    language.positions = {
        {"hindi",     DimensionalPosition( 0.00,  0.00)},
        {"urdu",      DimensionalPosition( 0.05, -0.20)},
        {"bengali",   DimensionalPosition(-0.30,  0.10)},
        {"tamil",     DimensionalPosition(-0.80, -0.30)},
        {"telugu",    DimensionalPosition(-0.60, -0.20)},
        {"marathi",   DimensionalPosition(-0.20,  0.05)},
        {"gujarati",  DimensionalPosition(-0.15,  0.10)},
        {"kannada",   DimensionalPosition(-0.65, -0.25)},
        {"malayalam", DimensionalPosition(-0.85, -0.35)},
        {"punjabi",   DimensionalPosition( 0.10,  0.20)},
        {"english",   DimensionalPosition( 0.40, -0.60)},
    };

    config.dimensions = {
        political,
        race,
        religion,
        geography_dim_default(),
        age_dim_default(),
        education_dim_default(),
        gender_dim_default(),
        income_dim_default(),
        language,
        class_culture_dim_default(),
    };

    return config;
}

// ============================================================================
// Brazil Default
// ============================================================================

IdentitySpaceConfig IdentitySpace::create_bra_default() {
    IdentitySpaceConfig config;
    config.country_id = "BRA";

    // Brazilian color spectrum
    IdentityDimensionConfig race;
    race.name = "race_ethnicity";
    race.num_dims = 2;
    race.weight = 15; // Race less sharply divided in Brazil than US
    race.decay_rate = 0.35;
    race.positions = {
        {"branco",   DimensionalPosition( 0.00,  0.00)},
        {"pardo",    DimensionalPosition(-0.30, -0.15)},
        {"preto",    DimensionalPosition(-0.60, -0.30)},
        {"indigena", DimensionalPosition(-0.40, -0.70)},
        {"amarelo",  DimensionalPosition( 0.20, -0.50)},
    };

    auto religion = religion_dim_default();
    religion.weight = 18; // Religion very salient (evangelical vs catholic politics)

    config.dimensions = {
        political_ideology_dim_default(),
        race,
        religion,
        geography_dim_default(),
        age_dim_default(),
        education_dim_default(),
        gender_dim_default(),
        income_dim_default(),
        class_culture_dim_default(),
    };

    return config;
}

// ============================================================================
// UK Default
// ============================================================================

IdentitySpaceConfig IdentitySpace::create_gbr_default() {
    IdentitySpaceConfig config;
    config.country_id = "GBR";

    // UK race/ethnicity
    IdentityDimensionConfig race;
    race.name = "race_ethnicity";
    race.num_dims = 2;
    race.weight = 15;
    race.decay_rate = 0.30;
    race.positions = {
        {"white_british",      DimensionalPosition( 0.00,  0.00)},
        {"white_other",        DimensionalPosition( 0.05, -0.15)},
        {"black_caribbean",    DimensionalPosition(-0.50, -0.40)},
        {"black_african",      DimensionalPosition(-0.55, -0.50)},
        {"south_asian",        DimensionalPosition(-0.30, -0.60)},
        {"east_asian",         DimensionalPosition( 0.10, -0.70)},
        {"mixed",              DimensionalPosition(-0.15, -0.20)},
    };

    // UK: class is more important than US
    auto class_culture = class_culture_dim_default();
    class_culture.weight = 8; // Class matters more in UK

    auto political = political_ideology_dim_default();
    political.weight = 22;

    config.dimensions = {
        political,
        race,
        religion_dim_default(),
        geography_dim_default(),
        age_dim_default(),
        education_dim_default(),
        gender_dim_default(),
        income_dim_default(),
        class_culture,
    };

    return config;
}

// ============================================================================
// France Default
// ============================================================================

IdentitySpaceConfig IdentitySpace::create_fra_default() {
    IdentitySpaceConfig config;
    config.country_id = "FRA";

    // French race/ethnicity (officially France doesn't collect race data,
    // but social boundaries exist)
    IdentityDimensionConfig race;
    race.name = "race_ethnicity";
    race.num_dims = 2;
    race.weight = 12; // Lower weight: French republicanism de-emphasizes race
    race.decay_rate = 0.35;
    race.positions = {
        {"francais_souche",   DimensionalPosition( 0.00,  0.00)},
        {"maghrebin",         DimensionalPosition(-0.50, -0.60)},
        {"sub_saharan",       DimensionalPosition(-0.60, -0.50)},
        {"european_other",    DimensionalPosition( 0.05, -0.10)},
        {"asian",             DimensionalPosition( 0.15, -0.55)},
    };

    // France: laicite makes religion a strong divider
    auto religion = religion_dim_default();
    religion.weight = 18;

    auto political = political_ideology_dim_default();
    political.weight = 25;

    config.dimensions = {
        political,
        race,
        religion,
        geography_dim_default(),
        age_dim_default(),
        education_dim_default(),
        gender_dim_default(),
        income_dim_default(),
        class_culture_dim_default(),
    };

    return config;
}
