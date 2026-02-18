#pragma once

#include "country.h"
#include "cross_border.h"
#include "media_diet.h"
#include "actor_capabilities.h"
#include <string>
#include <vector>
#include <functional>
#include <iostream>

// ============================================================================
// Phase 4: Global Invariants Scenario Harness
// ============================================================================
//
// Deterministic scenario framework for validating global architecture
// invariants. Each scenario sets up a known configuration and asserts
// that computed values satisfy structural contracts.
//
// Usage:
//   ScenarioHarness harness;
//   harness.register_scenario("cross_border_same_country", test_same_country);
//   harness.run_all();
//
// Invariants tested:
//   - CrossBorderFactors: same-country >= 0.9, high-tension cred <= 0.5
//   - MediaDiet: budget sums to 1.0, saturation < raw share
//   - ActorCapabilities: credibility in [floor, ceiling], production bounded
//   - End-to-end: Russian interference scenario matches expected patterns

struct ScenarioResult {
    std::string name;
    bool passed = false;
    std::string failure_reason;
    double duration_ms = 0.0;
};

class ScenarioHarness {
public:
    using ScenarioFn = std::function<bool(std::string&)>;

    void register_scenario(const std::string& name, ScenarioFn fn);
    std::vector<ScenarioResult> run_all();
    void print_results(const std::vector<ScenarioResult>& results) const;

    // Built-in scenario registration
    void register_all_builtin();

private:
    std::vector<std::pair<std::string, ScenarioFn>> scenarios_;
};

// ============================================================================
// Built-in Scenario Functions
// ============================================================================

namespace scenarios {

// --- CrossBorderFactors invariants ---
bool cross_border_same_country(std::string& reason);
bool cross_border_high_tension(std::string& reason);
bool cross_border_untranslated_foreign(std::string& reason);
bool cross_border_language_barrier(std::string& reason);
bool cross_border_state_propaganda(std::string& reason);

// --- MediaDiet invariants ---
bool media_diet_budget_conservation(std::string& reason);
bool media_diet_saturation_diminishing(std::string& reason);
bool media_diet_diaspora_split(std::string& reason);
bool media_diet_shift_preserves_budget(std::string& reason);

// --- ActorCapabilities invariants ---
bool actor_caps_credibility_bounds(std::string& reason);
bool actor_caps_production_bounded(std::string& reason);
bool actor_caps_state_vs_media(std::string& reason);
bool actor_caps_validate_profiles(std::string& reason);

// --- End-to-end scenarios ---
bool scenario_russian_interference(std::string& reason);
bool scenario_international_media_coverage(std::string& reason);
bool scenario_diaspora_media_consumption(std::string& reason);

} // namespace scenarios
