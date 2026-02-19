#include <algorithm>
#include <chrono>
#include <cctype>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_set>
#include <system_error>

#include "data_source.h"
#include "json.hpp"
#include "kernel.h"

using njson = nlohmann::json;

static void usage() {
    std::cout << "Usage: gsocialsim_cpp --stimuli <path> --ticks <n> --agents <n> "
                 "[--timing] [--timing-out <path>] [--timing-top <n>] "
                 "[--parallel-workers <n>] [--no-parallel] [--seed <n>] "
                 "[--avg-following <n>] [--network-mode <groups|random|geo>] "
                 "[--network-groups <n>] [--group-following <n>] [--inter-following <n>] "
                 "[--outlier-frac <f>] [--outlier-hub-frac <f>] [--outlier-hub-following <n>] "
                 "[--print-network-stats] "
                 "[--analytics] [--analytics-out <path>] [--analytics-mode <summary|detailed>] "
                 "[--export-state] [--export-dir <path>] "
                 "[--stream-json] [--config <path>]\n";
}

static bool parse_int(const std::string& v, int& out) {
    try {
        out = std::stoi(v);
        return true;
    } catch (...) {
        return false;
    }
}

static double clamp01(double v) {
    if (v < 0.0) return 0.0;
    if (v > 1.0) return 1.0;
    return v;
}

static double percentile(std::vector<size_t> values, double p) {
    if (values.empty()) return 0.0;
    std::sort(values.begin(), values.end());
    if (values.size() == 1) return static_cast<double>(values[0]);
    double pos = p * (static_cast<double>(values.size() - 1));
    size_t idx = static_cast<size_t>(std::floor(pos));
    size_t idx2 = std::min(values.size() - 1, idx + 1);
    double frac = pos - static_cast<double>(idx);
    double a = static_cast<double>(values[idx]);
    double b = static_cast<double>(values[idx2]);
    return a + (b - a) * frac;
}

static double mean(const std::vector<size_t>& values) {
    if (values.empty()) return 0.0;
    double sum = 0.0;
    for (size_t v : values) sum += static_cast<double>(v);
    return sum / static_cast<double>(values.size());
}

static void print_network_stats_report(
    const WorldKernel& kernel,
    int agents,
    const std::vector<int>* group_of,
    int group_count,
    const std::vector<bool>* is_outlier,
    const std::vector<bool>* is_hub
) {
    if (agents <= 0) return;

    std::vector<size_t> out_deg(static_cast<size_t>(agents));
    std::vector<size_t> in_deg(static_cast<size_t>(agents));
    size_t edges = 0;
    size_t isolates = 0;
    size_t mutual_edges = 0;

    for (int i = 0; i < agents; ++i) {
        AgentId aid = "A" + std::to_string(i);
        const auto& following = kernel.network.graph.get_following_ref(aid);
        const auto& followers = kernel.network.graph.get_followers_ref(aid);
        out_deg[static_cast<size_t>(i)] = following.size();
        in_deg[static_cast<size_t>(i)] = followers.size();
        edges += following.size();
    }

    for (int i = 0; i < agents; ++i) {
        if (out_deg[static_cast<size_t>(i)] == 0 && in_deg[static_cast<size_t>(i)] == 0) {
            isolates += 1;
        }
    }

    for (int i = 0; i < agents; ++i) {
        AgentId follower = "A" + std::to_string(i);
        const auto& following = kernel.network.graph.get_following_ref(follower);
        for (const auto& followed : following) {
            const auto& back = kernel.network.graph.get_following_ref(followed);
            if (back.find(follower) != back.end()) {
                mutual_edges += 1;
            }
        }
    }

    double possible_edges = static_cast<double>(agents) * static_cast<double>(agents - 1);
    double density = possible_edges > 0 ? static_cast<double>(edges) / possible_edges : 0.0;
    double reciprocity = edges > 0 ? static_cast<double>(mutual_edges) / static_cast<double>(edges) : 0.0;

    std::cout << "\nNETWORK STATS\n";
    std::cout << "agents=" << agents << " edges=" << edges << " density=" << density << "\n";
    std::cout << "isolates=" << isolates << " reciprocity=" << reciprocity << "\n";

    std::cout << "out_degree: mean=" << mean(out_deg)
              << " median=" << percentile(out_deg, 0.5)
              << " p90=" << percentile(out_deg, 0.9)
              << " max=" << percentile(out_deg, 1.0) << "\n";
    std::cout << "in_degree:  mean=" << mean(in_deg)
              << " median=" << percentile(in_deg, 0.5)
              << " p90=" << percentile(in_deg, 0.9)
              << " max=" << percentile(in_deg, 1.0) << "\n";

    std::vector<std::pair<size_t, int>> top_out;
    std::vector<std::pair<size_t, int>> top_in;
    top_out.reserve(static_cast<size_t>(agents));
    top_in.reserve(static_cast<size_t>(agents));
    for (int i = 0; i < agents; ++i) {
        top_out.emplace_back(out_deg[static_cast<size_t>(i)], i);
        top_in.emplace_back(in_deg[static_cast<size_t>(i)], i);
    }
    auto by_deg = [](const auto& a, const auto& b) { return a.first > b.first; };
    std::sort(top_out.begin(), top_out.end(), by_deg);
    std::sort(top_in.begin(), top_in.end(), by_deg);

    std::cout << "top_out_degree:";
    for (size_t i = 0; i < std::min<size_t>(5, top_out.size()); ++i) {
        std::cout << " A" << top_out[i].second << "(" << top_out[i].first << ")";
    }
    std::cout << "\n";
    std::cout << "top_in_degree:";
    for (size_t i = 0; i < std::min<size_t>(5, top_in.size()); ++i) {
        std::cout << " A" << top_in[i].second << "(" << top_in[i].first << ")";
    }
    std::cout << "\n";

    if (group_of && group_of->size() == static_cast<size_t>(agents) && group_count > 0) {
        size_t intra = 0;
        size_t inter = 0;
        std::vector<size_t> group_sizes(static_cast<size_t>(group_count), 0);
        for (int i = 0; i < agents; ++i) {
            int g = (*group_of)[static_cast<size_t>(i)];
            if (g >= 0 && g < group_count) {
                group_sizes[static_cast<size_t>(g)] += 1;
            }
        }
        for (int i = 0; i < agents; ++i) {
            AgentId follower = "A" + std::to_string(i);
            const auto& following = kernel.network.graph.get_following_ref(follower);
            for (const auto& followed : following) {
                int j = 0;
                if (followed.size() > 1 && followed[0] == 'A') {
                    try {
                        j = std::stoi(followed.substr(1));
                    } catch (...) {
                        continue;
                    }
                } else {
                    continue;
                }
                if (j < 0 || j >= agents) continue;
                if ((*group_of)[static_cast<size_t>(i)] == (*group_of)[static_cast<size_t>(j)]) {
                    intra += 1;
                } else {
                    inter += 1;
                }
            }
        }
        double inter_ratio = (edges > 0) ? static_cast<double>(inter) / static_cast<double>(edges) : 0.0;
        std::cout << "groups=" << group_count << " inter_edge_ratio=" << inter_ratio << "\n";
        std::cout << "group_sizes:";
        for (size_t g = 0; g < group_sizes.size(); ++g) {
            std::cout << " g" << g << "=" << group_sizes[g];
        }
        std::cout << "\n";
    }

    if (is_outlier && is_outlier->size() == static_cast<size_t>(agents)) {
        size_t outlier_count = 0;
        size_t hub_count = 0;
        size_t outlier_edges = 0;
        for (int i = 0; i < agents; ++i) {
            if ((*is_outlier)[static_cast<size_t>(i)]) {
                outlier_count += 1;
                outlier_edges += out_deg[static_cast<size_t>(i)];
            }
            if (is_hub && i < static_cast<int>(is_hub->size()) && (*is_hub)[static_cast<size_t>(i)]) {
                hub_count += 1;
            }
        }
        std::cout << "outliers=" << outlier_count;
        if (hub_count > 0) {
            std::cout << " hubs=" << hub_count;
        }
        std::cout << " outlier_edges=" << outlier_edges << "\n";
    }
}

static void ensure_dir(const std::string& path) {
    if (path.empty()) return;
    std::error_code ec;
    std::filesystem::create_directories(path, ec);
}

static void ensure_parent_dir(const std::string& path) {
    if (path.empty()) return;
    std::filesystem::path p(path);
    auto parent = p.parent_path();
    if (parent.empty()) return;
    std::error_code ec;
    std::filesystem::create_directories(parent, ec);
}

static std::string json_escape(const std::string& s) {
    std::string out;
    out.reserve(s.size());
    for (char c : s) {
        switch (c) {
            case '\\': out += "\\\\"; break;
            case '"': out += "\\\""; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default:
                if (static_cast<unsigned char>(c) < 0x20) {
                    out += " ";
                } else {
                    out += c;
                }
                break;
        }
    }
    return out;
}

static void load_config(const std::string& path, WorldKernel& kernel) {
    std::ifstream f(path);
    if (!f.is_open()) {
        std::cerr << "warn: could not open config file: " << path << "\n";
        return;
    }
    njson cfg;
    try {
        cfg = njson::parse(f);
    } catch (const std::exception& e) {
        std::cerr << "warn: failed to parse config JSON: " << e.what() << "\n";
        return;
    }

    // Influence dynamics → apply to all agents
    if (cfg.contains("influence_dynamics")) {
        auto& id = cfg["influence_dynamics"];
        for (auto& [_, agent] : kernel.agents.agents) {
            auto& c = agent.belief_engine.config;
            if (id.contains("inertia_rho")) c.inertia_rho = id["inertia_rho"].get<double>();
            if (id.contains("learning_rate_base")) c.learning_rate_base = id["learning_rate_base"].get<double>();
            if (id.contains("rebound_k")) c.rebound_k = id["rebound_k"].get<double>();
            if (id.contains("critical_velocity_threshold")) c.critical_velocity_threshold = id["critical_velocity_threshold"].get<double>();
            if (id.contains("critical_kappa")) c.critical_kappa = id["critical_kappa"].get<double>();
            if (id.contains("evidence_decay_lambda")) c.evidence_decay_lambda = id["evidence_decay_lambda"].get<double>();
            if (id.contains("evidence_threshold")) c.evidence_threshold = id["evidence_threshold"].get<double>();
            if (id.contains("trust_exponent_gamma")) c.trust_exponent_gamma = id["trust_exponent_gamma"].get<double>();
            if (id.contains("habituation_alpha")) c.habituation_alpha = id["habituation_alpha"].get<double>();
            if (id.contains("bounded_confidence_tau")) c.bounded_confidence_tau = id["bounded_confidence_tau"].get<double>();
        }
    }

    // Kernel params
    if (cfg.contains("kernel")) {
        auto& k = cfg["kernel"];
        if (k.contains("mutual_trust_weight")) kernel.mutual_trust_weight = k["mutual_trust_weight"].get<double>();
        if (k.contains("offline_contacts_per_tick")) kernel.offline_contacts_per_tick = k["offline_contacts_per_tick"].get<int>();
        if (k.contains("offline_base_prob")) kernel.offline_base_prob = k["offline_base_prob"].get<double>();
        if (k.contains("discovery_min_per_tick")) kernel.discovery_min_per_tick = k["discovery_min_per_tick"].get<int>();
        if (k.contains("discovery_max_per_tick")) kernel.discovery_max_per_tick = k["discovery_max_per_tick"].get<int>();
        if (k.contains("discovery_pool_size")) kernel.discovery_pool_size = k["discovery_pool_size"].get<size_t>();
    }

    // Feed queue params → apply to all agents
    if (cfg.contains("feed_queue")) {
        auto& fq = cfg["feed_queue"];
        double rw = fq.value("recency_weight", 0.4);
        double ew = fq.value("engagement_weight", 0.45);
        double pw = fq.value("proximity_weight", 0.1);
        double mw = fq.value("mutual_weight", 0.05);
        for (auto& [_, agent] : kernel.agents.agents) {
            agent.feed_queue = FeedPriorityQueue(rw, ew, pw, mw);
        }
    }

    // Broadcast feed network params
    if (cfg.contains("broadcast_feed") && kernel.network_manager) {
        auto* layer = kernel.network_manager->get_layer("broadcast_feed");
        if (layer) {
            auto* bf = dynamic_cast<BroadcastFeedNetwork*>(layer);
            if (bf) {
                auto& b = cfg["broadcast_feed"];
                if (b.contains("candidate_window_ticks")) bf->candidate_window_ticks = b["candidate_window_ticks"].get<int>();
                if (b.contains("max_candidates")) bf->max_candidates = b["max_candidates"].get<size_t>();
                if (b.contains("max_shown")) bf->max_shown = b["max_shown"].get<size_t>();
            }
        }
    }

    std::cout << "loaded config from " << path << "\n";
}

static void export_state_json(const WorldKernel& kernel, const std::string& dir) {
    if (dir.empty()) return;
    ensure_dir(dir);
    std::filesystem::path out_path = std::filesystem::path(dir) / "state.json";
    std::ofstream out(out_path);
    if (!out.is_open()) return;

    out << std::fixed << std::setprecision(4);
    out << "{\n";

    // Agents — enriched with demographics, beliefs, personality, psychographics
    out << "  \"agents\": [\n";
    bool first_agent = true;
    for (const auto& kv : kernel.agents.agents) {
        if (!first_agent) out << ",\n";
        first_agent = false;
        const auto& agent = kv.second;
        const auto& d = agent.demographics;
        const auto& p = agent.psychographics;

        out << "    {\"id\":\"" << json_escape(kv.first)
            << "\",\"political_lean\":" << agent.identity.political_lean
            << ",\"partisanship\":" << agent.identity.partisanship;

        // Demographics
        out << ",\"demographics\":{"
            << "\"age\":" << d.age
            << ",\"age_cohort\":\"" << json_escape(d.age_cohort) << "\""
            << ",\"race_ethnicity\":\"" << json_escape(d.race_ethnicity) << "\""
            << ",\"gender\":\"" << json_escape(d.gender) << "\""
            << ",\"geography_type\":\"" << json_escape(d.geography_type) << "\""
            << ",\"education_level\":\"" << json_escape(d.education_level) << "\""
            << ",\"income_bracket\":\"" << json_escape(d.income_bracket) << "\""
            << ",\"religion\":\"" << json_escape(d.religion) << "\""
            << ",\"religiosity\":" << d.religiosity
            << ",\"political_ideology\":" << d.political_ideology
            << ",\"political_label\":\"" << json_escape(d.political_label) << "\""
            << "}";

        // Big 5 personality
        out << ",\"personality\":{"
            << "\"openness\":" << p.openness
            << ",\"conscientiousness\":" << p.conscientiousness
            << ",\"extraversion\":" << p.extraversion
            << ",\"agreeableness\":" << p.agreeableness
            << ",\"neuroticism\":" << p.neuroticism
            << "}";

        // Psychographic scores
        out << ",\"psychographics\":{"
            << "\"susceptibility\":" << p.susceptibility
            << ",\"identity_rigidity\":" << p.identity_rigidity
            << ",\"bounded_confidence_tau\":" << p.bounded_confidence_tau
            << ",\"trust_in_sources_base\":" << p.trust_in_sources_base
            << ",\"engagement_propensity\":" << p.engagement_propensity
            << ",\"outrage_susceptibility\":" << p.outrage_susceptibility
            << "}";

        // Belief stances (all topics)
        out << ",\"beliefs\":{";
        bool first_belief = true;
        for (const auto& bkv : agent.beliefs) {
            if (!first_belief) out << ",";
            first_belief = false;
            out << "\"" << json_escape(bkv.first) << "\":{"
                << "\"stance\":" << bkv.second.stance
                << ",\"confidence\":" << bkv.second.confidence
                << ",\"salience\":" << bkv.second.salience
                << ",\"momentum\":" << bkv.second.momentum
                << "}";
        }
        out << "}";

        out << "}";
    }
    if (!first_agent) out << "\n";
    out << "  ],\n";

    // Metrics section — aggregate stats
    {
        double lean_sum = 0.0;
        double lean_sq_sum = 0.0;
        int agent_count = 0;
        size_t total_edges = 0;
        size_t mutual_count = 0;

        for (const auto& kv : kernel.agents.agents) {
            double lean = kv.second.identity.political_lean;
            lean_sum += lean;
            lean_sq_sum += lean * lean;
            agent_count++;
            total_edges += kernel.network.graph.get_following_ref(kv.first).size();
        }

        double lean_mean = (agent_count > 0) ? lean_sum / agent_count : 0.0;
        double lean_var = (agent_count > 0) ? (lean_sq_sum / agent_count) - (lean_mean * lean_mean) : 0.0;
        double possible = static_cast<double>(agent_count) * static_cast<double>(agent_count - 1);
        double density = (possible > 0) ? static_cast<double>(total_edges) / possible : 0.0;

        for (const auto& kv : kernel.agents.agents) {
            const auto& following = kernel.network.graph.get_following_ref(kv.first);
            for (const auto& followed : following) {
                const auto& back = kernel.network.graph.get_following_ref(followed);
                if (back.find(kv.first) != back.end()) {
                    mutual_count++;
                }
            }
        }
        double reciprocity = (total_edges > 0) ? static_cast<double>(mutual_count) / static_cast<double>(total_edges) : 0.0;

        out << "  \"metrics\": {"
            << "\"agent_count\":" << agent_count
            << ",\"total_edges\":" << total_edges
            << ",\"lean_mean\":" << lean_mean
            << ",\"lean_variance\":" << lean_var
            << ",\"network_density\":" << density
            << ",\"network_reciprocity\":" << reciprocity
            << ",\"total_impressions\":" << kernel.analytics_summary.impressions
            << ",\"total_consumed\":" << kernel.analytics_summary.consumed
            << ",\"total_belief_deltas\":" << kernel.analytics_summary.belief_deltas
            << "},\n";
    }

    // Following edges
    out << "  \"following\": [\n";
    bool first_edge = true;
    for (const auto& kv : kernel.agents.agents) {
        const auto& follower = kv.first;
        const auto& following = kernel.network.graph.get_following_ref(follower);
        for (const auto& followed : following) {
            if (!first_edge) out << ",\n";
            first_edge = false;
            out << "    {\"follower\":\"" << json_escape(follower)
                << "\",\"followed\":\"" << json_escape(followed) << "\"}";
        }
    }
    if (!first_edge) out << "\n";
    out << "  ],\n";

    // Stimuli
    out << "  \"stimuli\": [\n";
    bool first_stim = true;
    for (const auto& kv : kernel.stimulus_engine.stimuli_store()) {
        const auto& s = kv.second;
        if (!first_stim) out << ",\n";
        first_stim = false;
        out << "    {\"id\":\"" << json_escape(s.id)
            << "\",\"source\":\"" << json_escape(s.source)
            << "\",\"tick\":" << s.tick
            << ",\"content_text\":\"" << json_escape(s.content_text) << "\"";
        if (s.topic_hint.has_value()) {
            out << ",\"topic\":\"" << json_escape(s.topic_hint.value()) << "\"";
        }
        out << "}";
    }
    if (!first_stim) out << "\n";
    out << "  ]\n";

    out << "}\n";
}

static void assign_demographics(Agent& agent, std::mt19937& rng) {
    std::normal_distribution<double> age_dist(35.0, 18.0);
    int age = static_cast<int>(std::round(age_dist(rng)));
    if (age < 18) age = 18;
    if (age > 80) age = 80;
    agent.identity.age_years = age;

    std::uniform_real_distribution<double> u01(0.0, 1.0);
    double r = u01(rng);
    agent.identity.sex = (r < 0.5) ? "female" : "male";

    double rr = u01(rng);
    if (rr < 0.60) agent.identity.race = "white";
    else if (rr < 0.73) agent.identity.race = "black";
    else if (rr < 0.91) agent.identity.race = "latino";
    else if (rr < 0.97) agent.identity.race = "asian";
    else agent.identity.race = "other";

    std::uniform_real_distribution<double> lean_dist(-1.0, 1.0);
    agent.identity.political_lean = lean_dist(rng);
    agent.identity.partisanship = clamp01(u01(rng));

    agent.identity.demographics["age"] = std::to_string(agent.identity.age_years);
    agent.identity.demographics["sex"] = agent.identity.sex;
    agent.identity.demographics["race"] = agent.identity.race;
}

int main(int argc, char** argv) {
    std::string stimuli_path;
    std::string timing_out;
    int ticks = 3;
    int agents = 10;
    int timing_top = 20;
    int parallel_workers = 0;
    bool enable_timing = false;
    bool enable_parallel = true;
    int seed = 123;
    int avg_following = 12;
    std::string network_mode = "groups";
    int network_groups = 0;
    int group_following = -1;
    int inter_following = -1;
    double outlier_frac = 0.05;
    double outlier_hub_frac = 0.5;
    int outlier_hub_following = -1;
    bool enable_analytics = false;
    std::string analytics_path = "reports/analytics.csv";
    WorldKernel::AnalyticsMode analytics_mode = WorldKernel::AnalyticsMode::Summary;
    bool export_state = false;
    std::string export_dir = "reports";
    bool print_network_stats = false;
    bool stream_json = false;
    std::string config_path;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--stimuli" && i + 1 < argc) {
            stimuli_path = argv[++i];
        } else if (arg == "--ticks" && i + 1 < argc) {
            parse_int(argv[++i], ticks);
        } else if (arg == "--agents" && i + 1 < argc) {
            parse_int(argv[++i], agents);
        } else if (arg == "--timing") {
            enable_timing = true;
        } else if (arg == "--timing-out" && i + 1 < argc) {
            timing_out = argv[++i];
        } else if (arg == "--timing-top" && i + 1 < argc) {
            parse_int(argv[++i], timing_top);
        } else if (arg == "--parallel-workers" && i + 1 < argc) {
            parse_int(argv[++i], parallel_workers);
        } else if (arg == "--no-parallel") {
            enable_parallel = false;
        } else if (arg == "--seed" && i + 1 < argc) {
            parse_int(argv[++i], seed);
        } else if (arg == "--avg-following" && i + 1 < argc) {
            parse_int(argv[++i], avg_following);
        } else if (arg == "--network-mode" && i + 1 < argc) {
            network_mode = argv[++i];
        } else if (arg == "--network-groups" && i + 1 < argc) {
            parse_int(argv[++i], network_groups);
        } else if (arg == "--group-following" && i + 1 < argc) {
            parse_int(argv[++i], group_following);
        } else if (arg == "--inter-following" && i + 1 < argc) {
            parse_int(argv[++i], inter_following);
        } else if (arg == "--outlier-frac" && i + 1 < argc) {
            try {
                outlier_frac = std::stod(argv[++i]);
            } catch (...) {
                outlier_frac = 0.05;
            }
        } else if (arg == "--outlier-hub-frac" && i + 1 < argc) {
            try {
                outlier_hub_frac = std::stod(argv[++i]);
            } catch (...) {
                outlier_hub_frac = 0.5;
            }
        } else if (arg == "--outlier-hub-following" && i + 1 < argc) {
            parse_int(argv[++i], outlier_hub_following);
        } else if (arg == "--print-network-stats") {
            print_network_stats = true;
        } else if (arg == "--analytics") {
            enable_analytics = true;
        } else if (arg == "--analytics-out" && i + 1 < argc) {
            analytics_path = argv[++i];
        } else if (arg == "--analytics-mode" && i + 1 < argc) {
            std::string mode = argv[++i];
            if (mode == "summary") {
                analytics_mode = WorldKernel::AnalyticsMode::Summary;
            } else if (mode == "detailed") {
                analytics_mode = WorldKernel::AnalyticsMode::Detailed;
            } else {
                std::cerr << "Unknown analytics mode: " << mode << "\n";
                usage();
                return 1;
            }
        } else if (arg == "--export-state") {
            export_state = true;
        } else if (arg == "--export-dir" && i + 1 < argc) {
            export_dir = argv[++i];
        } else if (arg == "--stream-json") {
            stream_json = true;
        } else if (arg == "--config" && i + 1 < argc) {
            config_path = argv[++i];
        } else if (arg == "--help" || arg == "-h") {
            usage();
            return 0;
        }
    }

    auto setup_start = std::chrono::steady_clock::now();
    WorldKernel kernel;
    kernel.enable_timing = enable_timing;
    kernel.enable_parallel = enable_parallel;
    if (parallel_workers > 0) {
        kernel.parallel_workers = static_cast<size_t>(parallel_workers);
    }
    kernel.seed = static_cast<uint32_t>(seed);
    kernel.rng.seed(kernel.seed);
    kernel.enable_analytics = enable_analytics;
    kernel.analytics_path = analytics_path;
    kernel.analytics_mode = analytics_mode;
    if (enable_analytics) {
        ensure_parent_dir(analytics_path);
        std::ofstream touch(analytics_path, std::ios::app);
    }
    if (!timing_out.empty()) {
        ensure_parent_dir(timing_out);
    }
    if (export_state) {
        ensure_dir(export_dir);
    }
    if (!stimuli_path.empty()) {
        kernel.stimulus_engine.register_data_source(std::make_shared<CsvDataSource>(stimuli_path));
    }

    for (int i = 0; i < agents; ++i) {
        Agent a("A" + std::to_string(i), static_cast<uint32_t>(i + 1));
        assign_demographics(a, kernel.rng);
        kernel.agents.add_agent(a);
    }

    std::vector<int> group_of;
    std::vector<bool> is_outlier;
    std::vector<bool> is_hub;
    int group_count = 0;

    if (avg_following > 0 && agents > 1) {
        int effective_avg = std::min(avg_following, agents - 1);
        kernel.mutual_norm = static_cast<double>(std::max(1, effective_avg));

        std::string mode = network_mode;
        for (auto& c : mode) c = static_cast<char>(std::tolower(c));
        bool use_geo = (mode == "geo");
        bool use_random = (mode == "random");

        if (use_geo && !(kernel.geo.enable_life_cycle && kernel.geo.population_loaded)) {
            std::cerr << "warn: geo network requested but population not loaded; falling back to groups\n";
            use_geo = false;
        }

        if (use_geo) {
            int k = effective_avg;
            std::vector<std::vector<int>> by_cell;
            std::vector<std::vector<int>> by_country;
            std::unordered_map<std::string, int> cell_index;
            std::unordered_map<std::string, int> country_index;

            for (int i = 0; i < agents; ++i) {
                AgentId aid = "A" + std::to_string(i);
                kernel.geo.ensure_agent(aid, kernel.rng);
                const auto& loc = kernel.geo.agent_home[aid];
                if (!loc.cell_id.empty()) {
                    auto it = cell_index.find(loc.cell_id);
                    if (it == cell_index.end()) {
                        int idx = static_cast<int>(by_cell.size());
                        cell_index[loc.cell_id] = idx;
                        by_cell.push_back({});
                        it = cell_index.find(loc.cell_id);
                    }
                    by_cell[it->second].push_back(i);
                }
                if (!loc.country.empty()) {
                    auto it = country_index.find(loc.country);
                    if (it == country_index.end()) {
                        int idx = static_cast<int>(by_country.size());
                        country_index[loc.country] = idx;
                        by_country.push_back({});
                        it = country_index.find(loc.country);
                    }
                    by_country[it->second].push_back(i);
                }
            }

            std::uniform_int_distribution<int> pick_global(0, agents - 1);
            for (int i = 0; i < agents; ++i) {
                AgentId follower = "A" + std::to_string(i);
                std::unordered_set<int> chosen;
                chosen.reserve(static_cast<size_t>(k));

                int k_local = static_cast<int>(std::round(k * 0.6));
                int k_country = static_cast<int>(std::round(k * 0.3));
                int k_global = k - k_local - k_country;

                auto add_from_bucket = [&](const std::vector<int>& bucket, int target) {
                    if (bucket.empty()) return;
                    std::uniform_int_distribution<int> pick(0, static_cast<int>(bucket.size()) - 1);
                    int attempts = 0;
                    int max_attempts = target * 6 + 10;
                    while (static_cast<int>(chosen.size()) < k && target > 0 && attempts < max_attempts) {
                        int candidate = bucket[pick(kernel.rng)];
                        if (candidate != i) {
                            if (chosen.insert(candidate).second) {
                                --target;
                            }
                        }
                        ++attempts;
                    }
                };

                const auto& loc = kernel.geo.agent_home[follower];
                if (!by_cell.empty()) {
                    auto it = cell_index.find(loc.cell_id);
                    if (it != cell_index.end()) {
                        add_from_bucket(by_cell[it->second], k_local);
                    }
                }
                if (!by_country.empty()) {
                    auto itc = country_index.find(loc.country);
                    if (itc != country_index.end()) {
                        add_from_bucket(by_country[itc->second], k_country);
                    }
                }

                while (static_cast<int>(chosen.size()) < k && k_global > 0) {
                    int candidate = pick_global(kernel.rng);
                    if (candidate == i) continue;
                    chosen.insert(candidate);
                    --k_global;
                }

                for (int j : chosen) {
                    AgentId followed = "A" + std::to_string(j);
                    kernel.network.graph.add_edge(follower, followed, 0.5);
                }
            }
        } else if (use_random) {
            int k = effective_avg;
            std::uniform_int_distribution<int> pick_global(0, agents - 1);
            for (int i = 0; i < agents; ++i) {
                AgentId follower = "A" + std::to_string(i);
                std::unordered_set<int> chosen;
                chosen.reserve(static_cast<size_t>(k));
                int attempts = 0;
                int max_attempts = k * 6 + 10;
                while (static_cast<int>(chosen.size()) < k && attempts < max_attempts) {
                    int candidate = pick_global(kernel.rng);
                    if (candidate == i) {
                        ++attempts;
                        continue;
                    }
                    chosen.insert(candidate);
                    ++attempts;
                }
                for (int j : chosen) {
                    AgentId followed = "A" + std::to_string(j);
                    kernel.network.graph.add_edge(follower, followed, 0.5);
                }
            }
        } else {
            int base_avg = std::max(1, effective_avg);
            int derived_group_following = std::max(1, static_cast<int>(std::round(base_avg * 0.8)));
            int derived_inter_following = std::max(0, base_avg - derived_group_following);
            int gf = (group_following >= 0) ? group_following : derived_group_following;
            int inf = (inter_following >= 0) ? inter_following : derived_inter_following;

            group_count = network_groups;
            if (group_count <= 0) {
                group_count = std::max(3, std::min(12, agents / 50));
            }
            group_count = std::max(1, std::min(group_count, agents));

            int hub_following = outlier_hub_following;
            if (hub_following < 0) {
                hub_following = std::min(agents - 1, std::max(base_avg * 4, base_avg + 10));
            }

            double ofrac = std::max(0.0, std::min(0.5, outlier_frac));
            double hfrac = std::max(0.0, std::min(1.0, outlier_hub_frac));

            std::vector<int> indices(agents);
            std::iota(indices.begin(), indices.end(), 0);
            std::shuffle(indices.begin(), indices.end(), kernel.rng);

            group_of.assign(agents, 0);
            std::vector<std::vector<int>> groups(group_count);
            for (int gi = 0; gi < agents; ++gi) {
                int agent_idx = indices[gi];
                int g = gi % group_count;
                group_of[agent_idx] = g;
                groups[g].push_back(agent_idx);
            }

            int outlier_count = static_cast<int>(std::round(ofrac * agents));
            outlier_count = std::min(outlier_count, agents);
            int hub_count = static_cast<int>(std::round(outlier_count * hfrac));
            hub_count = std::min(hub_count, outlier_count);

            is_outlier.assign(agents, false);
            is_hub.assign(agents, false);
            for (int i = 0; i < outlier_count; ++i) {
                int agent_idx = indices[i];
                is_outlier[agent_idx] = true;
                if (i < hub_count) {
                    is_hub[agent_idx] = true;
                }
            }

            std::uniform_int_distribution<int> pick_global(0, agents - 1);
            for (int i = 0; i < agents; ++i) {
                AgentId follower = "A" + std::to_string(i);
                std::unordered_set<int> chosen;
                int target_total = 0;
                if (is_outlier[i]) {
                    if (!is_hub[i]) {
                        target_total = 0;
                    } else {
                        target_total = std::min(agents - 1, hub_following);
                    }
                } else {
                    target_total = std::min(agents - 1, gf + inf);
                }
                if (target_total <= 0) continue;
                chosen.reserve(static_cast<size_t>(target_total));

                auto add_from_bucket = [&](const std::vector<int>& bucket, int target) {
                    if (bucket.empty() || target <= 0) return;
                    std::uniform_int_distribution<int> pick(0, static_cast<int>(bucket.size()) - 1);
                    int attempts = 0;
                    int max_attempts = target * 8 + 10;
                    while (target > 0 && attempts < max_attempts) {
                        int candidate = bucket[pick(kernel.rng)];
                        if (candidate != i) {
                            if (chosen.insert(candidate).second) {
                                --target;
                            }
                        }
                        ++attempts;
                    }
                };

                if (!is_outlier[i]) {
                    add_from_bucket(groups[group_of[i]], gf);
                    int remaining_inter = inf;
                    int attempts = 0;
                    int max_attempts = remaining_inter * 8 + 10;
                    while (remaining_inter > 0 && attempts < max_attempts) {
                        int candidate = pick_global(kernel.rng);
                        if (candidate == i) {
                            ++attempts;
                            continue;
                        }
                        if (group_of[candidate] == group_of[i]) {
                            ++attempts;
                            continue;
                        }
                        if (chosen.insert(candidate).second) {
                            --remaining_inter;
                        }
                        ++attempts;
                    }
                } else if (is_hub[i]) {
                    int remaining = target_total;
                    int attempts = 0;
                    int max_attempts = remaining * 8 + 10;
                    while (remaining > 0 && attempts < max_attempts) {
                        int candidate = pick_global(kernel.rng);
                        if (candidate == i) {
                            ++attempts;
                            continue;
                        }
                        if (chosen.insert(candidate).second) {
                            --remaining;
                        }
                        ++attempts;
                    }
                }

                for (int j : chosen) {
                    AgentId followed = "A" + std::to_string(j);
                    kernel.network.graph.add_edge(follower, followed, 0.5);
                }
            }
        }
        kernel.network.graph.compute_edge_mutual();
        if (print_network_stats) {
            const std::vector<int>* group_ptr = group_of.empty() ? nullptr : &group_of;
            const std::vector<bool>* outlier_ptr = is_outlier.empty() ? nullptr : &is_outlier;
            const std::vector<bool>* hub_ptr = is_hub.empty() ? nullptr : &is_hub;
            print_network_stats_report(kernel, agents, group_ptr, group_count, outlier_ptr, hub_ptr);
        }
    }

    if (!kernel.geo.population_csv_path.empty()) {
        kernel.geo.load_population_csv();
    }

    // Initialize network manager with multiple layers
    std::cout << "Initializing network manager...\n";
    auto network_mgr = std::make_unique<NetworkManager>();

    // Create broadcast feed network (main social feed)
    auto broadcast_feed = std::make_unique<BroadcastFeedNetwork>("broadcast_feed");
    // Share the graph from kernel.network for backward compatibility
    broadcast_feed->graph = kernel.network.graph;
    network_mgr->register_layer(std::move(broadcast_feed));

    // Create direct message network
    auto direct_msg = std::make_unique<DirectMessageNetwork>("direct_message");
    network_mgr->register_layer(std::move(direct_msg));

    kernel.network_manager = network_mgr.release();
    std::cout << "Registered 2 network layers: broadcast_feed, direct_message\n";

    // Initialize population layer if geo is enabled
    if (kernel.geo.enable_life_cycle && kernel.geo.population_loaded) {
        std::cout << "Initializing population layer...\n";
        kernel.context.population.initialize_from_geo(kernel.geo);
        kernel.context.population.initialize_default_segments();
        std::cout << "Population layer: " << kernel.context.population.num_cells() << " cells, "
                  << kernel.context.population.num_segments() << " segments, "
                  << kernel.context.population.total_population() << " total population\n";
    }

    // Initialize subscriptions: auto-subscribe all agents to creators they follow
    // This maintains backward compatibility with the old broadcast model
    std::cout << "Initializing subscriptions...\n";
    size_t subscription_count = 0;
    for (const auto& [agent_id, agent] : kernel.agents.agents) {
        const auto& following = kernel.network.graph.get_following_ref(agent_id);
        for (const auto& followed_id : following) {
            // Subscribe to creator with strength 1.0
            kernel.context.subscriptions.subscribe(agent_id, SubscriptionType::CREATOR, followed_id, 1.0, 0);
            subscription_count++;
        }
    }
    std::cout << "Created " << subscription_count << " creator subscriptions\n";

    // Load JSON config overrides (after agents created, before start)
    if (!config_path.empty()) {
        load_config(config_path, kernel);
    }

    // When streaming JSON, force analytics summary mode so counters are populated
    if (stream_json) {
        kernel.enable_analytics = true;
        kernel.analytics_mode = WorldKernel::AnalyticsMode::Summary;
    }

    kernel.start();
    auto setup_end = std::chrono::steady_clock::now();
    double setup_elapsed = std::chrono::duration<double>(setup_end - setup_start).count();

    const int log_every = std::max(1, ticks / 10);
    auto sim_start = std::chrono::steady_clock::now();
    for (int t = 0; t < ticks; ++t) {
        kernel.step(1);
        if (stream_json) {
            std::cout << "{\"tick\":" << (t + 1)
                      << ",\"total\":" << ticks
                      << ",\"impressions\":" << kernel.analytics_summary.impressions
                      << ",\"consumed\":" << kernel.analytics_summary.consumed
                      << ",\"belief_deltas\":" << kernel.analytics_summary.belief_deltas;
            // Agent political lean snapshot
            std::cout << ",\"leans\":[";
            bool first = true;
            for (const auto& [id, agent] : kernel.agents.agents) {
                if (!first) std::cout << ",";
                first = false;
                std::cout << std::fixed << std::setprecision(3) << agent.identity.political_lean;
            }
            std::cout << "]}" << std::endl;
        } else if ((t + 1) % log_every == 0 || t == 0) {
            std::cout << "tick " << (t + 1) << "/" << ticks << "\n";
        }
    }
    auto end = std::chrono::steady_clock::now();
    double sim_elapsed = std::chrono::duration<double>(end - sim_start).count();
    double total_elapsed = std::chrono::duration<double>(end - setup_start).count();

    std::cout << "setup time: " << setup_elapsed << "s\n";
    std::cout << "simulation time: " << sim_elapsed << "s\n";
    std::cout << "total time: " << total_elapsed << "s\n";
    std::cout << "gsocialsim_cpp: kernel ran " << ticks << " ticks in " << sim_elapsed << "s\n";

    if (enable_timing) {
        auto report = kernel.timing_report();
        std::cout << "TIMING REPORT (top by total time):\n";
        int shown = 0;
        for (const auto& row : report) {
            if (shown >= timing_top) break;
            const auto& name = std::get<0>(row);
            double total = std::get<1>(row);
            size_t count = std::get<2>(row);
            double avg = std::get<3>(row);
            double max = 0.0;
            auto it = kernel.timing.find(name);
            if (it != kernel.timing.end()) max = it->second.max;
            std::cout << name << ": total=" << total << "s count=" << count
                      << " avg=" << avg << "s max=" << max << "s\n";
            shown++;
        }

        if (!timing_out.empty()) {
            bool json = false;
            if (timing_out.size() >= 5) {
                std::string tail = timing_out.substr(timing_out.size() - 5);
                for (auto& c : tail) c = static_cast<char>(std::tolower(c));
                json = (tail == ".json");
            }
            std::ofstream out(timing_out);
            if (out.is_open()) {
                if (json) {
                    out << "[\n";
                    for (size_t i = 0; i < report.size(); ++i) {
                        const auto& row = report[i];
                        const auto& name = std::get<0>(row);
                        double total = std::get<1>(row);
                        size_t count = std::get<2>(row);
                        double avg = std::get<3>(row);
                        double max = 0.0;
                        auto it = kernel.timing.find(name);
                        if (it != kernel.timing.end()) max = it->second.max;
                        out << "  {\"name\":\"" << name << "\","
                            << "\"total\":" << total << ","
                            << "\"count\":" << count << ","
                            << "\"avg\":" << avg << ","
                            << "\"max\":" << max << "}";
                        if (i + 1 < report.size()) out << ",";
                        out << "\n";
                    }
                    out << "]\n";
                } else {
                    out << "name,total,count,avg,max\n";
                    for (const auto& row : report) {
                        const auto& name = std::get<0>(row);
                        double total = std::get<1>(row);
                        size_t count = std::get<2>(row);
                        double avg = std::get<3>(row);
                        double max = 0.0;
                        auto it = kernel.timing.find(name);
                        if (it != kernel.timing.end()) max = it->second.max;
                        out << name << "," << total << "," << count << "," << avg << "," << max << "\n";
                    }
                }
            }
        }
    }
    if (export_state) {
        export_state_json(kernel, export_dir);
        std::cout << "wrote state export to " << export_dir << "/state.json\n";
    }
    return 0;
}
