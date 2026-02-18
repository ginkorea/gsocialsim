#include "belief_dynamics.h"

#include <algorithm>
#include <cmath>

// Helper to clamp value to range
static double clamp(double x, double lo, double hi) {
    return std::max(lo, std::min(hi, x));
}

// ============================================================================
// BeliefDynamicsEngine Implementation
// ============================================================================

BeliefDelta BeliefDynamicsEngine::compute_update(
    Belief& current,
    const Impression& impression,
    double trust,
    double identity_rigidity,
    bool is_self_source,
    double proximity) {

    BeliefDelta delta;
    delta.topic_id = impression.topic;

    double stance_signal = impression.stance_signal;
    double credibility = impression.credibility_signal;
    double social_proof = impression.social_proof;
    double primal_activation = impression.primal_activation;
    double identity_threat = impression.identity_threat;

    // === 1. Trust Gate (Superlinear) ===
    // Low trust has near-zero influence, high trust has amplified influence
    double trust_gated = apply_trust_gate(trust);

    // === 2. Bounded Confidence Check ===
    // Reject signals that are too far from current stance
    if (!check_bounded_confidence(current.stance, stance_signal)) {
        // Signal rejected, no belief update
        return delta;
    }

    // === 3. Habituation Effect ===
    // Repeated exposures have diminishing returns
    double habituation_mult = apply_habituation(current.exposure_count);
    current.exposure_count++;

    // === 4. Base Influence Calculation ===
    // Trust effect with proximity and social proof boosts
    double trust_effect = trust_gated * (1.0 + 0.15 * proximity + 0.25 * social_proof);

    // Self-source bonus
    if (is_self_source) {
        trust_effect *= 1.2;
    }

    // Credibility multiplier
    double credibility_mult = 0.5 + credibility;

    // Primal activation multiplier
    double primal_mult = 1.0 + 0.25 * primal_activation;

    // Physical proximity amplification (10x boost)
    double proximity_mult = 1.0 + 9.0 * proximity;

    // Scroll influence reduction (scrolled content less influential)
    double scroll_influence_mult = (impression.intake_mode == IntakeMode::SCROLL) ? 0.35 : 1.0;

    // Combined base multiplier
    double base_mult = trust_effect * credibility_mult * primal_mult * proximity_mult *
                       scroll_influence_mult * habituation_mult;

    // === 5. Identity Defense & Confirmation Bias ===
    double stance_diff = stance_signal - current.stance;
    double current_stance = current.stance;

    // Openness factor (identity rigidity resistance)
    double openness = 1.0 - identity_rigidity;

    // Identity threat causes defensive reversal
    bool is_threatening = (identity_threat > 0.5);
    bool is_opposed = (std::abs(stance_diff) > 1.0);

    if (is_threatening && is_opposed) {
        // Backfire effect: reverse the influence
        stance_diff = -stance_diff * 0.4;
    } else if (stance_diff * current_stance > 0) {
        // Confirming signal: boost by 10%
        stance_diff *= 1.1;
    } else if (is_opposed) {
        // Opposing but not threatening: reduce by openness
        stance_diff *= openness * 0.6;
    }

    // === 6. Evidence Accumulation (Multi-hit Requirement) ===
    // Update evidence accumulator with weighted signal
    double signal_weight = base_mult * 0.1;
    current.evidence_accumulator = update_evidence_accumulator(
        current.evidence_accumulator, stance_diff, signal_weight);

    // Only update if evidence exceeds threshold
    if (std::abs(current.evidence_accumulator) < config.evidence_threshold) {
        // Not enough evidence yet, no stance update
        return delta;
    }

    // === 7. Inertia & Momentum ===
    // Base stance change from evidence
    double raw_stance_change = config.learning_rate_base * current.evidence_accumulator;

    // Update momentum with inertia
    current.momentum = apply_inertia(current.momentum, raw_stance_change);

    // === 8. Critical Velocity (Nonlinear Gain) ===
    // Once momentum builds, additional aligned influence becomes easier
    double effective_learning_rate = apply_critical_velocity(current.momentum, config.learning_rate_base);

    // === 9. Rebound Force (Damped Spring to Core Value) ===
    // Pull stance back toward core value
    double rebound_force = apply_rebound(current.stance, current.core_value);

    // === 10. Final Stance Update ===
    // Combine momentum, learning rate, and rebound
    delta.stance_delta = effective_learning_rate * current.momentum + rebound_force;

    // Apply stance delta
    double new_stance = current.stance + delta.stance_delta;
    new_stance = clamp(new_stance, -1.0, 1.0);
    delta.stance_delta = new_stance - current.stance;

    // === 11. Confidence Update ===
    // Confirming signals increase confidence
    // Opposing signals decrease confidence
    if (stance_diff * current_stance > 0) {
        // Confirming
        delta.confidence_delta = 0.04 * trust_effect * base_mult;
    } else {
        // Opposing
        delta.confidence_delta = -0.02 * trust_effect * base_mult;
    }

    // Self-source confidence boost
    if (is_self_source) {
        delta.confidence_delta += 0.05;
    }

    // Clamp confidence change
    delta.confidence_delta = clamp(delta.confidence_delta, -0.2, 0.2);

    // Reset evidence accumulator after update
    current.evidence_accumulator *= 0.5;

    return delta;
}

// ============================================================================
// Private Helper Methods
// ============================================================================

double BeliefDynamicsEngine::apply_inertia(double old_momentum, double influence) const {
    // v_{t+1} = ρ * v_t + η * influence
    return config.inertia_rho * old_momentum + influence;
}

double BeliefDynamicsEngine::apply_rebound(double current_stance, double core_value) const {
    // F_rebound = -k * (stance - core_value)
    return -config.rebound_k * (current_stance - core_value);
}

double BeliefDynamicsEngine::apply_critical_velocity(double momentum, double base_learning_rate) const {
    // η_eff = η * (1 + κ * sigmoid(|v| - v_threshold))
    double velocity_excess = std::abs(momentum) - config.critical_velocity_threshold;
    if (velocity_excess <= 0) {
        return base_learning_rate;
    }
    double boost = config.critical_kappa * sigmoid(velocity_excess);
    return base_learning_rate * (1.0 + boost);
}

double BeliefDynamicsEngine::apply_trust_gate(double trust) const {
    // trust_effect = trust^γ (superlinear for γ > 1)
    return std::pow(std::max(0.0, std::min(1.0, trust)), config.trust_exponent_gamma);
}

double BeliefDynamicsEngine::update_evidence_accumulator(double old_acc, double signal, double weight) const {
    // E_t = λ * E_{t-1} + w * signal
    return config.evidence_decay_lambda * old_acc + weight * signal;
}

double BeliefDynamicsEngine::apply_habituation(int exposure_count) const {
    // w_i = 1 / (1 + α * n_exposures)
    return 1.0 / (1.0 + config.habituation_alpha * exposure_count);
}

bool BeliefDynamicsEngine::check_bounded_confidence(double current_stance, double signal_stance) const {
    // Reject if stance difference exceeds threshold
    double diff = std::abs(signal_stance - current_stance);
    return diff <= config.bounded_confidence_tau;
}

double BeliefDynamicsEngine::sigmoid(double x) const {
    return 1.0 / (1.0 + std::exp(-x));
}
