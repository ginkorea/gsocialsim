#include "kernel.h"

#include <algorithm>
#include <chrono>
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

static inline double elapsed_seconds(std::chrono::steady_clock::time_point start,
                                     std::chrono::steady_clock::time_point end) {
    return std::chrono::duration<double>(end - start).count();
}

void WorldKernel::_record_timing(const std::string& name, double seconds) {
    auto& stat = timing[name];
    stat.total += seconds;
    stat.count += 1;
    if (seconds > stat.max) stat.max = seconds;
}

std::vector<std::tuple<std::string, double, size_t, double>> WorldKernel::timing_report() const {
    std::vector<std::tuple<std::string, double, size_t, double>> out;
    out.reserve(timing.size());
    for (const auto& kv : timing) {
        const auto& stat = kv.second;
        out.emplace_back(kv.first, stat.total, stat.count,
                         stat.count ? (stat.total / static_cast<double>(stat.count)) : 0.0);
    }
    std::sort(out.begin(), out.end(), [](const auto& a, const auto& b) {
        return std::get<1>(a) > std::get<1>(b);
    });
    return out;
}

static inline void refresh_agent_cache(WorldKernel& kernel) {
    if (kernel.agent_ptr_cache.size() == kernel.agents.agents.size()) {
        return;
    }
    kernel.agent_ptr_cache.clear();
    kernel.agent_id_cache.clear();
    kernel.agent_ptr_cache.reserve(kernel.agents.agents.size());
    kernel.agent_id_cache.reserve(kernel.agents.agents.size());
    for (auto& kv : kernel.agents.agents) {
        kernel.agent_id_cache.push_back(kv.first);
        kernel.agent_ptr_cache.push_back(&kv.second);
    }
    kernel.remaining_cache.assign(kernel.agent_ptr_cache.size(), 0.0);
}

void WorldKernel::start() {
    if (started) return;
    rng.seed(seed);
    started = true;
}

void WorldKernel::step(int num_ticks) {
    if (num_ticks <= 0) return;
    if (!started) start();

    for (int i = 0; i < num_ticks; ++i) {
        int t = clock.t;
        auto tick_start = std::chrono::steady_clock::now();

        if (enable_timing) {
            auto s = std::chrono::steady_clock::now();
            _reset_tick_budgets(t);
            _record_timing("tick/reset_budgets", elapsed_seconds(s, std::chrono::steady_clock::now()));
        } else {
            _reset_tick_budgets(t);
        }

        context.begin_phase(t, "INGEST");
        if (enable_timing) {
            auto s = std::chrono::steady_clock::now();
            _ingest(t);
            _record_timing("phase/ingest", elapsed_seconds(s, std::chrono::steady_clock::now()));
        } else {
            _ingest(t);
        }

        context.begin_phase(t, "ACT");
        if (enable_timing) {
            auto s = std::chrono::steady_clock::now();
            _act_batch(t);
            _record_timing("phase/act_batch", elapsed_seconds(s, std::chrono::steady_clock::now()));
        } else {
            _act_batch(t);
        }

        context.begin_phase(t, "PERCEIVE");
        if (enable_timing) {
            auto s = std::chrono::steady_clock::now();
            _perceive_batch(t);
            _record_timing("phase/perceive_batch", elapsed_seconds(s, std::chrono::steady_clock::now()));
        } else {
            _perceive_batch(t);
        }

        context.begin_phase(t, "CONSOLIDATE");
        if (enable_timing) {
            auto s = std::chrono::steady_clock::now();
            _consolidate(t);
            _record_timing("phase/consolidate", elapsed_seconds(s, std::chrono::steady_clock::now()));
        } else {
            _consolidate(t);
        }

        context.clear_tick_buffers(t);
        clock.advance(1);

        if (enable_timing) {
            _record_timing("tick", elapsed_seconds(tick_start, std::chrono::steady_clock::now()));
        }
    }
}

void WorldKernel::_reset_tick_budgets(int /*t*/) {
    refresh_agent_cache(*this);
    double minutes_per_tick = static_cast<double>(clock.seconds_per_tick) / 60.0;
    for (size_t i = 0; i < agent_ptr_cache.size(); ++i) {
        Agent& agent = *agent_ptr_cache[i];
        agent.reset_time(minutes_per_tick);
        context.set_time_budget(agent.id, minutes_per_tick);
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
    refresh_agent_cache(*this);
    for (auto* agent_ptr : agent_ptr_cache) {
        Agent& agent = *agent_ptr;
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
    refresh_agent_cache(*this);
    for (auto* agent_ptr : agent_ptr_cache) {
        agent_ptr->clear_feed();
    }

    size_t total_content = context.posted_by_tick[t].size() + context.stimuli_by_tick[t].size();
    std::vector<Content> tick_content;
    tick_content.reserve(total_content);
    auto add_content = [&](const Content& content) -> const Content* {
        tick_content.emplace_back(content);
        return &tick_content.back();
    };

    std::vector<size_t> fallback_indices;
    size_t fallback_count = 0;
    if (max_recipients_per_content > 0 && max_recipients_per_content < agent_ptr_cache.size()) {
        fallback_indices.resize(agent_ptr_cache.size());
        for (size_t i = 0; i < fallback_indices.size(); ++i) fallback_indices[i] = i;
        std::shuffle(fallback_indices.begin(), fallback_indices.end(), rng);
        fallback_count = max_recipients_per_content;
    }

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
        } else if (max_recipients_per_content == 0 || max_recipients_per_content >= agent_ptr_cache.size()) {
            for (auto* agent : agent_ptr_cache) {
                agent->enqueue_content(ptr, t, t, content.social_proof);
            }
        } else {
            if (fallback_count == 0) {
                for (auto* agent : agent_ptr_cache) {
                    agent->enqueue_content(ptr, t, t, content.social_proof);
                }
            } else {
                for (size_t i = 0; i < fallback_count; ++i) {
                    agent_ptr_cache[fallback_indices[i]]->enqueue_content(ptr, t, t, content.social_proof);
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
        } else if (max_recipients_per_content == 0 || max_recipients_per_content >= agent_ptr_cache.size()) {
            for (auto* agent : agent_ptr_cache) {
                agent->enqueue_content(ptr, t, t, content.social_proof);
            }
        } else {
            if (fallback_count == 0) {
                for (auto* agent : agent_ptr_cache) {
                    agent->enqueue_content(ptr, t, t, content.social_proof);
                }
            } else {
                for (size_t i = 0; i < fallback_count; ++i) {
                    agent_ptr_cache[fallback_indices[i]]->enqueue_content(ptr, t, t, content.social_proof);
                }
            }
        }
    }

    for (size_t i = 0; i < agent_ptr_cache.size(); ++i) {
        const AgentId& aid = agent_ptr_cache[i]->id;
        auto it = context.time_remaining_by_agent.find(aid);
        remaining_cache[i] = (it == context.time_remaining_by_agent.end()) ? 0.0 : it->second;
    }

    size_t workers = enable_parallel ? (parallel_workers ? parallel_workers : std::thread::hardware_concurrency()) : 1;
    if (workers == 0) workers = 1;
    if (workers > agent_ptr_cache.size()) workers = agent_ptr_cache.size();

    std::vector<std::vector<std::pair<AgentId, BeliefDelta>>> thread_deltas(workers);

    auto process_range = [&](size_t start, size_t end, std::vector<std::pair<AgentId, BeliefDelta>>& out) {
        for (size_t i = start; i < end; ++i) {
            Agent& agent = *agent_ptr_cache[i];
            double rem = remaining_cache[i];
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
            remaining_cache[i] = rem;
        }
    };

    if (workers <= 1 || agent_ptr_cache.size() < 2) {
        process_range(0, agent_ptr_cache.size(), thread_deltas[0]);
    } else {
        std::vector<std::thread> threads;
        threads.reserve(workers);
        size_t chunk = (agent_ptr_cache.size() + workers - 1) / workers;
        for (size_t w = 0; w < workers; ++w) {
            size_t start = w * chunk;
            size_t end = std::min(agent_ptr_cache.size(), start + chunk);
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

    for (size_t i = 0; i < agent_ptr_cache.size(); ++i) {
        context.time_remaining_by_agent[agent_ptr_cache[i]->id] = remaining_cache[i];
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
