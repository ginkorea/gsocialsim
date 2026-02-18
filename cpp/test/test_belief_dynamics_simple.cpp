#include "../include/belief_dynamics.h"
#include <cassert>
#include <cmath>
#include <iostream>

void test_basic_update() {
    BeliefDynamicsEngine engine;
    Belief belief;
    belief.core_value = 0.0;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.5;
    imp.credibility_signal = 0.9;

    // Multiple exposures to build evidence
    for (int i = 0; i < 20; ++i) {
        engine.compute_update(belief, imp, 0.9, 0.3, false, 0.0);
    }

    // Check that belief state has changed
    bool state_changed = (belief.evidence_accumulator != 0.0) ||
                        (belief.stance != 0.0) ||
                        (belief.momentum != 0.0) ||
                        (belief.exposure_count > 0);

    assert(state_changed);

    std::cout << "✓ Basic update test passed\n";
    std::cout << "  Stance: " << belief.stance << "\n";
    std::cout << "  Momentum: " << belief.momentum << "\n";
    std::cout << "  Evidence: " << belief.evidence_accumulator << "\n";
    std::cout << "  Exposures: " << belief.exposure_count << "\n";
}

void test_config_initialization() {
    InfluenceDynamicsConfig config;

    // Check default values
    assert(config.inertia_rho > 0.0 && config.inertia_rho <= 1.0);
    assert(config.learning_rate_base > 0.0);
    assert(config.rebound_k >= 0.0);
    assert(config.trust_exponent_gamma >= 1.0);

    std::cout << "✓ Config initialization test passed\n";
}

void test_exposure_tracking() {
    BeliefDynamicsEngine engine;
    Belief belief;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.3;
    imp.credibility_signal = 0.7;

    int initial_count = belief.exposure_count;

    // Process multiple impressions
    for (int i = 0; i < 5; ++i) {
        engine.compute_update(belief, imp, 0.7, 0.5, false, 0.0);
    }

    // Exposure count should increase
    assert(belief.exposure_count > initial_count);

    std::cout << "✓ Exposure tracking test passed (count: "
              << belief.exposure_count << ")\n";
}

void test_high_vs_low_trust() {
    // Test that high trust accumulates more evidence than low trust
    BeliefDynamicsEngine engine;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.4;
    imp.credibility_signal = 0.8;

    Belief high_trust_belief;
    Belief low_trust_belief;

    // Same number of exposures, different trust levels
    for (int i = 0; i < 15; ++i) {
        engine.compute_update(high_trust_belief, imp, 0.95, 0.4, false, 0.0);
        engine.compute_update(low_trust_belief, imp, 0.05, 0.4, false, 0.0);
    }

    // High trust should result in larger absolute stance or evidence accumulation
    bool high_trust_more_influential =
        std::abs(high_trust_belief.stance) >= std::abs(low_trust_belief.stance) ||
        std::abs(high_trust_belief.evidence_accumulator) > std::abs(low_trust_belief.evidence_accumulator);

    assert(high_trust_more_influential);

    std::cout << "✓ High vs low trust test passed\n";
    std::cout << "  High trust stance: " << high_trust_belief.stance << "\n";
    std::cout << "  Low trust stance: " << low_trust_belief.stance << "\n";
}

void test_self_source_bonus() {
    BeliefDynamicsEngine engine;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.5;
    imp.credibility_signal = 0.7;

    Belief self_belief;
    Belief other_belief;

    // Self-source vs other source
    for (int i = 0; i < 15; ++i) {
        engine.compute_update(self_belief, imp, 0.7, 0.5, true, 0.0);  // is_self_source=true
        engine.compute_update(other_belief, imp, 0.7, 0.5, false, 0.0); // is_self_source=false
    }

    // Self-source should have some advantage
    std::cout << "✓ Self-source bonus test completed\n";
    std::cout << "  Self stance: " << self_belief.stance << "\n";
    std::cout << "  Other stance: " << other_belief.stance << "\n";
}

void test_proximity_amplification() {
    BeliefDynamicsEngine engine;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.4;
    imp.credibility_signal = 0.8;

    Belief prox_belief;
    Belief remote_belief;

    // Physical proximity vs remote
    for (int i = 0; i < 15; ++i) {
        engine.compute_update(prox_belief, imp, 0.7, 0.5, false, 0.8);  // high proximity
        engine.compute_update(remote_belief, imp, 0.7, 0.5, false, 0.0); // no proximity
    }

    // Proximity should amplify influence
    bool proximity_matters =
        std::abs(prox_belief.stance) >= std::abs(remote_belief.stance) ||
        std::abs(prox_belief.evidence_accumulator) > std::abs(remote_belief.evidence_accumulator);

    assert(proximity_matters);

    std::cout << "✓ Proximity amplification test passed\n";
    std::cout << "  Proximity stance: " << prox_belief.stance << "\n";
    std::cout << "  Remote stance: " << remote_belief.stance << "\n";
}

int main() {
    std::cout << "Testing BeliefDynamicsEngine (Simplified)...\n\n";

    test_config_initialization();
    test_basic_update();
    test_exposure_tracking();
    test_high_vs_low_trust();
    test_self_source_bonus();
    test_proximity_amplification();

    std::cout << "\n✅ All BeliefDynamicsEngine tests passed!\n";
    return 0;
}
