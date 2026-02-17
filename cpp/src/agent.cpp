#include "agent.h"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <unordered_map>

#include "kernel.h"

static inline double clamp(double v, double lo, double hi) {
    if (v < lo) return lo;
    if (v > hi) return hi;
    return v;
}

static inline double clamp01(double v) {
    return clamp(v, 0.0, 1.0);
}

static std::string lower_copy(const std::string& s) {
    std::string out = s;
    for (char& c : out) {
        if (c >= 'A' && c <= 'Z') c = static_cast<char>(c - 'A' + 'a');
    }
    return out;
}

static double base_consume(MediaType mt) {
    switch (mt) {
        case MediaType::NEWS: return 0.85;
        case MediaType::SOCIAL_POST: return 0.65;
        case MediaType::VIDEO: return 0.60;
        case MediaType::MEME: return 0.55;
        case MediaType::LONGFORM: return 0.50;
        case MediaType::FORUM_THREAD: return 0.45;
        default: return 0.60;
    }
}

static double base_interact(MediaType mt) {
    switch (mt) {
        case MediaType::NEWS: return 0.08;
        case MediaType::SOCIAL_POST: return 0.28;
        case MediaType::VIDEO: return 0.18;
        case MediaType::MEME: return 0.22;
        case MediaType::LONGFORM: return 0.10;
        case MediaType::FORUM_THREAD: return 0.16;
        default: return 0.15;
    }
}

static double intake_consume_mult(IntakeMode mode) {
    switch (mode) {
        case IntakeMode::SCROLL: return 1.00;
        case IntakeMode::SEEK: return 1.15;
        case IntakeMode::PHYSICAL: return 1.20;
        case IntakeMode::DEEP_FOCUS: return 1.40;
        default: return 1.0;
    }
}

static double intake_interact_mult(IntakeMode mode) {
    switch (mode) {
        case IntakeMode::SCROLL: return 1.00;
        case IntakeMode::SEEK: return 0.90;
        case IntakeMode::PHYSICAL: return 0.75;
        case IntakeMode::DEEP_FOCUS: return 0.60;
        default: return 1.0;
    }
}

static double base_attention_cost(MediaType mt) {
    switch (mt) {
        case MediaType::MEME: return 0.5;
        case MediaType::SOCIAL_POST: return 1.0;
        case MediaType::NEWS: return 2.0;
        case MediaType::VIDEO: return 4.0;
        case MediaType::FORUM_THREAD: return 3.0;
        case MediaType::LONGFORM: return 6.0;
        default: return 1.5;
    }
}

static double intake_cost_mult(IntakeMode mode) {
    switch (mode) {
        case IntakeMode::SCROLL: return 1.0;
        case IntakeMode::SEEK: return 1.25;
        case IntakeMode::PHYSICAL: return 1.50;
        case IntakeMode::DEEP_FOCUS: return 3.0;
        default: return 1.0;
    }
}

static double primal_base(MediaType mt) {
    switch (mt) {
        case MediaType::VIDEO: return 0.25;
        case MediaType::MEME: return 0.20;
        case MediaType::SOCIAL_POST: return 0.15;
        case MediaType::NEWS: return 0.10;
        case MediaType::LONGFORM: return 0.08;
        case MediaType::FORUM_THREAD: return 0.08;
        default: return 0.0;
    }
}

static double trigger_weight(const std::string& raw) {
    const std::string key = lower_copy(raw);
    if (key == "self" || key == "personal") return 0.12;
    if (key == "contrast" || key == "contrastable") return 0.10;
    if (key == "tangible") return 0.10;
    if (key == "start_end" || key == "beginning_end") return 0.08;
    if (key == "memorable") return 0.08;
    if (key == "visual") return 0.12;
    if (key == "emotion" || key == "emotional") return 0.12;
    return 0.05;
}

static std::string verb_to_string(InteractionVerb verb) {
    switch (verb) {
        case InteractionVerb::CREATE: return "create";
        case InteractionVerb::LIKE: return "like";
        case InteractionVerb::FORWARD: return "forward";
        case InteractionVerb::COMMENT: return "comment";
        case InteractionVerb::REPLY: return "reply";
        default: return "unknown";
    }
}

Impression AttentionSystem::evaluate(const Content& content, double proximity) const {
    Impression imp;
    imp.topic = content.topic;
    imp.content_id = content.id;
    imp.stance_signal = content.stance;
    if (content.identity_threat.has_value()) {
        imp.identity_threat = clamp01(content.identity_threat.value());
    } else {
        imp.identity_threat = content.is_identity_threatening ? 1.0 : 0.0;
    }
    imp.primal_activation = 0.0;
    imp.credibility_signal = clamp01(content.credibility_signal);
    imp.social_proof = clamp01(content.social_proof);
    imp.media_type = content.media_type;

    IntakeMode intake_mode = (proximity > 0.0) ? IntakeMode::PHYSICAL : IntakeMode::SCROLL;
    imp.intake_mode = intake_mode;

    const double consume = base_consume(content.media_type) * intake_consume_mult(intake_mode);
    const double interact = base_interact(content.media_type) * intake_interact_mult(intake_mode);
    imp.consumed_prob = clamp01(consume);
    imp.interact_prob = clamp01(interact);

    const double base_cost = base_attention_cost(content.media_type);
    imp.attention_cost = std::max(0.0, base_cost * intake_cost_mult(intake_mode));

    double base = primal_base(content.media_type);
    double trig = 0.0;
    for (const auto& t : content.primal_triggers) {
        trig += trigger_weight(t);
    }
    if (content.primal_intensity > 0.0) {
        trig += 0.4 * content.primal_intensity;
    }
    imp.primal_activation = clamp01(base + trig);

    return imp;
}

BeliefDelta BeliefUpdateEngine::update(
    const Belief* current,
    const Impression& impression,
    double trust,
    double identity_rigidity,
    bool is_self_source,
    double proximity
) const {
    trust = clamp01(trust);
    double credibility = clamp01(impression.credibility_signal);
    double primal_activation = clamp01(impression.primal_activation);
    double social_proof = clamp01(impression.social_proof);

    double primal_mult = 1.0 + 0.25 * primal_activation;
    double credibility_mult = 0.5 + credibility;

    proximity = clamp01(proximity);
    double multiplier = (proximity > 0.0) ? (1.0 + 9.0 * proximity) : 1.0;
    double trust_effect = (proximity > 0.0) ? std::min(1.0, trust + 0.15 * proximity) : trust;

    if (social_proof > 0.0) {
        multiplier *= (1.0 + 0.5 * social_proof);
        trust_effect = std::min(1.0, trust_effect + 0.25 * social_proof);
    }

    if (is_self_source) {
        multiplier *= 1.2;
    }

    if (!current) {
        double stance_delta = impression.stance_signal * trust_effect * multiplier;
        double conf_delta = (0.1 * trust_effect * multiplier) + (is_self_source ? (0.03 * trust_effect) : 0.0);
        return {impression.topic, stance_delta, conf_delta};
    }

    double stance_diff = impression.stance_signal - current->stance;
    bool is_confirming = (stance_diff > 0.0 && current->stance > 0.0) ||
                         (stance_diff < 0.0 && current->stance < 0.0);
    bool is_opposed = std::abs(stance_diff) > 1.0;
    bool is_threatening = impression.identity_threat > 0.5;

    double base = 0.10;
    double stance_change = stance_diff * base * trust_effect * multiplier * credibility_mult * primal_mult;
    double conf_change = 0.02 * trust_effect * multiplier * credibility_mult * primal_mult;

    if (is_confirming) {
        stance_change *= 1.1;
        conf_change += 0.04 * trust_effect * multiplier;
    }

    if (is_self_source) {
        conf_change += 0.03 * trust_effect;
    }

    if (is_threatening && is_opposed) {
        stance_change = -stance_diff * base * trust_effect * multiplier * 0.6;
        conf_change += 0.05 * trust_effect * multiplier;
    } else if (is_opposed) {
        double openness = clamp01(1.0 - identity_rigidity);
        double persuasive = trust_effect * credibility_mult;
        if (persuasive >= 0.7) {
            conf_change -= 0.01 * (0.3 + 0.7 * openness);
        }
    }

    return {impression.topic, stance_change, conf_change};
}

std::optional<Interaction> BanditPolicy::generate_interaction(Agent& agent, int tick) {
    std::uniform_real_distribution<double> u01(0.0, 1.0);
    bool can_create = !agent.beliefs.empty();
    bool can_react = !agent.recent_impressions.empty();
    if (!can_create && !can_react) return std::nullopt;

    double r = u01(agent.rng);
    bool choose_create = r < 0.5;
    if (choose_create && !can_create) choose_create = false;
    if (!choose_create && !can_react) choose_create = true;

    Interaction interaction;
    interaction.agent_id = agent.id;

    if (choose_create) {
        auto it = agent.beliefs.begin();
        std::advance(it, static_cast<long>(agent.rng() % agent.beliefs.size()));
        Content c;
        c.id = "C_" + agent.id + "_" + std::to_string(tick);
        c.author_id = agent.id;
        c.topic = it->first;
        c.stance = it->second.stance;
        c.media_type = MediaType::SOCIAL_POST;
        interaction.verb = InteractionVerb::CREATE;
        interaction.original_content = c;
        return interaction;
    }

    std::uniform_int_distribution<size_t> pick(0, agent.recent_impressions.size() - 1);
    ContentId target = agent.recent_impressions[pick(agent.rng)];
    interaction.target_stimulus_id = target;

    double rv = u01(agent.rng);
    if (rv < 0.5) {
        interaction.verb = InteractionVerb::LIKE;
    } else if (rv < 0.7) {
        interaction.verb = InteractionVerb::FORWARD;
    } else if (rv < 0.85) {
        interaction.verb = InteractionVerb::COMMENT;
    } else {
        interaction.verb = InteractionVerb::REPLY;
    }
    return interaction;
}

void BanditPolicy::learn(const std::string&, const RewardVector&) {
    // Placeholder for bandit updates.
}

Agent::Agent(const AgentId& agent_id, uint32_t seed)
    : id(agent_id), rng(seed) {}

void Agent::reset_time(double minutes) {
    time_remaining = minutes;
    reflect();
}

void Agent::reflect() {
    double reflect_cost = time_remaining * 0.2 * clamp01(activity.reflect_propensity);
    spend_time(reflect_cost);
}

bool Agent::spend_time(double minutes) {
    if (minutes <= 0.0) return true;
    if (time_remaining < minutes) return false;
    time_remaining -= minutes;
    return true;
}

void Agent::remember_impression(const Impression& imp) {
    recent_impressions.push_back(imp.content_id);
    while (recent_impressions.size() > max_recent_impressions) {
        recent_impressions.pop_front();
    }
}

PlannedAction Agent::plan_action(int tick) {
    PlannedAction plan{ id, std::nullopt, 0.0, std::nullopt, std::nullopt };
    auto interaction = policy.generate_interaction(*this, tick);
    if (!interaction) return plan;

    std::uniform_real_distribution<double> u01(0.0, 1.0);
    if (interaction->verb == InteractionVerb::CREATE) {
        if (u01(rng) > activity.write_propensity) return plan;
    } else {
        if (u01(rng) > activity.react_propensity) return plan;
    }

    double cost = 1.0;
    switch (interaction->verb) {
        case InteractionVerb::CREATE: cost = 5.0; break;
        case InteractionVerb::LIKE: cost = 1.0; break;
        case InteractionVerb::FORWARD: cost = 1.0; break;
        case InteractionVerb::COMMENT: cost = 3.0; break;
        case InteractionVerb::REPLY: cost = 3.0; break;
        default: cost = 1.0; break;
    }

    std::optional<RewardVector> reward;
    std::optional<std::string> action_key;
    if (interaction->verb == InteractionVerb::LIKE) {
        reward = RewardVector{0.0, 0.2};
        action_key = verb_to_string(interaction->verb) + "_" +
            interaction->target_stimulus_id.value_or("unknown");
    } else if (interaction->verb == InteractionVerb::FORWARD) {
        reward = RewardVector{0.3, 0.0};
        action_key = verb_to_string(interaction->verb) + "_" +
            interaction->target_stimulus_id.value_or("unknown");
    }

    plan.interaction = interaction;
    plan.cost_minutes = cost;
    plan.reward = reward;
    plan.action_key = action_key;
    return plan;
}

PerceptionPlan Agent::plan_perception(
    const Content& content,
    double trust,
    double proximity,
    bool compute_delta,
    const std::optional<ContentId>& stimulus_id
) {
    PerceptionPlan plan{ id, content, {}, proximity, stimulus_id, false, false, false, 0.0, 0.0, 0.0, std::nullopt, 0.0 };
    if (time_remaining <= 0.0) return plan;

    Impression impression = attention.evaluate(content, proximity);

    double read_pref = clamp01(activity.read_propensity);
    if (proximity > 0.0) {
        read_pref = std::min(1.0, 0.05 + 1.1 * read_pref);
    }

    std::uniform_real_distribution<double> u01(0.0, 1.0);
    bool exposed = u01(rng) < read_pref;
    if (!exposed) {
        plan.impression = impression;
        return plan;
    }

    bool consumed_roll = u01(rng) < clamp01(impression.consumed_prob);
    double attention_cost = impression.attention_cost;
    double exposure_cost = std::min(0.5, std::max(0.05, 0.15 * attention_cost));
    double consumption_extra_cost = std::max(0.0, attention_cost - exposure_cost);

    auto it = beliefs.find(content.topic);
    const Belief* cur = (it == beliefs.end()) ? nullptr : &it->second;
    bool has_belief = (cur != nullptr);
    double old_stance = has_belief ? cur->stance : 0.0;

    std::optional<BeliefDelta> delta;
    if (consumed_roll && compute_delta) {
        bool is_self_source = (content.author_id == id);
        delta = belief_engine.update(cur, impression, trust, identity.identity_rigidity, is_self_source, proximity);
    }

    plan.impression = impression;
    plan.exposed = true;
    plan.consumed_roll = consumed_roll;
    plan.has_belief = has_belief;
    plan.attention_cost = attention_cost;
    plan.exposure_cost = exposure_cost;
    plan.consumption_extra_cost = consumption_extra_cost;
    plan.delta = delta;
    plan.old_stance = old_stance;
    return plan;
}

bool Agent::apply_planned_action(const PlannedAction& plan, WorldContext* context) {
    if (!plan.interaction.has_value()) return false;
    auto spend = [&](double minutes) {
        if (minutes <= 0.0) return true;
        if (context) {
            return context->spend_time(id, minutes);
        }
        return spend_time(minutes);
    };
    if (!spend(plan.cost_minutes)) return false;
    daily_actions.push_back(plan.interaction.value());
    if (plan.action_key.has_value() && plan.reward.has_value()) {
        policy.learn(plan.action_key.value(), plan.reward.value());
    }
    return true;
}

void Agent::apply_perception_plan(const PerceptionPlan& plan, WorldContext* context) {
    if (!plan.exposed) return;

    auto spend = [&](double minutes) {
        if (minutes <= 0.0) return true;
        if (context) {
            return context->spend_time(id, minutes);
        }
        return spend_time(minutes);
    };

    if (!spend(plan.exposure_cost)) return;
    remember_impression(plan.impression);

    if (!plan.consumed_roll) return;
    if (!spend(plan.consumption_extra_cost)) return;

    daily_impressions_consumed.push_back(plan.impression);

    if (!plan.delta.has_value()) return;

    if (context && !context->in_consolidation) {
        context->queue_belief_delta(id, plan.delta.value());
        return;
    }

    apply_belief_delta(plan.delta.value());
}

void Agent::apply_perception_plan_local(
    const PerceptionPlan& plan,
    double& remaining_minutes,
    std::vector<std::pair<AgentId, BeliefDelta>>* out_deltas
) {
    if (!plan.exposed) return;
    if (remaining_minutes < plan.exposure_cost) return;
    remaining_minutes -= plan.exposure_cost;
    remember_impression(plan.impression);

    if (!plan.consumed_roll) return;
    if (remaining_minutes < plan.consumption_extra_cost) return;
    remaining_minutes -= plan.consumption_extra_cost;

    daily_impressions_consumed.push_back(plan.impression);

    if (!plan.delta.has_value()) return;
    if (out_deltas) {
        out_deltas->emplace_back(id, plan.delta.value());
    } else {
        apply_belief_delta(plan.delta.value());
    }
}

void Agent::enqueue_content(const Content& content, int tick, int current_tick, double engagement) {
    feed_queue.push(&content, tick, current_tick, engagement);
}

void Agent::enqueue_content(const Content* content, int tick, int current_tick, double engagement) {
    if (!content) return;
    feed_queue.push(content, tick, current_tick, engagement);
}

std::optional<FeedItem> Agent::dequeue_next_content() {
    if (feed_queue.empty()) {
        return std::nullopt;
    }
    return feed_queue.pop();
}

static size_t topic_to_dim(const std::string& topic, size_t dims) {
    if (dims == 0) return 0;
    return std::hash<std::string>{}(topic) % dims;
}

static void consolidate_identity(
    IdentityState& identity,
    const std::vector<Impression>& impressions,
    std::mt19937& rng,
    size_t max_samples = 30
) {
    if (impressions.empty()) return;

    size_t dims = identity.identity_vector.empty() ? 8 : identity.identity_vector.size();
    if (identity.identity_vector.empty()) {
        identity.identity_vector.assign(dims, 0.0);
    }

    auto weight = [](const Impression& imp) {
        double it = clamp01(imp.identity_threat);
        double ar = clamp01(imp.arousal);
        double sp = clamp01(imp.social_proof);
        return 0.2 + 0.5 * it + 0.3 * ar + 0.2 * sp;
    };

    std::vector<Impression> pool = impressions;
    std::vector<double> weights;
    weights.reserve(pool.size());
    for (const auto& imp : pool) {
        weights.push_back(std::max(0.0001, weight(imp)));
    }

    size_t k = std::min(max_samples, pool.size());
    std::vector<Impression> chosen;
    chosen.reserve(k);

    for (size_t i = 0; i < k && !pool.empty(); ++i) {
        std::discrete_distribution<size_t> dist(weights.begin(), weights.end());
        size_t idx = dist(rng);
        chosen.push_back(pool[idx]);
        pool.erase(pool.begin() + static_cast<long>(idx));
        weights.erase(weights.begin() + static_cast<long>(idx));
    }

    double total_w = 0.0;
    double threat_w = 0.0;
    std::vector<double> stance_push(dims, 0.0);

    for (const auto& imp : chosen) {
        double w = std::max(0.0001, weight(imp));
        total_w += w;
        threat_w += w * clamp01(imp.identity_threat);
        size_t dim = topic_to_dim(imp.topic, dims);
        stance_push[dim] += w * imp.stance_signal;
    }

    if (total_w <= 0.0) return;

    double avg_threat = threat_w / total_w;
    double rigidity_delta = (avg_threat - 0.25) * 0.05;
    identity.identity_rigidity = clamp(identity.identity_rigidity + rigidity_delta, 0.05, 0.95);

    double step = 0.03 * (1.0 - identity.identity_rigidity);
    for (size_t i = 0; i < dims; ++i) {
        double delta = (stance_push[i] / total_w) * step;
        identity.identity_vector[i] = clamp(identity.identity_vector[i] + delta, -1.0, 1.0);
    }

    std::uniform_real_distribution<double> u01(0.0, 1.0);
    for (size_t i = 0; i < dims; ++i) {
        if (std::abs(identity.identity_vector[i]) > 0.75) {
            std::string label = "ingroup_dim_" + std::to_string(i);
            if (identity.ingroup_labels.find(label) == identity.ingroup_labels.end()) {
                if (u01(rng) < 0.10) {
                    identity.ingroup_labels.insert(label);
                }
            }
        }
    }
}

void Agent::apply_belief_delta(const BeliefDelta& delta) {
    auto it = beliefs.find(delta.topic_id);
    if (it == beliefs.end()) {
        Belief b;
        b.stance = clamp(delta.stance_delta, -1.0, 1.0);
        b.confidence = clamp(delta.confidence_delta, 0.0, 1.0);
        b.salience = 0.0;
        b.knowledge = 0.0;
        beliefs.emplace(delta.topic_id, b);
        return;
    }
    it->second.stance = clamp(it->second.stance + delta.stance_delta, -1.0, 1.0);
    it->second.confidence = clamp(it->second.confidence + delta.confidence_delta, 0.0, 1.0);
}

void Agent::nudge_salience(const TopicId& topic, double delta) {
    auto it = beliefs.find(topic);
    if (it == beliefs.end()) {
        beliefs.emplace(topic, Belief{0.0, 0.0, clamp(delta, 0.0, 1.0), 0.0});
        return;
    }
    it->second.salience = clamp(it->second.salience + delta, 0.0, 1.0);
}

void Agent::nudge_knowledge(const TopicId& topic, double delta) {
    auto it = beliefs.find(topic);
    if (it == beliefs.end()) {
        beliefs.emplace(topic, Belief{0.0, 0.0, 0.0, clamp(delta, 0.0, 1.0)});
        return;
    }
    it->second.knowledge = clamp(it->second.knowledge + delta, 0.0, 1.0);
}

void Agent::dream() {
    if (daily_impressions_consumed.empty()) return;

    consolidate_identity(identity, daily_impressions_consumed, rng, 30);

    std::unordered_map<TopicId, int> counts;
    std::unordered_map<TopicId, double> sums;
    for (const auto& imp : daily_impressions_consumed) {
        counts[imp.topic] += 1;
        sums[imp.topic] += imp.stance_signal;
    }

    for (const auto& kv : counts) {
        const auto& topic = kv.first;
        int c = kv.second;
        nudge_salience(topic, 0.02 * std::min(10, c));
        nudge_knowledge(topic, 0.01 * std::min(10, c));

        auto it = beliefs.find(topic);
        if (it == beliefs.end()) continue;
        double mean_signal = sums[topic] / std::max(1, c);
        double openness = clamp01(1.0 - identity.identity_rigidity);
        double step = 0.02 * openness;
        double drift = (mean_signal - it->second.stance) * step;
        if (drift != 0.0) {
            apply_belief_delta(BeliefDelta{topic, drift, 0.0});
        }
    }
}

void Agent::consolidate_daily() {
    dream();
    daily_impressions_consumed.clear();
    daily_actions.clear();
}
