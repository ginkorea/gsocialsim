#pragma once

#include <deque>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "delivery_record.h"
#include "network.h"
#include "platform_mechanics.h"
#include "subscription_service.h"
#include "types.h"

// Forward declarations
struct WorldContext;
class ContentStore;

// -----------------------------
// Module: Network Manager
// Multi-layer network architecture with platform-specific mechanics
// -----------------------------

// Abstract base class for network layers
class NetworkLayerBase {
public:
    std::string id;
    NetworkGraph graph;
    PlatformMechanics mechanics;

    NetworkLayerBase(const std::string& layer_id) : id(layer_id) {}
    virtual ~NetworkLayerBase() = default;

    // Build list of eligible content for a viewer
    virtual std::vector<ContentId> build_candidates(
        const AgentId& viewer,
        const WorldContext& ctx,
        const std::vector<Content>& available_content) = 0;

    // Rank candidates for delivery
    virtual std::vector<ContentId> rank_candidates(
        const AgentId& viewer,
        const std::vector<ContentId>& candidates,
        const WorldContext& ctx,
        const std::unordered_map<ContentId, const Content*>& content_map) = 0;

    // Deliver content to viewer and return delivery record
    virtual DeliveryRecord deliver(
        const AgentId& viewer,
        IntakeMode mode,
        WorldContext& ctx,
        const std::unordered_map<ContentId, const Content*>& content_map) = 0;

    // Publish interaction to this layer
    virtual void publish(const Interaction& interaction, WorldContext& ctx) {}
};

// Broadcast feed network (subscription-driven)
class BroadcastFeedNetwork : public NetworkLayerBase {
public:
    int candidate_window_ticks = 96;  // Look back 1 day (96 ticks * 15min)
    size_t max_candidates = 500;
    size_t max_shown = 20;

    BroadcastFeedNetwork(const std::string& layer_id = "broadcast_feed")
        : NetworkLayerBase(layer_id) {}

    std::vector<ContentId> build_candidates(
        const AgentId& viewer,
        const WorldContext& ctx,
        const std::vector<Content>& available_content) override;

    std::vector<ContentId> rank_candidates(
        const AgentId& viewer,
        const std::vector<ContentId>& candidates,
        const WorldContext& ctx,
        const std::unordered_map<ContentId, const Content*>& content_map) override;

    DeliveryRecord deliver(
        const AgentId& viewer,
        IntakeMode mode,
        WorldContext& ctx,
        const std::unordered_map<ContentId, const Content*>& content_map) override;
};

// Direct message network (inbox-based)
class DirectMessageNetwork : public NetworkLayerBase {
public:
    std::unordered_map<AgentId, std::deque<ContentId>> inboxes;
    size_t max_inbox_size = 100;

    DirectMessageNetwork(const std::string& layer_id = "direct_message")
        : NetworkLayerBase(layer_id) {}

    std::vector<ContentId> build_candidates(
        const AgentId& viewer,
        const WorldContext& ctx,
        const std::vector<Content>& available_content) override;

    std::vector<ContentId> rank_candidates(
        const AgentId& viewer,
        const std::vector<ContentId>& candidates,
        const WorldContext& ctx,
        const std::unordered_map<ContentId, const Content*>& content_map) override;

    DeliveryRecord deliver(
        const AgentId& viewer,
        IntakeMode mode,
        WorldContext& ctx,
        const std::unordered_map<ContentId, const Content*>& content_map) override;

    void publish(const Interaction& interaction, WorldContext& ctx) override;

    // Add message to inbox
    void send_message(const AgentId& from, const AgentId& to, const ContentId& message_id);
};

// Network manager - manages multiple network layers
class NetworkManager {
public:
    NetworkManager() = default;

    // Register a network layer
    void register_layer(std::unique_ptr<NetworkLayerBase> layer);

    // Get a layer by ID
    NetworkLayerBase* get_layer(const std::string& layer_id);

    // Get all layers
    std::vector<NetworkLayerBase*> get_all_layers();

    // Deliver content across all layers to a viewer
    std::vector<DeliveryRecord> deliver_all(
        const AgentId& viewer,
        WorldContext& ctx,
        const std::unordered_map<ContentId, const Content*>& content_map);

private:
    std::unordered_map<std::string, std::unique_ptr<NetworkLayerBase>> layers_;
};
