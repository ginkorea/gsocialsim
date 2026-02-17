# Product Requirements Document (PRD)
## Project: Synthetic Social Ecology Simulator (SSES)

---

## 1. Purpose & Vision

The Synthetic Social Ecology Simulator (SSES) is a research platform designed to simulate **human-like social behavior, belief formation, and influence dynamics** across both **online social networks** and **offline physical interactions**.

It explicitly supports research into **how influence works**: who influences whom, through which channels (scroll/seek/physical), under what incentives, and with what measurable downstream effects (belief change, action, and network rewiring).

The system models:
- Persistent agents with personalities, identities, and learning
- Multiple social networks layered on top of a shared real-world social substrate
- Offline (physical) interactions with amplified influence
- Belief change with explicit attribution (“who brings who across the line”)
- Evolutionary selection of behaviors and personalities over time

The platform is intended for **research, experimentation, and counterfactual analysis**, not real-world deployment.

---

## 2. Explicit Non-Goals

- No live interaction with real social platforms
- No real-world persuasion or deployment
- No perfect language realism
- No free-form AGI cognition
- No single “correct” belief model

---

## 3. System Overview

### Core Subsystems
1. **World Kernel**
   - Global clock
   - Event scheduling
   - Deterministic replay
2. **Agent Engine**
   - Persistent agents with internal state and learning
3. **Global Social Reality**
   - Latent real-world relationships
4. **Online Network Layers**
   - Multiple social networks as overlays
5. **Physical (Offline) Layer**
   - Proximity-based interactions
6. **Stimulus Ingestion**
   - Read-only real-world data streams
7. **Learning & Reward System**
   - Personality-weighted reward optimization
8. **Evolutionary System**
   - Exit, reproduction, mutation
9. **Analytics & Attribution**
   - Belief crossing and influence pathways

---

## Status (2026-02-17)

- C++ analytics now defaults to summary mode to avoid huge CSVs; detailed mode retained for visualizations.
- C++ logs now include impression stance and interaction events for attribution and rendering.
- Added C++ `state.json` export (agents, following, stimuli) plus `render_from_cpp.py` to reuse Python visualizers.
- Visualization edges are now colored by influence direction (toward vs away), and agents are colored by political lean.
- Graph layout stabilized: physics runs to settle, then freezes; default layout spread increased with tunable options.
- Network generation defaults to sparse grouped structure with outliers; supports `groups|random|geo` modes.
- Added `--print-network-stats` to report degree stats, density, reciprocity, isolates, and group metrics.
- Influence from scrolled media is reduced (lower consumption/interaction and a scroll influence multiplier).

### Ideas to Implement (Influence Dynamics)

- Inertia: belief updates are resisted by a per-topic “mass” or stiffness term; small deltas decay instead of accumulate.
- Critical velocity: once belief momentum exceeds a threshold, additional aligned influence becomes easier (nonlinear gain).
- Rebound: restorative force toward a per-topic “core value” that prevents long-term drift.
- Hysteresis: direction of change depends on whether the agent is already moving toward or away from a stance.
- Trust gate: influence strength scales superlinearly with trust/credibility instead of linearly.
- Literature grounding: add a short math note mapping influence dynamics to known models and parameter ranges.

### Notes for Tomorrow (Influence Math)

- Evidence accumulator with decay (multi‑hit requirement):
  `E_t = λ E_{t-1} + w_i * s_i`, apply belief update only if `|E_t| > θ`.
  Use `λ ~ 0.85–0.98` and tune `θ` so single exposures rarely move beliefs.
- Inertia + rebound (damped spring to core value):
  `v_{t+1} = ρ v_t + η * influence - k * (b_t - b0)`, `b_{t+1} = b_t + v_{t+1}`.
  `b0` is a per-topic baseline; `k` controls how strongly beliefs revert.
- Critical velocity (nonlinear gain):
  `η_eff = η * (1 + κ * sigmoid(|v_t| - v0))` makes movement easier once momentum builds.
- Bounded confidence gate:
  suppress or invert influence when `|Δstance|` exceeds a threshold `τ`.
- Habituation per source:
  `w_i = w_i / (1 + α * n_exposures_from_source)` to reduce repeated exposure power.
- Trust gate (superlinear):
  `trust_effect = trust^γ` (γ in 2–4) so low trust yields near‑zero influence.

---

## 4. Agents

### 4.1 Persistent Agent Model

Agents are **long-lived processes**, not request/response bots.

Each agent runs a continuous loop:
- Perceive environment
- Update internal state
- Allocate attention
- Select intent
- Possibly act
- Consolidate memory

Most cycles result in **no visible action**, mirroring real human behavior.

---

### 4.2 Agent State

#### Identity (Slow-Changing)
- `identity_vector` (8–16 dimensions)
- `identity_rigidity` ∈ [0,1]
- `ingroup_labels`
- `taboo_boundaries`
- `political_lean` ∈ [-1,1]
- `partisanship` ∈ [0,1]
- `political_dimensions` (economic/social/security/environment/culture)
- `demographics` (immutable group tags)
- `group_affiliations` (mutable group strengths)

#### Beliefs (Topic-Based, Fast-Changing)
For each topic:
- `stance` ∈ [-1, +1]
- `confidence` ∈ [0,1]
- `salience` ∈ [0,1]
- `knowledge` ∈ [0,1]

#### Emotional State (Compact)
- valence
- arousal
- anger / anxiety (optional)

Emotions modulate learning rates and decision thresholds.

---

### 4.3 Time Budgets (Unequal by Design)

Each agent has a **per-tick time budget** (minutes) driven by its life schedule
(sleep / work / leisure). Perception and action draw from the same pool.

Time resets each tick; unused time is not banked.

---

### 4.4 Personality via Reward Weights

Agents maximize a **personality-weighted reward vector**:

1. Status
2. Affiliation
3. Dominance
4. Coherence
5. Novelty
6. Safety
7. Effort Cost (negative)

Weights differ per agent.
Some weights may invert (e.g., trolls reward backlash).

---

## 5. Cognition & Attention

### 5.1 Two-Tier Attention System

**Scroll + Seek Intake Layer**
- Extremely cheap, frequent perception
- Skims content and produces impression vectors
- No reasoning or text generation

**Deep Focus Layer**
- Rare, expensive
- Triggered by salience thresholds
- Used for long posts, arguments, coordination

---

### 5.2 Impression Object

Each exposure produces:
- emotional valence
- arousal
- stance signal
- credibility signal
- identity threat
- social proof
- relationship strength of source
- primal activation (optional)

Impressions decay rapidly.

---

## 6. Belief Update & Conversion

### 6.1 Belief Update Rules

Belief updates are bounded and depend on:
- trust
- confirmation bias
- identity defense / backfire
- repetition
- social proof
- relationship strength
- primal activation (neuromarketing-style)

Political salience can amplify identity threat and resistance.

### 6.1.1 Politics & Polarization

- Topics can be marked with `political_salience` ∈ [0,1].
- Agents carry a `political_lean` and `partisanship` strength.
- High political salience + high partisanship increases identity threat from opposing content.
- Non-hostile disagreement can still reduce confidence and allow gradual change.
- A default seed set of common political topics is provided for realistic initial distributions.

Beliefs do not random-walk.

---

### 6.2 Belief Crossing Events (Critical)

A belief crossing event occurs when:
- stance crosses a defined threshold
- confidence crosses a defined threshold
- identity compatibility is satisfied or overridden

Each event records:
- topic
- timestamp
- prior state
- new state
- attribution set

---

### 6.3 Attribution

- Sliding attribution window (3–14 days)
- Recency-weighted credit
- Strong-tie and physical-interaction multipliers
- Partial credit assignment

This is a primary research output.

---

### 6.4 Daily Identity Consolidation

Once per simulated day:
- compress beliefs
- re-anchor identity
- cap anchor drift
- stabilize behavior

Prevents identity random-walk and GA collapse.

---

## 7. Global Social Reality

### 7.1 Latent Relationship Vector

For relevant agent pairs, maintain a latent real-world relationship:

`R_uv = [affinity, trust, intimacy, conflict, reciprocity, status_delta, topic_alignment...]`

This represents **social reality independent of platforms**.

All interactions update `R_uv`.

---

## 8. Online Social Network Layers

### 8.1 Network Layers

Each social network is its own graph `G_n`:
- Shared agent nodes
- Distinct edges and mechanics

Minimum v1 layers:
- Broadcast feed
- Private messaging

Later:
- Forums / groups
- Media recommender networks

---

### 8.2 Relationship Projection

Edges in each network are projections of `R_uv`:

`E_uv^n = f_n(R_uv, agent_state_u, agent_state_v, network_state_n)`

---

### 8.3 Platform Mechanics

Each network defines:
- visibility rules
- ranking algorithms
- reward mapping
- moderation dynamics
- social risk profile

Networks are **views into the same social world**, not separate universes.

---

## 9. Physical (Offline) Layer

### 9.1 Purpose

The physical layer models **offline proximity interactions**:
- family
- coworkers
- classmates
- social groups

It is:
- closed
- sparse
- high-trust
- high-impact

---

### 9.2 Places & Schedules

Agents have:
- place memberships (home, work, school, clubs)
- daily schedules

Places define:
- size
- mixing rate
- norms
- topic bias

---

### 9.3 Physical Interaction Events

Generated by co-presence:
- chats
- arguments
- group conversations
- shared media

---

### 9.4 Amplification Rules

Physical interactions:
- update `R_uv` more strongly
- use higher belief learning rates
- impose higher social cost
- dominate belief crossing events

Physical influence is limited in reach but dominant in effect.

---

## 10. Exogenous World Data

### 10.1 Properties

- Read-only
- Immutable
- Time-indexed

---

### 10.2 Integration

External stimuli are transformed into:
- publisher posts
- influencer framings
- emotional derivatives

All derived content preserves provenance.

---

## 11. Learning System

### 11.1 Policy Structure

- Baseline behavior policy (“dumb LLM guide” or rules)
- Learning adjusts **action-template preferences**
- No RL over raw text

---

### 11.2 Learning Scope

1. Contextual bandits (default)
2. Short-horizon session learning
3. Optional long-horizon learning

Exploration is guided, not epsilon-greedy.

---

## 12. Moderation & Institutional Actors

### 12.1 Institutional Actors

- publishers
- influencers
- moderators
- optional fact-checkers

They stabilize the ecosystem and inject structure.

---

### 12.2 Moderation

- probabilistic enforcement
- reputation-dependent
- endogenous to the system

Moderation shapes evolutionary pressure.

---

## 13. Evolutionary Dynamics (GA)

### 13.1 Exit Conditions

Agents may exit due to:
- chronic low reward (personality-weighted)
- stress (except trolls)
- isolation
- boredom

---

### 13.2 Replacement

Exited agents are replaced by partial descendants:
- policy tendencies partially copied
- personality partially inherited
- mutation applied
- minimal social capital inheritance

No memory cloning.

---

### 13.3 Fitness

Fitness is multi-objective:
- reward
- connectedness
- reputation
- noise

Selection pressure is tunable to preserve diversity.

---

## 14. Logging & Research Outputs

### Required Logs
- eligible vs shown vs seen content
- impressions (include intake_mode: scroll/seek/physical)
- actions and costs
- reward components
- belief updates
- belief crossing events with attribution (mode-split credit)
- relationship updates (ΔR_uv) with causal event links
- influence events (attempts, successes, failures) with target + channel
- influence pathways (sequence of exposures leading to action/belief/relationship change)
- exits and births

---

### Key Metrics
- belief conversion pathways
- influence graph (who influences whom) by topic and channel
- influence efficiency (attempt → belief change / action change / relationship change)
- influence concentration (Gini/top-k share of influence)
- cascade shapes
- polarization drift
- personality survival rates
- platform selection effects
- scroll vs seek vs physical influence shares
- physical vs online influence ratios

---

## 15. v1 Scope (Recommended)

- Broadcast + DM networks
- Physical layer enabled
- Scroll + Seek intake enabled
- Templated text only
- Contextual bandits only
- Belief crossing fully implemented

---

## 16. Success Criteria

The platform is successful when:
- belief conversion is rare but attributable
- lurkers dominate population
- small elites drive most content
- physical layer dominates belief crossing
- different networks select for different personalities
- GA preserves diversity
- runs are reproducible under fixed seeds

---

## 17. Compute Assumptions

- One small LLM (“scroll / seek scanner”) per GPU
- Massive batching
- Hierarchical scanning (filter → scanner → deep focus)
- Tens of thousands of agents supported per high-end GPU

---

## 18. Research Framing

SSES is an **evolutionary attention-and-influence environment**:
- platforms define incentives
- personalities define reward
- learning defines adaptation
- evolution defines selection

The system is designed to answer:
**“Under which social and technical conditions do certain beliefs and behaviors survive, spread, and thrive, and what are the measurable mechanisms of influence that drive those outcomes?”**
