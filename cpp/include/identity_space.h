#pragma once

#include <cmath>
#include <string>
#include <unordered_map>
#include <vector>

// A position in 1-5 dimensional identity space
struct DimensionalPosition {
    std::vector<double> coords;

    DimensionalPosition() = default;
    explicit DimensionalPosition(const std::vector<double>& c) : coords(c) {}
    explicit DimensionalPosition(double x) : coords{x} {}
    DimensionalPosition(double x, double y) : coords{x, y} {}

    double distance_to(const DimensionalPosition& other) const {
        double sum = 0.0;
        size_t n = std::min(coords.size(), other.coords.size());
        for (size_t i = 0; i < n; ++i) {
            double d = coords[i] - other.coords[i];
            sum += d * d;
        }
        return std::sqrt(sum);
    }

    size_t dims() const { return coords.size(); }
};

// Configuration for a single identity dimension
struct IdentityDimensionConfig {
    std::string name;        // "religion", "race_ethnicity", "geography", etc.
    int num_dims = 1;        // 1D or 2D (up to 5 for political_ideology)
    double weight = 1.0;     // Relative importance (auto-normalized at runtime)
    double decay_rate = 0.5; // exp(-dist/decay_rate) controls sharpness

    // Label -> default position mapping
    std::unordered_map<std::string, DimensionalPosition> positions;

    // Optional: field name on agent to override y-coordinate (e.g., "religiosity")
    std::string y_source;
};

// Full identity space configuration (per country)
struct IdentitySpaceConfig {
    std::string country_id;
    std::vector<IdentityDimensionConfig> dimensions;
};

// Resolved coordinates for a single agent across all dimensions
using AgentIdentityCoords = std::unordered_map<std::string, DimensionalPosition>;

// Multi-dimensional political identity (moved here from country.h)
struct PoliticalIdentity {
    double economic_left_right = 0.0;           // [-1, +1]: socialist <-> capitalist
    double social_progressive_traditional = 0.0; // [-1, +1]: progressive <-> traditionalist
    double libertarian_authoritarian = 0.0;     // [-1, +1]: libertarian <-> authoritarian
    double cosmopolitan_nationalist = 0.0;      // [-1, +1]: globalist <-> nationalist
    double secular_religious = 0.0;             // [-1, +1]: secular <-> religious

    // Country-specific dimensions can be added dynamically
    std::unordered_map<std::string, double> additional_dimensions;
};

// Forward declaration
struct AgentDemographics;

// The identity space engine: resolves coordinates and computes similarity
class IdentitySpace {
public:
    explicit IdentitySpace(const IdentitySpaceConfig& config);

    // Resolve an agent's demographic labels into coordinate vectors
    AgentIdentityCoords resolve(const AgentDemographics& demo) const;

    // Compute similarity between two agents' resolved coordinates [0, 1]
    double compute_similarity(
        const AgentIdentityCoords& a,
        const AgentIdentityCoords& b,
        const AgentDemographics& demo_a,
        const AgentDemographics& demo_b) const;

    const IdentitySpaceConfig& config() const { return config_; }

    // Factory methods for country defaults
    static IdentitySpaceConfig create_default(const std::string& country_id);
    static IdentitySpaceConfig create_usa_default();
    static IdentitySpaceConfig create_ind_default();
    static IdentitySpaceConfig create_bra_default();
    static IdentitySpaceConfig create_gbr_default();
    static IdentitySpaceConfig create_fra_default();

private:
    IdentitySpaceConfig config_;
    double weight_sum_ = 0.0; // Precomputed for normalization

    // Get the agent's field value for y_source override
    static double get_agent_field(const AgentDemographics& demo, const std::string& field_name);

    // Build the political ideology position from PoliticalIdentity or scalar fallback
    static DimensionalPosition resolve_political(const AgentDemographics& demo);

    // Shared dimension configs used across countries
    static IdentityDimensionConfig religion_dim_default();
    static IdentityDimensionConfig geography_dim_default();
    static IdentityDimensionConfig education_dim_default();
    static IdentityDimensionConfig gender_dim_default();
    static IdentityDimensionConfig income_dim_default();
    static IdentityDimensionConfig age_dim_default();
    static IdentityDimensionConfig class_culture_dim_default();
    static IdentityDimensionConfig political_ideology_dim_default();
};
