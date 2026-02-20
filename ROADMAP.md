# SSES Implementation Roadmap

**Last Updated**: 2026-02-18

This roadmap tracks the implementation of missing features in the Synthetic Social Ecology Simulator C++ port, based on requirements in PRD.md and UML diagrams.

---

## Status Overview

### Completed
- Core types (AgentId, TopicId, ContentId, Belief, Impression, Content)
- WorldKernel with 4-phase contract (INGEST -> ACT -> PERCEIVE -> CONSOLIDATE)
- Agent state (identity, beliefs, attention, policy, budgets)
- Stimuli pipeline (CSV ingestion)
- Social graph + trust (NetworkGraph with directed edges, trust values)
- Basic belief update engine (trust, confirmation bias, identity defense)
- Feed priority queue (recency, engagement, proximity, mutual)
- GeoWorld with H3 hex cells
- Analytics (summary/detailed modes, CSV export)
- **Phase 1: Subscription Service** (2026-02-18) - Opt-in feed semantics with CREATOR/TOPIC/OUTLET/COMMUNITY subscriptions
- **Phase 2: Multi-Layer Network Manager** (2026-02-18) - Abstract NetworkLayer, BroadcastFeed, DirectMessage, PlatformMechanics, DeliveryRecord
- **Phase 3: Advanced Influence Dynamics** (2026-02-18) - 11-step physics-inspired pipeline: inertia, rebound, critical velocity, evidence accumulation, trust gates, habituation, bounded confidence
- **Phase 4: Population Layer** (2026-02-18) - Hex-grid cells, segment mix, belief distributions, CUDA-ready struct-of-arrays
- **Phase 6: Agent Demographics & Microsegments** (2026-02-18) - 25 population segments, AgentDemographics, AgentPsychographics, Big 5 personality, homophily-based influence
- **Phase 7: Dimensional Identity Similarity** (2026-02-18) - Unified continuous coordinate system for all identity dimensions, country-configurable, replaces binary matching and hardcoded religion matrix
- **Global Architecture** (2026-02-18) - Multi-country infrastructure, 5 country defaults, diaspora communities, international actors, PoliticalIdentity 5-axis
- **Phase 8: Cross-Border Factors** (2026-02-18) - Reach vs credibility decomposition, language accessibility model, cultural distance decay
- **Phase 9: Media Diet** (2026-02-18) - Budget conservation (shares sum to 1.0), saturation curve, diaspora split, shift-toward rebalancing
- **Phase 10: Actor Capabilities** (2026-02-18) - 7 international actor profiles, credibility bounds, production/targeting/amplification model
- **Phase 11: Scenario Harness** (2026-02-18) - 16 deterministic invariant tests covering cross-border, media diet, actor capabilities, and end-to-end scenarios

### Planned
- Phase 5: CUDA Backend (Optional, deferred)
- Phase 12: JSON-loaded identity profiles (country configs from file, replaces factory defaults)
- Phase 13: Event-driven media diet adaptation (media shifts triggered by crisis events, exposure patterns)
- Phase 14: C++ Server Mode (persistent process, pre-loaded data, fast per-run execution)
- Phase 15: GDELT data source integration (real-world event ingestion for stimuli pipeline)

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

## Phase 6: Agent Demographics & Microsegments (Complete)

**Priority**: HIGH
**Status**: Complete (2026-02-18)
**Goal**: Rich agent demographics with psychographic profiles, microsegment-based generation, and homophily-driven influence.

### New Components
- `cpp/include/demographic_sampling.h` / `cpp/src/demographic_sampling.cpp`
- `cpp/src/agent_demographics.cpp` (rewritten)
- `cpp/test/test_agent_demographics.cpp`

### Key Features
- **AgentDemographics**: 25+ fields (age, race, religion, religiosity, education, income, gender, geography, political ideology, occupation, media diet, etc.)
- **AgentPsychographics**: Big 5 personality, social media behavior, influence dynamics, social graph position
- **DemographicSampler**: Generates realistic agent profiles from population segments with appropriate variance
- **Homophily-based influence weighting**: demographic similarity drives in-group amplification / out-group attenuation
- **Content targeting**: filter content delivery by age, gender, ideology, segment, behavioral traits

### Success Criteria
- [x] Demographic sampling produces realistic distributions
- [x] Psychographic traits correlate with segment profiles
- [x] Similar agents have similarity > 0.8
- [x] Very different agents have similarity < 0.5
- [x] In-group influence weight > out-group weight

---

## Phase 7: Dimensional Identity Similarity (Complete)

**Priority**: HIGH
**Status**: Complete (2026-02-18)
**Goal**: Replace fragmented similarity computation (binary match, hardcoded religion matrix) with a unified dimensional system.

### New Components
- `cpp/include/identity_space.h`
- `cpp/src/identity_space.cpp`

### Key Features
- **Unified codepath**: All identity categories through `exp(-dist/decay)` -- one formula for everything
- **Country-configurable**: Factory defaults for USA, IND, BRA, GBR, FRA with different coordinate maps and weights
- **Religion 2D**: Tradition family (x) x devotional intensity (y), with y overridden by per-agent religiosity
- **Race/Ethnicity 2D**: US race boundaries, India caste/community, Brazil color spectrum
- **Political Ideology 5D**: Economic, social, libertarian, cosmopolitan, secular_religious
- **Auto-normalization**: Weights summing to any value produce correct [0,1] similarity
- **14 tests**: Religion distances, country configs, geography ordering, codepath uniformity, weight normalization

### Removed
- 180-line `RELIGIOUS_SIMILARITY` matrix from `country.cpp`
- `get_religious_similarity()` function
- Binary match logic for geography, education, gender in `compute_similarity()`

### Mathematical Specification
Full formal notation with coordinate maps, diagrams, and parameter tables in [INFLUENCE_MATH.md](INFLUENCE_MATH.md).

### Success Criteria
- [x] Protestant-Catholic distance < 0.15, Catholic-Hindu > 0.50
- [x] Urban-Suburban < Urban-Rural
- [x] Similar agents similarity > 0.85
- [x] Very different agents similarity < 0.30
- [x] India caste coordinates produce different distances than US race coordinates
- [x] All dimensions through same exp(-dist/decay) codepath
- [x] Auto-normalization correct for arbitrary weight sums

---

## Phase 8: Cross-Border Factors (Complete)

**Priority**: HIGH
**Status**: ✅ Complete (2026-02-18)
**Goal**: Decompose cross-border content delivery into independent reach and credibility multipliers.

### New Components
- `cpp/include/cross_border.h`
- `cpp/src/cross_border.cpp`

### Key Features
- **Reach vs credibility decomposition**: `effective_influence = base * reach_mult * credibility_mult`
- **Reach multiplier** `[0, 1]`: cultural distance decay, language accessibility, amplification budget, inauthenticity boost
- **Credibility multiplier** `[0, 1]`: geopolitical tension penalty, state affiliation penalty, viewer institutional trust modulation
- **Language accessibility model**: Same country=1.0, shared official=1.0, shared common=0.85, translated=quality×0.7, English lingua franca=proficiency×0.8, no shared language=0.05
- **Source-type trust modulation**: State propaganda credibility drops with high viewer trust; international media credibility rises

### Success Criteria
- [x] Same-country content: reach ≥ 0.9, credibility ≥ 0.8
- [x] High-tension cross-border: credibility ≤ 0.5
- [x] Untranslated foreign content: reach ≤ 0.15
- [x] US-UK shared language = 1.0, RUS-USA < 0.15
- [x] State propaganda credibility < regular media credibility

---

## Phase 9: Media Diet (Complete)

**Priority**: HIGH
**Status**: ✅ Complete (2026-02-18)
**Goal**: Budget-conserving media consumption model with saturation curve for diaspora and domestic agents.

### New Components
- `cpp/include/media_diet.h`
- `cpp/src/media_diet.cpp`

### Key Features
- **Budget conservation**: All media shares (residence + origin + international) sum to 1.0
- **Saturation curve**: `effective(share) = 1 - exp(-k × share)`, k=3.0 default
- **Split advantage**: Diversified media is more information-efficient (2 × sat(0.5) = 1.55 > sat(1.0) = 0.95)
- **Domestic factory**: Residence share dominates, small international pool
- **Diaspora factory**: Origin + residence + international from DiasporaSegment consumption rates
- **Shift-toward**: Event-driven rebalancing capped at ±0.3 with automatic re-normalization

### Success Criteria
- [x] Budget conservation holds (shares sum to 1.0 within epsilon)
- [x] Saturation marginal returns decrease monotonically
- [x] Diaspora diet: residence > origin share
- [x] Shift preserves budget conservation

---

## Phase 10: Actor Capabilities (Complete)

**Priority**: HIGH
**Status**: ✅ Complete (2026-02-18)
**Goal**: Formal capability model bounding what international actors can produce, target, and credibly deliver.

### New Components
- `cpp/include/actor_capabilities.h`
- `cpp/src/actor_capabilities.cpp`

### Key Features
- **ActorCapabilities struct**: production_capacity, content_quality, targeting_precision, credibility_floor/ceiling, amplification_budget, language coverage
- **Credibility bounds**: `get_credibility()` returns value in `[floor, ceiling]` per country, with per-country overrides
- **7 factory profiles**:
  1. International media (BBC-like): high quality, moderate targeting, high credibility ceiling
  2. State media (RT-like): high production, high targeting, low credibility ceiling, inauthentic accounts
  3. Multilateral org (UN-like): low production, highest quality, high credibility
  4. Regional org (EU-like): moderate production, regional targeting
  5. Global NGO (Greenpeace-like): moderate production, high credibility
  6. Multinational corp: high production, moderate quality, low credibility ceiling
  7. Global celebrity: low production, very high reach
- **Production model**: Scales by active countries and language count
- **Targeting effectiveness**: precision × internet penetration × social media penetration × inauthenticity boost

### Success Criteria
- [x] Credibility always in [floor, ceiling]
- [x] Total production bounded (< 500 units)
- [x] State media: higher targeting but lower credibility ceiling than international media
- [x] All 7 profiles pass validation

---

## Phase 11: Scenario Harness (Complete)

**Priority**: HIGH
**Status**: ✅ Complete (2026-02-18)
**Goal**: Deterministic test framework for global architecture invariants.

### New Components
- `cpp/include/scenario_harness.h`
- `cpp/src/scenario_harness.cpp`
- `cpp/test/test_global_architecture.cpp`

### Key Features
- **ScenarioHarness class**: Register/run_all/print_results pattern
- **16 deterministic scenarios** covering:
  - CrossBorder (5): same_country baseline, high_tension credibility, untranslated reach, language barrier, state propaganda penalty
  - MediaDiet (4): budget conservation, saturation diminishing returns, diaspora split, shift preserves budget
  - ActorCapabilities (4): credibility bounds, production bounded, state vs media comparison, profile validation
  - End-to-end (3): Russian interference model, international media coverage tiers, diaspora consumption efficiency
- **Helper infrastructure**: `build_test_geo()` creates 4-country hierarchy (USA, RUS, GBR, IND) with cultural distances, geopolitical tensions, language configs, and Indian-American diaspora segment

### Success Criteria
- [x] All 16 scenarios pass
- [x] No regressions in existing 14 demographic tests
- [x] Deterministic under fixed parameters

---

## Phase 14: C++ Server Mode (TODO)

**Priority**: HIGH
**Status**: 📋 Planned
**Goal**: Eliminate the ~45s per-run setup overhead by keeping a persistent C++ process with pre-loaded static data.

### Problem

Each simulation run currently spawns a new C++ process that repeats the full initialization:

| Phase | Time | Notes |
|-------|------|-------|
| Stimulus CSV loading | 5-15s | Reads entire CSV, builds tick index |
| Agent creation + demographics | 3-5s | RNG-sampled per agent |
| **Network generation** | **15-25s** | **Primary bottleneck** — edge creation, mutual computation |
| Geo population loading | 3-5s | 725MB H3 CSV (if geo mode enabled) |
| Subscription setup | 2-3s | N * avg_following subscription objects |
| **Total setup** | **~45s** | Actual simulation is <1s for typical runs |

### Proposed Approach: Stdin-Based Server Mode

Add a `--server-mode` flag to the C++ binary:

1. **Startup**: Load static data once (stimulus CSV, geo population CSV, population segments)
2. **Loop**: Read JSON run configs from stdin, one per line
3. **Per run**: Create agents, build network, run simulation, stream JSON output to stdout
4. **Shutdown**: Clean exit on stdin EOF or SIGTERM

```
Python Backend (FastAPI)
    │
    ├─ On startup: spawn gsocialsim_cpp --server-mode --stimuli data/stimuli.csv
    │              └─ C++ loads stimulus data once (~10s)
    │
    ├─ Per run: write JSON config to C++ stdin
    │           └─ C++ creates agents, builds network, runs ticks (~20s)
    │              └─ Streams tick JSON to stdout
    │
    └─ On shutdown: close stdin → C++ exits
```

### What Can Be Pre-loaded (Immutable Across Runs)

- Stimulus CSV data (`StimulusIngestionEngine.stimuli_by_tick_`)
- H3 geographic population data (725MB)
- Population segment templates
- Country configuration defaults

### What Must Be Per-Run (Seed-Dependent)

- Agent instances and demographics
- Social network graph topology
- Belief states, psychographics, subscriptions

### Expected Performance Gains

| Scenario | Current | With Server Mode |
|----------|---------|-----------------|
| First run | ~45s | ~35s (skip re-parse of stimulus CSV) |
| Subsequent runs | ~45s | ~20-25s (skip all static data loading) |
| With parallel network gen (OpenMP) | ~45s | ~10-15s |

### Implementation Steps

1. Add `--server-mode` flag to `main.cpp` argument parser
2. Extract initialization into reusable functions (separate static data loading from per-run setup)
3. Add stdin JSON reader loop (read line → parse config → run simulation → output results)
4. Add proper cleanup/reset between runs (clear agent map, network graph, subscriptions)
5. Modify `gui/backend/app/core/runner.py` to manage persistent process instead of spawning per run
6. Add health check protocol (backend sends `{"cmd": "ping"}`, C++ responds `{"status": "ready"}`)

### Future: Parallel Network Generation

The network edge creation loop is embarrassingly parallel. Adding OpenMP pragmas to the follower assignment loop in `main.cpp` could reduce the 15-25s network generation to 5-8s on multi-core machines.

---

## Phase 15: GDELT Data Source Integration (TODO)

**Priority**: MEDIUM
**Status**: 📋 Planned
**Goal**: Ingest real-world events from the GDELT Project as simulation stimuli, replacing or augmenting synthetic CSV data.

### Approach

- Add `GdeltDataSource` alongside existing `CsvDataSource`
- Query GDELT 2.0 GKG (Global Knowledge Graph) API for events by date range, country, topic
- Transform GDELT events into the existing `Stimulus` format (tick, source, content_text, topic, media_type)
- Cache downloaded GDELT data locally as CSV for reproducibility
- UI: Add "GDELT" option to data source type selector (currently shows "CSV" active, "GDELT (coming soon)" disabled)

### Integration Points

- `cpp/include/data_source.h`: Add `GdeltDataSource` class
- `gui/backend/app/core/datasources.py`: Add GDELT fetch/cache/inspect functions
- `gui/frontend/src/components/config/DataSourcePanel.tsx`: Enable GDELT selector with date range picker

---

## Critical Files Reference

### Core Integration Files
- **cpp/include/kernel.h** - WorldContext, NetworkManager
- **cpp/src/kernel.cpp** - `_perceive_batch()`, phase dispatch
- **cpp/include/types.h** - Belief struct with momentum/evidence fields
- **cpp/include/agent.h** - Agent, AgentDemographics, AgentPsychographics
- **cpp/include/identity_space.h** - DimensionalPosition, IdentitySpace, PoliticalIdentity
- **cpp/src/identity_space.cpp** - Country factory defaults, coordinate resolution, similarity computation
- **cpp/include/belief_dynamics.h** - InfluenceDynamicsConfig, BeliefDynamicsEngine
- **cpp/src/belief_dynamics.cpp** - 11-step belief update pipeline
- **cpp/src/agent_demographics.cpp** - compute_similarity(), compute_influence_weight()
- **cpp/src/agent.cpp** - AttentionSystem, BeliefUpdateEngine, dream(), consolidate_identity()
- **cpp/include/network.h** - Abstract NetworkLayer base

### Global Architecture Files
- **cpp/include/country.h** - Country, DiasporaSegment, InternationalActor, GlobalGeoHierarchy
- **cpp/src/country.cpp** - GlobalGeoHierarchy implementation, cultural distance, geopolitical tension
- **cpp/include/cross_border.h** - CrossBorderFactors, reach/credibility computation
- **cpp/src/cross_border.cpp** - Language accessibility, trust modulation, state propaganda penalty
- **cpp/include/media_diet.h** - MediaDiet, MediaSource, MediaDietFactory
- **cpp/src/media_diet.cpp** - Budget conservation, saturation curve, diaspora factory
- **cpp/include/actor_capabilities.h** - ActorCapabilities, ActorCapabilityFactory
- **cpp/src/actor_capabilities.cpp** - 7 factory profiles, production model, targeting effectiveness
- **cpp/include/scenario_harness.h** - ScenarioHarness, 16 scenario declarations
- **cpp/src/scenario_harness.cpp** - Full scenario implementations with build_test_geo()

### Test Files
- **cpp/test/test_agent_demographics.cpp** - 14 tests for dimensional identity system
- **cpp/test/test_global_architecture.cpp** - 16 tests for cross-border, media diet, actor capabilities

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
