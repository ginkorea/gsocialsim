#pragma once

#include <cstdint>
#include <functional>
#include <mutex>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "agent.h"
#include "geo_world.h"
#include "global_social_reality.h"
#include "network.h"
#include "network_manager.h"
#include "stimulus_ingestion.h"
#include "subscription_service.h"
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
    std::unordered_map<AgentId, double> time_remaining_by_agent;

    // Subscription service (Module: Subscriptions)
    SubscriptionService subscriptions;

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

    void set_time_budget(const AgentId& agent_id, double minutes) {
        time_remaining_by_agent[agent_id] = std::max(0.0, minutes);
    }

    bool spend_time(const AgentId& agent_id, double minutes) {
        double amt = std::max(0.0, minutes);
        auto it = time_remaining_by_agent.find(agent_id);
        if (it == time_remaining_by_agent.end()) {
            return true;
        }
        if (it->second < amt) return false;
        it->second -= amt;
        return true;
    }
};

struct WorldKernel {
    SimClock clock;
    WorldContext context;
    bool started = false;
    bool enable_parallel = true;
    size_t parallel_workers = 0;
    bool enable_timing = false;
    size_t max_recipients_per_content = 0; // deprecated

    double mutual_trust_weight = 0.2;
    double mutual_norm = 50.0;
    int offline_contacts_per_tick = 2;
    double offline_base_prob = 0.6;
    int discovery_min_per_tick = 1;
    int discovery_max_per_tick = 3;
    size_t discovery_pool_size = 200;

    struct TimingStat {
        double total = 0.0;
        double max = 0.0;
        size_t count = 0;
    };
    std::unordered_map<std::string, TimingStat> timing;

    struct AgentPopulation {
        std::unordered_map<AgentId, Agent> agents;

        void add_agent(const Agent& agent) { agents.insert_or_assign(agent.id, agent); }
        Agent* get(const AgentId& agent_id) {
            auto it = agents.find(agent_id);
            return it == agents.end() ? nullptr : &it->second;
        }
    };

    AgentPopulation agents;
    NetworkManager* network_manager = nullptr;
    NetworkLayer network;  // Kept for backward compatibility (aliases broadcast_feed graph)
    GlobalSocialReality gsr;
    StimulusIngestionEngine stimulus_engine;
    GeoWorld geo;

    uint32_t seed = 123;
    std::mt19937 rng = std::mt19937(seed);

    std::vector<AgentId> agent_id_cache;
    std::vector<Agent*> agent_ptr_cache;
    std::vector<double> remaining_cache;

    enum class AnalyticsMode {
        Summary,
        Detailed
    };

    struct AnalyticsSummary {
        int tick = 0;
        uint64_t impressions = 0;
        uint64_t consumed = 0;
        uint64_t belief_deltas = 0;

        void reset(int t) {
            tick = t;
            impressions = 0;
            consumed = 0;
            belief_deltas = 0;
        }
    };

    // Analytics (lightweight)
    bool enable_analytics = false;
    AnalyticsMode analytics_mode = AnalyticsMode::Summary;
    std::string analytics_path = "reports/analytics.csv";
    std::vector<std::string> analytics_buffer;
    size_t analytics_flush_every = 1000;
    std::mutex analytics_mutex;
    AnalyticsSummary analytics_summary;
    void analytics_log(int tick, const std::string& type, const std::string& payload);
    void analytics_flush();

    // Hooks for future modules (agent logic, stimuli ingestion, etc.)
    std::function<void(int, WorldContext&)> ingest_fn;
    std::function<void(int, WorldContext&)> act_fn;
    std::function<void(int, WorldContext&)> perceive_fn;
    std::function<void(int, WorldContext&)> consolidate_fn;

    void start();
    void step(int num_ticks);
    std::vector<std::tuple<std::string, double, size_t, double>> timing_report() const;

private:
    void _reset_tick_budgets(int t);
    void _ingest(int t);
    void _act_batch(int t);
    void _perceive_batch(int t);
    void _consolidate(int t);
    void _record_timing(const std::string& name, double seconds);
};
