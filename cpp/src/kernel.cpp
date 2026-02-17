#include "kernel.h"

#include <algorithm>
#include <deque>
#include <thread>

static inline double clamp01(double v) {
    if (v < 0.0) return 0.0;
    if (v > 1.0) return 1.0;
    return v;
}

static std::optional<double> parse_opt_double(const std::unordered_map<std::string, std::string>& metadata,
                                              const std::string& key) {
    auto it = metadata.find(key);
    if (it == metadata.end()) return std::nullopt;
    try {
        return std::stod(it->second);
    } catch (...) {
        return std::nullopt;
    }
}

static Content stimulus_to_content(const Stimulus& stim) {
    Content c;
    c.id = stim.id;
    c.author_id = stim.creator_id.value_or(stim.source);
    c.topic = stim.topic_hint.value_or("T_MISC");
    c.stance = stim.stance_hint.value_or(0.0);
    c.media_type = stim.media_type;
    c.content_text = stim.content_text;
    c.outlet_id = stim.outlet_id;
    c.community_id = stim.community_id;
    c.primal_triggers = stim.primal_triggers;
    c.primal_intensity = stim.primal_intensity.value_or(0.0);
    c.credibility_signal = 0.5;
    c.social_proof = 0.0;

    auto threat = parse_opt_double(stim.metadata, "identity_threat");
    if (threat.has_value()) {
        c.identity_threat = threat;
        c.is_identity_threatening = (threat.value() > 0.5);
    }
    auto social_proof = parse_opt_double(stim.metadata, "social_proof");
    if (social_proof.has_value()) {
        c.social_proof = clamp01(social_proof.value());
    }
    return c;
}

void WorldKernel::start() {
    if (started) return;
    started = true;
}

void WorldKernel::step(int num_ticks) {
    if (num_ticks <= 0) return;
    if (!started) start();

    for (int i = 0; i < num_ticks; ++i) {
        int t = clock.t;
        _reset_tick_budgets(t);

        context.begin_phase(t, "INGEST");
        _ingest(t);

        context.begin_phase(t, "ACT");
        _act_batch(t);

        context.begin_phase(t, "PERCEIVE");
        _perceive_batch(t);

        context.begin_phase(t, "CONSOLIDATE");
        _consolidate(t);

        context.clear_tick_buffers(t);
        clock.advance(1);
    }
}

void WorldKernel::_reset_tick_budgets(int /*t*/) {
    double minutes_per_tick = static_cast<double>(clock.seconds_per_tick) / 60.0;
    for (auto& kv : agents.agents) {
        kv.second.reset_time(minutes_per_tick);
        context.set_time_budget(kv.first, minutes_per_tick);
    }
}

void WorldKernel::_ingest(int t) {
    auto new_stimuli = stimulus_engine.tick(t);
    if (!new_stimuli.empty()) {
        context.stimuli_by_tick[t] = new_stimuli;
    }
    if (ingest_fn) ingest_fn(t, context);
}

void WorldKernel::_act_batch(int t) {
    for (auto& kv : agents.agents) {
        Agent& agent = kv.second;
        PlannedAction plan = agent.plan_action(t);
        if (!plan.interaction.has_value()) continue;
        if (!agent.apply_planned_action(plan, &context)) continue;
        const auto& interaction = plan.interaction.value();
        if (interaction.original_content.has_value()) {
            context.posted_by_tick[t].push_back(interaction.original_content.value());
        }
    }
    if (act_fn) act_fn(t, context);
}

void WorldKernel::_perceive_batch(int t) {
    std::vector<AgentId> all_agents;
    all_agents.reserve(agents.agents.size());
    for (const auto& kv : agents.agents) {
        all_agents.push_back(kv.first);
    }

    for (auto& kv : agents.agents) {
        kv.second.clear_feed();
    }

    std::deque<Content> tick_content;
    auto add_content = [&](const Content& content) -> const Content* {
        tick_content.push_back(content);
        return &tick_content.back();
    };

    for (const auto& content : context.posted_by_tick[t]) {
        const Content* ptr = add_content(content);
        const auto& followers = network.graph.get_followers_ref(content.author_id);
        if (!followers.empty()) {
            for (const auto& rid : followers) {
                if (auto* agent = agents.get(rid)) {
                    agent->enqueue_content(ptr, t, t, content.social_proof);
                }
            }
            if (auto* agent = agents.get(content.author_id)) {
                agent->enqueue_content(ptr, t, t, content.social_proof);
            }
        } else {
            for (const auto& rid : all_agents) {
                if (auto* agent = agents.get(rid)) {
                    agent->enqueue_content(ptr, t, t, content.social_proof);
                }
            }
        }
    }

    for (const auto& stim : context.stimuli_by_tick[t]) {
        Content content = stimulus_to_content(stim);
        const Content* ptr = add_content(content);
        const auto& followers = network.graph.get_followers_ref(content.author_id);
        if (!followers.empty()) {
            for (const auto& rid : followers) {
                if (auto* agent = agents.get(rid)) {
                    agent->enqueue_content(ptr, t, t, content.social_proof);
                }
            }
            if (auto* agent = agents.get(content.author_id)) {
                agent->enqueue_content(ptr, t, t, content.social_proof);
            }
        } else {
            for (const auto& rid : all_agents) {
                if (auto* agent = agents.get(rid)) {
                    agent->enqueue_content(ptr, t, t, content.social_proof);
                }
            }
        }
    }

    std::vector<Agent*> agent_list;
    agent_list.reserve(agents.agents.size());
    for (auto& kv : agents.agents) {
        agent_list.push_back(&kv.second);
    }

    std::vector<double> remaining(agent_list.size(), 0.0);
    for (size_t i = 0; i < agent_list.size(); ++i) {
        const AgentId& aid = agent_list[i]->id;
        auto it = context.time_remaining_by_agent.find(aid);
        remaining[i] = (it == context.time_remaining_by_agent.end()) ? 0.0 : it->second;
    }

    size_t workers = enable_parallel ? (parallel_workers ? parallel_workers : std::thread::hardware_concurrency()) : 1;
    if (workers == 0) workers = 1;
    if (workers > agent_list.size()) workers = agent_list.size();

    std::vector<std::vector<std::pair<AgentId, BeliefDelta>>> thread_deltas(workers);

    auto process_range = [&](size_t start, size_t end, std::vector<std::pair<AgentId, BeliefDelta>>& out) {
        for (size_t i = start; i < end; ++i) {
            Agent& agent = *agent_list[i];
            double rem = remaining[i];
            if (rem <= 0.0) continue;
            while (rem > 0.0) {
                auto next = agent.dequeue_next_content();
                if (!next.has_value()) break;
                if (!next->content) break;
                const Content& content = *next->content;

                double trust = 0.5;
                auto tval = network.graph.get_edge_trust(agent.id, content.author_id);
                if (tval.has_value()) trust = tval.value();

                agent.time_remaining = rem;
                auto plan = agent.plan_perception(content, trust, 0.0, true, std::nullopt);
                agent.apply_perception_plan_local(plan, rem, &out);
                agent.time_remaining = rem;
            }
            remaining[i] = rem;
        }
    };

    if (workers <= 1 || agent_list.size() < 2) {
        process_range(0, agent_list.size(), thread_deltas[0]);
    } else {
        std::vector<std::thread> threads;
        threads.reserve(workers);
        size_t chunk = (agent_list.size() + workers - 1) / workers;
        for (size_t w = 0; w < workers; ++w) {
            size_t start = w * chunk;
            size_t end = std::min(agent_list.size(), start + chunk);
            if (start >= end) break;
            threads.emplace_back(process_range, start, end, std::ref(thread_deltas[w]));
        }
        for (auto& th : threads) th.join();
    }

    for (const auto& deltas : thread_deltas) {
        for (const auto& item : deltas) {
            context.deferred_belief_deltas.push_back(item);
        }
    }

    for (size_t i = 0; i < agent_list.size(); ++i) {
        context.time_remaining_by_agent[agent_list[i]->id] = remaining[i];
    }

    if (perceive_fn) perceive_fn(t, context);
}

void WorldKernel::_consolidate(int t) {
    auto deltas = context.pop_all_belief_deltas();
    for (const auto& item : deltas) {
        auto* agent = agents.get(item.first);
        if (!agent) continue;
        agent->apply_belief_delta(item.second);
    }
    if (consolidate_fn) consolidate_fn(t, context);
}
