#pragma once

#include <functional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "types.h"

// -----------------------------
// Module 1: Kernel (Phase Contract)
// -----------------------------

struct SimClock {
    int t = 0;
    int ticks_per_day = 96;
    int seconds_per_tick = 900;

    int tick_of_day() const {
        if (ticks_per_day <= 0) return 0;
        return t % ticks_per_day;
    }

    void advance(int dt) { t += dt; }
};

struct WorldContext {
    int current_tick = 0;
    std::string current_phase = "INIT";
    bool in_consolidation = false;

    // Core buffers (Module 0)
    std::unordered_map<int, std::vector<Stimulus>> stimuli_by_tick;
    std::unordered_map<int, std::vector<Content>> posted_by_tick;
    std::vector<std::pair<AgentId, BeliefDelta>> deferred_belief_deltas;

    void begin_phase(int tick, const std::string& phase) {
        current_tick = tick;
        current_phase = phase;
        in_consolidation = (phase == "CONSOLIDATE");
    }

    void clear_tick_buffers(int tick) {
        stimuli_by_tick.erase(tick);
        posted_by_tick.erase(tick);
    }

    void queue_belief_delta(const AgentId& agent_id, const BeliefDelta& delta) {
        deferred_belief_deltas.emplace_back(agent_id, delta);
    }

    std::vector<std::pair<AgentId, BeliefDelta>> pop_all_belief_deltas() {
        std::vector<std::pair<AgentId, BeliefDelta>> out;
        out.swap(deferred_belief_deltas);
        return out;
    }
};

struct WorldKernel {
    SimClock clock;
    WorldContext context;
    bool started = false;

    // Hooks for future modules (agent logic, stimuli ingestion, etc.)
    std::function<void(int, WorldContext&)> ingest_fn;
    std::function<void(int, WorldContext&)> act_fn;
    std::function<void(int, WorldContext&)> perceive_fn;
    std::function<void(int, WorldContext&)> consolidate_fn;

    void start();
    void step(int num_ticks);

private:
    void _reset_tick_budgets(int t);
    void _ingest(int t);
    void _act_batch(int t);
    void _perceive_batch(int t);
    void _consolidate(int t);
};
