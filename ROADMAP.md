# ROADMAP.md

# SSES Implementation Roadmap

**Last Updated**: 2026-02-19

This roadmap defines the controlled evolution of the Synthetic Social Ecology Simulator (SSES) into a fully reactive, scenario-generated, event-driven influence ecosystem.

The system evolves in strict dependency order.

---

# Foundations (Phases 1–11 Complete)

The deterministic mathematical core is complete:

* Subscription Service
* Multi-Layer Network Manager
* 11-Step Influence Dynamics
* Population Layer (CUDA-ready structure)
* Dimensional Identity Similarity
* Cross-Border Reach/Credibility
* Media Diet with Saturation
* Actor Capability Profiles
* Scenario Harness (16 invariant tests)

These form the immutable physics layer.

Everything forward builds on this.

---

# Phase 12 — Persistent C++ Server Mode (Infrastructure)

**Why first?**
Fast iteration is required before building reactive layers.

## Goals

* Eliminate 45-second spawn-per-run overhead
* Keep process warm between runs
* Enable interactive scenario testing

## Features

* `--server-mode` flag (persistent process, reads configs from stdin)
* Static preload (stimuli, geo, segments, country configs)
* Stdin JSON protocol: `{"cmd": "run", ...params}` → stream tick JSON to stdout
* Per-run state reset (clear agents, network graph, subscriptions)
* OpenMP parallel network generation
* Memory pool reuse between runs (pre-allocate agent/edge buffers at max expected size)

## Performance Targets

| Metric | Current | Target |
|--------|---------|--------|
| Network generation (1k agents) | 15-25s | < 8s (OpenMP) |
| Network generation (10k agents) | minutes | < 30s (OpenMP) |
| Simulation runtime (96 ticks) | < 1s | < 1s (no change) |
| First run (cold start) | ~45s | < 35s |
| Subsequent runs (warm) | ~45s | < 15-20s |

## Concurrency Model

Current runner supports `max_concurrent=4` via semaphore. With a persistent process, options:

1. **Serialize** through one process (simplest, sufficient for GUI)
2. **Process pool** of N server-mode instances (for tuning parallelism)
3. **Thread pool** inside C++ (complex, deferred)

Start with option 1; option 2 if tuning needs it.

## Health Protocol

* Backend sends `{"cmd": "ping"}` → C++ responds `{"status": "ready"}`
* Backend sends `{"cmd": "shutdown"}` → C++ exits cleanly
* Watchdog: restart process if no response within 10s

---

# Content Novelty & Message Entropy (Influence Dynamics Extension)

**Why here?**
The core dynamics must be correct before scenarios and reactive layers build on them. The current habituation mechanism (`1/(1 + α*n)`) is per-source only — it penalizes repeated exposure to ANY content from the same source, but does not distinguish between novel arguments and verbatim spam. An actor can currently maximize influence by repeating the exact same message, which contradicts established persuasion research.

## Literature Basis

### Cacioppo-Petty Repetition Curve (1979)

Persuasive impact follows an **inverted-U** as a function of message repetition:

* **1-3 exposures**: Increasing persuasion (familiarity, fluency, mere exposure)
* **3-5 exposures**: Peak, then diminishing returns (argument satiation)
* **5+ exposures**: Wear-out — declining persuasion, increased counterarguing
* **10+ exposures**: Reactance — perceived manipulation, boomerang effect

> Cacioppo & Petty (1979). "Effects of message repetition and position on cognitive response, recall, and persuasion." *Journal of Personality and Social Psychology*, 37(1), 97-109.

### Berlyne's Arousal Theory (1970)

Hedonic response to stimuli follows an inverted-U over arousal potential, which is driven by **novelty and complexity**. Intermediate novelty is preferred; both very novel and very familiar stimuli produce aversion.

> Berlyne, D.E. (1970). "Novelty, complexity, and hedonic value." *Perception & Psychophysics*, 8(5), 279-286.

### Zajonc's Mere Exposure Effect (1968)

Familiarity breeds liking, but with saturation. Maximum positive affect at 10-20 exposures; sustained repetition can reverse the effect.

> Zajonc, R.B. (1968). "Attitudinal effects of mere exposure." *Journal of Personality and Social Psychology*, 9(2), 1-27.

### Psychological Reactance (Brehm, 1966)

When individuals perceive that their freedom of choice is threatened (e.g., by repetitive persuasion attempts), they experience reactance — a motivation to resist and sometimes adopt the opposite position (boomerang).

> Brehm, J.W. (1966). *A Theory of Psychological Reactance*. Academic Press.

### Shannon Information Theory (1948)

A stream of identical messages carries zero information (entropy = 0). A diverse message stream carries high information (entropy = log₂|topics|). Influence should scale with the information content (surprise) of the message relative to the receiver's recent exposure.

> Shannon, C.E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal*, 27(3), 379-423.

## Mathematical Formulation

### 1. Content Fingerprint

Each content item is represented as a feature vector in a low-dimensional space:

```
f(c) = (topic, stance_signal, frame, media_type, source_id)
```

Two items are "content-similar" when their feature distance is small:

```
content_sim(c₁, c₂) = exp(-||f(c₁) - f(c₂)||₂ / σ)
```

Where σ controls the similarity radius (default: 0.3).

### 2. Effective Repetition Count

For each incoming content item, compute its effective repetition count relative to the agent's recent exposure history window (last W exposures, default W=50):

```
n_eff(c, history) = Σ_{h ∈ history} content_sim(c, h)
```

This is a soft count: identical messages contribute 1.0 each; partially similar messages contribute fractionally.

### 3. Repetition-Adjusted Impact (Cacioppo-Petty Curve)

The impact multiplier follows the inverted-U:

```
repetition_mult(n) = n · exp(-β · (n - 1))
```

Where β controls the wear-out rate (default: 0.3).

| n_eff | mult | Interpretation |
|-------|------|---------------|
| 1.0 | 1.00 | Novel — full impact |
| 2.0 | 1.35 | Mere exposure boost |
| 3.0 | 1.22 | Near peak |
| 5.0 | 0.68 | Wear-out begins |
| 10.0 | 0.07 | Severe wear-out |
| 15.0 | 0.002 | Near-zero (spam) |

### 4. Reactance Penalty (Boomerang)

When effective repetition exceeds a reactance threshold (default: 8), the agent perceives manipulation. This triggers a **sign flip** on the influence signal with magnitude proportional to overshoot:

```
if n_eff > n_reactance:
    reactance_strength = min(1.0, (n_eff - n_reactance) / n_reactance)
    stance_signal *= -(reactance_strength * 0.3)
```

This makes spam actively counterproductive — the content pushes the agent AWAY from the intended direction.

### 5. Stream Entropy Penalty (Actor-Level)

For an actor's observed content stream (as seen by a given agent), compute Shannon entropy over topic distribution:

```
H_actor = -Σᵢ p(topicᵢ) · log₂(p(topicᵢ))
H_max = log₂(|observed_topics|)
diversity_score = H_actor / H_max   ∈ [0, 1]
```

Low diversity penalizes all content from that actor:

```
actor_diversity_mult = 0.3 + 0.7 · diversity_score
```

An actor with a single-topic stream (H=0) operates at 30% effectiveness. A maximally diverse actor operates at 100%.

### 6. Combined Pipeline Position

These enter the existing 11-step pipeline between step 3 (habituation) and step 4 (base influence):

```
Step 3:  habituation_mult  = 1/(1 + α · exposure_count)        [existing, per-source]
Step 3b: novelty_mult      = repetition_mult(n_eff)              [NEW, per-content]
Step 3c: diversity_mult    = actor_diversity_mult                 [NEW, per-actor stream]
Step 3d: reactance check   → possible sign flip on stance_signal [NEW]
Step 4:  base_mult = trust * credibility * ... * habituation * novelty * diversity
```

## Integration Points

* **belief_dynamics.h**: Add `novelty_decay_beta`, `reactance_threshold`, `content_sim_sigma`, `diversity_floor` to `InfluenceDynamicsConfig`
* **belief_dynamics.cpp**: Add `apply_content_novelty()`, `apply_stream_entropy()`, `check_reactance()` methods
* **agent.h**: Add `ContentExposureHistory` ring buffer (last W content fingerprints per agent)
* **types.h**: Add content fingerprint fields to `Impression` struct
* **kernel.cpp**: Populate content fingerprints during PERCEIVE phase

## Invariant Tests

* Identical message repeated 10x: influence < 10% of single novel message
* Diverse 5-message campaign: total influence > single message repeated 5x
* Spam beyond reactance threshold: net influence reverses sign
* Single-topic actor: 30% effectiveness vs multi-topic actor at 100%
* Stream entropy = 0 (all identical): diversity_mult = 0.3
* Stream entropy = max (uniform topics): diversity_mult = 1.0

---

# Phase 13 — ScenarioBundle Schema + LLM Compiler

Scenarios become structured artifacts.

## Core

Define `ScenarioBundle_v1`:

```json
{
  "meta": {},
  "world": {},
  "belief_dynamics": {},
  "feed_algorithm": {},
  "casting": {},
  "actors": {},
  "stimuli_plan": {},
  "event_schedule": {}
}
```

## Versioning Strategy

Ship `ScenarioBundle_v0` first with only the fields that exist today:

* `meta`, `world`, `belief_dynamics`, `feed_algorithm`, `casting`

Extend to v1 after Phase 14-15 land:

* Add `event_schedule` (depends on Phase 14)
* Add `stimuli_plan` (depends on Phase 15)
* Add `actors` (depends on Phase 15 content factory)

This prevents Phase 13 from blocking on later phases.

## Requirements

* Strict JSON schema validation
* Seed required
* Bounds enforcement server-side
* Intervention whitelist
* Deterministic replay

## LLM Flow

1. Intent draft (natural language)
2. Compiler → strict JSON (bounded, validated)

Scenarios become reproducible experiments.

## GUI

* Scenario tab: create, browse, load, run scenarios
* Schema-driven form editor with validation

---

# Phase 14 — Event Engine (Reactive Core)

World becomes event-driven.

## Event Types

* Crisis
* Policy change
* Platform shift
* Actor activation
* Foreign interference
* Economic shock
* Violence spike
* Scandal

## Event Effects

* Parameter override (temporary, duration-based)
* Salience spike
* Actor production multiplier
* Media shift nudge
* Targeting precision boost

## Endogenous Triggers

* Polarization threshold → instability event
* Momentum spike → cascade event
* Trust collapse → migration event

**Hysteresis requirement**: Endogenous triggers must have a cooldown period (minimum 10 ticks between same-type triggers) and a dead-zone (±5% around threshold) to prevent oscillation where events fire → metric drops → event stops → metric rises → event fires again.

Reactive loop begins here.

## GUI

* Event timeline visualization (horizontal axis = ticks, events as markers)
* Event inspector panel (click event → see parameter overrides and effects)

---

# Phase 15 — Stimuli Plan + Content Factory

Stimuli no longer static CSV-only.

## Stimuli Plan

Defines:

* Topic distributions
* Stance distributions
* Frame mix
* Intensity curves
* Media type mix

## Content Factory (LLM Bounded)

Produces numeric-only content objects:

```json
{
  "topic": "T_election",
  "stance_signal": 0.7,
  "credibility": 0.6,
  "intensity": 0.4,
  "primal_triggers": ["fear"]
}
```

Text optional. Numeric fields required.

## Backward Compatibility

`CsvDataSource` remains for real-world text stimuli (including existing GDELT path). `ContentFactory` generates numeric-only synthetic stimuli. Both feed the same `StimulusIngestionEngine` — the engine accepts either format. This enables A/B comparison: synthetic stimuli plan vs real-world CSV in identical simulation conditions.

Events → Stimuli Plan → Content → Engine.

---

# Phase 16 — Endogenous Agent Content

Agents become producers.

## ACT Phase Upgrade

Agents post when:

* Salience high
* Emotional arousal high
* Reward threshold met
* Social proof sufficient

Generated content inherits:

* Ideology
* Emotional state
* Identity framing
* Topic salience

## Cascades

* Multi-hop amplification
* Cascade depth tracking (**bounded**: max depth = 10 hops, per-tick amplification budget per agent to prevent computational explosion)
* Viral threshold detection

Now the system becomes endogenous.

## GUI

* Cascade visualization (tree/graph of content propagation paths)

---

# Phase 17 — Adaptive Media Diet

Media environment responds to belief shifts.

## Adaptive Rules

* Trust collapse → outlet abandonment
* Identity reinforcement → echo chamber tightening
* Crisis → international spike
* Cross-border credibility shifts
* Budget conservation maintained

Media becomes dynamic.

---

# Phase 18 — Regime Detection & Advanced Metrics

Detect structural phase changes.

## Metrics

* Belief entropy
* Segment entropy
* Momentum energy (Σ velocity²)
* First/second derivative of polarization
* Cascade onset detection
* Influence Gini
* Cross-border share
* **Content stream entropy** (per-actor and system-wide, from Phase 12b)

System becomes measurable as a dynamical regime.

## GUI

* Regime timeline (annotated with detected phase transitions)
* Metric comparison panel across runs

---

# Phase 19 — Interactive Simulation Mode

Human-in-the-loop capability.

* Inject human agent
* Live content posting API
* Live event triggers
* Actor manual control
* Platform parameter control

Now it becomes a live ecosystem.

## GUI

* Interactive control panel: post content, trigger events, adjust parameters mid-run
* Agent inspector: click agent → see beliefs, exposure history, demographics

---

# Phase 20 — CUDA Backend (Optimization Last)

Only after system stable.

* Population updates
* Batch belief updates
* GPU feed ranking
* Exposure reductions
* Bitwise equivalence testing

Optimization comes last.

---

# Guardrails

1. LLM never in belief hot loop
2. Numeric bounded content only
3. Determinism under fixed seed
4. Schema validation mandatory
5. Event engine isolated from belief dynamics
6. No hidden mutable global state

---

# End Vision

A scalable, event-reactive, scenario-generated influence ecosystem that:

* Evolves endogenously
* Detects regime shifts
* Supports interaction
* Remains mathematically grounded
* Punishes spam and rewards diverse, novel argumentation
