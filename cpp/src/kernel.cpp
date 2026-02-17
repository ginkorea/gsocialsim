#include "kernel.h"

#include <algorithm>
#include <chrono>
#include <deque>
#include <fstream>
#include <sstream>
#include <mutex>
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

void WorldKernel::analytics_log(int tick, const std::string& type, const std::string& payload) {
    if (!enable_analytics) return;
    std::lock_guard<std::mutex> lock(analytics_mutex);
    if (analytics_mode == AnalyticsMode::Summary) {
        if (analytics_summary.tick != tick) {
            analytics_summary.reset(tick);
        }
        if (type == "impression") {
            analytics_summary.impressions += 1;
            if (payload.find("|consumed=1") != std::string::npos) {
                analytics_summary.consumed += 1;
            }
        } else if (type == "belief_delta") {
            analytics_summary.belief_deltas += 1;
        }
        return;
    }
    std::ostringstream os;
    os << tick << "," << type << "," << payload;
    analytics_buffer.push_back(os.str());
}

void WorldKernel::analytics_flush() {
    if (!enable_analytics) return;
    if (analytics_mode == AnalyticsMode::Summary) {
        AnalyticsSummary snap;
        {
            std::lock_guard<std::mutex> lock(analytics_mutex);
            snap = analytics_summary;
        }
        std::ofstream out(analytics_path, std::ios::app);
        if (!out.is_open()) return;
        out << snap.tick << ",summary"
            << ",impressions=" << snap.impressions
            << "|consumed=" << snap.consumed
            << "|belief_deltas=" << snap.belief_deltas
            << "\n";
        return;
    }
    std::vector<std::string> local;
    {
        std::lock_guard<std::mutex> lock(analytics_mutex);
        if (analytics_buffer.empty()) return;
        local.swap(analytics_buffer);
    }
    std::ofstream out(analytics_path, std::ios::app);
    if (!out.is_open()) return;
    for (const auto& line : local) {
        out << line << "\n";
    }
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
    if (geo.enable_life_cycle && !geo.population_loaded) {
        geo.load_population_csv();
    }
    started = true;
}

void WorldKernel::step(int num_ticks) {
    if (num_ticks <= 0) return;
    if (!started) start();

    for (int i = 0; i < num_ticks; ++i) {
        int t = clock.t;
        auto tick_start = std::chrono::steady_clock::now();
        if (enable_analytics && analytics_mode == AnalyticsMode::Summary) {
            std::lock_guard<std::mutex> lock(analytics_mutex);
            analytics_summary.reset(t);
        }

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
        if (geo.enable_life_cycle) {
            geo.ensure_agent(agent.id, rng);
        }
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

    std::unordered_map<AgentId, const Content*> latest_post_by_author;
    latest_post_by_author.reserve(context.posted_by_tick[t].size());

    for (const auto& content : context.posted_by_tick[t]) {
        const Content* ptr = add_content(content);
        latest_post_by_author[content.author_id] = ptr;
        const auto& followers = network.graph.get_followers_ref(content.author_id);
        if (!followers.empty()) {
            for (const auto& rid : followers) {
                if (auto* agent = agents.get(rid)) {
                    double proximity = geo.enable_life_cycle ? geo.proximity(agent->id, content.author_id) : 0.0;
                    double mutual_raw = 0.0;
                    if (auto mv = network.graph.get_edge_mutual(agent->id, content.author_id)) {
                        mutual_raw = *mv;
                    }
                    double mutual_score = mutual_norm > 0.0 ? clamp01(mutual_raw / mutual_norm) : 0.0;
                    agent->enqueue_content(ptr, t, t, content.social_proof, proximity, mutual_score);
                }
            }
            if (auto* agent = agents.get(content.author_id)) {
                agent->enqueue_content(ptr, t, t, content.social_proof, 1.0, 1.0);
            }
        } else {
            // Unfollowed authors are not broadcast; discovery path handles them.
        }
    }

    for (const auto& stim : context.stimuli_by_tick[t]) {
        Content content = stimulus_to_content(stim);
        const Content* ptr = add_content(content);
        const auto& followers = network.graph.get_followers_ref(content.author_id);
        if (!followers.empty()) {
            for (const auto& rid : followers) {
                if (auto* agent = agents.get(rid)) {
                    double proximity = geo.enable_life_cycle ? geo.proximity(agent->id, content.author_id) : 0.0;
                    double mutual_raw = 0.0;
                    if (auto mv = network.graph.get_edge_mutual(agent->id, content.author_id)) {
                        mutual_raw = *mv;
                    }
                    double mutual_score = mutual_norm > 0.0 ? clamp01(mutual_raw / mutual_norm) : 0.0;
                    agent->enqueue_content(ptr, t, t, content.social_proof, proximity, mutual_score);
                }
            }
            if (auto* agent = agents.get(content.author_id)) {
                agent->enqueue_content(ptr, t, t, content.social_proof, 1.0, 1.0);
            }
        } else {
            // Unfollowed authors are not broadcast; discovery path handles them.
        }
    }

    std::vector<const Content*> discovery_pool;
    if (!tick_content.empty() && discovery_pool_size > 0) {
        discovery_pool.reserve(tick_content.size());
        for (const auto& c : tick_content) {
            discovery_pool.push_back(&c);
        }
        size_t pool = std::min(discovery_pool_size, discovery_pool.size());
        std::partial_sort(
            discovery_pool.begin(),
            discovery_pool.begin() + static_cast<long>(pool),
            discovery_pool.end(),
            [](const Content* a, const Content* b) {
                return a->social_proof > b->social_proof;
            });
        discovery_pool.resize(pool);
    }

    if (geo.enable_life_cycle && offline_contacts_per_tick > 0) {
        std::uniform_real_distribution<double> u01(0.0, 1.0);
        for (auto* agent : agent_ptr_cache) {
            const auto& peers = geo.peers_in_cell(agent->id);
            if (peers.size() <= 1) continue;
            double hour = (static_cast<double>(clock.tick_of_day()) / std::max(1, clock.ticks_per_day)) * 24.0;
            double time_factor = (hour >= 8.0 && hour <= 20.0) ? 1.2 : (hour >= 6.0 && hour < 8.0 ? 0.8 : 0.5);
            int age = agent->identity.age_years;
            double age_factor = (age < 25) ? 1.3 : (age < 40 ? 1.1 : (age < 60 ? 0.9 : 0.6));
            int target = static_cast<int>(std::round(offline_contacts_per_tick * time_factor * age_factor));
            if (target < 1) continue;
            target = std::min<int>(target, 4);
            target = std::min<int>(target, static_cast<int>(peers.size()) - 1);
            int attempts = 0;
            int selected = 0;
            while (selected < target && attempts < target * 5) {
                ++attempts;
                std::uniform_int_distribution<size_t> pick(0, peers.size() - 1);
                const AgentId& other_id = peers[pick(rng)];
                if (other_id == agent->id) continue;
                auto it = latest_post_by_author.find(other_id);
                if (it == latest_post_by_author.end()) continue;

                double proximity = geo.proximity(agent->id, other_id);
                if (proximity <= 0.0) continue;

                int age_a = agent->identity.age_years;
                int age_b = age_a;
                if (auto itb = agents.get(other_id)) {
                    age_b = itb->identity.age_years;
                }
                double age_sim = 1.0 - std::min(1.0, std::abs(age_a - age_b) / 40.0);

                double lean_a = agent->identity.political_lean;
                double lean_b = lean_a;
                if (auto itb = agents.get(other_id)) {
                    lean_b = itb->identity.political_lean;
                }
                double align = 1.0 - std::min(1.0, std::abs(lean_a - lean_b) / 2.0);

                int demo_match = 0;
                if (auto itb = agents.get(other_id)) {
                    if (!agent->identity.sex.empty() && agent->identity.sex == itb->identity.sex) demo_match++;
                    if (!agent->identity.race.empty() && agent->identity.race == itb->identity.race) demo_match++;
                }
                double demo_score = demo_match > 0 ? (demo_match / 2.0) : 0.0;

                double mutual_raw = static_cast<double>(network.graph.mutual_following_count(agent->id, other_id));
                double mutual_score = mutual_norm > 0.0 ? clamp01(mutual_raw / mutual_norm) : 0.0;

                double prob = offline_base_prob * proximity;
                prob *= (1.0 + 0.25 * align + 0.15 * age_sim + 0.15 * demo_score + 0.2 * mutual_score);
                prob = clamp01(prob);
                if (u01(rng) > prob) continue;

                agent->enqueue_content(it->second, t, t, it->second->social_proof, proximity, mutual_score);
                selected++;
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

            if (!discovery_pool.empty() && discovery_max_per_tick > 0) {
                int min_k = std::max(0, discovery_min_per_tick);
                int max_k = std::max(min_k, discovery_max_per_tick);
                std::uniform_int_distribution<int> pick_k(min_k, max_k);
                int target = pick_k(rng);
                if (target > 0) {
                    const auto& following = network.graph.get_following_ref(agent.id);
                    std::uniform_int_distribution<size_t> pick_idx(0, discovery_pool.size() - 1);
                    int attempts = 0;
                    int selected = 0;
                    while (selected < target && attempts < target * 5) {
                        ++attempts;
                        const Content* cand = discovery_pool[pick_idx(rng)];
                        if (!cand) continue;
                        if (cand->author_id == agent.id) continue;
                        if (following.find(cand->author_id) != following.end()) continue;

                        double align = 0.5;
                        if (auto author = agents.get(cand->author_id)) {
                            double diff = std::abs(agent.identity.political_lean - author->identity.political_lean);
                            align = 1.0 - std::min(1.0, diff / 2.0);
                        }
                        double mutual_raw = 0.0;
                        if (auto mv = network.graph.get_edge_mutual(agent.id, cand->author_id)) {
                            mutual_raw = *mv;
                        }
                        double mutual_score = mutual_norm > 0.0 ? clamp01(mutual_raw / mutual_norm) : 0.0;
                        double popularity = clamp01(cand->social_proof);

                        double p = clamp01(0.4 * align + 0.3 * mutual_score + 0.3 * popularity);
                        std::uniform_real_distribution<double> u01(0.0, 1.0);
                        if (u01(rng) > p) continue;

                        double proximity = geo.enable_life_cycle ? 0.2 * geo.proximity(agent.id, cand->author_id) : 0.0;
                        agent.enqueue_content(cand, t, t, cand->social_proof, proximity, mutual_score);
                        selected++;
                    }
                }
            }
            while (rem > 0.0) {
                auto next = agent.dequeue_next_content();
                if (!next.has_value()) break;
                if (!next->content) break;
                const Content& content = *next->content;

                double trust = 0.5;
                auto tval = network.graph.get_edge_trust(agent.id, content.author_id);
                if (tval.has_value()) trust = tval.value();

                agent.time_remaining = rem;
                trust = clamp01(trust + mutual_trust_weight * next->mutual_score);
                auto plan = agent.plan_perception(content, trust, next->proximity, true, std::nullopt);
                agent.apply_perception_plan_local(plan, rem, &out);
                if (enable_analytics && plan.exposed) {
                    std::ostringstream os;
                    os << "viewer=" << agent.id
                       << "|author=" << content.author_id
                       << "|content=" << content.id
                       << "|topic=" << content.topic
                       << "|exposed=1"
                       << "|consumed=" << (plan.consumed_roll ? 1 : 0)
                       << "|proximity=" << next->proximity
                       << "|mutual=" << next->mutual_score;
                    analytics_log(t, "impression", os.str());
                }
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
        if (enable_analytics) {
            std::ostringstream os;
            os << "agent=" << item.first
               << "|topic=" << item.second.topic_id
               << "|stance_delta=" << item.second.stance_delta
               << "|confidence_delta=" << item.second.confidence_delta;
            analytics_log(t, "belief_delta", os.str());
        }
        agent->apply_belief_delta(item.second);
    }
    if (consolidate_fn) consolidate_fn(t, context);

    analytics_flush();
}
