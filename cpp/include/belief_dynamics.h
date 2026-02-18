#pragma once

#include "types.h"

// -----------------------------
// Module: Belief Dynamics
// Advanced influence dynamics with physics-inspired models
// -----------------------------

struct InfluenceDynamicsConfig {
    // Inertia & momentum
    double inertia_rho = 0.85;              // Momentum decay [0,1] (higher = more persistent)
    double learning_rate_base = 0.10;       // Base learning rate for stance updates

    // Rebound (damped spring to core value)
    double rebound_k = 0.05;                // Spring constant [0,1] (higher = stronger pull)

    // Critical velocity (nonlinear gain)
    double critical_velocity_threshold = 0.1;  // Threshold for momentum boost
    double critical_kappa = 2.0;               // Nonlinear gain multiplier

    // Evidence accumulation (multi-hit requirement)
    double evidence_decay_lambda = 0.90;    // Evidence decay per tick [0,1]
    double evidence_threshold = 0.5;        // Minimum evidence to update belief

    // Trust gate (superlinear)
    double trust_exponent_gamma = 2.0;      // Exponent for trust scaling (1=linear, >1=superlinear)

    // Habituation
    double habituation_alpha = 0.05;        // Habituation decay rate per exposure

    // Bounded confidence
    double bounded_confidence_tau = 1.5;    // Threshold for stance difference rejection

    InfluenceDynamicsConfig() = default;
};

class BeliefDynamicsEngine {
public:
    InfluenceDynamicsConfig config;

    BeliefDynamicsEngine() = default;
    explicit BeliefDynamicsEngine(const InfluenceDynamicsConfig& cfg) : config(cfg) {}

    // Compute belief update with advanced dynamics
    BeliefDelta compute_update(
        Belief& current,
        const Impression& impression,
        double trust,
        double identity_rigidity,
        bool is_self_source,
        double proximity);

private:
    // Apply inertia to momentum
    double apply_inertia(double old_momentum, double influence) const;

    // Apply rebound force toward core value
    double apply_rebound(double current_stance, double core_value) const;

    // Apply critical velocity boost
    double apply_critical_velocity(double momentum, double base_learning_rate) const;

    // Apply trust gate (superlinear)
    double apply_trust_gate(double trust) const;

    // Update evidence accumulator with decay
    double update_evidence_accumulator(double old_acc, double signal, double weight) const;

    // Apply habituation effect
    double apply_habituation(int exposure_count) const;

    // Check bounded confidence (reject if stance difference too large)
    bool check_bounded_confidence(double current_stance, double signal_stance) const;

    // Sigmoid helper
    double sigmoid(double x) const;
};
