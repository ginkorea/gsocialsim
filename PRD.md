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

## Status (2026-02-18)

### Completed Systems
- **Phase 1**: Subscription service with opt-in feed semantics (CREATOR/TOPIC/OUTLET/COMMUNITY)
- **Phase 2**: Multi-layer network manager (BroadcastFeed, DirectMessage, DeliveryRecords)
- **Phase 3**: Advanced influence dynamics (11-step physics-inspired pipeline)
- **Phase 4**: Population layer with hex-grid cells, segment mixes, CUDA-ready struct-of-arrays
- **Phase 5**: CUDA backend (deferred, architecture ready)
- **Phase 6**: Agent demographics and microsegment system (25 population segments, psychographics, Big 5)
- **Phase 7**: Dimensional identity similarity system (replaces binary matching and religion matrix)
- **Global architecture**: Multi-country simulation with 5 country defaults, diaspora, international actors
- **Phase 8**: Cross-border factors with reach vs credibility decomposition, language accessibility model
- **Phase 9**: Media diet with budget conservation, saturation curve, diaspora split
- **Phase 10**: Actor capabilities with 7 international actor profiles, credibility bounds, production model
- **Phase 11**: Scenario harness with 16 deterministic invariant tests

### Recent Changes
- Cross-border content delivery decomposed into independent reach and credibility multipliers
- Language accessibility model: shared official/common languages, translation quality, English lingua franca
- Media diet with budget conservation (all shares sum to 1.0) and saturation curve for diminishing returns
- Diaspora media consumption from origin + residence + international with automatic normalization
- 7 international actor capability profiles (international media, state media, multilateral org, regional org, global NGO, multinational corp, global celebrity)
- Actor credibility bounded by floor/ceiling with per-country overrides
- 16 deterministic scenario tests covering cross-border, media diet, actor capabilities, and end-to-end invariants
- Content novelty and message entropy extension designed (steps 3b-3d): Cacioppo-Petty repetition curve, stream entropy penalty, psychological reactance/boomerang effect
- Full mathematical specification for all systems in [INFLUENCE_MATH.md](INFLUENCE_MATH.md)

### Infrastructure
- C++ analytics: summary/detailed modes, CSV export
- Export bridge: `reports/state.json` + `reports/analytics.csv` + Python renderers
- Visualization: agents-only, platform, bipartite, threshold, full graph (physics settle then freeze)
- Network generation: sparse grouped structure with outliers; supports `groups|random|geo` modes
- 30 tests total: 14 for dimensional identity system + 16 for global architecture invariants

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
- `identity_vector` (8-16 dimensions)
- `identity_rigidity` in [0,1]
- `ingroup_labels`
- `taboo_boundaries`
- `political_identity` (5-axis: economic, social, libertarian, cosmopolitan, secular_religious)
- `political_ideology` in [-1,1] (scalar, backward-compatible)
- `demographics` (AgentDemographics: age, race, religion, education, income, gender, geography, etc.)
- `identity_coords` (cached dimensional coordinates, resolved by IdentitySpace)
- `country_id` (ISO code, determines which coordinate system to use)
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

### 6.1 Belief Update Rules (11-Step Pipeline + Novelty/Entropy Extension)

Belief updates pass through an 11-step physics-inspired pipeline with 3 sub-steps for content novelty and message entropy (see [INFLUENCE_MATH.md](INFLUENCE_MATH.md) for formal notation):

1. **Trust gate**: `trust^gamma` (superlinear, gamma=2.0) -- low trust yields near-zero influence
2. **Bounded confidence**: reject if `|signal - stance| > tau` (tau=1.5)
3. **Habituation**: `1/(1 + alpha*n)` -- diminishing returns from repeated exposure to same source
   - 3b. **Content novelty** (Cacioppo-Petty curve): `w_n = n·exp(-beta*(n-1))` -- inverted-U over effective repetition count; identical messages wear out, partially similar messages contribute fractionally
   - 3c. **Stream entropy**: `w_d = 0.3 + 0.7*(H/H_max)` -- Shannon entropy over actor's topic distribution; single-topic actors operate at 30% effectiveness
   - 3d. **Reactance check**: if n_eff > threshold (default 8), stance signal flips sign -- spam becomes actively counterproductive (boomerang effect)
4. **Base influence**: trust x credibility x primal activation x proximity x scroll penalty x novelty x diversity
5. **Identity defense**: backfire (reverse influence under identity threat), confirmation boost (1.1x), openness gating
6. **Evidence accumulation**: `E_t = lambda*E_{t-1} + w*signal`, gate at threshold (theta=0.5) -- single exposures rarely move beliefs
7. **Inertia and momentum**: `v = rho*v + eta*E` -- persistent velocity with decay (rho=0.85)
8. **Critical velocity**: nonlinear gain once momentum exceeds threshold (kappa=2.0)
9. **Rebound force**: `-k*(stance - core_value)` -- damped spring to baseline (k=0.05)
10. **Stance update**: `stance += eta_eff*momentum + rebound`
11. **Confidence update**: +0.04 (confirming) / -0.02 (opposing)

**Anti-spam properties**: The novelty/entropy extension ensures that (a) verbatim message repetition suffers severe wear-out (10 identical messages produce < 10% of a single novel message's impact), (b) diverse multi-topic campaigns outperform single-message spam, and (c) excessive repetition triggers psychological reactance that reverses the intended influence direction. This is grounded in Cacioppo-Petty (1979) repetition curves, Brehm (1966) reactance theory, and Shannon information theory.

### 6.1.1 Politics & Polarization

- Agents carry a **5-axis political identity**: economic, social, libertarian/authoritarian, cosmopolitan/nationalist, secular/religious governance
- Scalar `political_ideology` [-1, +1] is preserved for backward compatibility and expanded to 5D
- Topics can be marked with `political_salience` in [0,1]
- High political salience + high identity rigidity increases identity threat from opposing content
- Non-hostile disagreement can still reduce confidence and allow gradual change

### 6.1.2 Dimensional Identity Similarity

Demographic similarity is computed through a unified dimensional system:

- Every identity category embedded onto 1-5D continuous coordinates
- Per-dimension: `exp(-euclidean_dist / decay_rate)`
- Overall: weighted sum, auto-normalized
- Country-configurable coordinates, weights, and decay rates
- Factory defaults for USA, India, Brazil, UK, France

Similarity drives **homophily-based influence weighting**: in-group (similarity > 0.7) amplifies influence up to 1.6x; out-group (similarity < 0.3) attenuates down to 0.3x.

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

## 9.5 Cross-Border Content Delivery

Content crossing national borders passes through a **reach vs credibility decomposition**:

- **Reach multiplier** `[0, 1]`: cultural distance decay, language accessibility, amplification budget
- **Credibility multiplier** `[0, 1]`: geopolitical tension, state affiliation penalty, viewer institutional trust

```
effective_influence = base_influence * reach_mult * credibility_mult
```

**Media Diet**: Every agent has a media consumption budget that sums to 1.0:
- Domestic agents: residence share + small international pool
- Diaspora agents: origin + residence + international, normalized from DiasporaSegment consumption rates
- Saturation curve (`1 - exp(-k * share)`) gives diminishing returns, making diversified consumption more efficient

**International Actors**: Formal capability profiles bounding production, targeting, and credibility:
- 7 actor types: international media, state media, multilateral org, regional org, global NGO, multinational corp, global celebrity
- Credibility bounded by `[floor, ceiling]` per actor type with per-country overrides
- State media has higher targeting precision but lower credibility ceiling than independent media

See [GLOBAL_ARCHITECTURE.md](GLOBAL_ARCHITECTURE.md) and [INFLUENCE_MATH.md](INFLUENCE_MATH.md) for full specification.

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
