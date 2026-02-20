# TODO

# LLM Integration Layer (Cross-Cutting Infrastructure)

Agent per-tick loop: DELIVER → ATTEND → PERCEIVE (LLM) → UPDATE (math) → DECIDE (rules) → ACT (LLM) → CONSOLIDATE (math)

## Attention Priority Queue (ATTEND phase)

* [ ] Implement priority queue ranking: source trust, topic salience, primal cues, intake mode, recency
* [ ] Per-tick time budget enforcement (consume in priority order, discard when exhausted)
* [ ] Intake mode cost multipliers (scroll=1.0, seek=1.25, physical=1.5, deep_focus=3.0)
* [ ] Only consumed content proceeds to LLM perception batch

## LLM Perception Batch (PERCEIVE phase)

* [ ] Define async batch interface: `perceive_batch(items) → impressions[]`
* [ ] Agent-specific perception: (content, agent_context) → numeric impression vector
* [ ] Impression includes content fingerprint for novelty/entropy system
* [ ] Deep focus tier: re-perceive with richer context when scroll-layer impression exceeds salience/threat threshold

## Personality-Driven Action (DECIDE + ACT phases)

* [ ] Personality-weighted reward evaluation for action threshold
* [ ] Personality archetypes: troll (low threshold, provocative), lurker (high threshold, rare), influencer (moderate, audience-aligned), activist (salient topics), casual (sporadic)
* [ ] Intent parameter generation: topic (salience × reward), stance (belief-driven), frame (personality-driven), desired effect (reward-optimizing)
* [ ] Define async batch interface: `generate_batch(intents) → content[]`

## LLM Backend Abstraction

* [ ] Backend-agnostic interface (single config choice, not separate code paths)
* [ ] Local backend: HTTP to vLLM / Ollama / llama.cpp server on localhost
* [ ] Cloud backend: HTTP to provider API (Anthropic, OpenAI, Azure) with rate limiting and retry
* [ ] Hybrid mode: local for perceive (high volume, smaller model), cloud for generate (lower volume, larger model)
* [ ] Replay-only mode: run entirely from cached impression vectors + generated content (no LLM needed)

## Deterministic Replay Cache

* [ ] Cache all LLM outputs (impression vectors + generated content) per tick per run
* [ ] Cache keyed by (run_id, tick, content_id, agent_id) for perceive; (run_id, tick, agent_id) for generate
* [ ] Same cache + same seed = identical dynamics on replay
* [ ] Cache storage format (JSON lines or binary)

---

# Phase 12 — Persistent C++ Server Mode

* [ ] Add `--server-mode` flag to main.cpp argument parser
* [ ] Separate static preload vs per-run init (extract initialization into reusable functions)
* [ ] Pre-load static data (stimuli CSV, geo population, segments, country configs)
* [ ] Stdin JSON protocol: `{"cmd": "run", ...}` / `{"cmd": "ping"}` / `{"cmd": "shutdown"}`
* [ ] Tick streaming via stdout (same `--stream-json` format)
* [ ] Per-run state reset (clear agent map, network graph, subscriptions, RNG re-seed)
* [ ] Memory pool reuse (pre-allocate agent/edge buffers at max expected size)
* [ ] OpenMP parallel network generation (follower assignment loop)
* [ ] Update `runner.py` to manage persistent process (stdin/stdout pipe, not spawn-per-run)
* [ ] Concurrency: serialize runs through one process initially; process pool for tuning later
* [ ] Health check: backend sends ping, watchdog restarts if no response in 10s

Performance targets:

* [ ] Network generation (1k agents) < 8s with OpenMP
* [ ] Subsequent warm runs < 15-20s
* [ ] 10k agents: network gen < 30s, simulation runtime < 2s

---

# Content Novelty & Message Entropy (Influence Dynamics Extension)

Extends Step 3 (habituation) of the 11-step belief dynamics pipeline.

Core principle: identical/similar repeated messages have diminishing and eventually counterproductive impact.

* [ ] Add `ContentExposureHistory` ring buffer to Agent (last W=50 content fingerprints)
* [ ] Define content fingerprint: `(topic, stance_signal, frame, media_type, source_id)`
* [ ] Implement `content_sim(c1, c2) = exp(-||f(c1)-f(c2)||/σ)` (σ=0.3 default)
* [ ] Implement `n_eff(c, history)` — soft repetition count via similarity sum
* [ ] Implement Cacioppo-Petty curve: `repetition_mult(n) = n · exp(-β·(n-1))` (β=0.3)
* [ ] Implement reactance check: n_eff > threshold (default 8) → sign flip on stance_signal
* [ ] Implement stream entropy: Shannon H over actor's observed topic distribution
* [ ] `diversity_mult = 0.3 + 0.7 · (H / H_max)` — single-topic actor at 30% effectiveness
* [ ] Add config params: `novelty_decay_beta`, `reactance_threshold`, `content_sim_sigma`, `diversity_floor`
* [ ] Insert into pipeline between Step 3 and Step 4 (habituation → novelty → diversity → reactance → base influence)
* [ ] Populate content fingerprints during PERCEIVE phase in kernel.cpp

Invariant tests:

* [ ] Identical message ×10: influence < 10% of single novel message
* [ ] Diverse 5-message campaign: total influence > same message ×5
* [ ] Spam past reactance threshold: net influence reverses sign
* [ ] Stream entropy = 0: diversity_mult = 0.3
* [ ] Stream entropy = max: diversity_mult = 1.0

---

# Phase 13 — ScenarioBundle + LLM Compiler

* [ ] Define `ScenarioBundle_v0` schema (meta, world, belief_dynamics, feed_algorithm, casting)
* [ ] Strict JSON schema validation layer
* [ ] Seed required, bounds enforcement server-side
* [ ] Intervention whitelist
* [ ] Scenario persistence (save/load)
* [ ] GUI Scenario tab (create, browse, load, run)
* [ ] LLM two-stage flow (intent → compiler → strict JSON)
* [ ] Extend to v1 after Phases 14-15 (add event_schedule, stimuli_plan, actors)

---

# Phase 14 — Event Engine

* [ ] Implement `WorldEvent` struct (type, tick, duration, parameter overrides)
* [ ] Implement `EventScheduler` (priority queue by tick)
* [ ] Parameter override events (temporary, duration-based with automatic revert)
* [ ] Salience spike events
* [ ] Actor activation events
* [ ] Endogenous trigger events (polarization → instability, momentum → cascade, trust → migration)
* [ ] Hysteresis: cooldown period (min 10 ticks) + dead-zone (±5%) for endogenous triggers
* [ ] Duration-based temporary overrides with clean revert
* [ ] GUI: event timeline visualization + event inspector panel

---

# Phase 15 — Stimuli Plan + Content Factory

* [ ] Define `stimuli_plan_v1` schema (topic/stance/frame/intensity distributions)
* [ ] Topic distribution curves (per-tick)
* [ ] Stance distributions (per-topic)
* [ ] Frame distributions
* [ ] Intensity curves
* [ ] Implement ContentFactory (numeric-only content generation)
* [ ] Numeric-only content schema (text optional, numeric fields required)
* [ ] Batch generation
* [ ] Cohort generation
* [ ] Seed-consistent generation
* [ ] Backward compat: CsvDataSource stays for real-world text stimuli; ContentFactory for synthetic

---

# Phase 16 — Endogenous Agent Content

* [ ] Content generation probability model (salience × arousal × reward)
* [ ] Emotional arousal threshold
* [ ] Reward optimization gate
* [ ] Social proof amplification
* [ ] Cascade depth tracking (max depth = 10, per-tick amplification budget per agent)
* [ ] Viral threshold detection
* [ ] GUI: cascade tree/graph visualization

---

# Phase 17 — Adaptive Media Diet

* [ ] Belief-driven migration
* [ ] Trust collapse → outlet abandonment model
* [ ] Crisis-driven international spike
* [ ] Echo chamber tightening (identity reinforcement)
* [ ] Budget renormalization (conservation maintained)
* [ ] Cross-border credibility shifts

---

# Phase 18 — Regime Detection & Metrics

* [ ] Belief entropy
* [ ] Segment entropy
* [ ] Momentum energy (Σ velocity²)
* [ ] Polarization first/second derivatives
* [ ] Cascade detection
* [ ] Influence concentration metrics (Gini)
* [ ] Content stream entropy (per-actor, system-wide — from entropy extension)
* [ ] GUI: regime timeline + metric comparison across runs

---

# Phase 19 — Interactive Mode

* [ ] Human agent injection
* [ ] Live content posting API
* [ ] Live event trigger API
* [ ] Actor manual mode
* [ ] Moderation panel
* [ ] Live parameter tuning
* [ ] GUI: interactive control panel + agent inspector

---

# Phase 20 — CUDA Backend

* [ ] Population GPU updates
* [ ] Batch belief GPU updates
* [ ] GPU feed ranking
* [ ] Exposure reductions
* [ ] Bitwise equivalence tests (CPU vs GPU)

---

# Architectural Guardrails

* [ ] LLM produces inputs (impressions) and outputs (content); math computes all belief updates
* [ ] Batch LLM only — no synchronous per-agent LLM calls in hot loop
* [ ] LLM backend configurable: local, cloud, hybrid, or replay-only from cache
* [ ] All runtime content numeric + bounded (text is optional metadata, not a dynamics input)
* [ ] Deterministic replay under fixed seed (cached LLM outputs, no LLM needed for replay)
* [ ] ScenarioBundle required for reproducible runs
* [ ] Event engine isolated from belief dynamics
* [ ] No hidden mutable global state
