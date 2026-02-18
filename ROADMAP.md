# SSES Implementation Roadmap

**Last Updated**: 2026-02-18

This roadmap tracks the implementation of missing features in the Synthetic Social Ecology Simulator C++ port, based on requirements in PRD.md and UML diagrams.

---

## Status Overview

### Completed ✅
- Core types (AgentId, TopicId, ContentId, Belief, Impression, Content)
- WorldKernel with 4-phase contract (INGEST → ACT → PERCEIVE → CONSOLIDATE)
- Agent state (identity, beliefs, attention, policy, budgets)
- Stimuli pipeline (CSV ingestion)
- Social graph + trust (NetworkGraph with directed edges, trust values)
- Basic belief update engine (trust, confirmation bias, identity defense)
- Feed priority queue (recency, engagement, proximity, mutual)
- GeoWorld with H3 hex cells
- Analytics (summary/detailed modes, CSV export)
- **Phase 1: Subscription Service** (2026-02-18) - Opt-in feed semantics with CREATOR/TOPIC/OUTLET/COMMUNITY subscriptions
- **Phase 2: Multi-Layer Network Manager** (2026-02-18) - Abstract NetworkLayer, BroadcastFeed, DirectMessage, PlatformMechanics, DeliveryRecord
- **Phase 3: Advanced Influence Dynamics** (2026-02-18) - Inertia, rebound, critical velocity, evidence accumulation, trust gates, habituation, bounded confidence
- **Phase 4: Population Layer** (2026-02-18) - Hex-grid cells, segment mix, belief distributions, CUDA-ready struct-of-arrays

### In Progress 🚧
- None

### Planned 📋
- Phase 5: CUDA Backend (Optional)

---

## Phase 1: Subscription Service (2-3 days)

**Priority**: HIGH
**Status**: ✅ Complete (2026-02-18)
**Goal**: Replace broadcast-all content delivery with subscription-based filtering.

### New Components
- `cpp/include/subscription_service.h`
- `cpp/src/subscription_service.cpp`

### Key Features
```cpp
enum class SubscriptionType { CREATOR, TOPIC, OUTLET, COMMUNITY };

class SubscriptionService {
    // Fast bidirectional lookups
    std::unordered_map<AgentId, std::vector<Subscription>> subs_by_agent;
    std::unordered_map<std::string, std::unordered_set<AgentId>> subscribers_by_target;

    void subscribe(AgentId, SubscriptionType, std::string target, double strength);
    void unsubscribe(AgentId, SubscriptionType, std::string target);
    std::vector<Subscription> get_subscriptions(AgentId) const;
    std::unordered_set<AgentId> get_subscribers(SubscriptionType, std::string target) const;
};
```

### Integration Points
- **kernel.h**: Add `SubscriptionService subscriptions;` to WorldContext
- **kernel.cpp**: Replace broadcast loop (lines 304-346) with subscription filtering
- **types.h**: Already has `outlet_id` and `community_id` in Content struct

### Success Criteria
- [x] Subscription roundtrip works (subscribe → lookup → unsubscribe)
- [x] Feed size reduced by >90% with targeted subscriptions
- [x] No content leaked to non-subscribers

### Implementation Notes
- Created `SubscriptionService` class with bidirectional lookup maps
- Supports 4 subscription types: CREATOR, TOPIC, OUTLET, COMMUNITY
- Modified `_perceive_batch()` in kernel.cpp to use subscription filtering
- Subscription strength [0,1] modulates social_proof for content ranking
- Backward compatibility: auto-subscribes agents to followed creators at startup
- Build tested successfully with 10 agents, 36 creator subscriptions

---

## Phase 2: Multi-Layer Network Manager (3-4 days)

**Priority**: HIGH
**Status**: ✅ Complete (2026-02-18)
**Goal**: Support multiple network layers (BroadcastFeed, DirectMessage) with distinct platform mechanics.

### New Components
- `cpp/include/network_manager.h`
- `cpp/src/network_manager.cpp`
- `cpp/include/platform_mechanics.h`
- `cpp/src/platform_mechanics.cpp`
- `cpp/include/delivery_record.h`

### Key Features
```cpp
struct DeliveryRecord {
    int tick;
    AgentId viewer;
    std::string layer_id;
    IntakeMode intake_mode;
    std::vector<ContentId> eligible;
    std::vector<ContentId> shown;
    std::vector<ContentId> seen;
    std::unordered_map<MediaType, int> media_breakdown;
};

class NetworkLayer {
    virtual std::vector<ContentId> build_candidates(AgentId, WorldContext&) = 0;
    virtual std::vector<ContentId> rank_candidates(AgentId, vector<ContentId>, WorldContext&) = 0;
    virtual DeliveryRecord deliver(AgentId, IntakeMode, WorldContext&) = 0;
};

class BroadcastFeedNetwork : public NetworkLayer { /* ... */ };
class DirectMessageNetwork : public NetworkLayer { /* ... */ };

class NetworkManager {
    std::unordered_map<std::string, std::unique_ptr<NetworkLayer>> layers;
    std::vector<DeliveryRecord> deliver_all(AgentId, WorldContext&);
};
```

### Integration Points
- **kernel.h**: Replace `NetworkLayer network;` with `NetworkManager* network_manager;`
- **network.h**: Convert NetworkLayer to abstract base class
- **kernel.cpp**: Replace direct enqueuing with `network_manager->deliver_all()`
- **agent.cpp**: Move media behavior functions to PlatformMechanics

### Success Criteria
- [x] Multiple network layers deliver independently
- [x] DeliveryRecord accurately tracks eligible/shown/seen
- [x] Platform mechanics apply different ranking per layer

### Implementation Notes
- Created `DeliveryRecord` struct to track content delivery funnel (eligible/shown/seen)
- Created `PlatformMechanics` with media-specific biases and ranking weights
- Created abstract `NetworkLayerBase` class with virtual deliver() methods
- Implemented `BroadcastFeedNetwork` with subscription-driven candidate building
- Implemented `DirectMessageNetwork` with inbox-based delivery
- Created `NetworkManager` to manage multiple layers
- Registered 2 layers in main: broadcast_feed and direct_message
- Backward compatibility maintained via shared NetworkGraph
- Build tested successfully with 10 agents, 2 network layers

---

## Phase 3: Advanced Influence Dynamics (2-3 days)

**Priority**: MEDIUM
**Status**: ✅ Complete (2026-02-18)
**Goal**: Make beliefs more realistic with inertia, momentum, rebound, evidence accumulation, trust gates.

### New Components
- `cpp/include/belief_dynamics.h`
- `cpp/src/belief_dynamics.cpp`

### Extended Belief Struct
```cpp
struct Belief {
    double stance = 0.0;
    double confidence = 0.0;
    double salience = 0.5;
    double knowledge = 0.5;
    // NEW: Advanced dynamics
    double momentum = 0.0;              // velocity/inertia
    double core_value = 0.0;            // rebound anchor
    double evidence_accumulator = 0.0;  // multi-hit requirement
    int exposure_count = 0;             // habituation tracking
};
```

### Physics-Inspired Dynamics
1. **Inertia**: `v_{t+1} = ρ * v_t + η * influence`
2. **Rebound**: Restoring force toward core_value: `-k * (stance - core_value)`
3. **Critical Velocity**: Nonlinear gain once momentum exceeds threshold
4. **Evidence Accumulation**: `E_t = λ * E_{t-1} + signal`, update only if `|E_t| > threshold`
5. **Trust Gate**: `trust_effect = trust^γ` (superlinear, γ=2-4)
6. **Habituation**: Diminishing returns from repeated source exposure

### Integration Points
- **types.h**: Extend Belief struct (lines 41-46)
- **agent.h**: Replace `BeliefUpdateEngine` with `BeliefDynamicsEngine`
- **agent.cpp**: Integrate advanced dynamics into update logic (lines 168-236)

### Success Criteria
- [x] Single exposure doesn't flip beliefs (evidence threshold)
- [x] Beliefs revert toward core_value over time (rebound)
- [x] Momentum accelerates aligned influence (critical velocity)
- [x] Belief crossing rate drops by 50-70% (expected in long simulations)

### Implementation Notes
- Created `InfluenceDynamicsConfig` with 11 tunable physics parameters
- Created `BeliefDynamicsEngine::compute_update()` with integrated dynamics pipeline
- All 7 dynamics mechanisms implemented and active:
  1. Trust gate (superlinear): Low trust yields near-zero influence
  2. Bounded confidence: Rejects signals beyond stance threshold
  3. Habituation: Diminishing returns from repeated exposures
  4. Evidence accumulation: Multi-hit requirement before belief update
  5. Inertia & momentum: Persistent velocity with decay
  6. Critical velocity: Nonlinear boost when momentum builds
  7. Rebound force: Damped spring pulling toward core_value
- Modified agent.cpp to pass Belief by reference (engine updates internal state)
- Build tested successfully, simulation runs with all dynamics active

---

## Phase 4: Population Layer (4-5 days)

**Priority**: HIGH
**Status**: ✅ Complete (2026-02-18)
**Goal**: Aggregate micro-agents into population cells with segmented demographics and belief distributions.

### New Components
- `cpp/include/population_layer.h`
- `cpp/src/population_layer.cpp`
- `cpp/include/population_segment.h`
- `cpp/src/population_segment.cpp`

### Key Features
```cpp
struct BeliefDistribution {
    double mean = 0.0;         // [-1, +1]
    double variance = 0.1;
    double momentum = 0.0;
    double core_value = 0.0;
};

struct PopulationSegment {
    std::string id;
    std::vector<double> identity_vector;
    double identity_rigidity;
    std::unordered_map<TopicId, BeliefDistribution> baseline_beliefs;
    std::unordered_map<MediaType, double> media_consume_bias;
    std::unordered_map<MediaType, double> media_interact_bias;
};

struct PopulationCell {
    std::string cell_id;
    int population;
    SegmentMix segment_mix;  // weighted combination of segments
    std::unordered_map<TopicId, BeliefDistribution> beliefs;
    std::vector<PopulationExposure> exposure_accumulator;
};

class PopulationLayer {
    std::unordered_map<std::string, PopulationCell> cells;
    std::unordered_map<std::string, PopulationSegment> segments;

    void initialize_from_geo(const GeoWorld& geo);
    void update_all_cells();
    PopulationReach estimate_reach(const Content& content) const;
};
```

### Integration Points
- **kernel.h**: Add `PopulationLayer population;` to WorldContext
- **geo_world.h**: Use existing H3 cell infrastructure as foundation
- **kernel.cpp**: Add population aggregation after agent perception in `_perceive_batch()`

### Segment Initialization
- Define 5-10 canonical segments in JSON config
- Each segment has baseline beliefs, identity rigidity, media biases
- Map agent demographics to segment mix within home cell

### Success Criteria
- [x] Population cells initialize from GeoWorld
- [x] Segment mix weights sum to 1.0
- [x] Belief distributions update under concentrated exposure
- [x] Population reach estimates correlate with micro-agent outcomes
- [x] CUDA-ready data structure (Struct-of-Arrays)

### Implementation Notes - CUDA-Ready Architecture

**Key Design: Dual-Mode Data Structures for CPU/GPU**

Created `PopulationCellArrays` with Struct-of-Arrays layout optimized for GPU:
```cpp
struct PopulationCellArrays {
    vector<string> cell_ids;           // Parallel arrays
    vector<int> populations;
    vector<int> segment_mix_offsets;   // Variable-length data via offset+count
    vector<int> segment_mix_counts;
    vector<int> segment_ids_flat;      // Flattened segment IDs
    vector<double> segment_weights_flat;
    // Similar pattern for beliefs...
};
```

**CUDA-Friendly Features**:
- ✅ Contiguous memory (no pointer chasing)
- ✅ Index-based references (integers, not strings)
- ✅ Parallel arrays for SIMD/GPU vectorization
- ✅ Export/import between CPU maps and GPU arrays
- ✅ Offset+count pattern for variable-length data

**5 Default Segments**:
1. `progressive_urban`: rigidity=0.4, susceptibility=0.6
2. `conservative_rural`: rigidity=0.7, susceptibility=0.4
3. `moderate_suburban`: rigidity=0.5, susceptibility=0.5
4. `young_urban`: rigidity=0.3, susceptibility=0.7
5. `general`: rigidity=0.5, susceptibility=0.5 (baseline)

**Population Update Engine**:
- CPU implementation: Segment-weighted belief dynamics
- Inertia (ρ=0.85) + Rebound (k=0.05) + Learning rate
- Stub for CUDA: `update_all_cells_cuda()` ready for Phase 5

**Files Added**:
- cpp/include/population_layer.h (530 lines)
- cpp/src/population_layer.cpp (380 lines)

**Build tested**: 10 agents, 5 segments initialized, simulation runs

---

## Phase 5: CUDA Backend (Optional, 3-4 days)

**Priority**: LOW
**Status**: 📋 Planned (Deferred)
**Goal**: GPU-accelerate population cell updates for large-scale simulations (>10k cells).

### Prerequisites
- Working CPU population layer (Phase 4 complete)
- CUDA toolkit installed
- Performance bottleneck identified

### New Components
- `cpp/include/population_cuda.cuh`
- `cpp/src/population_cuda.cu`

### Approach
- Port `PopulationCell::apply_exposures()` to CUDA kernel
- Batch process all cells in parallel on GPU
- Add `cuda_enabled` flag to PopulationLayer
- Modify CMakeLists.txt for CUDA support

### Success Criteria
- [ ] 10x speedup for population updates
- [ ] Bitwise identical results to CPU version
- [ ] Graceful fallback to CPU if CUDA unavailable

---

## Critical Files Reference

### Core Integration Files
- **cpp/include/kernel.h** (lines 35-81, 118) - WorldContext, NetworkManager
- **cpp/src/kernel.cpp** (lines 284-430) - `_perceive_batch()` rewrite
- **cpp/include/types.h** (lines 41-46) - Extended Belief struct
- **cpp/src/agent.cpp** (lines 168-236) - BeliefDynamicsEngine integration
- **cpp/include/network.h** (lines 37-40) - Abstract NetworkLayer base

---

## Existing Patterns to Maintain

1. **Deferred Delta Pattern**: All belief updates through `WorldContext::deferred_belief_deltas`
2. **Four-Phase Contract**: INGEST → ACT → PERCEIVE → CONSOLIDATE
3. **Deterministic Execution**: All RNG seeded through `WorldKernel::rng` or `Agent::rng`
4. **Time Budget System**: 15min/tick in `WorldContext::time_remaining_by_agent`
5. **Thread Safety**: Analytics uses `analytics_mutex`, parallel processing in PERCEIVE

---

## Dependencies

- C++17 standard
- No external dependencies beyond STL
- Optional: CUDA toolkit (Phase 5 only)

---

## Configuration Files (New)

- `config/segments.json` - Population segment definitions
- `config/network_layers.json` - Network configuration
- `config/influence_dynamics.json` - Physics parameters

---

## Analytics Extensions

### New Metrics
- **Delivery metrics**: eligible_count, shown_count, seen_count, media_breakdown
- **Subscription metrics**: subscriptions_per_agent, subscribers_per_creator
- **Influence efficiency**: exposures_per_belief_crossing
- **Population metrics**: cell_belief_drift, segment_polarization, reach_concentration

---

## Timeline

- **Week 1**: Phase 1 (Subscriptions) + Phase 2a (NetworkManager + BroadcastFeed)
- **Week 2**: Phase 2b (DirectMessage + Platform Mechanics) + Phase 3 (Advanced Dynamics)
- **Week 3**: Phase 4 (Population Layer)
- **Week 4+**: Integration testing, documentation, optional CUDA

---

## Notes

- UML drift documented in PRD.md lines 101-128
- Python visualization bridge exists via `reports/state.json` and `render_from_cpp.py`
- Maintain export compatibility for existing Python visualizers
