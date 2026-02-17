#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <algorithm>

namespace py = pybind11;

static inline float clamp01(float v) {
    return std::max(0.0f, std::min(1.0f, v));
}

static inline std::pair<float, float> compute_delta(
    float stance_signal,
    float current_stance,
    bool has_belief,
    float trust,
    float credibility,
    float primal_activation,
    float identity_threat,
    bool is_self_source,
    float identity_rigidity,
    bool is_physical
) {
    trust = clamp01(trust);
    float multiplier = is_physical ? 10.0f : 1.0f;
    float trust_effect = is_physical ? std::min(1.0f, trust + 0.15f) : trust;

    credibility = clamp01(credibility);
    float credibility_mult = 0.5f + credibility;

    primal_activation = clamp01(primal_activation);
    float primal_mult = 1.0f + 0.25f * primal_activation;

    if (is_self_source) {
        multiplier *= 1.2f;
    }

    bool is_threatening = identity_threat > 0.5f;

    if (!has_belief) {
        float stance_delta = stance_signal * trust_effect * multiplier;
        float confidence_delta = (0.1f * trust_effect * multiplier) + (is_self_source ? (0.03f * trust_effect) : 0.0f);
        return {stance_delta, confidence_delta};
    }

    float stance_difference = stance_signal - current_stance;
    bool is_confirming = (stance_difference > 0.0f && current_stance > 0.0f) ||
                         (stance_difference < 0.0f && current_stance < 0.0f);
    bool is_opposed = std::abs(stance_difference) > 1.0f;

    float base_influence = 0.10f;
    float stance_change = stance_difference * base_influence * trust_effect * multiplier * credibility_mult * primal_mult;
    float confidence_change = 0.02f * trust_effect * multiplier * credibility_mult * primal_mult;

    if (is_confirming) {
        stance_change *= 1.1f;
        confidence_change += 0.04f * trust_effect * multiplier;
    }

    if (is_self_source) {
        confidence_change += 0.03f * trust_effect;
    }

    if (is_threatening && is_opposed) {
        stance_change = -stance_difference * base_influence * trust_effect * multiplier * 0.6f;
        confidence_change += 0.05f * trust_effect * multiplier;
    } else if (is_opposed) {
        float openness = clamp01(1.0f - identity_rigidity);
        float persuasive = trust_effect * credibility_mult;
        if (persuasive >= 0.7f) {
            confidence_change -= 0.01f * (0.3f + 0.7f * openness);
        }
    }

    return {stance_change, confidence_change};
}

py::tuple compute_belief_delta(
    float stance_signal,
    float current_stance,
    bool has_belief,
    float trust,
    float credibility,
    float primal_activation,
    float identity_threat,
    bool is_self_source,
    float identity_rigidity,
    bool is_physical
) {
    auto out = compute_delta(
        stance_signal,
        current_stance,
        has_belief,
        trust,
        credibility,
        primal_activation,
        identity_threat,
        is_self_source,
        identity_rigidity,
        is_physical
    );
    return py::make_tuple(out.first, out.second);
}

py::tuple compute_belief_deltas(
    py::array_t<float, py::array::c_style | py::array::forcecast> stance_signal,
    py::array_t<float, py::array::c_style | py::array::forcecast> current_stance,
    py::array_t<bool, py::array::c_style | py::array::forcecast> has_belief,
    py::array_t<float, py::array::c_style | py::array::forcecast> trust,
    py::array_t<float, py::array::c_style | py::array::forcecast> credibility,
    py::array_t<float, py::array::c_style | py::array::forcecast> primal_activation,
    py::array_t<float, py::array::c_style | py::array::forcecast> identity_threat,
    py::array_t<bool, py::array::c_style | py::array::forcecast> is_self_source,
    py::array_t<float, py::array::c_style | py::array::forcecast> identity_rigidity,
    py::array_t<bool, py::array::c_style | py::array::forcecast> is_physical
) {
    auto n = stance_signal.size();
    py::array_t<float> stance_delta(n);
    py::array_t<float> confidence_delta(n);

    auto s = stance_signal.unchecked<1>();
    auto cs = current_stance.unchecked<1>();
    auto hb = has_belief.unchecked<1>();
    auto tr = trust.unchecked<1>();
    auto cr = credibility.unchecked<1>();
    auto pa = primal_activation.unchecked<1>();
    auto it = identity_threat.unchecked<1>();
    auto ss = is_self_source.unchecked<1>();
    auto ir = identity_rigidity.unchecked<1>();
    auto ip = is_physical.unchecked<1>();

    auto out_s = stance_delta.mutable_unchecked<1>();
    auto out_c = confidence_delta.mutable_unchecked<1>();

    for (py::ssize_t i = 0; i < n; ++i) {
        auto out = compute_delta(
            s(i),
            cs(i),
            hb(i),
            tr(i),
            cr(i),
            pa(i),
            it(i),
            ss(i),
            ir(i),
            ip(i)
        );
        out_s(i) = out.first;
        out_c(i) = out.second;
    }

    return py::make_tuple(stance_delta, confidence_delta);
}

PYBIND11_MODULE(_fast_perception, m) {
    m.doc() = "Fast perception kernel for belief delta computation";
    m.def("compute_belief_delta", &compute_belief_delta, "Compute belief delta for a single impression");
    m.def("compute_belief_deltas", &compute_belief_deltas, "Compute belief deltas for batches");
}
