#include "network_manager.h"

#include <algorithm>
#include <cmath>

#include "kernel.h"

// Helper to clamp value to [0, 1]
static double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

// ============================================================================
// BroadcastFeedNetwork Implementation
// ============================================================================

std::vector<ContentId> BroadcastFeedNetwork::build_candidates(
    const AgentId& viewer,
    const WorldContext& ctx,
    const std::vector<Content>& available_content) {

    std::vector<ContentId> candidates;
    candidates.reserve(available_content.size());

    // Get viewer's subscriptions
    auto viewer_subs = ctx.subscriptions.get_subscriptions(viewer);

    // Check each content item
    for (const auto& content : available_content) {
        // Skip viewer's own content (will be shown separately with proximity=1.0)
        if (content.author_id == viewer) {
            continue;
        }

        // Check if viewer is subscribed to this content via any channel
        bool is_subscribed = false;

        // Check creator subscription
        if (ctx.subscriptions.is_subscribed(viewer, SubscriptionType::CREATOR, content.author_id)) {
            is_subscribed = true;
        }

        // Check topic subscription
        if (!is_subscribed && !content.topic.empty()) {
            if (ctx.subscriptions.is_subscribed(viewer, SubscriptionType::TOPIC, content.topic)) {
                is_subscribed = true;
            }
        }

        // Check outlet subscription
        if (!is_subscribed && content.outlet_id.has_value() && !content.outlet_id->empty()) {
            if (ctx.subscriptions.is_subscribed(viewer, SubscriptionType::OUTLET, *content.outlet_id)) {
                is_subscribed = true;
            }
        }

        // Check community subscription
        if (!is_subscribed && content.community_id.has_value() && !content.community_id->empty()) {
            if (ctx.subscriptions.is_subscribed(viewer, SubscriptionType::COMMUNITY, *content.community_id)) {
                is_subscribed = true;
            }
        }

        if (is_subscribed) {
            candidates.push_back(content.id);
        }
    }

    // Limit candidates
    if (candidates.size() > max_candidates) {
        candidates.resize(max_candidates);
    }

    return candidates;
}

std::vector<ContentId> BroadcastFeedNetwork::rank_candidates(
    const AgentId& viewer,
    const std::vector<ContentId>& candidates,
    const WorldContext& ctx,
    const std::unordered_map<ContentId, const Content*>& content_map) {

    if (candidates.empty()) {
        return {};
    }

    // Score each candidate
    struct ScoredContent {
        ContentId id;
        double score;
    };

    std::vector<ScoredContent> scored;
    scored.reserve(candidates.size());

    int current_tick = ctx.current_tick;

    for (const auto& cid : candidates) {
        auto it = content_map.find(cid);
        if (it == content_map.end()) continue;

        const Content* content = it->second;

        // Recency score (decay with age)
        int age = 1;  // Default age if we can't determine it
        double recency = 1.0 / (1.0 + age);

        // Engagement score (social proof)
        double engagement = content->social_proof;

        // Platform-specific ranking weight
        double media_weight = mechanics.get_ranking_weight(content->media_type);

        // Subscription strength
        double sub_strength = std::max({
            ctx.subscriptions.get_subscription_strength(viewer, SubscriptionType::CREATOR, content->author_id),
            content->topic.empty() ? 0.0 : ctx.subscriptions.get_subscription_strength(viewer, SubscriptionType::TOPIC, content->topic),
            content->outlet_id.has_value() ? ctx.subscriptions.get_subscription_strength(viewer, SubscriptionType::OUTLET, *content->outlet_id) : 0.0,
            content->community_id.has_value() ? ctx.subscriptions.get_subscription_strength(viewer, SubscriptionType::COMMUNITY, *content->community_id) : 0.0
        });

        // Combined score
        double score = (mechanics.recency_weight * recency +
                       mechanics.engagement_weight * engagement) *
                       media_weight * sub_strength;

        scored.push_back({cid, score});
    }

    // Sort by score descending
    std::sort(scored.begin(), scored.end(),
        [](const ScoredContent& a, const ScoredContent& b) {
            return a.score > b.score;
        });

    // Extract ranked IDs
    std::vector<ContentId> ranked;
    ranked.reserve(scored.size());
    for (const auto& sc : scored) {
        ranked.push_back(sc.id);
    }

    // Limit to max_shown
    if (ranked.size() > max_shown) {
        ranked.resize(max_shown);
    }

    return ranked;
}

DeliveryRecord BroadcastFeedNetwork::deliver(
    const AgentId& viewer,
    IntakeMode mode,
    WorldContext& ctx,
    const std::unordered_map<ContentId, const Content*>& content_map) {

    DeliveryRecord record(ctx.current_tick, viewer, id, mode);

    // Build candidates from available content
    std::vector<Content> available;
    for (const auto& [cid, content_ptr] : content_map) {
        available.push_back(*content_ptr);
        record.add_eligible(cid, content_ptr->media_type);
    }

    // Build and rank candidates
    auto candidates = build_candidates(viewer, ctx, available);
    auto ranked = rank_candidates(viewer, candidates, ctx, content_map);

    // Mark as shown
    for (const auto& cid : ranked) {
        record.add_shown(cid);
    }

    return record;
}

// ============================================================================
// DirectMessageNetwork Implementation
// ============================================================================

std::vector<ContentId> DirectMessageNetwork::build_candidates(
    const AgentId& viewer,
    const WorldContext& ctx,
    const std::vector<Content>& available_content) {

    // Direct messages come from inbox, not from available content
    auto it = inboxes.find(viewer);
    if (it == inboxes.end() || it->second.empty()) {
        return {};
    }

    std::vector<ContentId> candidates;
    for (const auto& cid : it->second) {
        candidates.push_back(cid);
    }

    return candidates;
}

std::vector<ContentId> DirectMessageNetwork::rank_candidates(
    const AgentId& viewer,
    const std::vector<ContentId>& candidates,
    const WorldContext& ctx,
    const std::unordered_map<ContentId, const Content*>& content_map) {

    // Direct messages are already ordered by arrival time (FIFO in deque)
    // Return as-is
    return candidates;
}

DeliveryRecord DirectMessageNetwork::deliver(
    const AgentId& viewer,
    IntakeMode mode,
    WorldContext& ctx,
    const std::unordered_map<ContentId, const Content*>& content_map) {

    DeliveryRecord record(ctx.current_tick, viewer, id, mode);

    auto it = inboxes.find(viewer);
    if (it == inboxes.end() || it->second.empty()) {
        return record;
    }

    // Get messages from inbox
    auto& inbox = it->second;
    std::vector<ContentId> messages;

    // Take up to 10 messages
    size_t count = std::min(static_cast<size_t>(10), inbox.size());
    for (size_t i = 0; i < count; ++i) {
        messages.push_back(inbox.front());
        inbox.pop_front();
    }

    // Mark as eligible and shown
    for (const auto& cid : messages) {
        auto cit = content_map.find(cid);
        if (cit != content_map.end()) {
            record.add_eligible(cid, cit->second->media_type);
            record.add_shown(cid);
        }
    }

    return record;
}

void DirectMessageNetwork::publish(const Interaction& interaction, WorldContext& ctx) {
    // TODO: Handle direct messages when interaction model supports target_agent
    // For now, DMs are sent explicitly via send_message()
    (void)interaction;  // Suppress unused parameter warning
    (void)ctx;
}

void DirectMessageNetwork::send_message(const AgentId& from, const AgentId& to, const ContentId& message_id) {
    auto& inbox = inboxes[to];
    inbox.push_back(message_id);

    // Limit inbox size
    while (inbox.size() > max_inbox_size) {
        inbox.pop_front();
    }
}

// ============================================================================
// NetworkManager Implementation
// ============================================================================

void NetworkManager::register_layer(std::unique_ptr<NetworkLayerBase> layer) {
    std::string layer_id = layer->id;
    layers_[layer_id] = std::move(layer);
}

NetworkLayerBase* NetworkManager::get_layer(const std::string& layer_id) {
    auto it = layers_.find(layer_id);
    return it != layers_.end() ? it->second.get() : nullptr;
}

std::vector<NetworkLayerBase*> NetworkManager::get_all_layers() {
    std::vector<NetworkLayerBase*> result;
    for (auto& [id, layer] : layers_) {
        result.push_back(layer.get());
    }
    return result;
}

std::vector<DeliveryRecord> NetworkManager::deliver_all(
    const AgentId& viewer,
    WorldContext& ctx,
    const std::unordered_map<ContentId, const Content*>& content_map) {

    std::vector<DeliveryRecord> records;
    records.reserve(layers_.size());

    for (auto& [layer_id, layer] : layers_) {
        // Determine intake mode based on layer type
        IntakeMode mode = IntakeMode::SCROLL;
        if (layer_id == "direct_message") {
            mode = IntakeMode::SEEK;
        }

        auto record = layer->deliver(viewer, mode, ctx, content_map);
        records.push_back(record);
    }

    return records;
}
