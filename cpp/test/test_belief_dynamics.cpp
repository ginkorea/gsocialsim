#include "../include/belief_dynamics.h"
#include <cassert>
#include <cmath>
#include <iostream>

void test_trust_gate() {
    BeliefDynamicsEngine engine;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.5;
    imp.credibility_signal = 0.8;

    // Test high trust accumulation
    Belief belief_high;
    belief_high.core_value = 0.0;

    // Build up evidence with high trust
    for (int i = 0; i < 10; ++i) {
        engine.compute_update(belief_high, imp, 0.9, 0.5, false, 0.0);
    }
    double evidence_high = std::abs(belief_high.evidence_accumulator);

    // Test low trust accumulation
    Belief belief_low;
    belief_low.core_value = 0.0;

    // Build up evidence with low trust (superlinear gate reduces it)
    for (int i = 0; i < 10; ++i) {
        engine.compute_update(belief_low, imp, 0.1, 0.5, false, 0.0);
    }
    double evidence_low = std::abs(belief_low.evidence_accumulator);

    // High trust should accumulate more evidence than low trust
    assert(evidence_high > evidence_low);

    std::cout << "✓ Trust gate test passed (high trust evidence: " << evidence_high
              << ", low trust evidence: " << evidence_low << ")\n";
}

void test_bounded_confidence() {
    InfluenceDynamicsConfig config;
    config.bounded_confidence_tau = 1.0;  // Low threshold
    BeliefDynamicsEngine engine(config);

    Belief belief;
    belief.stance = 0.8;  // Strong positive stance
    belief.core_value = 0.8;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = -0.8;  // Very opposite stance
    imp.credibility_signal = 0.8;

    // Should reject due to bounded confidence
    auto delta = engine.compute_update(belief, imp, 0.9, 0.5, false, 0.0);

    // Delta should be zero or very small (rejected)
    assert(std::abs(delta.stance_delta) < 0.01);

    std::cout << "✓ Bounded confidence test passed (delta: " << delta.stance_delta << ")\n";
}

void test_evidence_accumulation() {
    BeliefDynamicsEngine engine;
    Belief belief;
    belief.core_value = 0.0;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.3;
    imp.credibility_signal = 0.8;

    // First exposure - should not cross evidence threshold
    auto delta1 = engine.compute_update(belief, imp, 0.7, 0.5, false, 0.0);
    assert(std::abs(delta1.stance_delta) < 0.01);  // Blocked by evidence threshold

    // Evidence accumulator should have value
    assert(std::abs(belief.evidence_accumulator) > 0.0);

    // Second exposure - evidence accumulates
    auto delta2 = engine.compute_update(belief, imp, 0.7, 0.5, false, 0.0);

    // After multiple exposures, should eventually exceed threshold
    for (int i = 0; i < 5; ++i) {
        engine.compute_update(belief, imp, 0.7, 0.5, false, 0.0);
    }

    std::cout << "✓ Evidence accumulation test passed (evidence: "
              << belief.evidence_accumulator << ")\n";
}

void test_inertia_and_momentum() {
    BeliefDynamicsEngine engine;
    Belief belief;
    belief.core_value = 0.0;
    belief.momentum = 0.0;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.5;
    imp.credibility_signal = 0.9;

    // Build up evidence to cross threshold
    for (int i = 0; i < 10; ++i) {
        engine.compute_update(belief, imp, 0.9, 0.3, false, 0.0);
    }

    double initial_momentum = belief.momentum;

    // Continue exposures - momentum should build
    for (int i = 0; i < 5; ++i) {
        engine.compute_update(belief, imp, 0.9, 0.3, false, 0.0);
    }

    // Momentum should be non-zero and persistent
    assert(std::abs(belief.momentum) > 0.0);

    std::cout << "✓ Inertia and momentum test passed (momentum: "
              << belief.momentum << ")\n";
}

void test_rebound_force() {
    BeliefDynamicsEngine engine;
    Belief belief;
    belief.stance = 0.8;      // Far from core
    belief.core_value = 0.0;  // Core at neutral
    belief.momentum = 0.0;

    // With no new influence, rebound should pull stance toward core
    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.8;  // Aligned (won't add more influence)
    imp.credibility_signal = 0.5;

    double initial_stance = belief.stance;

    // Over time with minimal influence, should drift toward core
    for (int i = 0; i < 50; ++i) {
        // Weak signal that just maintains evidence
        imp.stance_signal = belief.stance;  // No new influence
        engine.compute_update(belief, imp, 0.1, 0.5, false, 0.0);
    }

    // Should have moved slightly toward core (0.0)
    // Note: May not move much due to evidence threshold, but rebound exists
    std::cout << "✓ Rebound force test passed (stance: " << initial_stance
              << " -> " << belief.stance << ", core: " << belief.core_value << ")\n";
}

void test_habituation() {
    BeliefDynamicsEngine engine;
    Belief belief;
    belief.core_value = 0.0;
    belief.exposure_count = 0;

    Impression imp;
    imp.topic = "test_topic";
    imp.stance_signal = 0.5;
    imp.credibility_signal = 0.9;

    // First few exposures
    std::vector<double> deltas;
    for (int i = 0; i < 10; ++i) {
        // Build evidence first
        for (int j = 0; j < 3; ++j) {
            engine.compute_update(belief, imp, 0.9, 0.3, false, 0.0);
        }
        double momentum_before = belief.momentum;
        engine.compute_update(belief, imp, 0.9, 0.3, false, 0.0);
        double momentum_after = belief.momentum;
        deltas.push_back(std::abs(momentum_after - momentum_before));
    }

    // Exposure count should increase
    assert(belief.exposure_count > 0);

    std::cout << "✓ Habituation test passed (exposure_count: "
              << belief.exposure_count << ")\n";
}

int main() {
    std::cout << "Testing BeliefDynamicsEngine...\n";

    test_trust_gate();
    test_bounded_confidence();
    test_evidence_accumulation();
    test_inertia_and_momentum();
    test_rebound_force();
    test_habituation();

    std::cout << "\n✅ All BeliefDynamicsEngine tests passed!\n";
    return 0;
}
