#pragma once

#include <optional>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using AgentId = std::string;
using TopicId = std::string;
using ContentId = std::string;
using ActorId = std::string;

enum class MediaType {
    UNKNOWN = 0,
    NEWS,
    SOCIAL_POST,
    VIDEO,
    MEME,
    LONGFORM,
    FORUM_THREAD
};

enum class IntakeMode {
    SCROLL = 0,
    SEEK,
    PHYSICAL,
    DEEP_FOCUS
};

inline MediaType media_type_from_string(const std::string& v) {
    if (v == "news") return MediaType::NEWS;
    if (v == "social_post") return MediaType::SOCIAL_POST;
    if (v == "video") return MediaType::VIDEO;
    if (v == "meme") return MediaType::MEME;
    if (v == "longform") return MediaType::LONGFORM;
    if (v == "forum_thread") return MediaType::FORUM_THREAD;
    return MediaType::UNKNOWN;
}

struct Belief {
    double stance = 0.0;
    double confidence = 0.0;
    double salience = 0.5;
    double knowledge = 0.5;

    // Advanced influence dynamics (Phase 3)
    double momentum = 0.0;              // Velocity/inertia for belief change
    double core_value = 0.0;            // Rebound anchor (stable baseline stance)
    double evidence_accumulator = 0.0;  // Multi-hit requirement tracker
    int exposure_count = 0;             // Habituation tracking (per-topic)
};

struct RewardVector {
    double status = 0.0;
    double affiliation = 0.0;

    RewardVector& operator+=(const RewardVector& other) {
        status += other.status;
        affiliation += other.affiliation;
        return *this;
    }
};

struct RewardWeights {
    double status = 1.0;
    double affiliation = 1.0;
    double dominance = 1.0;
    double coherence = 1.0;
    double novelty = 1.0;
    double safety = 1.0;
    double effort_cost = -1.0;
};

struct IdentityState {
    std::vector<double> identity_vector = std::vector<double>(8, 0.0);
    double identity_rigidity = 0.5;
    std::unordered_set<std::string> ingroup_labels;
    std::unordered_set<std::string> taboo_boundaries;
    double political_lean = 0.0;
    double partisanship = 0.0;
    int age_years = 35;
    std::string sex = "unknown";
    std::string race = "unknown";
    std::unordered_map<std::string, double> political_dimensions;
    std::unordered_map<std::string, std::string> demographics;
    std::unordered_map<std::string, double> group_affiliations;
};

struct EmotionState {
    double valence = 0.0;
    double arousal = 0.0;
    double anger = 0.0;
    double anxiety = 0.0;
};

struct Impression {
    TopicId topic;
    ContentId content_id;
    double stance_signal = 0.0;
    IntakeMode intake_mode = IntakeMode::SCROLL;
    MediaType media_type = MediaType::UNKNOWN;
    double consumed_prob = 1.0;
    double interact_prob = 0.0;
    double attention_cost = 1.0;
    double identity_threat = 0.0;
    double primal_activation = 0.0;
    double credibility_signal = 0.5;
    double emotional_valence = 0.0;
    double arousal = 0.0;
    double social_proof = 0.0;
    double relationship_strength_source = 0.0;
};

struct Content {
    ContentId id;
    AgentId author_id;
    TopicId topic;
    double stance = 0.0;
    bool is_identity_threatening = false;
    std::optional<std::string> content_text;
    std::optional<double> identity_threat;
    MediaType media_type = MediaType::UNKNOWN;
    std::vector<std::string> primal_triggers;
    double primal_intensity = 0.0;
    double credibility_signal = 0.5;
    double social_proof = 0.0;
    std::optional<std::string> outlet_id;
    std::optional<std::string> community_id;
    std::unordered_map<std::string, std::string> provenance;
};

enum class InteractionVerb {
    CREATE = 0,
    LIKE,
    FORWARD,
    COMMENT,
    REPLY
};

struct Interaction {
    AgentId agent_id;
    InteractionVerb verb = InteractionVerb::CREATE;
    std::optional<ContentId> target_stimulus_id;
    std::optional<Content> original_content;
};

struct BeliefDelta {
    TopicId topic_id;
    double stance_delta = 0.0;
    double confidence_delta = 0.0;
};

struct Stimulus {
    ContentId id;
    int tick = 0;
    AgentId source;
    std::string content_text;
    std::optional<std::string> creator_id;
    std::optional<std::string> outlet_id;
    std::optional<std::string> community_id;
    std::optional<std::string> topic_hint;
    std::optional<double> stance_hint;
    std::optional<double> political_salience;
    std::vector<std::string> primal_triggers;
    std::optional<double> primal_intensity;
    std::unordered_map<std::string, std::string> metadata;
    MediaType media_type = MediaType::UNKNOWN;
};
