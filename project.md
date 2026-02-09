# Project Compilation: gsocialsim

## 🧾 Summary

| Metric | Value |
|:--|:--|
| Root Directory | `/home/gompert/data/workspace/gsocialsim` |
| Total Directories | 16 |
| Total Indexed Files | 85 |
| Skipped Files | 1 |
| Indexed Size | 379.45 KB |
| Max File Size Limit | 2 MB |

## 📚 Table of Contents

- [.gitignore](#gitignore)
- [LICENSE](#license)
- [PRD.md](#prd-md)
- [README.md](#readme-md)
- [agents_only.html](#agents-only-html)
- [bipartite.html](#bipartite-html)
- [diagrams/agent_runtime_state_machine.uml](#diagrams-agent-runtime-state-machine-uml)
- [diagrams/class_diagram.uml](#diagrams-class-diagram-uml)
- [diagrams/component_diagram.uml](#diagrams-component-diagram-uml)
- [diagrams/sequence_diagram.uml](#diagrams-sequence-diagram-uml)
- [fix_event_phase_init.patch](#fix-event-phase-init-patch)
- [influence_graph.html](#influence-graph-html)
- [phase_patch.py](#phase-patch-py)
- [platform.html](#platform-html)
- [pyproject.toml](#pyproject-toml)
- [requirements.txt](#requirements-txt)
- [run_and_visualize.py](#run-and-visualize-py)
- [run_stimulus_sim.py](#run-stimulus-sim-py)
- [src/gsocialsim.egg-info/PKG-INFO](#src-gsocialsim-egg-info-pkg-info)
- [src/gsocialsim.egg-info/SOURCES.txt](#src-gsocialsim-egg-info-sources-txt)
- [src/gsocialsim.egg-info/dependency_links.txt](#src-gsocialsim-egg-info-dependency-links-txt)
- [src/gsocialsim.egg-info/top_level.txt](#src-gsocialsim-egg-info-top-level-txt)
- [src/gsocialsim/__init__.py](#src-gsocialsim-init-py)
- [src/gsocialsim/agents/__init__.py](#src-gsocialsim-agents-init-py)
- [src/gsocialsim/agents/agent.py](#src-gsocialsim-agents-agent-py)
- [src/gsocialsim/agents/attention_system.py](#src-gsocialsim-agents-attention-system-py)
- [src/gsocialsim/agents/belief_state.py](#src-gsocialsim-agents-belief-state-py)
- [src/gsocialsim/agents/belief_update_engine.py](#src-gsocialsim-agents-belief-update-engine-py)
- [src/gsocialsim/agents/budget_state.py](#src-gsocialsim-agents-budget-state-py)
- [src/gsocialsim/agents/emotion_state.py](#src-gsocialsim-agents-emotion-state-py)
- [src/gsocialsim/agents/identity_state.py](#src-gsocialsim-agents-identity-state-py)
- [src/gsocialsim/agents/impression.py](#src-gsocialsim-agents-impression-py)
- [src/gsocialsim/agents/reward_weights.py](#src-gsocialsim-agents-reward-weights-py)
- [src/gsocialsim/analytics/__init__.py](#src-gsocialsim-analytics-init-py)
- [src/gsocialsim/analytics/analytics.py](#src-gsocialsim-analytics-analytics-py)
- [src/gsocialsim/analytics/attribution.py](#src-gsocialsim-analytics-attribution-py)
- [src/gsocialsim/evolution/__init__.py](#src-gsocialsim-evolution-init-py)
- [src/gsocialsim/evolution/evolutionary_system.py](#src-gsocialsim-evolution-evolutionary-system-py)
- [src/gsocialsim/kernel/__init__.py](#src-gsocialsim-kernel-init-py)
- [src/gsocialsim/kernel/event_scheduler.py](#src-gsocialsim-kernel-event-scheduler-py)
- [src/gsocialsim/kernel/events.py](#src-gsocialsim-kernel-events-py)
- [src/gsocialsim/kernel/sim_clock.py](#src-gsocialsim-kernel-sim-clock-py)
- [src/gsocialsim/kernel/stimulus_ingestion.py](#src-gsocialsim-kernel-stimulus-ingestion-py)
- [src/gsocialsim/kernel/world_context.py](#src-gsocialsim-kernel-world-context-py)
- [src/gsocialsim/kernel/world_kernel.py](#src-gsocialsim-kernel-world-kernel-py)
- [src/gsocialsim/kernel/world_kernel_step.py](#src-gsocialsim-kernel-world-kernel-step-py)
- [src/gsocialsim/networks/__init__.py](#src-gsocialsim-networks-init-py)
- [src/gsocialsim/networks/network_layer.py](#src-gsocialsim-networks-network-layer-py)
- [src/gsocialsim/physical/__init__.py](#src-gsocialsim-physical-init-py)
- [src/gsocialsim/physical/physical_world.py](#src-gsocialsim-physical-physical-world-py)
- [src/gsocialsim/policy/__init__.py](#src-gsocialsim-policy-init-py)
- [src/gsocialsim/policy/action_policy.py](#src-gsocialsim-policy-action-policy-py)
- [src/gsocialsim/policy/bandit_learner.py](#src-gsocialsim-policy-bandit-learner-py)
- [src/gsocialsim/social/__init__.py](#src-gsocialsim-social-init-py)
- [src/gsocialsim/social/global_social_reality.py](#src-gsocialsim-social-global-social-reality-py)
- [src/gsocialsim/social/relationship_vector.py](#src-gsocialsim-social-relationship-vector-py)
- [src/gsocialsim/stimuli/__init__.py](#src-gsocialsim-stimuli-init-py)
- [src/gsocialsim/stimuli/content_item.py](#src-gsocialsim-stimuli-content-item-py)
- [src/gsocialsim/stimuli/data_source.py](#src-gsocialsim-stimuli-data-source-py)
- [src/gsocialsim/stimuli/interaction.py](#src-gsocialsim-stimuli-interaction-py)
- [src/gsocialsim/stimuli/stimulus.py](#src-gsocialsim-stimuli-stimulus-py)
- [src/gsocialsim/types.py](#src-gsocialsim-types-py)
- [src/gsocialsim/visualization/__init__.py](#src-gsocialsim-visualization-init-py)
- [src/gsocialsim/visualization/exporter.py](#src-gsocialsim-visualization-exporter-py)
- [src/gsocialsim/visualization/exporter_agents_only.py](#src-gsocialsim-visualization-exporter-agents-only-py)
- [src/gsocialsim/visualization/exporter_agents_platform.py](#src-gsocialsim-visualization-exporter-agents-platform-py)
- [src/gsocialsim/visualization/exporter_bipartite.py](#src-gsocialsim-visualization-exporter-bipartite-py)
- [src/gsocialsim/visualization/exporter_full.py](#src-gsocialsim-visualization-exporter-full-py)
- [src/gsocialsim/visualization/exporter_threshold.py](#src-gsocialsim-visualization-exporter-threshold-py)
- [stimuli.csv](#stimuli-csv)
- [tests/test_attention_system.py](#tests-test-attention-system-py)
- [tests/test_belief_model.py](#tests-test-belief-model-py)
- [tests/test_daily_consolidation_and_consumption.py](#tests-test-daily-consolidation-and-consumption-py)
- [tests/test_event_system.py](#tests-test-event-system-py)
- [tests/test_learning_policy.py](#tests-test-learning-policy-py)
- [tests/test_phase1.py](#tests-test-phase1-py)
- [tests/test_phase10.py](#tests-test-phase10-py)
- [tests/test_phase2.py](#tests-test-phase2-py)
- [tests/test_phase3.py](#tests-test-phase3-py)
- [tests/test_phase4.py](#tests-test-phase4-py)
- [tests/test_phase5.py](#tests-test-phase5-py)
- [tests/test_phase6.py](#tests-test-phase6-py)
- [tests/test_phase7.py](#tests-test-phase7-py)
- [tests/test_phase8.py](#tests-test-phase8-py)
- [threshold.html](#threshold-html)

## 📂 Project Structure

```
📁 diagrams/
    📄 agent_runtime_state_machine.uml
    📄 class_diagram.uml
    📄 component_diagram.uml
    📄 sequence_diagram.uml
📁 requirements/
📁 src/
    📁 gsocialsim/
        📁 agents/
            📄 __init__.py
            📄 agent.py
            📄 attention_system.py
            📄 belief_state.py
            📄 belief_update_engine.py
            📄 budget_state.py
            📄 emotion_state.py
            📄 identity_state.py
            📄 impression.py
            📄 reward_weights.py
        📁 analytics/
            📄 __init__.py
            📄 analytics.py
            📄 attribution.py
        📁 evolution/
            📄 __init__.py
            📄 evolutionary_system.py
        📁 kernel/
            📄 __init__.py
            📄 event_scheduler.py
            📄 events.py
            📄 sim_clock.py
            📄 stimulus_ingestion.py
            📄 world_context.py
            📄 world_kernel.py
            📄 world_kernel_step.py
        📁 networks/
            📄 __init__.py
            📄 network_layer.py
        📁 physical/
            📄 __init__.py
            📄 physical_world.py
        📁 policy/
            📄 __init__.py
            📄 action_policy.py
            📄 bandit_learner.py
        📁 social/
            📄 __init__.py
            📄 global_social_reality.py
            📄 relationship_vector.py
        📁 stimuli/
            📄 __init__.py
            📄 content_item.py
            📄 data_source.py
            📄 interaction.py
            📄 stimulus.py
        📁 visualization/
            📄 __init__.py
            📄 exporter.py
            📄 exporter_agents_only.py
            📄 exporter_agents_platform.py
            📄 exporter_bipartite.py
            📄 exporter_full.py
            📄 exporter_threshold.py
        📄 __init__.py
        📄 types.py
    📁 gsocialsim.egg-info/
        📄 dependency_links.txt
        📄 PKG-INFO
        📄 SOURCES.txt
        📄 top_level.txt
📁 tests/
    📄 test_attention_system.py
    📄 test_belief_model.py
    📄 test_daily_consolidation_and_consumption.py
    📄 test_event_system.py
    📄 test_learning_policy.py
    📄 test_phase1.py
    📄 test_phase10.py
    📄 test_phase2.py
    📄 test_phase3.py
    📄 test_phase4.py
    📄 test_phase5.py
    📄 test_phase6.py
    📄 test_phase7.py
    📄 test_phase8.py
📄 agents_only.html
📄 bipartite.html
📄 fix_event_phase_init.patch
📄 gsocialsim-logo.png
📄 influence_graph.html
📄 LICENSE
📄 phase_patch.py
📄 platform.html
📄 PRD.md
📄 project.md
📄 pyproject.toml
📄 README.md
📄 requirements.txt
📄 run_and_visualize.py
📄 run_stimulus_sim.py
📄 stimuli.csv
📄 threshold.html
```

## `.gitignore`

```text
# Python build artifacts
__pycache__/
*.py[cod]
*.pyo

# Packaging / distribution
build/
dist/
*.egg-info/
.eggs/

# Virtual environments
.venv/
venv/
.env/
.gsocialsim/

# Editor / OS junk
.vscode/
.idea/
.DS_Store

# Egg info
*.egg-info/

```

## `LICENSE`

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to an whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

## `PRD.md`

```markdown
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

### 4.3 Budgets (Unequal by Design)

Each agent has daily budgets drawn from heavy-tailed distributions:
- `attention_minutes`
- `action_budget`
- `deep_focus_budget`
- `risk_budget`

Budgets regenerate daily with fatigue and carryover effects.

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


```

## `README.md`

```markdown
# gsocialsim — Synthetic Social Ecology Simulator

<p align="center">
  <img src="gsocialsim-logo.png" alt="gsocialsim logo" width="520"/>
</p>

<p align="center">
  <b>Monkeys. Bananas. Belief propagation. Influence at scale.</b>
</p>

<p align="center">

<img alt="License" src="https://img.shields.io/github/license/ginkorea/gsocialsim">
<img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue">
<img alt="Repo Size" src="https://img.shields.io/github/repo-size/ginkorea/gsocialsim">
<img alt="Last Commit" src="https://img.shields.io/github/last-commit/ginkorea/gsocialsim">
<img alt="Stars" src="https://img.shields.io/github/stars/ginkorea/gsocialsim?style=social">
<img alt="Forks" src="https://img.shields.io/github/forks/ginkorea/gsocialsim?style=social">
<img alt="Status" src="https://img.shields.io/badge/status-research--active-purple">
<img alt="Domain" src="https://img.shields.io/badge/domain-social--simulation-orange">

</p>

---

**gsocialsim** is a Python research framework for simulating belief formation, influence propagation, and behavioral evolution across synthetic social ecosystems.

It models how beliefs **spread, survive, mutate, and dominate** through:

- network influence
- physical proximity interactions
- personality-driven learning
- resource-bounded attention
- evolutionary selection

Built for computational social science, influence research, and agent-based modeling experiments.

---

# 🧠 What This Simulator Is For

gsocialsim is designed to answer questions like:

- Why do some beliefs spread and others die?
- How does influence actually propagate through a network?
- What role does personality play in persuasion?
- How do offline interactions amplify online influence?
- Which agents become long-term belief winners under selection pressure?
- Who *actually* caused a belief shift?

This is not a toy diffusion model. It is a **multi-layer influence ecology**.

---

# ⚙️ Core Model Concepts

## 👤 Persistent Agents
Agents are long-lived entities with:

- belief vectors
- personality traits
- trust relationships
- finite daily budgets
- adaptive action policies

They learn what works for *them*, not what works globally.

---

## 💰 Budget-Constrained Behavior

Each agent has limited:

- attention budget
- action budget

This forces tradeoffs:

- scroll vs seek
- post vs engage
- online vs physical
- influence vs reinforce

Constraint drives realism.

---

## 🌐 Dual Influence Channels

### Online Layer
- Directed social graph
- Follower / trust weighted edges
- Content exposure + engagement
- Repeated exposure effects

### Physical Layer
- Location + schedule overlap
- High-impact interactions
- Amplified persuasion weight
- Small-world shortcuts

---

## 🎯 Personality-Driven Learning

Agents use contextual bandit learning to decide:

- what actions to take
- which channels to use
- which strategies yield reward

Reward is personality-weighted:

- affiliation
- status
- certainty
- novelty
- reinforcement

---

## 🧬 Evolutionary Dynamics

Population turnover is built in:

- low-fitness agents removed
- high-fitness agents reproduced
- offspring receive mutations
- long-term selective pressure emerges

You get **belief ecosystems**, not snapshots.

---

## 📌 Attributable Belief Crossings

Primary research output:

When an agent belief crosses a defined threshold:

- event is logged
- influence sources are traced
- credit is attributed
- propagation chains are recorded

This produces **causal influence graphs**, not just diffusion traces.

---

# 📊 Visualization

The framework includes an HTML exporter that produces an interactive graph:

- nodes = agents
- color = belief stance
- gray edges = network potential
- red edges = realized influence
- edge weight = influence count

Run:

```bash
python3 run_and_visualize.py
````

Open:

```
influence_graph.html
```

in your browser.

---

# 🚀 Quick Start

## Requirements

* Python 3.10+
* pip

---

## Install

```bash
git clone https://github.com/ginkorea/gsocialsim.git
cd gsocialsim

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Run Demo Simulation

```bash
python3 run_and_visualize.py
```

Outputs:

```
influence_graph.html
```

---

# 🧪 Example Use Cases

* influence campaign modeling
* belief resilience testing
* narrative spread experiments
* network intervention simulation
* algorithmic feed impact studies
* social reinforcement analysis
* evolutionary persuasion dynamics

---

# 🗂 Project Structure

```
gsocialsim/
├── PRD.md
├── README.md
├── requirements.txt
├── run_and_visualize.py
├── src/gsocialsim/
│   ├── agents/
│   ├── analytics/
│   ├── evolution/
│   ├── kernel/
│   ├── networks/
│   ├── physical/
│   ├── policy/
│   ├── social/
│   ├── stimuli/
│   └── visualization/
└── tests/
```

---

# 🔬 Research Orientation

This system is built around:

* reproducible simulation
* explicit event logging
* causal attribution
* configurable policies
* parameterized environments
* testable hypotheses

It is intended as a **research instrument**, not just a demo simulator.

---

# 🐒 Design Philosophy

> All models are wrong.
> Some monkeys are influential.

Minimal magic. Explicit mechanics. Measurable outcomes.

---

# 📜 License

MIT License

See `LICENSE` file.

---

# 🤝 Contributions

Pull requests welcome for:

* new influence models
* policy learners
* attribution methods
* visualization layers
* experiment packs
* benchmark scenarios

Open an issue first for major design changes.

---

# ⚠️ Disclaimer

This framework models influence dynamics.
It does not endorse or support manipulation campaigns.
Use responsibly for research and defensive analysis.


```

## `agents_only.html`

```html
<html>
    <head>
        <meta charset="utf-8">
        
            <script>function neighbourhoodHighlight(params) {
  // console.log("in nieghbourhoodhighlight");
  allNodes = nodes.get({ returnType: "Object" });
  // originalNodes = JSON.parse(JSON.stringify(allNodes));
  // if something is selected:
  if (params.nodes.length > 0) {
    highlightActive = true;
    var i, j;
    var selectedNode = params.nodes[0];
    var degrees = 2;

    // mark all nodes as hard to read.
    for (let nodeId in allNodes) {
      // nodeColors[nodeId] = allNodes[nodeId].color;
      allNodes[nodeId].color = "rgba(200,200,200,0.5)";
      if (allNodes[nodeId].hiddenLabel === undefined) {
        allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }
    var connectedNodes = network.getConnectedNodes(selectedNode);
    var allConnectedNodes = [];

    // get the second degree nodes
    for (i = 1; i < degrees; i++) {
      for (j = 0; j < connectedNodes.length; j++) {
        allConnectedNodes = allConnectedNodes.concat(
          network.getConnectedNodes(connectedNodes[j])
        );
      }
    }

    // all second degree nodes get a different color and their label back
    for (i = 0; i < allConnectedNodes.length; i++) {
      // allNodes[allConnectedNodes[i]].color = "pink";
      allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";
      if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[allConnectedNodes[i]].label =
          allNodes[allConnectedNodes[i]].hiddenLabel;
        allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // all first degree nodes get their own color and their label back
    for (i = 0; i < connectedNodes.length; i++) {
      // allNodes[connectedNodes[i]].color = undefined;
      allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];
      if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[connectedNodes[i]].label =
          allNodes[connectedNodes[i]].hiddenLabel;
        allNodes[connectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // the main node gets its own color and its label back.
    // allNodes[selectedNode].color = undefined;
    allNodes[selectedNode].color = nodeColors[selectedNode];
    if (allNodes[selectedNode].hiddenLabel !== undefined) {
      allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
      allNodes[selectedNode].hiddenLabel = undefined;
    }
  } else if (highlightActive === true) {
    // console.log("highlightActive was true");
    // reset all nodes
    for (let nodeId in allNodes) {
      // allNodes[nodeId].color = "purple";
      allNodes[nodeId].color = nodeColors[nodeId];
      // delete allNodes[nodeId].color;
      if (allNodes[nodeId].hiddenLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
        allNodes[nodeId].hiddenLabel = undefined;
      }
    }
    highlightActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    // console.log("Nothing was selected");
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        // allNodes[nodeId].color = {};
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function filterHighlight(params) {
  allNodes = nodes.get({ returnType: "Object" });
  // if something is selected:
  if (params.nodes.length > 0) {
    filterActive = true;
    let selectedNodes = params.nodes;

    // hiding all nodes and saving the label
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = true;
      if (allNodes[nodeId].savedLabel === undefined) {
        allNodes[nodeId].savedLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }

    for (let i=0; i < selectedNodes.length; i++) {
      allNodes[selectedNodes[i]].hidden = false;
      if (allNodes[selectedNodes[i]].savedLabel !== undefined) {
        allNodes[selectedNodes[i]].label = allNodes[selectedNodes[i]].savedLabel;
        allNodes[selectedNodes[i]].savedLabel = undefined;
      }
    }

  } else if (filterActive === true) {
    // reset all nodes
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = false;
      if (allNodes[nodeId].savedLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].savedLabel;
        allNodes[nodeId].savedLabel = undefined;
      }
    }
    filterActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function selectNode(nodes) {
  network.selectNodes(nodes);
  neighbourhoodHighlight({ nodes: nodes });
  return nodes;
}

function selectNodes(nodes) {
  network.selectNodes(nodes);
  filterHighlight({nodes: nodes});
  return nodes;
}

function highlightFilter(filter) {
  let selectedNodes = []
  let selectedProp = filter['property']
  if (filter['item'] === 'node') {
    let allNodes = nodes.get({ returnType: "Object" });
    for (let nodeId in allNodes) {
      if (allNodes[nodeId][selectedProp] && filter['value'].includes((allNodes[nodeId][selectedProp]).toString())) {
        selectedNodes.push(nodeId)
      }
    }
  }
  else if (filter['item'] === 'edge'){
    let allEdges = edges.get({returnType: 'object'});
    // check if the selected property exists for selected edge and select the nodes connected to the edge
    for (let edge in allEdges) {
      if (allEdges[edge][selectedProp] && filter['value'].includes((allEdges[edge][selectedProp]).toString())) {
        selectedNodes.push(allEdges[edge]['from'])
        selectedNodes.push(allEdges[edge]['to'])
      }
    }
  }
  selectNodes(selectedNodes)
}</script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            
            
            
            
            
            

        
<center>
<h1></h1>
</center>

<!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
<script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
          crossorigin="anonymous"
        />
        <script
          src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf"
          crossorigin="anonymous"
        ></script>


        <center>
          <h1></h1>
        </center>
        <style type="text/css">

             #mynetwork {
                 width: 100%;
                 height: 100vh;
                 background-color: #ffffff;
                 border: 1px solid lightgray;
                 position: relative;
                 float: left;
             }

             

             

             
        </style>
    </head>


    <body>
        <div class="card" style="width: 100%">
            
            
            <div id="mynetwork" class="card-body"></div>
        </div>

        
        

        <script type="text/javascript">

              // initialize global variables.
              var edges;
              var nodes;
              var allNodes;
              var allEdges;
              var nodeColors;
              var originalNodes;
              var network;
              var container;
              var options, data;
              var filter = {
                  item : '',
                  property : '',
                  value : []
              };

              

              

              // This method is responsible for drawing the graph, returns the drawn network
              function drawGraph() {
                  var container = document.getElementById('mynetwork');

                  

                  // parsing and collecting nodes and edges from the python
                  nodes = new vis.DataSet([{"color": "#cccccc", "id": "A", "label": "A", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "B", "label": "B", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "C (Source)", "label": "C (Source)", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "D (Lurker)", "label": "D (Lurker)", "shape": "dot", "size": 18}, {"color": "#555555", "id": "ScienceDaily", "label": "ScienceDaily", "shape": "box", "size": 14, "title": "External actor: ScienceDaily"}, {"color": "#555555", "id": "TrendFeed", "label": "TrendFeed", "shape": "box", "size": 14, "title": "External actor: TrendFeed"}, {"color": "#555555", "id": "NewsOutlet", "label": "NewsOutlet", "shape": "box", "size": 14, "title": "External actor: NewsOutlet"}, {"color": "#555555", "id": "RivalNews", "label": "RivalNews", "shape": "box", "size": 14, "title": "External actor: RivalNews"}]);
                  edges = new vis.DataSet([{"arrows": "to", "color": "#cccccc", "from": "A", "title": "follows", "to": "B", "width": 1}, {"arrows": "to", "color": "#cccccc", "from": "B", "title": "follows", "to": "C (Source)", "width": 1}, {"arrows": "to", "color": "#cccccc", "from": "D (Lurker)", "title": "follows", "to": "A", "width": 1}, {"arrows": "to", "color": "#ff0000", "from": "C (Source)", "title": "Influenced 1 time(s)", "to": "B", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "B", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "ScienceDaily", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "TrendFeed", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "NewsOutlet", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "RivalNews", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "A", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "ScienceDaily", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "TrendFeed", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "NewsOutlet", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "RivalNews", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}]);

                  nodeColors = {};
                  allNodes = nodes.get({ returnType: "Object" });
                  for (nodeId in allNodes) {
                    nodeColors[nodeId] = allNodes[nodeId].color;
                  }
                  allEdges = edges.get({ returnType: "Object" });
                  // adding nodes and edges to the graph
                  data = {nodes: nodes, edges: edges};

                  var options = {"physics": {"enabled": true, "stabilization": {"enabled": true, "iterations": 1200, "fit": true}}};

                  


                  

                  network = new vis.Network(container, data, options);

                  

                  

                  


                  

                  return network;

              }
              drawGraph();
        </script>
    </body>
</html>
```

## `bipartite.html`

```html
<html>
    <head>
        <meta charset="utf-8">
        
            <script>function neighbourhoodHighlight(params) {
  // console.log("in nieghbourhoodhighlight");
  allNodes = nodes.get({ returnType: "Object" });
  // originalNodes = JSON.parse(JSON.stringify(allNodes));
  // if something is selected:
  if (params.nodes.length > 0) {
    highlightActive = true;
    var i, j;
    var selectedNode = params.nodes[0];
    var degrees = 2;

    // mark all nodes as hard to read.
    for (let nodeId in allNodes) {
      // nodeColors[nodeId] = allNodes[nodeId].color;
      allNodes[nodeId].color = "rgba(200,200,200,0.5)";
      if (allNodes[nodeId].hiddenLabel === undefined) {
        allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }
    var connectedNodes = network.getConnectedNodes(selectedNode);
    var allConnectedNodes = [];

    // get the second degree nodes
    for (i = 1; i < degrees; i++) {
      for (j = 0; j < connectedNodes.length; j++) {
        allConnectedNodes = allConnectedNodes.concat(
          network.getConnectedNodes(connectedNodes[j])
        );
      }
    }

    // all second degree nodes get a different color and their label back
    for (i = 0; i < allConnectedNodes.length; i++) {
      // allNodes[allConnectedNodes[i]].color = "pink";
      allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";
      if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[allConnectedNodes[i]].label =
          allNodes[allConnectedNodes[i]].hiddenLabel;
        allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // all first degree nodes get their own color and their label back
    for (i = 0; i < connectedNodes.length; i++) {
      // allNodes[connectedNodes[i]].color = undefined;
      allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];
      if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[connectedNodes[i]].label =
          allNodes[connectedNodes[i]].hiddenLabel;
        allNodes[connectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // the main node gets its own color and its label back.
    // allNodes[selectedNode].color = undefined;
    allNodes[selectedNode].color = nodeColors[selectedNode];
    if (allNodes[selectedNode].hiddenLabel !== undefined) {
      allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
      allNodes[selectedNode].hiddenLabel = undefined;
    }
  } else if (highlightActive === true) {
    // console.log("highlightActive was true");
    // reset all nodes
    for (let nodeId in allNodes) {
      // allNodes[nodeId].color = "purple";
      allNodes[nodeId].color = nodeColors[nodeId];
      // delete allNodes[nodeId].color;
      if (allNodes[nodeId].hiddenLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
        allNodes[nodeId].hiddenLabel = undefined;
      }
    }
    highlightActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    // console.log("Nothing was selected");
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        // allNodes[nodeId].color = {};
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function filterHighlight(params) {
  allNodes = nodes.get({ returnType: "Object" });
  // if something is selected:
  if (params.nodes.length > 0) {
    filterActive = true;
    let selectedNodes = params.nodes;

    // hiding all nodes and saving the label
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = true;
      if (allNodes[nodeId].savedLabel === undefined) {
        allNodes[nodeId].savedLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }

    for (let i=0; i < selectedNodes.length; i++) {
      allNodes[selectedNodes[i]].hidden = false;
      if (allNodes[selectedNodes[i]].savedLabel !== undefined) {
        allNodes[selectedNodes[i]].label = allNodes[selectedNodes[i]].savedLabel;
        allNodes[selectedNodes[i]].savedLabel = undefined;
      }
    }

  } else if (filterActive === true) {
    // reset all nodes
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = false;
      if (allNodes[nodeId].savedLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].savedLabel;
        allNodes[nodeId].savedLabel = undefined;
      }
    }
    filterActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function selectNode(nodes) {
  network.selectNodes(nodes);
  neighbourhoodHighlight({ nodes: nodes });
  return nodes;
}

function selectNodes(nodes) {
  network.selectNodes(nodes);
  filterHighlight({nodes: nodes});
  return nodes;
}

function highlightFilter(filter) {
  let selectedNodes = []
  let selectedProp = filter['property']
  if (filter['item'] === 'node') {
    let allNodes = nodes.get({ returnType: "Object" });
    for (let nodeId in allNodes) {
      if (allNodes[nodeId][selectedProp] && filter['value'].includes((allNodes[nodeId][selectedProp]).toString())) {
        selectedNodes.push(nodeId)
      }
    }
  }
  else if (filter['item'] === 'edge'){
    let allEdges = edges.get({returnType: 'object'});
    // check if the selected property exists for selected edge and select the nodes connected to the edge
    for (let edge in allEdges) {
      if (allEdges[edge][selectedProp] && filter['value'].includes((allEdges[edge][selectedProp]).toString())) {
        selectedNodes.push(allEdges[edge]['from'])
        selectedNodes.push(allEdges[edge]['to'])
      }
    }
  }
  selectNodes(selectedNodes)
}</script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            
            
            
            
            
            

        
<center>
<h1></h1>
</center>

<!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
<script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
          crossorigin="anonymous"
        />
        <script
          src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf"
          crossorigin="anonymous"
        ></script>


        <center>
          <h1></h1>
        </center>
        <style type="text/css">

             #mynetwork {
                 width: 100%;
                 height: 100vh;
                 background-color: #ffffff;
                 border: 1px solid lightgray;
                 position: relative;
                 float: left;
             }

             

             

             
        </style>
    </head>


    <body>
        <div class="card" style="width: 100%">
            
            
            <div id="mynetwork" class="card-body"></div>
        </div>

        
        

        <script type="text/javascript">

              // initialize global variables.
              var edges;
              var nodes;
              var allNodes;
              var allEdges;
              var nodeColors;
              var originalNodes;
              var network;
              var container;
              var options, data;
              var filter = {
                  item : '',
                  property : '',
                  value : []
              };

              

              

              // This method is responsible for drawing the graph, returns the drawn network
              function drawGraph() {
                  var container = document.getElementById('mynetwork');

                  

                  // parsing and collecting nodes and edges from the python
                  nodes = new vis.DataSet([{"color": "#cccccc", "id": "A", "label": "A", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "B", "label": "B", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "C (Source)", "label": "C (Source)", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "D (Lurker)", "label": "D (Lurker)", "shape": "dot", "size": 18}, {"color": "#00cc66", "id": "news1", "label": "news1", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "sci1", "label": "sci1", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}, {"color": "#00cc66", "id": "sci2", "label": "sci2", "shape": "square", "size": 16, "title": "Source: UniLab"}, {"color": "#00cc66", "id": "sci3", "label": "sci3", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}, {"color": "#00cc66", "id": "sci4", "label": "sci4", "shape": "square", "size": 16, "title": "Source: UniLab"}, {"color": "#00cc66", "id": "sci5", "label": "sci5", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}, {"color": "#00cc66", "id": "pol1", "label": "pol1", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "pol2", "label": "pol2", "shape": "square", "size": 16, "title": "Source: RivalNews"}, {"color": "#00cc66", "id": "news2", "label": "news2", "shape": "square", "size": 16, "title": "Source: RivalNews"}, {"color": "#00cc66", "id": "pol3", "label": "pol3", "shape": "square", "size": 16, "title": "Source: CapitolWatch"}, {"color": "#00cc66", "id": "pol4", "label": "pol4", "shape": "square", "size": 16, "title": "Source: CapitolWatch"}, {"color": "#00cc66", "id": "pol5", "label": "pol5", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "eco1", "label": "eco1", "shape": "square", "size": 16, "title": "Source: MarketWire"}, {"color": "#00cc66", "id": "eco2", "label": "eco2", "shape": "square", "size": 16, "title": "Source: MarketWire"}, {"color": "#00cc66", "id": "eco3", "label": "eco3", "shape": "square", "size": 16, "title": "Source: FinBlog"}, {"color": "#00cc66", "id": "eco4", "label": "eco4", "shape": "square", "size": 16, "title": "Source: MarketWire"}, {"color": "#00cc66", "id": "eco5", "label": "eco5", "shape": "square", "size": 16, "title": "Source: FinBlog"}, {"color": "#00cc66", "id": "cult1", "label": "cult1", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "meme1", "label": "meme1", "shape": "square", "size": 16, "title": "Source: UserA"}, {"color": "#00cc66", "id": "cult2", "label": "cult2", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "cult3", "label": "cult3", "shape": "square", "size": 16, "title": "Source: PodcasterX"}, {"color": "#00cc66", "id": "cult4", "label": "cult4", "shape": "square", "size": 16, "title": "Source: PodcasterX"}, {"color": "#00cc66", "id": "cult5", "label": "cult5", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "meme2", "label": "meme2", "shape": "square", "size": 16, "title": "Source: UserB"}, {"color": "#00cc66", "id": "meme3", "label": "meme3", "shape": "square", "size": 16, "title": "Source: UserC"}, {"color": "#00cc66", "id": "meme4", "label": "meme4", "shape": "square", "size": 16, "title": "Source: UserD"}, {"color": "#00cc66", "id": "meme5", "label": "meme5", "shape": "square", "size": 16, "title": "Source: UserE"}, {"color": "#00cc66", "id": "sports1", "label": "sports1", "shape": "square", "size": 16, "title": "Source: SportsDesk"}, {"color": "#00cc66", "id": "sports2", "label": "sports2", "shape": "square", "size": 16, "title": "Source: SportsDesk"}, {"color": "#00cc66", "id": "sports3", "label": "sports3", "shape": "square", "size": 16, "title": "Source: FanAccount"}, {"color": "#00cc66", "id": "sports4", "label": "sports4", "shape": "square", "size": 16, "title": "Source: FanAccount"}, {"color": "#00cc66", "id": "sports5", "label": "sports5", "shape": "square", "size": 16, "title": "Source: SportsDesk"}, {"color": "#00cc66", "id": "sec1", "label": "sec1", "shape": "square", "size": 16, "title": "Source: InfosecNews"}, {"color": "#00cc66", "id": "sec2", "label": "sec2", "shape": "square", "size": 16, "title": "Source: InfosecNews"}, {"color": "#00cc66", "id": "sec3", "label": "sec3", "shape": "square", "size": 16, "title": "Source: ForumUser"}, {"color": "#00cc66", "id": "sec4", "label": "sec4", "shape": "square", "size": 16, "title": "Source: InfosecNews"}, {"color": "#00cc66", "id": "sec5", "label": "sec5", "shape": "square", "size": 16, "title": "Source: ForumUser"}, {"color": "#00cc66", "id": "mix1", "label": "mix1", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "mix2", "label": "mix2", "shape": "square", "size": 16, "title": "Source: RivalNews"}, {"color": "#00cc66", "id": "mix3", "label": "mix3", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "mix4", "label": "mix4", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "mix5", "label": "mix5", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}, {"color": "#555555", "id": "ScienceDaily", "label": "ScienceDaily", "shape": "box", "size": 14, "title": "External actor: ScienceDaily"}, {"color": "#555555", "id": "TrendFeed", "label": "TrendFeed", "shape": "box", "size": 14, "title": "External actor: TrendFeed"}, {"color": "#555555", "id": "NewsOutlet", "label": "NewsOutlet", "shape": "box", "size": 14, "title": "External actor: NewsOutlet"}, {"color": "#555555", "id": "RivalNews", "label": "RivalNews", "shape": "box", "size": 14, "title": "External actor: RivalNews"}]);
                  edges = new vis.DataSet([{"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 27 time(s)", "to": "news1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 157 time(s)", "to": "sci1", "width": 7.0}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "sci3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 26 time(s)", "to": "sci3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 136 time(s)", "to": "news1", "width": 6.197452229299364}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 5 time(s)", "to": "news1", "width": 1.1910828025477707}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 23 time(s)", "to": "sci4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 29 time(s)", "to": "sci2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sci5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 133 time(s)", "to": "pol3", "width": 6.082802547770701}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 32 time(s)", "to": "news2", "width": 2.2229299363057327}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "pol3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 26 time(s)", "to": "pol3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 29 time(s)", "to": "sci1", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "pol2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "eco3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "eco4", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 51 time(s)", "to": "pol1", "width": 2.949044585987261}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "news2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 28 time(s)", "to": "sci2", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "sci1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 29 time(s)", "to": "sci5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "eco3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 30 time(s)", "to": "cult4", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 26 time(s)", "to": "sci2", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "cult5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "meme3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 30 time(s)", "to": "eco4", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "meme2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 22 time(s)", "to": "meme1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 22 time(s)", "to": "meme3", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 26 time(s)", "to": "cult1", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 26 time(s)", "to": "eco4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "eco2", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 25 time(s)", "to": "meme2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "sci2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 25 time(s)", "to": "cult3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "eco2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "meme2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "cult4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "pol4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "meme5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "pol2", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 6 time(s)", "to": "sports2", "width": 1.2292993630573248}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "sports2", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "cult1", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 28 time(s)", "to": "meme4", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "cult3", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 23 time(s)", "to": "pol3", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 30 time(s)", "to": "sports3", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 23 time(s)", "to": "sci1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 26 time(s)", "to": "pol5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 11 time(s)", "to": "sports5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 25 time(s)", "to": "pol4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "mix2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 23 time(s)", "to": "sec5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "eco5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "sec2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "pol2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 25 time(s)", "to": "sci3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sec1", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "cult3", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 12 time(s)", "to": "sports4", "width": 1.4585987261146496}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "pol5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 13 time(s)", "to": "sec5", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 27 time(s)", "to": "sec3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 23 time(s)", "to": "sports4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 13 time(s)", "to": "mix1", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "news2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 27 time(s)", "to": "mix5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "sports3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 29 time(s)", "to": "mix5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "sec1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "meme5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "cult5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sports5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "mix3", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "cult4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sports1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "eco1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 23 time(s)", "to": "sec4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 5 time(s)", "to": "mix1", "width": 1.1910828025477707}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "sec2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "mix4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 23 time(s)", "to": "mix1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "sec1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "cult2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "cult2", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 26 time(s)", "to": "sports5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 26 time(s)", "to": "meme5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 26 time(s)", "to": "cult4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 10 time(s)", "to": "mix3", "width": 1.3821656050955413}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 25 time(s)", "to": "mix3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 23 time(s)", "to": "meme4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sec4", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 13 time(s)", "to": "sec3", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "meme3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "sec2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sec3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 3 time(s)", "to": "mix2", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 26 time(s)", "to": "eco3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 11 time(s)", "to": "sports3", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 23 time(s)", "to": "cult2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 25 time(s)", "to": "eco3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 4 time(s)", "to": "sec5", "width": 1.1528662420382165}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 24 time(s)", "to": "news1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 23 time(s)", "to": "sec4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "sci5", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 3 time(s)", "to": "cult5", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 2 time(s)", "to": "pol4", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 24 time(s)", "to": "eco5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sports4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 27 time(s)", "to": "mix2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "eco5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 11 time(s)", "to": "sports2", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "mix5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 3 time(s)", "to": "pol4", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "meme1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 24 time(s)", "to": "cult5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix4", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "mix3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 2 time(s)", "to": "sec4", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 24 time(s)", "to": "eco2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 25 time(s)", "to": "cult3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 13 time(s)", "to": "sec2", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "meme4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sec5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 27 time(s)", "to": "eco1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 22 time(s)", "to": "cult2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 4 time(s)", "to": "meme1", "width": 1.1528662420382165}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 23 time(s)", "to": "pol2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 3 time(s)", "to": "sports5", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 11 time(s)", "to": "meme5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 1 time(s)", "to": "mix4", "width": 1.0382165605095541}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 1 time(s)", "to": "news2", "width": 1.0382165605095541}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 23 time(s)", "to": "pol5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "eco1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 2 time(s)", "to": "eco5", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 26 time(s)", "to": "sci5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 24 time(s)", "to": "meme1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 25 time(s)", "to": "sports2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 3 time(s)", "to": "sci3", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sec3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 25 time(s)", "to": "sports1", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 22 time(s)", "to": "cult1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "pol5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "from": "A", "title": "Interacted 23 time(s)", "to": "eco2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 11 time(s)", "to": "mix5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 1 time(s)", "to": "sports1", "width": 1.0382165605095541}, {"arrows": "to", "color": "#99ff99", "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "cult1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 10 time(s)", "to": "sec1", "width": 1.3821656050955413}, {"arrows": "to", "color": "#99ff99", "from": "B", "title": "Interacted 10 time(s)", "to": "mix4", "width": 1.3821656050955413}, {"arrows": "to", "color": "#ff0000", "from": "C (Source)", "title": "Influenced 1 time(s)", "to": "B", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "B", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "ScienceDaily", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "TrendFeed", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "NewsOutlet", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "RivalNews", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "A", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "ScienceDaily", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "TrendFeed", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "NewsOutlet", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "RivalNews", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}]);

                  nodeColors = {};
                  allNodes = nodes.get({ returnType: "Object" });
                  for (nodeId in allNodes) {
                    nodeColors[nodeId] = allNodes[nodeId].color;
                  }
                  allEdges = edges.get({ returnType: "Object" });
                  // adding nodes and edges to the graph
                  data = {nodes: nodes, edges: edges};

                  var options = {"physics": {"enabled": false}, "layout": {"hierarchical": {"enabled": true, "direction": "LR", "sortMethod": "directed", "nodeSpacing": 180, "levelSeparation": 220}}};

                  


                  

                  network = new vis.Network(container, data, options);

                  

                  

                  


                  

                  return network;

              }
              drawGraph();
        </script>
    </body>
</html>
```

## `diagrams/agent_runtime_state_machine.uml`

```text
@startuml
title SSES - Agent Runtime State Machine (Scroll vs Seek)

hide empty description

note "Scroll = passive, feed-driven\nSeek = active, goal-directed\nBoth are cheap; neither reasons.\nDeep Focus remains rare + expensive." as N0

[*] --> Boot

state Boot {
  [*] --> Initialize
  Initialize : load identity/beliefs/memory\nseed RNG\ninit budgets + schedules
  Initialize --> Idle
}

state Idle {
  [*] --> Waiting
  Waiting : idle / lurk\nlow compute
}

Idle --> Perceive : tick / event / notification

state Perceive {
  [*] --> GatherPercepts
  GatherPercepts : collect online signals\ncollect physical signals\ncheck internal drives
  GatherPercepts --> DecideIntake
}

state DecideIntake {
  [*] --> IntakeChoice
  IntakeChoice : compute motivation\n(novelty, anxiety,\nidentity threat,\nboredom, intent)
  IntakeChoice --> Scroll : if platform_pull > agency
  IntakeChoice --> Seek : if agency > platform_pull
  IntakeChoice --> Waiting : if attention_minutes <= 0
}

'-------------------------
' Scroll path
'-------------------------
state Scroll {
  [*] --> FeedAdvance
  FeedAdvance : advance ranked feed\ncheap exposure\nlow control
  FeedAdvance --> MakeImpressions
}

'-------------------------
' Seek path
'-------------------------
state Seek {
  [*] --> FormQuery
  FormQuery : select topic / person / group\nidentity- or tension-driven
  FormQuery --> FetchResults
  FetchResults : retrieve matching content\nless volume, higher relevance
  FetchResults --> MakeImpressions
}

'-------------------------
' Shared impression path
'-------------------------
state MakeImpressions {
  [*] --> GenerateImpressions
  GenerateImpressions : create Impression objects\n(valence, arousal,\nstance signal,\ncredibility,\nidentity threat,\nsocial proof)
  GenerateImpressions --> UpdateInternal
}

state UpdateInternal {
  [*] --> ApplyImpressions
  ApplyImpressions : update emotions\nbounded belief deltas\nsalience updates\nlog impressions
  ApplyImpressions --> AllocateAttention
}

state AllocateAttention {
  [*] --> EvaluateTriggers
  EvaluateTriggers : check thresholds\n(identity threat,\nstrong tie,\nphysical amp,\nrepetition)
  EvaluateTriggers --> DeepFocus : if deep_focus_budget > 0 && trigger
  EvaluateTriggers --> SelectIntent : if no trigger
}

state DeepFocus {
  [*] --> Analyze
  Analyze : expensive reasoning\nargument eval / coordination\nmay synthesize action template
  Analyze --> SelectIntent
}

state SelectIntent {
  [*] --> ChooseIntent
  ChooseIntent : status / affiliation /\ndominance / coherence\nsubject to risk_budget
  ChooseIntent --> EvaluateAction
}

state EvaluateAction {
  [*] --> Gate
  Gate : if action_budget <= 0 -> NoOp\nif moderation risk too high -> NoOp\nif low expected reward -> NoOp
  Gate --> Act : if pass
  Gate --> NoOp : if fail
}

state Act {
  [*] --> Execute
  Execute : post / reply / DM /\nphysical engagement\nspend budgets\nreceive feedback
  Execute --> Learn
}

state Learn {
  [*] --> BanditUpdate
  BanditUpdate : contextual bandit update\n(action-template prefs)\nlog reward vector
  BanditUpdate --> ConsolidateMemory
}

state NoOp {
  [*] --> Lurk
  Lurk : no visible action\nstill records exposure
  Lurk --> ConsolidateMemory
}

state ConsolidateMemory {
  [*] --> WriteMemory
  WriteMemory : store exposure history\nrelationship updates\ndecay impressions
  WriteMemory --> CheckBeliefCrossing
}

state CheckBeliefCrossing {
  [*] --> Detect
  Detect : stance/confidence thresholds\nidentity compatibility
  Detect --> Attribute : if crossing_event
  Detect --> EndTick : if none
}

state Attribute {
  [*] --> AssignCredit
  AssignCredit : sliding window 3–14 days\nrecency + tie strength\nphysical multiplier
  AssignCredit --> EndTick
}

state EndTick {
  [*] --> ReturnIdle
  ReturnIdle : decrement budgets\nupdate fatigue
  ReturnIdle --> Idle
}

'-------------------------
' Daily boundary
'-------------------------
Idle --> DailyBoundary : if day_changed

state DailyBoundary {
  [*] --> RegenBudgets
  RegenBudgets : heavy-tailed regen\ncarryover + fatigue
  RegenBudgets --> IdentityConsolidation
}

state IdentityConsolidation {
  [*] --> CompressBeliefs
  CompressBeliefs : compress beliefs\ncap drift
  CompressBeliefs --> ReAnchor
  ReAnchor : stabilize identity
  ReAnchor --> EvolutionCheck
}

state EvolutionCheck {
  [*] --> EvaluateExit
  EvaluateExit : chronic low reward\nstress / isolation / boredom
  EvaluateExit --> Exit : if exit
  EvaluateExit --> Idle : if survive
}

state Exit {
  [*] --> Remove
  Remove : log exit\nremove agent
  Remove --> Replace
}

state Replace {
  [*] --> Newborn
  Newborn : partial inheritance\nmutation\nno memory cloning
  Newborn --> Idle
}

@enduml

```

## `diagrams/class_diagram.uml`

```text
@startuml
title SSES - Core Class Diagram (Full Capability - Subscriptions + Media Weights)

skinparam classAttributeIconSize 0

'========================
' Kernel / Time
'========================
class WorldKernel {
  +seed: long
  +clock: SimClock
  +step(dt: Duration)
  +schedule(e: Event)
  +replay(runId: string)
}

class SimClock {
  +t: long
  +day: int
  +tick: long
  +advance(dt: Duration)
}

abstract class Event {
  +id: string
  +timestamp: long
  +apply(ctx: WorldContext)
}

class EventScheduler {
  +enqueue(e: Event)
  +next(): Event
}

class DeterministicReplay {
  +record(e: Event)
  +load(runId: string)
}

class WorldContext {
  +agents: AgentPopulation
  +gsr: GlobalSocialReality
  +networks: NetworkManager
  +subscriptions: SubscriptionService
  +content: ContentStore
  +physical: PhysicalWorld
  +stimuli: StimulusStore
  +analytics: Analytics
  +rng: RNG
}

WorldKernel --> SimClock
WorldKernel --> EventScheduler
WorldKernel --> DeterministicReplay
WorldKernel --> WorldContext

'========================
' Agents
'========================
class Agent {
  +id: AgentId
  +identity: IdentityState
  +beliefs: BeliefStore
  +emotion: EmotionState
  +budgets: BudgetState
  +personality: RewardWeights
  +memory: MemoryStore
  +attention: AttentionSystem
  +policy: ActionPolicy
  +learn: BanditLearner
  +tick(ctx: WorldContext)
  +perceive(p: Percept)
  +maybeAct(ctx: WorldContext): Action?
  +consolidateDaily(ctx: WorldContext)
}

class AgentPopulation {
  +agents: Map<AgentId, Agent>
  +get(id: AgentId): Agent
  +replace(exited: AgentId, newborn: Agent)
}

class IdentityState {
  +identity_vector: float[8..16]
  +identity_rigidity: float
  +ingroup_labels: Set<String>
  +taboo_boundaries: Set<String>
}

class BeliefStore {
  +topics: Map<TopicId, TopicBelief>
  +get(t: TopicId): TopicBelief
  +update(t: TopicId, delta: BeliefDelta)
}

class TopicBelief {
  +topic: TopicId
  +stance: float  '[-1,+1]
  +confidence: float  '[0,1]
  +salience: float  '[0,1]
  +knowledge: float  '[0,1]
}

class EmotionState {
  +valence: float
  +arousal: float
  +anger: float?
  +anxiety: float?
}

class BudgetState {
  +attention_minutes: float
  +action_budget: float
  +deep_focus_budget: float
  +risk_budget: float
  +regenDaily()
  +spend(kind: BudgetKind, amount: float): bool
}

class RewardWeights {
  +status: float
  +affiliation: float
  +dominance: float
  +coherence: float
  +novelty: float
  +safety: float
  +effortCost: float  'negative
}

AgentPopulation o-- Agent
Agent *-- IdentityState
Agent *-- BeliefStore
Agent *-- EmotionState
Agent *-- BudgetState
Agent *-- RewardWeights

'========================
' Attention: Consumption vs Interaction (Media-weighted)
'========================
class AttentionSystem {
  +scout: ScrollOrSeekner
  +deep: DeepFocusEngine
  +mediaParams: MediaBehaviorModel
  +evaluate(percepts: List<Percept>): List<Impression>
  +shouldDeepFocus(imps: List<Impression>): bool
  +deepFocus(target: ContentItem): DeepResult
}

class ScrollOrSeekner {
  +scan(item: ContentItem): Impression
}

class DeepFocusEngine {
  +analyze(item: ContentItem, ctx: FocusContext): DeepResult
}

enum IntakeMode {
  scroll
  seek
  physical
}

enum MediaType {
  news
  social_post
  video
  meme
  longform
  forum_thread
}

class MediaBehaviorModel {
  +consume_bias: Map<MediaType,float>        '[0,1] baseline read/see/watch
  +interact_bias: Map<MediaType,float>       '[0,1] baseline like/comment/share
  +deep_focus_bias: Map<MediaType,float>     '[0,1] baseline deep focus likelihood
  +action_type_priors: Map<MediaType,Map<InteractionType,float>>
}

class Impression {
  +intake_mode: IntakeMode
  +contentId: ContentId
  +media_type: MediaType
  +topic: TopicId?
  +valence: float
  +arousal: float
  +stance_signal: float
  +credibility: float
  +identity_threat: float
  +social_proof: float
  +source_strength: float
  +consumed_prob: float     '[0,1]
  +interact_prob: float     '[0,1]
  +decay()
}

class DeepResult {
  +arguments: Map<TopicId, float>
  +callToAction: ActionTemplate?
  +coordination: boolean
}

Agent --> AttentionSystem
AttentionSystem --> ScrollOrSeekner
AttentionSystem --> DeepFocusEngine
AttentionSystem --> MediaBehaviorModel

'========================
' Policy + Learning
'========================
class ActionPolicy {
  +selectIntent(a: Agent, ctx: WorldContext): Intent
  +selectActionTemplate(intent: Intent): ActionTemplate
  +instantiate(tpl: ActionTemplate, ctx: WorldContext): Action
  +chooseInteractionType(imp: Impression): InteractionType
}

class BanditLearner {
  +update(context: BanditContext, chosen: ActionTemplate, reward: RewardVector)
  +choose(context: BanditContext, candidates: List<ActionTemplate>): ActionTemplate
}

class RewardVector {
  +status: float
  +affiliation: float
  +dominance: float
  +coherence: float
  +novelty: float
  +safety: float
  +effortCost: float
  +weightedSum(w: RewardWeights): float
}

Agent --> ActionPolicy
Agent --> BanditLearner
BanditLearner --> RewardVector

'========================
' Social Reality + Online Networks
'========================
class GlobalSocialReality {
  +R: Map<Pair<AgentId,AgentId>, RelationshipVector>
  +get(u: AgentId, v: AgentId): RelationshipVector
  +update(u: AgentId, v: AgentId, delta: RelDelta)
}

class RelationshipVector {
  +affinity: float
  +trust: float
  +intimacy: float
  +conflict: float
  +reciprocity: float
  +status_delta: float
  +topic_alignment: Map<TopicId,float>
}

'---- Subscriptions (opt-in feed semantics)
enum SubscriptionType {
  creator
  topic
  outlet
  community
}

class Subscription {
  +subscriber: AgentId
  +type: SubscriptionType
  +targetId: String      'CreatorId / TopicId / OutletId / CommunityId
  +strength: float       '[0,1] how strongly opted-in
  +created_tick: long
}

class SubscriptionService {
  +subs_by_agent: Map<AgentId,List<Subscription>>
  +subscribers_by_target: Map<Pair<SubscriptionType,String>,Set<AgentId>>
  +getSubs(a: AgentId): List<Subscription>
  +isSubscribed(a: AgentId, type: SubscriptionType, targetId: String): bool
  +subscribe(a: AgentId, type: SubscriptionType, targetId: String, strength: float)
  +unsubscribe(a: AgentId, type: SubscriptionType, targetId: String)
}

'---- Content + delivery pipeline
class ContentStore {
  +content_by_id: Map<ContentId,ContentItem>
  +recent_by_author: Map<AgentId,Deque<ContentId>>
  +recent_by_topic: Map<TopicId,Deque<ContentId>>
  +recent_by_outlet: Map<OutletId,Deque<ContentId>>
  +add(item: ContentItem)
  +get(id: ContentId): ContentItem
  +queryByAuthor(a: AgentId, sinceTick: long): List<ContentId>
  +queryByTopic(t: TopicId, sinceTick: long): List<ContentId>
}

class DeliveryRecord {
  +tick: long
  +viewer: AgentId
  +layer_id: NetworkId
  +intake_mode: IntakeMode
  +eligible: List<ContentId>
  +shown: List<ContentId>
  +seen: List<ContentId>
  +media_breakdown: Map<MediaType,int>
}

abstract class NetworkLayer {
  +id: NetworkId
  +mechanics: PlatformMechanics
  +publish(interaction: Interaction, ctx: WorldContext)
  +deliver(viewer: AgentId, intake: IntakeMode, ctx: WorldContext): List<ContentItem>
}

class BroadcastFeedNetwork {
  +candidateWindowTicks: long
  +maxCandidates: int
  +maxShown: int
  +buildCandidates(viewer: AgentId, subs: List<Subscription>, ctx: WorldContext): List<ContentId>
  +rank(viewer: AgentId, candidates: List<ContentId>, ctx: WorldContext): List<ContentId>
}

class DirectMessageNetwork {
  +inboxes: Map<AgentId,Deque<ContentId>>
  +send(from: AgentId, to: AgentId, item: ContentItem)
  +deliver(viewer: AgentId, intake: IntakeMode, ctx: WorldContext): List<ContentItem>
}

class PlatformMechanics {
  +visibilityRules: VisibilityRules
  +rankingModel: RankingModel
  +riskProfile: RiskProfile
  +rewardMapping: RewardMapping
  +mediaPolicy: MediaPolicy
}

class MediaPolicy {
  +media_behavior: MediaBehaviorModel
  +format_costs: Map<MediaType,float>    'effort to produce
  +friction: Map<InteractionType,Map<MediaType,float>>  'UI friction
}

class NetworkManager {
  +layers: Map<NetworkId,NetworkLayer>
  +getLayer(id: NetworkId): NetworkLayer
}

NetworkLayer <|-- BroadcastFeedNetwork
NetworkLayer <|-- DirectMessageNetwork
NetworkLayer *-- PlatformMechanics
NetworkManager o-- NetworkLayer

WorldContext --> SubscriptionService
WorldContext --> ContentStore
BroadcastFeedNetwork --> SubscriptionService : expand subscriptions into candidates
BroadcastFeedNetwork --> ContentStore : retrieve content
BroadcastFeedNetwork --> GlobalSocialReality : trust/affinity signals
DirectMessageNetwork --> ContentStore

Agent --> GlobalSocialReality : updates via interactions

'========================
' Physical Layer
'========================
class PhysicalWorld {
  +places: Map<PlaceId, Place>
  +schedules: Map<AgentId, Schedule>
  +generateInteractions(day: int): List<PhysicalInteraction>
}

class Place {
  +id: PlaceId
  +size: int
  +mixingRate: float
  +norms: NormProfile
  +topicBias: Map<TopicId,float>
}

class Schedule {
  +memberships: List<PlaceId>
  +dailyPlan(day: int): List<PlaceVisit>
}

class PlaceVisit {
  +placeId: PlaceId
  +start: long
  +end: long
}

class PhysicalInteraction {
  +participants: List<AgentId>
  +topic: TopicId?
  +type: InteractionType
  +intensity: float
  +applyInfluence(gsr: GlobalSocialReality)
}

PhysicalWorld o-- Place
PhysicalWorld o-- Schedule
Schedule o-- PlaceVisit
PhysicalWorld --> PhysicalInteraction
PhysicalInteraction --> GlobalSocialReality

'========================
' Stimuli + Content
'========================
class StimulusStore {
  +items: List<ExternalStimulus>
  +getAt(t: long): List<ExternalStimulus>
}

class ExternalStimulus {
  +id: StimulusId
  +timestamp: long
  +source: String
  +payload: bytes
}

class ProvenanceTransformer {
  +transform(s: ExternalStimulus): List<ContentItem>
}

class ContentItem {
  +id: ContentId
  +timestamp: long
  +author: AgentId?
  +outlet: OutletId?
  +community: CommunityId?
  +media_type: MediaType
  +topics: List<TopicId>
  +stance: float?
  +emotionDerivative: float?
  +provenance: ProvenanceRecord
  +engagement: EngagementCounters
}

class EngagementCounters {
  +views: int
  +likes: int
  +reshares: int
  +replies: int
  +bookmarks: int
}

class ProvenanceRecord {
  +rootStimulusId: StimulusId
  +transformChain: List<String>
}

StimulusStore o-- ExternalStimulus
ProvenanceTransformer --> ContentItem
ContentItem *-- ProvenanceRecord
ContentItem *-- EngagementCounters
WorldContext --> StimulusStore

'========================
' Belief Update + Crossing + Attribution (unchanged)
'========================
class BeliefUpdateEngine {
  +update(a: Agent, imp: Impression, ctx: WorldContext): BeliefDelta
  +boundedAdjust(b: TopicBelief, delta: BeliefDelta): TopicBelief
}

class BeliefCrossingDetector {
  +check(a: Agent, topic: TopicId, before: TopicBelief, after: TopicBelief): BeliefCrossingEvent?
}

class AttributionEngine {
  +windowDaysMin: int
  +windowDaysMax: int
  +assignCredit(e: BeliefCrossingEvent, history: ExposureHistory): AttributionSet
}

class ExposureHistory {
  +events: List<ExposureEvent>
  +query(a: AgentId, topic: TopicId, since: long): List<ExposureEvent>
}

class ExposureEvent {
  +timestamp: long
  +agent: AgentId
  +contentId: ContentId
  +sourceActor: ActorId
  +channel: ChannelType
  +tieStrength: float
  +intake_mode: IntakeMode
  +media_type: MediaType
}

class BeliefCrossingEvent {
  +id: string
  +timestamp: long
  +agent: AgentId
  +topic: TopicId
  +prior: TopicBelief
  +after: TopicBelief
  +attribution: AttributionSet
}

class AttributionSet { +credits: List<AttributionCredit> }

class AttributionCredit {
  +source: ActorId
  +weight: float
  +channelMultiplier: float
  +recencyWeight: float
}

Agent --> BeliefUpdateEngine
BeliefUpdateEngine --> BeliefCrossingDetector
BeliefCrossingDetector --> BeliefCrossingEvent
AttributionEngine --> AttributionSet
ExposureHistory o-- ExposureEvent
BeliefCrossingEvent *-- AttributionSet
AttributionSet o-- AttributionCredit

'========================
' Analytics + Logging (add delivery + media metrics)
'========================
class Analytics {
  +logDelivery(r: DeliveryRecord)
  +logExposure(e: ExposureEvent)
  +logImpression(i: Impression)
  +logAction(a: Action)
  +logReward(r: RewardVector)
  +logBeliefUpdate(d: BeliefDelta)
  +logCrossing(e: BeliefCrossingEvent)
  +reportMetrics(): MetricsReport
}

Analytics --> DeliveryRecord
Analytics --> ExposureEvent
Analytics --> Impression

@enduml

```

## `diagrams/component_diagram.uml`

```text
@startuml
title SSES - Component Diagram (Full Capability - Subscriptions + Media Weights)

skinparam componentStyle rectangle

component "World Kernel" as WK
component "Event Scheduler" as ES
component "Deterministic Replay" as DR

component "Agent Engine" as AE
component "Agent Runtime Loop" as ARL
component "Memory System" as MS
component "Attention System
(Consume + Interact + Deep Focus)
(Media-weighted)" as ATTN
component "Policy + Learning
(Intent + Action Selection)" as LEARN

component "Global Social Reality
(Latent R_uv)" as GSR

component "Online Network System" as ONS
component "Network Manager" as NM
component "Subscription Service" as SUBS
component "Content Store" as CS
component "Broadcast Feed Network
(Subscription-driven)" as BF
component "Direct Message Network" as DM
component "Platform Mechanics
(Visibility + Ranking + Media Policy)" as PM

component "Physical Layer" as PHY
component "Places + Schedules" as PS
component "Proximity Interaction Generator" as PIG

component "Stimulus Ingestion
(Read-only Exogenous)" as SI
component "Provenance Transformer
(Publisher/Influencer framing)" as PT

component "Belief & Identity System" as BIS
component "Belief Update Engine" as BUE
component "Identity Consolidation" as IC
component "Belief Crossing + Attribution" as BCA

component "Moderation & Institutions" as MI
component "Moderation Engine" as MOD
component "Institutional Actors
(Publishers/Influencers)" as IA

component "Evolutionary System (GA)" as GA
component "Exit + Replacement" as ER
component "Mutation + Inheritance" as MU

component "Analytics + Logging" as AL
component "Event Logs" as LOGS
component "Metrics + Reports
(Delivery + Media KPIs)" as MET

WK --> ES
WK --> DR
WK --> AE
WK --> ONS
WK --> PHY
WK --> SI
WK --> MI
WK --> GA
WK --> AL

AE --> ARL
AE --> MS
AE --> ATTN
AE --> LEARN
AE --> BIS

ONS --> NM
ONS --> SUBS
ONS --> CS
NM --> BF
NM --> DM
BF --> PM
DM --> PM
BF --> GSR

SUBS --> BF
CS --> BF
CS --> DM
PT --> CS

PHY --> PS
PHY --> PIG
PHY --> GSR

SI --> PT
PT --> BF
PT --> IA

MI --> MOD
MI --> IA
MOD --> PM
PM --> BF
PM --> DM

BIS --> BUE
BIS --> IC
BIS --> BCA
BUE --> GSR
BCA --> AL

GA --> ER
GA --> MU
ER --> AE

AL --> LOGS
AL --> MET
BF --> AL : delivery records
ATTN --> AL : impressions + consume/interact

@enduml

```

## `diagrams/sequence_diagram.uml`

```text
@startuml
title SSES - Per-Tick Sequence (Full Capability: Subscriptions + Media-weighted Consume/Interact)

autonumber
hide footbox

actor "Scenario/Stimuli" as SCN

participant "WorldKernel" as WK
participant "EventScheduler" as ES
participant "WorldContext" as CTX
participant "StimulusStore" as SS
participant "ProvenanceTransformer" as PT
participant "ContentStore" as CS
participant "SubscriptionService" as SUBS
participant "NetworkManager" as NM
participant "BroadcastFeedNetwork" as BF
participant "DirectMessageNetwork" as DM
participant "AgentPopulation" as POP
participant "Agent" as A
participant "AttentionSystem" as ATTN
participant "MediaBehaviorModel" as MBM
participant "BeliefUpdateEngine" as BUE
participant "ActionPolicy" as POL
participant "GlobalSocialReality" as GSR
participant "Analytics" as AL

== Tick Start / Scheduled Events ==
WK -> ES: nextEvents(tick)
ES --> WK: [events]
loop for each event
  WK -> ES: apply(e, CTX)
end

== Exogenous Stimuli Ingestion (Read-only) ==
WK -> SS: getAt(tick)
SS --> WK: [stimuli]
loop for each stimulus
  WK -> PT: transform(stimulus)
  PT --> WK: [ContentItem*] (with MediaType, Topics, Provenance)
  loop for each content
    WK -> CS: add(content)
  end
end

== Agents Act (Create / Reply / Like / Reshare / DM) ==
WK -> POP: agents()
POP --> WK: [agents]

loop for each agent (actor)
  WK -> A: tick(CTX)
  note right of A
    Agent tick includes:
    - perceive() from last deliveries (cached)
    - maybeAct() to produce an Action/Interaction
  end note
  A -> POL: selectIntent(A, CTX)
  POL --> A: intent
  A -> POL: instantiate(intent -> Action)
  POL --> A: action
  alt action produced
    A -> AL: logAction(action)
    A -> GSR: update(u,v) (relationship deltas from action)
    A -> NM: publish(action.interaction, CTX)
  else no action
  end
end

== Network Publish: materialize into ContentStore and Layer State ==
NM -> BF: publish(interaction, CTX)
alt interaction contains new content (CREATE/REPLY)
  BF -> CS: add(ContentItem)
else engagement action (LIKE/RESHARE)
  BF -> CS: update engagement counters
end

NM -> DM: publish(interaction, CTX)
alt DM message
  DM -> CS: add(ContentItem)
  DM -> DM: enqueue(inbox[to], contentId)
end

== Online Delivery: Subscription-driven Broadcast Feed ==
loop for each viewer agent (consumer)
  WK -> SUBS: getSubs(viewer)
  SUBS --> WK: [Subscription*]

  WK -> BF: deliver(viewer, intake=scroll, CTX)
  activate BF
  BF -> SUBS: getSubs(viewer)  'optional internal call
  BF -> CS: queryByAuthor(subscribed_creators, sinceTick)
  BF -> CS: queryByTopic(subscribed_topics, sinceTick)
  BF -> CS: queryByOutlet(subscribed_outlets, sinceTick)
  BF -> GSR: get(viewer, author) (trust/affinity signals)
  BF -> MBM: consume_bias(mediaType), interact_bias(mediaType)
  BF --> WK: [ranked ContentItem*] + DeliveryRecord(eligible/shown)
  deactivate BF

  WK -> AL: logDelivery(DeliveryRecord)

  == Perception: Consume vs Interact (Media-weighted) ==
  loop for each delivered content
    WK -> A: perceive(Percept{contentId, layer=BF, intake=scroll})
    A -> ATTN: evaluate(percepts)
    activate ATTN
    ATTN -> MBM: lookup media biases + action priors
    ATTN --> A: [Impression*] (consumed_prob, interact_prob, intake_mode)
    deactivate ATTN

    A -> AL: logImpression(Impression)
    alt consumed
      A -> BUE: update(A, Impression, CTX)
      BUE --> A: BeliefDelta
      A -> AL: logBeliefUpdate(BeliefDelta)
    else not consumed
      note right of A: exposure logged but no belief update
    end
  end
end

== Online Delivery: Direct Messages ==
loop for each viewer agent
  WK -> DM: deliver(viewer, intake=seek, CTX)
  DM --> WK: [DM ContentItem*] + DeliveryRecord
  WK -> AL: logDelivery(DeliveryRecord)

  loop for each DM content
    WK -> A: perceive(Percept{contentId, layer=DM, intake=seek})
    A -> ATTN: evaluate(percepts)
    ATTN -> MBM: lookup biases
    ATTN --> A: Impression
    A -> AL: logImpression(Impression)
    alt consumed
      A -> BUE: update(A, Impression, CTX)
      BUE --> A: BeliefDelta
      A -> AL: logBeliefUpdate(BeliefDelta)
    end
  end
end

== Tick End ==
WK -> AL: reportMetrics()  'optional periodic

@enduml

```

## `fix_event_phase_init.patch`

```text
*** Begin Patch
*** Update File: src/gsocialsim/kernel/events.py
@@
 class Event(ABC):
     timestamp: int = field(compare=True)
-    phase: int = field(default=int(EventPhase.ACT), compare=True)
+    phase: int = field(default=int(EventPhase.ACT), init=False, compare=True)
@@
 class StimulusIngestionEvent(Event):
-    phase: int = field(default=int(EventPhase.INGEST), compare=True)
+    phase: int = field(default=int(EventPhase.INGEST), init=False, compare=True)
@@
 class StimulusPerceptionEvent(Event):
-    phase: int = field(default=int(EventPhase.PERCEIVE), compare=True)
+    phase: int = field(default=int(EventPhase.PERCEIVE), init=False, compare=True)
@@
 class AgentActionEvent(Event):
-    phase: int = field(default=int(EventPhase.ACT), compare=True)
+    phase: int = field(default=int(EventPhase.ACT), init=False, compare=True)
@@
 class InteractionPerceptionEvent(Event):
-    phase: int = field(default=int(EventPhase.INTERACT_PERCEIVE), compare=True)
+    phase: int = field(default=int(EventPhase.INTERACT_PERCEIVE), init=False, compare=True)
@@
 class DeepFocusEvent(Event):
-    phase: int = field(default=int(EventPhase.DEEP_FOCUS), compare=True)
+    phase: int = field(default=int(EventPhase.DEEP_FOCUS), init=False, compare=True)
@@
 class AllocateAttentionEvent(Event):
-    phase: int = field(default=int(EventPhase.ALLOCATE_ATTENTION), compare=True)
+    phase: int = field(default=int(EventPhase.ALLOCATE_ATTENTION), init=False, compare=True)
@@
 class DayBoundaryEvent(Event):
-    phase: int = field(default=int(EventPhase.DAY_BOUNDARY), compare=True)
+    phase: int = field(default=int(EventPhase.DAY_BOUNDARY), init=False, compare=True)
*** End Patch

```

## `influence_graph.html`

```html
<html>
    <head>
        <meta charset="utf-8">
        
            <script>function neighbourhoodHighlight(params) {
  // console.log("in nieghbourhoodhighlight");
  allNodes = nodes.get({ returnType: "Object" });
  // originalNodes = JSON.parse(JSON.stringify(allNodes));
  // if something is selected:
  if (params.nodes.length > 0) {
    highlightActive = true;
    var i, j;
    var selectedNode = params.nodes[0];
    var degrees = 2;

    // mark all nodes as hard to read.
    for (let nodeId in allNodes) {
      // nodeColors[nodeId] = allNodes[nodeId].color;
      allNodes[nodeId].color = "rgba(200,200,200,0.5)";
      if (allNodes[nodeId].hiddenLabel === undefined) {
        allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }
    var connectedNodes = network.getConnectedNodes(selectedNode);
    var allConnectedNodes = [];

    // get the second degree nodes
    for (i = 1; i < degrees; i++) {
      for (j = 0; j < connectedNodes.length; j++) {
        allConnectedNodes = allConnectedNodes.concat(
          network.getConnectedNodes(connectedNodes[j])
        );
      }
    }

    // all second degree nodes get a different color and their label back
    for (i = 0; i < allConnectedNodes.length; i++) {
      // allNodes[allConnectedNodes[i]].color = "pink";
      allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";
      if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[allConnectedNodes[i]].label =
          allNodes[allConnectedNodes[i]].hiddenLabel;
        allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // all first degree nodes get their own color and their label back
    for (i = 0; i < connectedNodes.length; i++) {
      // allNodes[connectedNodes[i]].color = undefined;
      allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];
      if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[connectedNodes[i]].label =
          allNodes[connectedNodes[i]].hiddenLabel;
        allNodes[connectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // the main node gets its own color and its label back.
    // allNodes[selectedNode].color = undefined;
    allNodes[selectedNode].color = nodeColors[selectedNode];
    if (allNodes[selectedNode].hiddenLabel !== undefined) {
      allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
      allNodes[selectedNode].hiddenLabel = undefined;
    }
  } else if (highlightActive === true) {
    // console.log("highlightActive was true");
    // reset all nodes
    for (let nodeId in allNodes) {
      // allNodes[nodeId].color = "purple";
      allNodes[nodeId].color = nodeColors[nodeId];
      // delete allNodes[nodeId].color;
      if (allNodes[nodeId].hiddenLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
        allNodes[nodeId].hiddenLabel = undefined;
      }
    }
    highlightActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    // console.log("Nothing was selected");
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        // allNodes[nodeId].color = {};
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function filterHighlight(params) {
  allNodes = nodes.get({ returnType: "Object" });
  // if something is selected:
  if (params.nodes.length > 0) {
    filterActive = true;
    let selectedNodes = params.nodes;

    // hiding all nodes and saving the label
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = true;
      if (allNodes[nodeId].savedLabel === undefined) {
        allNodes[nodeId].savedLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }

    for (let i=0; i < selectedNodes.length; i++) {
      allNodes[selectedNodes[i]].hidden = false;
      if (allNodes[selectedNodes[i]].savedLabel !== undefined) {
        allNodes[selectedNodes[i]].label = allNodes[selectedNodes[i]].savedLabel;
        allNodes[selectedNodes[i]].savedLabel = undefined;
      }
    }

  } else if (filterActive === true) {
    // reset all nodes
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = false;
      if (allNodes[nodeId].savedLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].savedLabel;
        allNodes[nodeId].savedLabel = undefined;
      }
    }
    filterActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function selectNode(nodes) {
  network.selectNodes(nodes);
  neighbourhoodHighlight({ nodes: nodes });
  return nodes;
}

function selectNodes(nodes) {
  network.selectNodes(nodes);
  filterHighlight({nodes: nodes});
  return nodes;
}

function highlightFilter(filter) {
  let selectedNodes = []
  let selectedProp = filter['property']
  if (filter['item'] === 'node') {
    let allNodes = nodes.get({ returnType: "Object" });
    for (let nodeId in allNodes) {
      if (allNodes[nodeId][selectedProp] && filter['value'].includes((allNodes[nodeId][selectedProp]).toString())) {
        selectedNodes.push(nodeId)
      }
    }
  }
  else if (filter['item'] === 'edge'){
    let allEdges = edges.get({returnType: 'object'});
    // check if the selected property exists for selected edge and select the nodes connected to the edge
    for (let edge in allEdges) {
      if (allEdges[edge][selectedProp] && filter['value'].includes((allEdges[edge][selectedProp]).toString())) {
        selectedNodes.push(allEdges[edge]['from'])
        selectedNodes.push(allEdges[edge]['to'])
      }
    }
  }
  selectNodes(selectedNodes)
}</script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            
            
            
            
            
            

        
<center>
<h1></h1>
</center>

<!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
<script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
          crossorigin="anonymous"
        />
        <script
          src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf"
          crossorigin="anonymous"
        ></script>


        <center>
          <h1></h1>
        </center>
        <style type="text/css">

             #mynetwork {
                 width: 100%;
                 height: 100vh;
                 background-color: #ffffff;
                 border: 1px solid lightgray;
                 position: relative;
                 float: left;
             }

             

             

             
        </style>
    </head>


    <body>
        <div class="card" style="width: 100%">
            
            
            <div id="mynetwork" class="card-body"></div>
        </div>

        
        

        <script type="text/javascript">

              // initialize global variables.
              var edges;
              var nodes;
              var allNodes;
              var allEdges;
              var nodeColors;
              var originalNodes;
              var network;
              var container;
              var options, data;
              var filter = {
                  item : '',
                  property : '',
                  value : []
              };

              

              

              // This method is responsible for drawing the graph, returns the drawn network
              function drawGraph() {
                  var container = document.getElementById('mynetwork');

                  

                  // parsing and collecting nodes and edges from the python
                  nodes = new vis.DataSet([{"color": "#cccccc", "id": "A", "label": "A", "shape": "dot", "size": 27.76, "title": "Agent A\nTopic: T_Original\nStance: 0.09"}, {"color": "#cccccc", "id": "B", "label": "B", "shape": "dot", "size": 27.680000000000003, "title": "Agent B\nTopic: T_Sports\nStance: 0.00"}, {"color": "#0080ff", "id": "C (Source)", "label": "C (Source)", "shape": "dot", "size": 35.0, "title": "Agent C (Source)\nTopic: T_Original\nStance: 0.81"}, {"color": "#cccccc", "id": "D (Lurker)", "label": "D (Lurker)", "shape": "dot", "size": 26.400000000000002, "title": "Agent D (Lurker)\nTopic: T_Science\nStance: 0.00"}, {"color": "#00cc66", "id": "news1", "label": "news1", "shape": "square", "size": 18, "title": "Stimulus: news1\nSource: NewsOutlet\nContent: A major scientific breakthrough has been announced."}, {"color": "#00cc66", "id": "sci1", "label": "sci1", "shape": "square", "size": 18, "title": "Stimulus: sci1\nSource: ScienceDaily\nContent: Peer review highlights key limitations in the breakthrough study."}, {"color": "#00cc66", "id": "sci2", "label": "sci2", "shape": "square", "size": 18, "title": "Stimulus: sci2\nSource: UniLab\nContent: Researchers publish replication results with mixed outcomes."}, {"color": "#00cc66", "id": "sci3", "label": "sci3", "shape": "square", "size": 18, "title": "Stimulus: sci3\nSource: ScienceDaily\nContent: Explainer: what the breakthrough actually claims and what it does not."}, {"color": "#00cc66", "id": "sci4", "label": "sci4", "shape": "square", "size": 18, "title": "Stimulus: sci4\nSource: UniLab\nContent: New dataset released to validate claims independently."}, {"color": "#00cc66", "id": "sci5", "label": "sci5", "shape": "square", "size": 18, "title": "Stimulus: sci5\nSource: ScienceDaily\nContent: Interview: lead author responds to criticism."}, {"color": "#00cc66", "id": "pol1", "label": "pol1", "shape": "square", "size": 18, "title": "Stimulus: pol1\nSource: NewsOutlet\nContent: Lawmakers call for hearings on research funding priorities."}, {"color": "#00cc66", "id": "pol2", "label": "pol2", "shape": "square", "size": 18, "title": "Stimulus: pol2\nSource: RivalNews\nContent: Opposition says the hearings are political theater."}, {"color": "#00cc66", "id": "news2", "label": "news2", "shape": "square", "size": 18, "title": "Stimulus: news2\nSource: RivalNews\nContent: A competing report raises doubts about the recent breakthrough."}, {"color": "#00cc66", "id": "pol3", "label": "pol3", "shape": "square", "size": 18, "title": "Stimulus: pol3\nSource: CapitolWatch\nContent: Bill introduced to increase transparency in grants."}, {"color": "#00cc66", "id": "pol4", "label": "pol4", "shape": "square", "size": 18, "title": "Stimulus: pol4\nSource: CapitolWatch\nContent: Committee schedules public testimony next week."}, {"color": "#00cc66", "id": "pol5", "label": "pol5", "shape": "square", "size": 18, "title": "Stimulus: pol5\nSource: NewsOutlet\nContent: Debate escalates over who benefits from the new policy."}, {"color": "#00cc66", "id": "eco1", "label": "eco1", "shape": "square", "size": 18, "title": "Stimulus: eco1\nSource: MarketWire\nContent: Markets react to the news with modest volatility."}, {"color": "#00cc66", "id": "eco2", "label": "eco2", "shape": "square", "size": 18, "title": "Stimulus: eco2\nSource: MarketWire\nContent: Analysts: impact may be overstated in the short term."}, {"color": "#00cc66", "id": "eco3", "label": "eco3", "shape": "square", "size": 18, "title": "Stimulus: eco3\nSource: FinBlog\nContent: Thread: how hype cycles distort investment decisions."}, {"color": "#00cc66", "id": "eco4", "label": "eco4", "shape": "square", "size": 18, "title": "Stimulus: eco4\nSource: MarketWire\nContent: Report: funding reallocations could reshape the sector."}, {"color": "#00cc66", "id": "eco5", "label": "eco5", "shape": "square", "size": 18, "title": "Stimulus: eco5\nSource: FinBlog\nContent: Opinion: focus on fundamentals not narratives."}, {"color": "#00cc66", "id": "cult1", "label": "cult1", "shape": "square", "size": 18, "title": "Stimulus: cult1\nSource: TrendFeed\nContent: Influencers argue the story proves \"experts are out of touch.\""}, {"color": "#00cc66", "id": "meme1", "label": "meme1", "shape": "square", "size": 18, "title": "Stimulus: meme1\nSource: UserA\nContent: That feeling when you realize it\u0027s Friday, lol"}, {"color": "#00cc66", "id": "cult2", "label": "cult2", "shape": "square", "size": 18, "title": "Stimulus: cult2\nSource: TrendFeed\nContent: Viral clip sparks debate about scientific literacy."}, {"color": "#00cc66", "id": "cult3", "label": "cult3", "shape": "square", "size": 18, "title": "Stimulus: cult3\nSource: PodcasterX\nContent: Hot take: institutions cannot be trusted anymore."}, {"color": "#00cc66", "id": "cult4", "label": "cult4", "shape": "square", "size": 18, "title": "Stimulus: cult4\nSource: PodcasterX\nContent: Counterpoint: skepticism is healthy but facts matter."}, {"color": "#00cc66", "id": "cult5", "label": "cult5", "shape": "square", "size": 18, "title": "Stimulus: cult5\nSource: TrendFeed\nContent: Community notes provide corrections and sources."}, {"color": "#00cc66", "id": "meme2", "label": "meme2", "shape": "square", "size": 18, "title": "Stimulus: meme2\nSource: UserB\nContent: Me reading the comments: \u0027I will not engage\u0027 (engages anyway)."}, {"color": "#00cc66", "id": "meme3", "label": "meme3", "shape": "square", "size": 18, "title": "Stimulus: meme3\nSource: UserC\nContent: Breaking: my confidence is 1.0 and my evidence is vibes."}, {"color": "#00cc66", "id": "meme4", "label": "meme4", "shape": "square", "size": 18, "title": "Stimulus: meme4\nSource: UserD\nContent: When your model overfits and you call it \u0027intuition\u0027."}, {"color": "#00cc66", "id": "meme5", "label": "meme5", "shape": "square", "size": 18, "title": "Stimulus: meme5\nSource: UserE\nContent: Trust me bro, I ran it once."}, {"color": "#00cc66", "id": "sports1", "label": "sports1", "shape": "square", "size": 18, "title": "Stimulus: sports1\nSource: SportsDesk\nContent: Upset win sparks celebration and trash talk."}, {"color": "#00cc66", "id": "sports2", "label": "sports2", "shape": "square", "size": 18, "title": "Stimulus: sports2\nSource: SportsDesk\nContent: Analysts debate whether the win was luck or skill."}, {"color": "#00cc66", "id": "sports3", "label": "sports3", "shape": "square", "size": 18, "title": "Stimulus: sports3\nSource: FanAccount\nContent: Hot take: refs decided the game."}, {"color": "#00cc66", "id": "sports4", "label": "sports4", "shape": "square", "size": 18, "title": "Stimulus: sports4\nSource: FanAccount\nContent: Replay breakdown thread goes viral."}, {"color": "#00cc66", "id": "sports5", "label": "sports5", "shape": "square", "size": 18, "title": "Stimulus: sports5\nSource: SportsDesk\nContent: Coach addresses controversy in press conference."}, {"color": "#00cc66", "id": "sec1", "label": "sec1", "shape": "square", "size": 18, "title": "Stimulus: sec1\nSource: InfosecNews\nContent: Security researchers disclose a new vulnerability class."}, {"color": "#00cc66", "id": "sec2", "label": "sec2", "shape": "square", "size": 18, "title": "Stimulus: sec2\nSource: InfosecNews\nContent: Patch guidance issued with mitigations and timelines."}, {"color": "#00cc66", "id": "sec3", "label": "sec3", "shape": "square", "size": 18, "title": "Stimulus: sec3\nSource: ForumUser\nContent: This will be exploited in the wild within 72 hours."}, {"color": "#00cc66", "id": "sec4", "label": "sec4", "shape": "square", "size": 18, "title": "Stimulus: sec4\nSource: InfosecNews\nContent: Early telemetry suggests opportunistic scanning."}, {"color": "#00cc66", "id": "sec5", "label": "sec5", "shape": "square", "size": 18, "title": "Stimulus: sec5\nSource: ForumUser\nContent: If you are unpatched you are already compromised."}, {"color": "#00cc66", "id": "mix1", "label": "mix1", "shape": "square", "size": 18, "title": "Stimulus: mix1\nSource: NewsOutlet\nContent: Summary: what we know so far and what is still uncertain."}, {"color": "#00cc66", "id": "mix2", "label": "mix2", "shape": "square", "size": 18, "title": "Stimulus: mix2\nSource: RivalNews\nContent: Opinion: the story is being misframed by both sides."}, {"color": "#00cc66", "id": "mix3", "label": "mix3", "shape": "square", "size": 18, "title": "Stimulus: mix3\nSource: NewsOutlet\nContent: Fact check: common claims circulating are inaccurate."}, {"color": "#00cc66", "id": "mix4", "label": "mix4", "shape": "square", "size": 18, "title": "Stimulus: mix4\nSource: TrendFeed\nContent: Compilation: reactions across platforms and communities."}, {"color": "#00cc66", "id": "mix5", "label": "mix5", "shape": "square", "size": 18, "title": "Stimulus: mix5\nSource: ScienceDaily\nContent: Update: new evidence clarifies earlier ambiguities."}, {"color": "#555555", "id": "ScienceDaily", "label": "ScienceDaily", "shape": "box", "size": 14, "title": "External actor: ScienceDaily"}, {"color": "#555555", "id": "TrendFeed", "label": "TrendFeed", "shape": "box", "size": 14, "title": "External actor: TrendFeed"}, {"color": "#555555", "id": "NewsOutlet", "label": "NewsOutlet", "shape": "box", "size": 14, "title": "External actor: NewsOutlet"}, {"color": "#555555", "id": "RivalNews", "label": "RivalNews", "shape": "box", "size": 14, "title": "External actor: RivalNews"}]);
                  edges = new vis.DataSet([{"arrows": "to", "color": "#cccccc", "from": "A", "title": "follows", "to": "B", "width": 1}, {"arrows": "to", "color": "#cccccc", "from": "B", "title": "follows", "to": "C (Source)", "width": 1}, {"arrows": "to", "color": "#cccccc", "from": "D (Lurker)", "title": "follows", "to": "A", "width": 1}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "news1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 157 time(s)", "to": "sci1", "width": 7.0}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "sci3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 26 time(s)", "to": "sci3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 136 time(s)", "to": "news1", "width": 6.197452229299364}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 5 time(s)", "to": "news1", "width": 1.1910828025477707}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sci4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 29 time(s)", "to": "sci2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sci5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 133 time(s)", "to": "pol3", "width": 6.082802547770701}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 32 time(s)", "to": "news2", "width": 2.2229299363057327}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "pol3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "pol3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 29 time(s)", "to": "sci1", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "pol2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "eco3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "eco4", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 51 time(s)", "to": "pol1", "width": 2.949044585987261}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "news2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 28 time(s)", "to": "sci2", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "sci1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 29 time(s)", "to": "sci5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "eco3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 30 time(s)", "to": "cult4", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "sci2", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "cult5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "meme3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 30 time(s)", "to": "eco4", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "meme2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "meme1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "meme3", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "cult1", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "eco4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "eco2", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "meme2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sci2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "cult3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "eco2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "meme2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "cult4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "pol4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "meme5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "pol2", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 6 time(s)", "to": "sports2", "width": 1.2292993630573248}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "sports2", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "cult1", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 28 time(s)", "to": "meme4", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "cult3", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "pol3", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 30 time(s)", "to": "sports3", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "sci1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "pol5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "sports5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "pol4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "mix2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sec5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "eco5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "sec2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "pol2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "sci3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sec1", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "cult3", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 12 time(s)", "to": "sports4", "width": 1.4585987261146496}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "pol5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "sec5", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "sec3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sports4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "mix1", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "news2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "mix5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sports3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 29 time(s)", "to": "mix5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sec1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "meme5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "cult5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sports5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "mix3", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "cult4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sports1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "eco1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 23 time(s)", "to": "sec4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 5 time(s)", "to": "mix1", "width": 1.1910828025477707}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "sec2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "mix4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "mix1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "sec1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "cult2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "cult2", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 26 time(s)", "to": "sports5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "meme5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "cult4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 10 time(s)", "to": "mix3", "width": 1.3821656050955413}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "mix3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "meme4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sec4", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "sec3", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "meme3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sec2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sec3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 3 time(s)", "to": "mix2", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "eco3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "sports3", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "cult2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "eco3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 4 time(s)", "to": "sec5", "width": 1.1528662420382165}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "news1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sec4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "sci5", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 3 time(s)", "to": "cult5", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 2 time(s)", "to": "pol4", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "eco5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sports4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "mix2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "eco5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "sports2", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "mix5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 3 time(s)", "to": "pol4", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "meme1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "cult5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix4", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "mix3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 2 time(s)", "to": "sec4", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "eco2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "cult3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "sec2", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "meme4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sec5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "eco1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "cult2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 4 time(s)", "to": "meme1", "width": 1.1528662420382165}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "pol2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 3 time(s)", "to": "sports5", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "meme5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 1 time(s)", "to": "mix4", "width": 1.0382165605095541}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 1 time(s)", "to": "news2", "width": 1.0382165605095541}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "pol5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "eco1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 2 time(s)", "to": "eco5", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "sci5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "meme1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "sports2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 3 time(s)", "to": "sci3", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sec3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "sports1", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "cult1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "pol5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "eco2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "mix5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 1 time(s)", "to": "sports1", "width": 1.0382165605095541}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "cult1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 10 time(s)", "to": "sec1", "width": 1.3821656050955413}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 10 time(s)", "to": "mix4", "width": 1.3821656050955413}, {"arrows": "to", "color": "#ff0000", "from": "C (Source)", "title": "Influenced 1 time(s)", "to": "B", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "B", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "ScienceDaily", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "TrendFeed", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "NewsOutlet", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "RivalNews", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "A", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "ScienceDaily", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "TrendFeed", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "NewsOutlet", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "RivalNews", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}]);

                  nodeColors = {};
                  allNodes = nodes.get({ returnType: "Object" });
                  for (nodeId in allNodes) {
                    nodeColors[nodeId] = allNodes[nodeId].color;
                  }
                  allEdges = edges.get({ returnType: "Object" });
                  // adding nodes and edges to the graph
                  data = {nodes: nodes, edges: edges};

                  var options = {"physics": {"enabled": true, "barnesHut": {"gravitationalConstant": -25000, "centralGravity": 0.25, "springLength": 180, "springConstant": 0.04, "damping": 0.5, "avoidOverlap": 0.2}, "stabilization": {"enabled": true, "iterations": 1500, "updateInterval": 50, "fit": true}}, "interaction": {"hover": true, "tooltipDelay": 80}};

                  


                  

                  network = new vis.Network(container, data, options);

                  

                  

                  


                  

                  return network;

              }
              drawGraph();
        </script>
    </body>
</html>
```

## `phase_patch.py`

```python
#!/usr/bin/env python3
"""
apply_phase_scheduler_patch.py

Drop this file in your repo root (gsocialsim) and run:
  python apply_phase_scheduler_patch.py

It writes a unified diff patch to a temp file and applies it using:
  1) git apply
  2) patch -p1  (fallback)

This implements:
- EventPhase + phase ordering
- Scheduler ordering: (timestamp, phase, tie_breaker)
- Agent.last_perception_tick set on perceive()
- AllocateAttentionEvent reactive gate (must have perceived this tick)
- Updates test_event_system expectations for phase ordering

If it fails, it prints stderr so you can see what mismatched.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

PATCH_TEXT = r"""diff --git a/src/gsocialsim/kernel/event_scheduler.py b/src/gsocialsim/kernel/event_scheduler.py
index 1f3c1a2..0d7a4b1 100644
--- a/src/gsocialsim/kernel/event_scheduler.py
+++ b/src/gsocialsim/kernel/event_scheduler.py
@@ -1,23 +1,24 @@
 import heapq
 from typing import List
 from gsocialsim.kernel.events import Event
 
 class EventScheduler:
     """A priority queue to manage and dispatch events in chronological order."""
     def __init__(self):
-        # The queue now stores tuples: (timestamp, tie_breaker, event_object)
-        self._queue: List[tuple[int, int, Event]] = []
+        # The queue stores tuples: (timestamp, phase, tie_breaker, event_object)
+        self._queue: List[tuple[int, int, int, Event]] = []
 
     def schedule(self, event: Event):
         """Add an event to the queue as a tuple for robust sorting."""
-        entry = (event.timestamp, event.tie_breaker, event)
+        entry = (event.timestamp, int(event.phase), event.tie_breaker, event)
         heapq.heappush(self._queue, entry)
 
     def get_next_event(self) -> Event | None:
         """Pop the next event from the queue."""
         if not self._queue:
             return None
-        # The event object is the third item in the tuple
-        return heapq.heappop(self._queue)[2]
+        # The event object is the fourth item in the tuple
+        return heapq.heappop(self._queue)[3]
 
     def is_empty(self) -> bool:
         return len(self._queue) == 0
diff --git a/src/gsocialsim/kernel/events.py b/src/gsocialsim/kernel/events.py
index 0b4f3aa..d6f4f73 100644
--- a/src/gsocialsim/kernel/events.py
+++ b/src/gsocialsim/kernel/events.py
@@ -1,19 +1,34 @@
 from __future__ import annotations
 from abc import ABC, abstractmethod
 from dataclasses import dataclass, field
 from typing import TYPE_CHECKING
 import itertools
+from enum import IntEnum
 
 from gsocialsim.agents.budget_state import BudgetKind
 from gsocialsim.stimuli.content_item import ContentItem
 from gsocialsim.agents.impression import Impression, IntakeMode
 from gsocialsim.types import TopicId
 
 if TYPE_CHECKING:
     from gsocialsim.kernel.world_kernel import WorldContext
     from gsocialsim.stimuli.interaction import Interaction
     from gsocialsim.stimuli.stimulus import Stimulus
 
 _event_counter = itertools.count()
 
+class EventPhase(IntEnum):
+    """
+    Ordering within the same simulation tick.
+    Smaller runs earlier.
+    """
+    INGEST = 10
+    PERCEIVE = 20
+    INTERACT_PERCEIVE = 30
+    ACT = 40
+    ALLOCATE_ATTENTION = 50
+    DEEP_FOCUS = 60
+
 @dataclass(order=True)
 class Event(ABC):
     timestamp: int = field(compare=True)
+    phase: int = field(default=int(EventPhase.ACT), compare=True)
     tie_breaker: int = field(init=False, compare=True)
     def __post_init__(self): self.tie_breaker = next(_event_counter)
     @abstractmethod
     def apply(self, context: "WorldContext"):
         pass
 
 @dataclass(order=True)
 class StimulusIngestionEvent(Event):
+    phase: int = field(default=int(EventPhase.INGEST), compare=True)
     def apply(self, context: "WorldContext"):
         new_stimuli = context.stimulus_engine.tick(self.timestamp)
         if new_stimuli:
             for stimulus in new_stimuli:
                 context.scheduler.schedule(StimulusPerceptionEvent(timestamp=self.timestamp, stimulus_id=stimulus.id))
         context.scheduler.schedule(StimulusIngestionEvent(timestamp=self.timestamp + 1))
 
 @dataclass(order=True)
 class StimulusPerceptionEvent(Event):
+    phase: int = field(default=int(EventPhase.PERCEIVE), compare=True)
     stimulus_id: str = field(compare=False)
     def apply(self, context: "WorldContext"):
         stimulus = context.stimulus_engine.get_stimulus(self.stimulus_id)
         if not stimulus: return
         
         temp_content = ContentItem(id=stimulus.id, author_id=stimulus.source, topic=TopicId(f"stim_{stimulus.id}"), stance=0.0)
         for agent in context.agents.agents.values():
             agent.perceive(temp_content, context, stimulus_id=stimulus.id)
 
 @dataclass(order=True)
 class AgentActionEvent(Event):
+    phase: int = field(default=int(EventPhase.ACT), compare=True)
     agent_id: str = field(compare=False)
     def apply(self, context: "WorldContext"):
         agent = context.agents.get(self.agent_id)
         if not agent: return
 
@@ -35,11 +50,12 @@ class AgentActionEvent(Event):
         context.scheduler.schedule(AgentActionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))
 
 @dataclass(order=True)
 class InteractionPerceptionEvent(Event):
+    phase: int = field(default=int(EventPhase.INTERACT_PERCEIVE), compare=True)
     interaction: "Interaction" = field(compare=False)
 
     def apply(self, context: "WorldContext"):
         from gsocialsim.policy.bandit_learner import RewardVector
         from gsocialsim.stimuli.interaction import InteractionVerb
@@ -90,6 +106,7 @@ class InteractionPerceptionEvent(Event):
             author.learn(action_key, reward)
 
 @dataclass(order=True)
 class DeepFocusEvent(Event):
+    phase: int = field(default=int(EventPhase.DEEP_FOCUS), compare=True)
     agent_id: str = field(compare=False)
     content_id: str = field(compare=False)
     original_impression: Impression = field(compare=False) # Store the impression that led to deep focus
 
@@ -141,10 +158,26 @@ class DeepFocusEvent(Event):
             print(f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] failed Deep Focus due to insufficient budget.")
 
 @dataclass(order=True)
 class AllocateAttentionEvent(Event):
+    phase: int = field(default=int(EventPhase.ALLOCATE_ATTENTION), compare=True)
     agent_id: str = field(compare=False)
     def apply(self, context: "WorldContext"):
         agent = context.agents.get(self.agent_id)
         if not agent: return
 
+        # Deep focus should be reactive: only consider deep focus if the agent perceived
+        # something at this same tick. Otherwise, just schedule next allocation tick.
+        if getattr(agent, "last_perception_tick", None) != self.timestamp:
+            context.scheduler.schedule(
+                AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id)
+            )
+            return
+
         # PRD: Triggered by salience thresholds. Consumes deep_focus_budget.
         # For this phase: if a recent impression has high salience, trigger deep focus.
         high_salience_impressions = []
         for impression in agent.recent_impressions.values():
             if agent.beliefs.get(impression.topic) and agent.beliefs.get(impression.topic).salience > 0.5: # Example threshold
                 high_salience_impressions.append(impression)
         
         if high_salience_impressions and agent.budgets.deep_focus_budget >= 1 and agent.budgets.attention_minutes >= 10:
             # Choose one high-salience impression to deep focus on
             impression_to_focus = agent.rng.choice(high_salience_impressions)
             context.scheduler.schedule(DeepFocusEvent(timestamp=self.timestamp, agent_id=self.agent_id, content_id=impression_to_focus.content_id, original_impression=impression_to_focus))
         
         # Schedule next attention allocation event (e.g., for next tick)
         context.scheduler.schedule(AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))
 
 @dataclass(order=True)
 class DayBoundaryEvent(Event):
     def apply(self, context: "WorldContext"):
         for agent in context.agents.agents.values():
             agent.consolidate_daily(context)
         context.scheduler.schedule(DayBoundaryEvent(timestamp=self.timestamp + context.clock.ticks_per_day))
diff --git a/src/gsocialsim/agents/agent.py b/src/gsocialsim/agents/agent.py
index 3f9f9c1..c5adf63 100644
--- a/src/gsocialsim/agents/agent.py
+++ b/src/gsocialsim/agents/agent.py
@@ -1,6 +1,6 @@
 from dataclasses import dataclass, field
 from typing import Optional, TYPE_CHECKING
 from collections import deque
 import random
 
@@ -33,6 +33,8 @@ class Agent:
     policy: BanditLearner = field(default_factory=BanditLearner)
     # Store the most recent impressions, keyed by content_id
     recent_impressions: dict[str, Impression] = field(default_factory=dict)
+    # Tracks whether the agent perceived anything during a given tick
+    last_perception_tick: Optional[int] = None
 
     def __post_init__(self):
         self.rng = random.Random(self.seed)
         self.budgets._rng = self.rng
 
     def perceive(self, content: ContentItem, context: "WorldContext", is_physical: bool = False, stimulus_id: Optional[str] = None):
+        self.last_perception_tick = context.clock.t
         impression = self.attention.evaluate(content, is_physical=is_physical)
         # Store the impression for potential deep focus/later action
         if impression.content_id:
             self.recent_impressions[impression.content_id] = impression
diff --git a/tests/test_event_system.py b/tests/test_event_system.py
index 8b1c3c0..6a9bb7d 100644
--- a/tests/test_event_system.py
+++ b/tests/test_event_system.py
@@ -1,12 +1,13 @@
 import unittest
 from unittest.mock import Mock
 from gsocialsim.kernel.event_scheduler import EventScheduler
 from gsocialsim.kernel.events import (
     Event,
     StimulusIngestionEvent,
     DayBoundaryEvent,
     AgentActionEvent,
+    EventPhase,
 )
 
 class TestEventSystem(unittest.TestCase):
 
     def test_event_scheduler_tie_breaking(self):
@@ -14,35 +15,44 @@ class TestEventSystem(unittest.TestCase):
         Verify that the EventScheduler correctly orders and dispatches
         different event types that are scheduled for the exact same timestamp.
         """
         print("
 --- Test: Event Scheduler Tie-Breaking ---")
         scheduler = EventScheduler()
         
         # Schedule three different event types for the same timestamp (t=0)
-        # Their tie-breaker values will be 0, 1, 2 respectively.
+        # Now ordering is by (timestamp, phase, tie_breaker).
         e1 = StimulusIngestionEvent(timestamp=0)
         e2 = DayBoundaryEvent(timestamp=0)
         e3 = AgentActionEvent(timestamp=0, agent_id="A1")
 
         scheduler.schedule(e1)
         scheduler.schedule(e2)
         scheduler.schedule(e3)
 
         # Retrieve the events.
-        # They should come out in the order they were added
-        # because the tie-breaker maintains insertion order for same-timestamp events.
+        # They should come out ordered by phase first:
+        #   INGEST (StimulusIngestionEvent) -> ACT (AgentActionEvent) -> default (DayBoundaryEvent uses ACT default unless set)
+        # DayBoundaryEvent is a system boundary event; if you later give it a specific phase,
+        # update this test accordingly.
         out1 = scheduler.get_next_event()
         out2 = scheduler.get_next_event()
         out3 = scheduler.get_next_event()
 
         self.assertIsInstance(out1, StimulusIngestionEvent, "First event should be StimulusIngestionEvent")
-        self.assertIsInstance(out2, DayBoundaryEvent, "Second event should be DayBoundaryEvent")
-        self.assertIsInstance(out3, AgentActionEvent, "Third event should be AgentActionEvent")
-        print("Verified: Events with the same timestamp are dispatched in a stable, predictable order.")
+        # AgentActionEvent has ACT phase
+        self.assertIsInstance(out2, AgentActionEvent, "Second event should be AgentActionEvent (ACT phase)")
+        # DayBoundaryEvent currently inherits default phase (ACT). If you later set DayBoundaryEvent phase,
+        # this should be updated.
+        self.assertIsInstance(out3, DayBoundaryEvent, "Third event should be DayBoundaryEvent")
+        print("Verified: Events with the same timestamp are dispatched in a stable, phase-driven order.")
 
     def test_event_apply_calls(self):
         """
         Verify that calling apply() on an event triggers its logic.
         """
"""

def _run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr

def main() -> int:
    repo_root = Path.cwd()
    tmp_patch = repo_root / ".tmp_phase_scheduler.patch"
    tmp_patch.write_text(PATCH_TEXT, encoding="utf-8")

    try:
        # Prefer git apply if available
        if shutil.which("git"):
            code, out, err = _run(["git", "apply", str(tmp_patch)])
            if code == 0:
                print("OK: applied patch with git apply")
                return 0
            print("git apply failed, trying patch -p1")
            if out.strip():
                print(out)
            if err.strip():
                print(err, file=sys.stderr)

        if shutil.which("patch"):
            code, out, err = _run(["patch", "-p1", "-i", str(tmp_patch)])
            if code == 0:
                print("OK: applied patch with patch -p1")
                return 0
            if out.strip():
                print(out)
            if err.strip():
                print(err, file=sys.stderr)

        print("ERROR: could not apply patch (no git/patch or patch did not match).", file=sys.stderr)
        print(f"Patch file left at: {tmp_patch}", file=sys.stderr)
        return 2

    finally:
        # Keep it around if something failed so you can inspect; delete on success
        pass

if __name__ == "__main__":
    raise SystemExit(main())

```

## `platform.html`

```html
<html>
    <head>
        <meta charset="utf-8">
        
            <script>function neighbourhoodHighlight(params) {
  // console.log("in nieghbourhoodhighlight");
  allNodes = nodes.get({ returnType: "Object" });
  // originalNodes = JSON.parse(JSON.stringify(allNodes));
  // if something is selected:
  if (params.nodes.length > 0) {
    highlightActive = true;
    var i, j;
    var selectedNode = params.nodes[0];
    var degrees = 2;

    // mark all nodes as hard to read.
    for (let nodeId in allNodes) {
      // nodeColors[nodeId] = allNodes[nodeId].color;
      allNodes[nodeId].color = "rgba(200,200,200,0.5)";
      if (allNodes[nodeId].hiddenLabel === undefined) {
        allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }
    var connectedNodes = network.getConnectedNodes(selectedNode);
    var allConnectedNodes = [];

    // get the second degree nodes
    for (i = 1; i < degrees; i++) {
      for (j = 0; j < connectedNodes.length; j++) {
        allConnectedNodes = allConnectedNodes.concat(
          network.getConnectedNodes(connectedNodes[j])
        );
      }
    }

    // all second degree nodes get a different color and their label back
    for (i = 0; i < allConnectedNodes.length; i++) {
      // allNodes[allConnectedNodes[i]].color = "pink";
      allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";
      if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[allConnectedNodes[i]].label =
          allNodes[allConnectedNodes[i]].hiddenLabel;
        allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // all first degree nodes get their own color and their label back
    for (i = 0; i < connectedNodes.length; i++) {
      // allNodes[connectedNodes[i]].color = undefined;
      allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];
      if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[connectedNodes[i]].label =
          allNodes[connectedNodes[i]].hiddenLabel;
        allNodes[connectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // the main node gets its own color and its label back.
    // allNodes[selectedNode].color = undefined;
    allNodes[selectedNode].color = nodeColors[selectedNode];
    if (allNodes[selectedNode].hiddenLabel !== undefined) {
      allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
      allNodes[selectedNode].hiddenLabel = undefined;
    }
  } else if (highlightActive === true) {
    // console.log("highlightActive was true");
    // reset all nodes
    for (let nodeId in allNodes) {
      // allNodes[nodeId].color = "purple";
      allNodes[nodeId].color = nodeColors[nodeId];
      // delete allNodes[nodeId].color;
      if (allNodes[nodeId].hiddenLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
        allNodes[nodeId].hiddenLabel = undefined;
      }
    }
    highlightActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    // console.log("Nothing was selected");
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        // allNodes[nodeId].color = {};
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function filterHighlight(params) {
  allNodes = nodes.get({ returnType: "Object" });
  // if something is selected:
  if (params.nodes.length > 0) {
    filterActive = true;
    let selectedNodes = params.nodes;

    // hiding all nodes and saving the label
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = true;
      if (allNodes[nodeId].savedLabel === undefined) {
        allNodes[nodeId].savedLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }

    for (let i=0; i < selectedNodes.length; i++) {
      allNodes[selectedNodes[i]].hidden = false;
      if (allNodes[selectedNodes[i]].savedLabel !== undefined) {
        allNodes[selectedNodes[i]].label = allNodes[selectedNodes[i]].savedLabel;
        allNodes[selectedNodes[i]].savedLabel = undefined;
      }
    }

  } else if (filterActive === true) {
    // reset all nodes
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = false;
      if (allNodes[nodeId].savedLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].savedLabel;
        allNodes[nodeId].savedLabel = undefined;
      }
    }
    filterActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function selectNode(nodes) {
  network.selectNodes(nodes);
  neighbourhoodHighlight({ nodes: nodes });
  return nodes;
}

function selectNodes(nodes) {
  network.selectNodes(nodes);
  filterHighlight({nodes: nodes});
  return nodes;
}

function highlightFilter(filter) {
  let selectedNodes = []
  let selectedProp = filter['property']
  if (filter['item'] === 'node') {
    let allNodes = nodes.get({ returnType: "Object" });
    for (let nodeId in allNodes) {
      if (allNodes[nodeId][selectedProp] && filter['value'].includes((allNodes[nodeId][selectedProp]).toString())) {
        selectedNodes.push(nodeId)
      }
    }
  }
  else if (filter['item'] === 'edge'){
    let allEdges = edges.get({returnType: 'object'});
    // check if the selected property exists for selected edge and select the nodes connected to the edge
    for (let edge in allEdges) {
      if (allEdges[edge][selectedProp] && filter['value'].includes((allEdges[edge][selectedProp]).toString())) {
        selectedNodes.push(allEdges[edge]['from'])
        selectedNodes.push(allEdges[edge]['to'])
      }
    }
  }
  selectNodes(selectedNodes)
}</script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            
            
            
            
            
            

        
<center>
<h1></h1>
</center>

<!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
<script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
          crossorigin="anonymous"
        />
        <script
          src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf"
          crossorigin="anonymous"
        ></script>


        <center>
          <h1></h1>
        </center>
        <style type="text/css">

             #mynetwork {
                 width: 100%;
                 height: 100vh;
                 background-color: #ffffff;
                 border: 1px solid lightgray;
                 position: relative;
                 float: left;
             }

             

             

             
        </style>
    </head>


    <body>
        <div class="card" style="width: 100%">
            
            
            <div id="mynetwork" class="card-body"></div>
        </div>

        
        

        <script type="text/javascript">

              // initialize global variables.
              var edges;
              var nodes;
              var allNodes;
              var allEdges;
              var nodeColors;
              var originalNodes;
              var network;
              var container;
              var options, data;
              var filter = {
                  item : '',
                  property : '',
                  value : []
              };

              

              

              // This method is responsible for drawing the graph, returns the drawn network
              function drawGraph() {
                  var container = document.getElementById('mynetwork');

                  

                  // parsing and collecting nodes and edges from the python
                  nodes = new vis.DataSet([{"color": "#cccccc", "id": "A", "label": "A", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "B", "label": "B", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "C (Source)", "label": "C (Source)", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "D (Lurker)", "label": "D (Lurker)", "shape": "dot", "size": 18}, {"color": "#2aa198", "id": "SRC:CapitolWatch", "label": "CapitolWatch", "shape": "box", "size": 18, "title": "Platform/Source: CapitolWatch"}, {"color": "#2aa198", "id": "SRC:FanAccount", "label": "FanAccount", "shape": "box", "size": 18, "title": "Platform/Source: FanAccount"}, {"color": "#2aa198", "id": "SRC:FinBlog", "label": "FinBlog", "shape": "box", "size": 18, "title": "Platform/Source: FinBlog"}, {"color": "#2aa198", "id": "SRC:ForumUser", "label": "ForumUser", "shape": "box", "size": 18, "title": "Platform/Source: ForumUser"}, {"color": "#2aa198", "id": "SRC:InfosecNews", "label": "InfosecNews", "shape": "box", "size": 18, "title": "Platform/Source: InfosecNews"}, {"color": "#2aa198", "id": "SRC:MarketWire", "label": "MarketWire", "shape": "box", "size": 18, "title": "Platform/Source: MarketWire"}, {"color": "#2aa198", "id": "SRC:NewsOutlet", "label": "NewsOutlet", "shape": "box", "size": 18, "title": "Platform/Source: NewsOutlet"}, {"color": "#2aa198", "id": "SRC:PodcasterX", "label": "PodcasterX", "shape": "box", "size": 18, "title": "Platform/Source: PodcasterX"}, {"color": "#2aa198", "id": "SRC:RivalNews", "label": "RivalNews", "shape": "box", "size": 18, "title": "Platform/Source: RivalNews"}, {"color": "#2aa198", "id": "SRC:ScienceDaily", "label": "ScienceDaily", "shape": "box", "size": 18, "title": "Platform/Source: ScienceDaily"}, {"color": "#2aa198", "id": "SRC:SportsDesk", "label": "SportsDesk", "shape": "box", "size": 18, "title": "Platform/Source: SportsDesk"}, {"color": "#2aa198", "id": "SRC:TrendFeed", "label": "TrendFeed", "shape": "box", "size": 18, "title": "Platform/Source: TrendFeed"}, {"color": "#2aa198", "id": "SRC:UniLab", "label": "UniLab", "shape": "box", "size": 18, "title": "Platform/Source: UniLab"}, {"color": "#2aa198", "id": "SRC:UserA", "label": "UserA", "shape": "box", "size": 18, "title": "Platform/Source: UserA"}, {"color": "#2aa198", "id": "SRC:UserB", "label": "UserB", "shape": "box", "size": 18, "title": "Platform/Source: UserB"}, {"color": "#2aa198", "id": "SRC:UserC", "label": "UserC", "shape": "box", "size": 18, "title": "Platform/Source: UserC"}, {"color": "#2aa198", "id": "SRC:UserD", "label": "UserD", "shape": "box", "size": 18, "title": "Platform/Source: UserD"}, {"color": "#2aa198", "id": "SRC:UserE", "label": "UserE", "shape": "box", "size": 18, "title": "Platform/Source: UserE"}]);
                  edges = new vis.DataSet([{"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 125 time(s)", "to": "SRC:NewsOutlet", "width": 4.086419753086419}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 234 time(s)", "to": "SRC:ScienceDaily", "width": 6.777777777777778}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 111 time(s)", "to": "SRC:ScienceDaily", "width": 3.7407407407407405}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 243 time(s)", "to": "SRC:NewsOutlet", "width": 7.0}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 106 time(s)", "to": "SRC:NewsOutlet", "width": 3.617283950617284}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 47 time(s)", "to": "SRC:UniLab", "width": 2.1604938271604937}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 54 time(s)", "to": "SRC:UniLab", "width": 2.333333333333333}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 136 time(s)", "to": "SRC:CapitolWatch", "width": 4.3580246913580245}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 83 time(s)", "to": "SRC:RivalNews", "width": 3.049382716049383}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 49 time(s)", "to": "SRC:CapitolWatch", "width": 2.2098765432098766}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 28 time(s)", "to": "SRC:CapitolWatch", "width": 1.691358024691358}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 51 time(s)", "to": "SRC:UniLab", "width": 2.259259259259259}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 88 time(s)", "to": "SRC:ScienceDaily", "width": 3.1728395061728394}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 82 time(s)", "to": "SRC:RivalNews", "width": 3.0246913580246915}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 56 time(s)", "to": "SRC:FinBlog", "width": 2.382716049382716}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 81 time(s)", "to": "SRC:MarketWire", "width": 3.0}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 73 time(s)", "to": "SRC:RivalNews", "width": 2.802469135802469}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 53 time(s)", "to": "SRC:UniLab", "width": 2.308641975308642}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 49 time(s)", "to": "SRC:FinBlog", "width": 2.2098765432098766}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 55 time(s)", "to": "SRC:PodcasterX", "width": 2.3580246913580245}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 111 time(s)", "to": "SRC:TrendFeed", "width": 3.7407407407407405}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "SRC:UserC", "width": 1.5925925925925926}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 80 time(s)", "to": "SRC:MarketWire", "width": 2.9753086419753085}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "SRC:UserB", "width": 1.5432098765432098}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "SRC:UserA", "width": 1.5432098765432098}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "SRC:UserC", "width": 1.5432098765432098}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 74 time(s)", "to": "SRC:TrendFeed", "width": 2.8271604938271606}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 50 time(s)", "to": "SRC:MarketWire", "width": 2.234567901234568}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 51 time(s)", "to": "SRC:MarketWire", "width": 2.259259259259259}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "SRC:UserB", "width": 1.617283950617284}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 51 time(s)", "to": "SRC:PodcasterX", "width": 2.259259259259259}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "SRC:UserB", "width": 1.5925925925925926}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 57 time(s)", "to": "SRC:PodcasterX", "width": 2.4074074074074074}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "SRC:UserE", "width": 1.6419753086419753}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 55 time(s)", "to": "SRC:SportsDesk", "width": 2.3580246913580245}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 83 time(s)", "to": "SRC:SportsDesk", "width": 3.049382716049383}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 28 time(s)", "to": "SRC:UserD", "width": 1.691358024691358}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "SRC:UserD", "width": 1.6666666666666665}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 48 time(s)", "to": "SRC:CapitolWatch", "width": 2.185185185185185}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 55 time(s)", "to": "SRC:FanAccount", "width": 2.3580246913580245}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 85 time(s)", "to": "SRC:ScienceDaily", "width": 3.0987654320987654}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "SRC:UserB", "width": 1.6666666666666665}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "SRC:SportsDesk", "width": 1.567901234567901}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 50 time(s)", "to": "SRC:ForumUser", "width": 2.234567901234568}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 72 time(s)", "to": "SRC:InfosecNews", "width": 2.7777777777777777}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 55 time(s)", "to": "SRC:PodcasterX", "width": 2.3580246913580245}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "SRC:FanAccount", "width": 1.567901234567901}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "SRC:ForumUser", "width": 1.6419753086419753}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 47 time(s)", "to": "SRC:FanAccount", "width": 2.1604938271604937}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 94 time(s)", "to": "SRC:NewsOutlet", "width": 3.3209876543209877}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 71 time(s)", "to": "SRC:InfosecNews", "width": 2.753086419753086}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "SRC:UserE", "width": 1.5925925925925926}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "SRC:UserC", "width": 1.6666666666666665}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 68 time(s)", "to": "SRC:InfosecNews", "width": 2.6790123456790123}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 54 time(s)", "to": "SRC:FanAccount", "width": 2.333333333333333}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 77 time(s)", "to": "SRC:TrendFeed", "width": 2.9012345679012346}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "SRC:UserE", "width": 1.6419753086419753}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "SRC:UserD", "width": 1.567901234567901}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "SRC:UserC", "width": 1.5925925925925926}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "SRC:ForumUser", "width": 1.7160493827160495}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 27 time(s)", "to": "SRC:RivalNews", "width": 1.6666666666666665}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 50 time(s)", "to": "SRC:FinBlog", "width": 2.234567901234568}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "SRC:FinBlog", "width": 1.6666666666666665}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "SRC:UserA", "width": 1.6666666666666665}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 78 time(s)", "to": "SRC:TrendFeed", "width": 2.9259259259259256}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "SRC:InfosecNews", "width": 1.617283950617284}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "SRC:UserD", "width": 1.6419753086419753}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 49 time(s)", "to": "SRC:ForumUser", "width": 2.2098765432098766}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 4 time(s)", "to": "SRC:UserA", "width": 1.0987654320987654}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 53 time(s)", "to": "SRC:SportsDesk", "width": 2.308641975308642}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "SRC:UserE", "width": 1.2716049382716048}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "SRC:UserA", "width": 1.5925925925925926}, {"arrows": "to", "color": "#ff0000", "from": "C (Source)", "title": "Influenced 1 time(s)", "to": "B", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "B", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:ScienceDaily", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:TrendFeed", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:NewsOutlet", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:RivalNews", "title": "Influenced 1 time(s)", "to": "A", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "A", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:ScienceDaily", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:TrendFeed", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:NewsOutlet", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}, {"arrows": "to", "color": "#ff0000", "from": "SRC:RivalNews", "title": "Influenced 1 time(s)", "to": "D (Lurker)", "width": 2}]);

                  nodeColors = {};
                  allNodes = nodes.get({ returnType: "Object" });
                  for (nodeId in allNodes) {
                    nodeColors[nodeId] = allNodes[nodeId].color;
                  }
                  allEdges = edges.get({ returnType: "Object" });
                  // adding nodes and edges to the graph
                  data = {nodes: nodes, edges: edges};

                  var options = {"physics": {"enabled": true, "stabilization": {"enabled": true, "iterations": 1300, "fit": true}}};

                  


                  

                  network = new vis.Network(container, data, options);

                  

                  

                  


                  

                  return network;

              }
              drawGraph();
        </script>
    </body>
</html>
```

## `pyproject.toml`

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "gsocialsim"
version = "0.1.0"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

```

## `requirements.txt`

```text
pyvis>=0.3.2

```

## `run_and_visualize.py`

```python
import argparse
from typing import Any, Dict

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.relationship_vector import RelationshipVector
from gsocialsim.stimuli.data_source import CsvDataSource

# IMPORTANT: import the package to auto-register exporters
import gsocialsim.visualization as viz
from gsocialsim.visualization import ExportRequest, get_exporter, list_exporters, generate_influence_graph_html


def setup_simulation_scenario(kernel: WorldKernel, *, stimuli_csv: str = "stimuli.csv"):
    print("Setting up simulation scenario...")

    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C (Source)"), seed=3)
    agent_D = Agent(id=AgentId("D (Lurker)"), seed=4)

    agents = [agent_A, agent_B, agent_C, agent_D]

    topics = [
        TopicId("T_Original"),
        TopicId("T_Science"),
        TopicId("T_Politics"),
        TopicId("T_Economy"),
        TopicId("T_Culture"),
        TopicId("T_Memes"),
        TopicId("T_Sports"),
        TopicId("T_Security"),
    ]

    for a in agents:
        a.budgets.action_budget = 5000
        for t in topics:
            a.beliefs.update(t, stance=0.0, confidence=0.5, salience=0.1, knowledge=0.1)
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)
    graph.add_edge(follower=agent_D.id, followed=agent_A.id)

    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9))
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6))

    agent_C.beliefs.update(TopicId("T_Original"), stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)

    csv_source = CsvDataSource(file_path=stimuli_csv)
    kernel.world_context.stimulus_engine.register_data_source(csv_source)

    print("Scenario setup complete.")


def print_sanity_summary(kernel: WorldKernel):
    print("\n--- SANITY SUMMARY ---")
    analytics = kernel.analytics

    exposure_counts = getattr(analytics, "exposure_counts", {})
    consumed_counts = getattr(analytics, "consumed_counts", {})
    agent_ids = sorted(set(list(exposure_counts.keys()) + list(consumed_counts.keys())))

    if agent_ids:
        for aid in agent_ids:
            exp = exposure_counts.get(aid, 0)
            con = consumed_counts.get(aid, 0)
            print(f"Agent {aid}: exposures={exp}, consumed={con}")
    else:
        print("No exposure/consumption counters found (analytics too old?).")

    dream_runs = getattr(analytics, "dream_runs", [])
    print(f"dream_runs={len(dream_runs)}")
    if dream_runs:
        last = dream_runs[-1]
        print(
            f"last_dream: agent={last.get('agent_id')} "
            f"consolidated={last.get('consolidated')} actions={last.get('actions')}"
        )

    consumed_by_media = getattr(analytics, "consumed_by_media", None)
    if isinstance(consumed_by_media, dict) or hasattr(consumed_by_media, "items"):
        top = sorted(consumed_by_media.items(), key=lambda kv: kv[1], reverse=True)
        if top:
            print("consumed_by_media:", ", ".join([f"{k}={v}" for k, v in top[:8]]))

    print("--- END SUMMARY ---\n")


def build_extra_args(args: argparse.Namespace) -> Dict[str, Any]:
    extra: Dict[str, Any] = {}

    if args.viz == "threshold":
        extra["min_influence_edges"] = args.min_influence_edges
        extra["min_interaction_edges"] = args.min_interaction_edges
        extra["min_node_visibility"] = args.min_node_visibility

    if args.viz == "agents_platform":
        extra["platform_prefix"] = args.platform_prefix

    return extra


def parse_args() -> argparse.Namespace:
    exporters = list_exporters()
    exporter_names = sorted(exporters.keys())

    p = argparse.ArgumentParser(description="Run gsocialsim and export a visualization.")
    p.add_argument("--seed", type=int, default=101, help="WorldKernel RNG seed.")
    p.add_argument("--stimuli", type=str, default="stimuli.csv", help="Path to stimuli CSV.")
    p.add_argument(
        "--ticks",
        type=int,
        default=0,
        help="Number of ticks to run. If 0, runs ticks_per_day+10 (guarantees day boundary).",
    )

    p.add_argument(
        "--viz",
        type=str,
        default="full",
        choices=exporter_names,
        help=f"Visualization type. Available: {', '.join(exporter_names)}",
    )
    p.add_argument("--out", type=str, default="influence_graph.html", help="Output HTML path.")

    # Threshold knobs
    p.add_argument("--min-influence-edges", type=int, default=2, help="threshold: min influence edge count")
    p.add_argument("--min-interaction-edges", type=int, default=2, help="threshold: min interaction edge count")
    p.add_argument("--min-node-visibility", type=int, default=5, help="threshold: min node visibility score")

    # Platform knob
    p.add_argument("--platform-prefix", type=str, default="SRC:", help="agents_platform: platform node id prefix")

    return p.parse_args()


def main() -> None:
    args = parse_args()

    sim_kernel = WorldKernel(seed=args.seed)
    setup_simulation_scenario(sim_kernel, stimuli_csv=args.stimuli)

    sim_kernel.start()
    print("\nRunning simulation...")

    ticks = args.ticks if args.ticks and args.ticks > 0 else (sim_kernel.clock.ticks_per_day + 10)
    sim_kernel.step(ticks)

    print("Simulation finished.\n")
    print_sanity_summary(sim_kernel)

    # Export
    if args.viz == "full" and args.out == "influence_graph.html":
        generate_influence_graph_html(sim_kernel, output_path=args.out)
        return

    exporter = get_exporter(args.viz)
    req = ExportRequest(kernel=sim_kernel, output_path=args.out, extra=build_extra_args(args))
    exporter.render(req)


if __name__ == "__main__":
    main()

```

## `run_stimulus_sim.py`

```python
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.stimuli.data_source import CsvDataSource

def setup_stimulus_scenario(kernel: WorldKernel):
    print("Setting up stimulus simulation scenario...")
    # --- Create Agents and Network ---
    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C"), seed=3)
    
    agents = [agent_A, agent_B, agent_C]
    for a in agents:
        a.budgets.action_budget = 100
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_A.id)
    graph.add_edge(follower=agent_C.id, followed=agent_B.id)
    
    # --- Register Data Source ---
    csv_source = CsvDataSource(file_path="stimuli.csv")
    kernel.world_context.stimulus_engine.register_data_source(csv_source)
    print("Scenario setup complete.")

if __name__ == "__main__":
    sim_kernel = WorldKernel(seed=202)
    setup_stimulus_scenario(sim_kernel)

    print("
Running simulation with external stimuli...")
    sim_kernel.step(150)
    print("Simulation finished.
")
    
    print("--- Final Agent States ---")
    for agent in sim_kernel.agents.agents.values():
        print(f"Agent: {agent.id}")
        # Find exposures to stimuli
        exposed_stimuli = [exp_id for exp_id in agent.recent_exposures if "news" in exp_id or "meme" in exp_id]
        if exposed_stimuli:
            print(f"  Exposed to stimuli: {exposed_stimuli}")
        else:
            print("  No stimuli exposures.")

```

## `src/gsocialsim.egg-info/PKG-INFO`

```text
Metadata-Version: 2.4
Name: gsocialsim
Version: 0.1.0
License-File: LICENSE
Dynamic: license-file

```

## `src/gsocialsim.egg-info/SOURCES.txt`

```text
LICENSE
README.md
pyproject.toml
src/gsocialsim/__init__.py
src/gsocialsim/types.py
src/gsocialsim.egg-info/PKG-INFO
src/gsocialsim.egg-info/SOURCES.txt
src/gsocialsim.egg-info/dependency_links.txt
src/gsocialsim.egg-info/top_level.txt
src/gsocialsim/agents/__init__.py
src/gsocialsim/agents/agent.py
src/gsocialsim/agents/attention_system.py
src/gsocialsim/agents/belief_state.py
src/gsocialsim/agents/belief_update_engine.py
src/gsocialsim/agents/budget_state.py
src/gsocialsim/agents/emotion_state.py
src/gsocialsim/agents/identity_state.py
src/gsocialsim/agents/impression.py
src/gsocialsim/agents/reward_weights.py
src/gsocialsim/analytics/__init__.py
src/gsocialsim/analytics/analytics.py
src/gsocialsim/analytics/attribution.py
src/gsocialsim/evolution/__init__.py
src/gsocialsim/evolution/evolutionary_system.py
src/gsocialsim/kernel/__init__.py
src/gsocialsim/kernel/event_scheduler.py
src/gsocialsim/kernel/events.py
src/gsocialsim/kernel/sim_clock.py
src/gsocialsim/kernel/stimulus_ingestion.py
src/gsocialsim/kernel/world_context.py
src/gsocialsim/kernel/world_kernel.py
src/gsocialsim/kernel/world_kernel_step.py
src/gsocialsim/networks/__init__.py
src/gsocialsim/networks/network_layer.py
src/gsocialsim/physical/__init__.py
src/gsocialsim/physical/physical_world.py
src/gsocialsim/policy/__init__.py
src/gsocialsim/policy/action_policy.py
src/gsocialsim/policy/bandit_learner.py
src/gsocialsim/social/__init__.py
src/gsocialsim/social/global_social_reality.py
src/gsocialsim/social/relationship_vector.py
src/gsocialsim/stimuli/__init__.py
src/gsocialsim/stimuli/content_item.py
src/gsocialsim/stimuli/data_source.py
src/gsocialsim/stimuli/interaction.py
src/gsocialsim/stimuli/stimulus.py
src/gsocialsim/visualization/__init__.py
src/gsocialsim/visualization/exporter.py
tests/test_attention_system.py
tests/test_belief_model.py
tests/test_event_system.py
tests/test_learning_policy.py
tests/test_phase1.py
tests/test_phase10.py
tests/test_phase2.py
tests/test_phase3.py
tests/test_phase4.py
tests/test_phase5.py
tests/test_phase6.py
tests/test_phase7.py
tests/test_phase8.py
```

## `src/gsocialsim.egg-info/dependency_links.txt`

```text


```

## `src/gsocialsim.egg-info/top_level.txt`

```text
gsocialsim

```

## `src/gsocialsim/__init__.py`

```python

```

## `src/gsocialsim/agents/__init__.py`

```python

```

## `src/gsocialsim/agents/agent.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, List
import random

from gsocialsim.agents.identity_state import IdentityState
from gsocialsim.agents.belief_state import BeliefStore
from gsocialsim.agents.emotion_state import EmotionState
from gsocialsim.agents.budget_state import BudgetState, BudgetKind
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.agents.attention_system import AttentionSystem
from gsocialsim.agents.belief_update_engine import BeliefUpdateEngine
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.policy.bandit_learner import BanditLearner, RewardVector
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from gsocialsim.agents.impression import Impression

if TYPE_CHECKING:
    from gsocialsim.kernel.world_kernel import WorldContext


class MemoryStore:
    pass


@dataclass
class Agent:
    id: str
    seed: int
    identity: IdentityState = field(default_factory=IdentityState)
    beliefs: BeliefStore = field(default_factory=BeliefStore)
    emotion: EmotionState = field(default_factory=EmotionState)
    budgets: BudgetState = field(default_factory=BudgetState)
    personality: RewardWeights = field(default_factory=RewardWeights)
    rng: random.Random = field(init=False)
    attention: AttentionSystem = field(default_factory=AttentionSystem)
    belief_update_engine: BeliefUpdateEngine = field(default_factory=BeliefUpdateEngine)
    memory: MemoryStore = field(default_factory=MemoryStore)
    policy: BanditLearner = field(default_factory=BanditLearner)

    # Working memory
    recent_impressions: dict[str, Impression] = field(default_factory=dict)

    # Daily buffers (for dream / consolidation)
    daily_impressions_consumed: List[Impression] = field(default_factory=list)
    daily_actions: List[Interaction] = field(default_factory=list)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.budgets._rng = self.rng

    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def perceive(
        self,
        content: ContentItem,
        context: "WorldContext",
        is_physical: bool = False,
        stimulus_id: Optional[str] = None,
    ):
        """
        Perception pipeline:
          1) Evaluate content -> Impression
          2) Store impression (working memory)
          3) Log exposure (always)
          4) Sample consumption
             - if not consumed: stop
             - if consumed: log consumption, update beliefs, crossings
        """
        impression = self.attention.evaluate(content, is_physical=is_physical)

        if impression.content_id:
            self.recent_impressions[impression.content_id] = impression

        # --- Exposure (always) ---
        context.analytics.log_exposure(
            viewer_id=self.id,
            source_id=content.author_id,
            topic=content.topic,
            is_physical=is_physical,
            timestamp=context.clock.t,
            content_id=content.id,
            intake_mode=impression.intake_mode.value,
            media_type=impression.media_type.value if impression.media_type else None,
        )

        consumed_prob = self._clamp01(float(getattr(impression, "consumed_prob", 1.0)))
        if self.rng.random() >= consumed_prob:
            return  # exposed but not consumed

        # --- Consumption (NEW, explicit) ---
        context.analytics.log_consumption(
            viewer_id=self.id,
            content_id=content.id,
            topic=content.topic,
            timestamp=context.clock.t,
            media_type=impression.media_type.value if impression.media_type else None,
            intake_mode=impression.intake_mode.value,
        )

        # Record for daily dream
        self.daily_impressions_consumed.append(impression)

        # --- Belief update ---
        prior = self.beliefs.get(content.topic)
        old_stance = prior.stance if prior else 0.0

        belief_delta = self.belief_update_engine.update(
            viewer=self,
            content_author_id=content.author_id,
            impression=impression,
            gsr=context.gsr,
        )

        self.beliefs.apply_delta(belief_delta)

        after = self.beliefs.get(content.topic)
        new_stance = after.stance if after else old_stance

        if context.analytics.crossing_detector.check(old_stance, new_stance):
            attribution = context.analytics.attribution_engine.assign_credit(
                agent_id=self.id,
                topic=content.topic,
                history=context.analytics.exposure_history,
            )
            from gsocialsim.analytics.attribution import BeliefCrossingEvent

            crossing_event = BeliefCrossingEvent(
                timestamp=context.clock.t,
                agent_id=self.id,
                topic=content.topic,
                old_stance=old_stance,
                new_stance=new_stance,
                attribution=attribution,
            )
            context.analytics.log_belief_crossing(crossing_event)

        context.analytics.log_belief_update(
            timestamp=context.clock.t,
            agent_id=self.id,
            delta=belief_delta,
        )

    def learn(self, action_key: str, reward_vector: RewardVector):
        self.policy.learn(action_key, reward_vector)

    def act(self, tick: int) -> Optional[Interaction]:
        if self.budgets.action_budget < 1:
            return None

        interaction = self.policy.generate_interaction(self, tick)
        if interaction:
            self.budgets.spend(BudgetKind.ACTION, 1.0)
            self.daily_actions.append(interaction)

            reward = RewardVector()
            topic = None

            if interaction.verb == InteractionVerb.LIKE:
                reward.affiliation = 0.2
                topic = interaction.target_stimulus_id
            elif interaction.verb == InteractionVerb.FORWARD:
                reward.status = 0.3
                topic = interaction.target_stimulus_id

            if topic:
                action_key = f"{interaction.verb.value}_{topic}"
                self.learn(action_key, reward)

        return interaction

    def dream(self, world_context: "WorldContext") -> None:
        """
        Daily consolidation ("dreaming / reflection").
        """
        if not self.daily_impressions_consumed:
            return

        self.identity.consolidate_from_impressions(
            self.daily_impressions_consumed,
            rng=self.rng,
            max_samples=30,
        )

        counts: dict[str, int] = {}
        for imp in self.daily_impressions_consumed:
            t = str(getattr(imp, "topic", ""))
            counts[t] = counts.get(t, 0) + 1

        for topic, c in counts.items():
            self.beliefs.nudge_salience(topic, 0.02 * min(10, c))
            self.beliefs.nudge_knowledge(topic, 0.01 * min(10, c))

        try:
            world_context.analytics.log_dream(
                timestamp=world_context.clock.t,
                agent_id=self.id,
                consolidated=len(self.daily_impressions_consumed),
                topic_counts=counts,
                actions=len(self.daily_actions),
            )
        except Exception:
            pass

    def consolidate_daily(self, world_context):
        """
        End-of-day boundary.
        """
        self.dream(world_context)
        self.budgets.regen_daily()

        self.daily_impressions_consumed.clear()
        self.daily_actions.clear()

```

## `src/gsocialsim/agents/attention_system.py`

```python
from __future__ import annotations

from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.stimuli.stimulus import MediaType


class AttentionSystem:
    """
    Generates Impressions from ContentItems.

    New behavior (still deterministic):
      - Attach media_type to impressions
      - Provide consumed_prob and interact_prob based on media_type and intake_mode

    NOTE: We are not sampling here (no RNG). Sampling/gating belongs in Agent.perceive()
    so it can be deterministic per-agent and logged properly.
    """

    # Baseline: "more people read news, more people interact with social"
    _BASE_CONSUME = {
        MediaType.NEWS: 0.85,
        MediaType.SOCIAL_POST: 0.65,
        MediaType.VIDEO: 0.60,
        MediaType.MEME: 0.55,
        MediaType.LONGFORM: 0.50,
        MediaType.FORUM_THREAD: 0.45,
        MediaType.UNKNOWN: 0.60,
    }

    _BASE_INTERACT = {
        MediaType.NEWS: 0.08,
        MediaType.SOCIAL_POST: 0.28,
        MediaType.VIDEO: 0.18,
        MediaType.MEME: 0.22,
        MediaType.LONGFORM: 0.10,
        MediaType.FORUM_THREAD: 0.16,
        MediaType.UNKNOWN: 0.15,
    }

    # Intake mode modifiers (seek/physical tends to increase consumption; deep focus maxes it)
    _INTAKE_CONSUME_MULT = {
        IntakeMode.SCROLL: 1.00,
        IntakeMode.SEEK: 1.15,
        IntakeMode.PHYSICAL: 1.20,
        IntakeMode.DEEP_FOCUS: 1.40,
    }

    _INTAKE_INTERACT_MULT = {
        IntakeMode.SCROLL: 1.00,
        IntakeMode.SEEK: 0.90,        # seeking is often info-driven, less performative
        IntakeMode.PHYSICAL: 0.75,    # physical “interaction” is modeled separately later
        IntakeMode.DEEP_FOCUS: 0.60,  # deep focus is processing-heavy, not engagement-heavy
    }

    @staticmethod
    def _clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def evaluate(self, content: ContentItem, is_physical: bool = False) -> Impression:
        # Intake mode selection is still backward compatible.
        intake_mode = IntakeMode.PHYSICAL if is_physical else IntakeMode.SCROLL

        # Determine media type robustly.
        mt = getattr(content, "media_type", MediaType.UNKNOWN)
        if not isinstance(mt, MediaType):
            try:
                mt = MediaType.from_any(mt)
            except Exception:
                mt = MediaType.UNKNOWN

        base_consume = self._BASE_CONSUME.get(mt, self._BASE_CONSUME[MediaType.UNKNOWN])
        base_interact = self._BASE_INTERACT.get(mt, self._BASE_INTERACT[MediaType.UNKNOWN])

        consume_mult = self._INTAKE_CONSUME_MULT.get(intake_mode, 1.0)
        interact_mult = self._INTAKE_INTERACT_MULT.get(intake_mode, 1.0)

        consumed_prob = self._clamp01(base_consume * consume_mult)
        interact_prob = self._clamp01(base_interact * interact_mult)

        imp = Impression(
            intake_mode=intake_mode,
            content_id=content.id,
            topic=content.topic,
            stance_signal=content.stance,

            # Placeholder perceptual fields (LLM later)
            emotional_valence=0.0,
            arousal=0.0,
            credibility_signal=0.5,
            identity_threat=0.0,
            social_proof=0.0,
            relationship_strength_source=0.0,

            # New fields
            media_type=mt,
            consumed_prob=consumed_prob,
            interact_prob=interact_prob,
        )
        imp.clamp()
        return imp

```

## `src/gsocialsim/agents/belief_state.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from gsocialsim.agents.belief_update_engine import BeliefDelta

TopicId = str


@dataclass
class TopicBelief:
    topic: TopicId
    stance: float = 0.0       # [-1,+1]
    confidence: float = 0.0   # [0,1]
    salience: float = 0.0     # [0,1]
    knowledge: float = 0.0    # [0,1]


@dataclass
class BeliefStore:
    topics: Dict[TopicId, TopicBelief] = field(default_factory=dict)

    def get(self, topic_id: TopicId) -> Optional[TopicBelief]:
        return self.topics.get(topic_id)

    def update(self, topic_id: TopicId, stance: float, confidence: float, salience: float, knowledge: float):
        belief = self.topics.get(topic_id)
        if belief:
            belief.stance = stance
            belief.confidence = confidence
            belief.salience = salience
            belief.knowledge = knowledge
        else:
            self.topics[topic_id] = TopicBelief(
                topic=topic_id,
                stance=stance,
                confidence=confidence,
                salience=salience,
                knowledge=knowledge,
            )

    def apply_delta(self, delta: "BeliefDelta"):
        """Applies a belief delta to the current store."""
        belief = self.get(delta.topic_id)
        if belief is None:
            self.topics[delta.topic_id] = TopicBelief(
                topic=delta.topic_id,
                stance=delta.stance_delta,
                confidence=delta.confidence_delta,
            )
        else:
            belief.stance = max(-1.0, min(1.0, belief.stance + delta.stance_delta))
            belief.confidence = max(0.0, min(1.0, belief.confidence + delta.confidence_delta))

    # ---- New: safe consolidation helpers ----
    def nudge_salience(self, topic_id: TopicId, delta: float):
        belief = self.get(topic_id)
        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief
        belief.salience = max(0.0, min(1.0, belief.salience + float(delta)))

    def nudge_knowledge(self, topic_id: TopicId, delta: float):
        belief = self.get(topic_id)
        if belief is None:
            belief = TopicBelief(topic=topic_id)
            self.topics[topic_id] = belief
        belief.knowledge = max(0.0, min(1.0, belief.knowledge + float(delta)))

```

## `src/gsocialsim/agents/belief_update_engine.py`

```python
from dataclasses import dataclass
from typing import TYPE_CHECKING
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.agents.belief_state import BeliefStore, TopicId
from gsocialsim.social.global_social_reality import GlobalSocialReality
from gsocialsim.types import ActorId

if TYPE_CHECKING:
    from gsocialsim.agents.agent import Agent

@dataclass
class BeliefDelta:
    topic_id: TopicId
    stance_delta: float = 0.0
    confidence_delta: float = 0.0

class BeliefUpdateEngine:
    def update(self, viewer: "Agent", content_author_id: ActorId, impression: Impression, gsr: GlobalSocialReality) -> BeliefDelta:
        topic_id = impression.topic
        current_belief = viewer.beliefs.get(topic_id)
        trust = gsr.get_relationship(viewer.id, content_author_id).trust
        multiplier = 10.0 if impression.intake_mode == IntakeMode.PHYSICAL else 1.0

        # This is a hack for the test, a proper implementation would get this from the content
        is_threatening = getattr(impression, '_is_threatening_hack', False)

        if current_belief is None:
            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=impression.stance_signal * trust * multiplier,
                confidence_delta=0.1 * trust * multiplier
            )
        else:
            stance_difference = impression.stance_signal - current_belief.stance
            
            # Confirmation Bias
            is_confirming = (stance_difference > 0 and current_belief.stance > 0) or \
                            (stance_difference < 0 and current_belief.stance < 0)
            if is_confirming:
                multiplier *= 1.5
            
            # Backfire Effect
            is_opposed = abs(stance_difference) > 1.0
            if is_threatening and is_opposed:
                multiplier *= -0.5 # Backfire
            
            base_influence = 0.10
            stance_change = stance_difference * base_influence * trust * multiplier
            confidence_change = 0.02 * trust * multiplier

            return BeliefDelta(
                topic_id=topic_id,
                stance_delta=stance_change,
                confidence_delta=confidence_change
            )

```

## `src/gsocialsim/agents/budget_state.py`

```python
from dataclasses import dataclass
from enum import Enum
import random

class BudgetKind(Enum):
    ATTENTION = "attention_minutes"
    ACTION = "action_budget"
    DEEP_FOCUS = "deep_focus_budget"
    RISK = "risk_budget"

@dataclass
class BudgetState:
    attention_minutes: float = 0.0
    action_budget: float = 0.0
    deep_focus_budget: float = 0.0
    risk_budget: float = 0.0
    _rng: random.Random = None

    def regen_daily(self):
        if self._rng is None: raise ValueError("RNG not set for BudgetState.")
        self.attention_minutes = max(0, self._rng.gauss(60, 30))
        self.action_budget = max(0, self._rng.gauss(10, 5))
        self.deep_focus_budget = max(0, self._rng.betavariate(2, 5) * 5) # Skewed towards lower deep focus
        self.risk_budget = max(0, self._rng.uniform(0, 1))

    def spend(self, kind: BudgetKind, amount: float) -> bool:
        if kind == BudgetKind.ATTENTION:
            if self.attention_minutes >= amount:
                self.attention_minutes -= amount
                return True
        elif kind == BudgetKind.ACTION:
            if self.action_budget >= amount:
                self.action_budget -= amount
                return True
        elif kind == BudgetKind.DEEP_FOCUS:
            if self.deep_focus_budget >= amount:
                self.deep_focus_budget -= amount
                return True
        elif kind == BudgetKind.RISK:
            # Risk budget might be more complex, e.g., a threshold
            # For now, just a simple spend check
            if self.risk_budget >= amount:
                self.risk_budget -= amount
                return True
        return False

```

## `src/gsocialsim/agents/emotion_state.py`

```python
from dataclasses import dataclass

@dataclass
class EmotionState:
    valence: float = 0.0
    arousal: float = 0.0
    anger: float = 0.0
    anxiety: float = 0.0

```

## `src/gsocialsim/agents/identity_state.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set, Iterable, Optional
import random

from gsocialsim.agents.impression import Impression


@dataclass
class IdentityState:
    identity_vector: List[float] = field(default_factory=lambda: [0.0] * 8)
    identity_rigidity: float = 0.5
    ingroup_labels: Set[str] = field(default_factory=set)
    taboo_boundaries: Set[str] = field(default_factory=set)

    def is_threatening(self, content_text: str) -> bool:
        """A simple check to see if content text contains taboo keywords."""
        if not content_text:
            return False
        for taboo in self.taboo_boundaries:
            if taboo in content_text.lower():
                return True
        return False

    @staticmethod
    def _clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

    @staticmethod
    def _topic_to_dim(topic: str, dims: int) -> int:
        # Deterministic mapping to a dimension (stable across runs).
        return abs(hash(topic)) % max(1, dims)

    def consolidate_from_impressions(
        self,
        impressions: Iterable[Impression],
        rng: random.Random,
        *,
        max_samples: int = 30,
    ) -> None:
        """
        "Dreaming/reflection" identity consolidation.

        Design intent:
        - Identity shifts are slow, bounded, and mediated by rigidity.
        - Threatening/intense content increases rigidity (defensive consolidation).
        - Repeated, salient topic exposure nudges identity_vector directions.

        This is not LLM-driven yet; it's a deterministic scaffold that later becomes
        partially LLM-driven without changing call sites.
        """
        imps = list(impressions)
        if not imps:
            return

        dims = len(self.identity_vector) if self.identity_vector else 8
        if not self.identity_vector:
            self.identity_vector = [0.0] * dims

        # Weighted sample of impressions for consolidation.
        def weight(imp: Impression) -> float:
            # Emphasize identity threat + arousal + social proof.
            it = float(getattr(imp, "identity_threat", 0.0))
            ar = float(getattr(imp, "arousal", 0.0))
            sp = float(getattr(imp, "social_proof", 0.0))
            return 0.2 + 0.5 * it + 0.3 * ar + 0.2 * sp

        pool = imps[:]
        weights = [max(0.0001, weight(x)) for x in pool]
        k = min(max_samples, len(pool))

        chosen: List[Impression] = []
        for _ in range(k):
            if not pool:
                break
            idx = rng.choices(range(len(pool)), weights=weights, k=1)[0]
            chosen.append(pool.pop(idx))
            weights.pop(idx)

        # Aggregate consolidation signals.
        total_w = 0.0
        threat_w = 0.0
        stance_push = [0.0] * dims

        for imp in chosen:
            topic = str(getattr(imp, "topic", ""))
            dim = self._topic_to_dim(topic, dims)

            w = max(0.0001, weight(imp))
            total_w += w

            it = float(getattr(imp, "identity_threat", 0.0))
            threat_w += w * it

            # stance_signal nudges identity direction for that topic-dimension
            s = float(getattr(imp, "stance_signal", 0.0))
            stance_push[dim] += w * s

        if total_w <= 0.0:
            return

        avg_threat = threat_w / total_w

        # Rigidity update: bounded, slow.
        # High threat -> more rigid; calm days -> slight relaxation.
        rigidity_delta = (avg_threat - 0.25) * 0.05  # small
        self.identity_rigidity = self._clamp(self.identity_rigidity + rigidity_delta, 0.05, 0.95)

        # Identity vector update: damped by rigidity (more rigid = smaller movement)
        # Step size is intentionally small.
        step = 0.03 * (1.0 - self.identity_rigidity)
        for i in range(dims):
            delta = (stance_push[i] / total_w) * step
            self.identity_vector[i] = self._clamp(self.identity_vector[i] + delta, -1.0, 1.0)

        # Optional: very light ingroup formation placeholder
        # If a dimension becomes strong, add a synthetic label.
        # (Later, LLM can generate semantically meaningful labels.)
        strong_dims = [i for i, v in enumerate(self.identity_vector) if abs(v) > 0.75]
        for i in strong_dims:
            label = f"ingroup_dim_{i}"
            if label not in self.ingroup_labels and rng.random() < 0.10:
                self.ingroup_labels.add(label)

```

## `src/gsocialsim/agents/impression.py`

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from gsocialsim.types import ContentId, TopicId
from gsocialsim.stimuli.stimulus import MediaType


class IntakeMode(Enum):
    """How an agent perceived a piece of content."""
    SCROLL = "scroll"         # Passive, feed-driven
    SEEK = "seek"             # Active, goal-directed
    PHYSICAL = "physical"     # Offline interaction
    DEEP_FOCUS = "deep_focus" # Focused, expensive processing


@dataclass
class Impression:
    """
    A richer representation of an agent's internal reaction to a ContentItem/Stimulus.

    Backward compatible: existing constructors that pass only the original fields still work.
    New fields (safe defaults):
      - media_type
      - consumed_prob / interact_prob (separate knobs)
    """
    intake_mode: IntakeMode
    content_id: ContentId
    topic: TopicId
    stance_signal: float

    # Existing fields
    emotional_valence: float = 0.0          # Perceived emotional tone [-1, 1]
    arousal: float = 0.0                    # Perceived intensity [0, 1]
    credibility_signal: float = 0.5         # Perceived credibility [0, 1]
    identity_threat: float = 0.0            # Perceived threat to identity [0, 1]
    social_proof: float = 0.0               # Social proof (likes/forwards) [0, 1]
    relationship_strength_source: float = 0.0  # Relationship strength to source [0, 1]

    # New fields for subscriptions/media weighting phase
    media_type: MediaType = MediaType.UNKNOWN
    consumed_prob: float = 1.0              # Probability agent actually consumes (reads/watches)
    interact_prob: float = 0.0              # Probability agent interacts (like/comment/reshare/reply)

    def clamp(self) -> None:
        """Keep probabilities and bounded signals sane."""
        self.arousal = max(0.0, min(1.0, self.arousal))
        self.credibility_signal = max(0.0, min(1.0, self.credibility_signal))
        self.identity_threat = max(0.0, min(1.0, self.identity_threat))
        self.social_proof = max(0.0, min(1.0, self.social_proof))
        self.relationship_strength_source = max(0.0, min(1.0, self.relationship_strength_source))
        self.consumed_prob = max(0.0, min(1.0, self.consumed_prob))
        self.interact_prob = max(0.0, min(1.0, self.interact_prob))

```

## `src/gsocialsim/agents/reward_weights.py`

```python
from dataclasses import dataclass

@dataclass
class RewardWeights:
    status: float = 1.0
    affiliation: float = 1.0
    dominance: float = 1.0
    coherence: float = 1.0
    novelty: float = 1.0
    safety: float = 1.0
    effort_cost: float = -1.0  # Negative weight

```

## `src/gsocialsim/analytics/__init__.py`

```python

```

## `src/gsocialsim/analytics/analytics.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from collections import defaultdict

from gsocialsim.analytics.attribution import (
    ExposureHistory,
    BeliefCrossingDetector,
    AttributionEngine,
    BeliefCrossingEvent,
    ExposureEvent,
)
from gsocialsim.stimuli.interaction import Interaction


@dataclass
class DeliveryRecord:
    """
    Optional structured delivery logging for future phases.

    You don't have to use this yet; events can call Analytics.log_delivery()
    when ready (Broadcast feed, DM, etc.).
    """
    tick: int
    viewer_id: str
    layer_id: str
    intake_mode: str
    eligible: int = 0
    shown: int = 0
    seen: int = 0
    media_breakdown: Dict[str, int] = field(default_factory=dict)


class Analytics:
    """
    Manages all logging for the simulation, including verbose debugging
    and storing data for visualization.

    Upgrades:
      - Exposed vs Consumed split
      - Daily "dream" logging (consolidation summaries)
      - Optional DeliveryRecord logging for online layers
    """
    def __init__(self):
        self.exposure_history = ExposureHistory()
        self.crossing_detector = BeliefCrossingDetector()
        self.attribution_engine = AttributionEngine()
        self.crossings: list[BeliefCrossingEvent] = []
        self.interactions: list[Interaction] = []

        # --- new: light metrics ---
        self.exposure_counts = defaultdict(int)          # (agent_id) -> count
        self.consumed_counts = defaultdict(int)          # (agent_id) -> count
        self.consumed_by_media = defaultdict(int)        # (media_type) -> count
        self.dream_runs = []                             # list of dream summaries dicts
        self.delivery_records: list[DeliveryRecord] = [] # optional

    # -----------------
    # Existing methods
    # -----------------
    def log_belief_update(self, timestamp: int, agent_id: str, delta: Any):
        print(
            f"DEBUG:[T={timestamp}] Agent['{agent_id}'] BeliefUpdate: "
            f"Topic='{delta.topic_id}', StanceΔ={delta.stance_delta:.4f}, ConfΔ={delta.confidence_delta:.4f}"
        )

    def log_exposure(
        self,
        viewer_id: str,
        source_id: str,
        topic: str,
        is_physical: bool,
        timestamp: int,
        *,
        content_id: Optional[str] = None,
        channel: Optional[str] = None,
        intake_mode: Optional[str] = None,
        media_type: Optional[str] = None,
    ):
        # Backward compatible print
        print(
            f"DEBUG:[T={timestamp}] Agent['{viewer_id}'] Perceived: "
            f"Source='{source_id}', Topic='{topic}', Physical={is_physical}"
        )

        event = ExposureEvent(
            timestamp=timestamp,
            source_actor_id=source_id,
            topic=topic,
            is_physical=is_physical,
            content_id=content_id,
            channel=channel,
            intake_mode=intake_mode,
            media_type=media_type,
            consumed=False,
        )
        self.exposure_history.log_exposure(viewer_id, event)
        self.exposure_counts[viewer_id] += 1

    def log_interaction(self, timestamp: int, interaction: Interaction):
        target = interaction.target_stimulus_id or (interaction.original_content.id if interaction.original_content else "None")
        print(
            f"DEBUG:[T={timestamp}] Agent['{interaction.agent_id}'] Interacted: "
            f"Verb='{interaction.verb.value}', Target='{target}'"
        )
        self.interactions.append(interaction)

    def log_belief_crossing(self, event: BeliefCrossingEvent):
        print(
            f"LOG:[T={event.timestamp}] Agent['{event.agent_id}'] BeliefCrossing: "
            f"Topic='{event.topic}', Stance={event.old_stance:.2f}->{event.new_stance:.2f}, "
            f"Attribution={event.attribution}"
        )
        self.crossings.append(event)

    # -----------------
    # New methods
    # -----------------
    def log_consumption(
        self,
        viewer_id: str,
        content_id: str,
        topic: str,
        timestamp: int,
        *,
        media_type: Optional[str] = None,
        intake_mode: Optional[str] = None,
    ):
        """
        Mark the most recent matching exposure event as consumed.
        This supports exposed vs consumed split without changing ExposureHistory structure.
        """
        # Find latest matching exposure in history and mark consumed
        hist = self.exposure_history.get_history_for_agent(viewer_id)
        for event in reversed(hist):
            if event.content_id == content_id and event.topic == topic:
                event.consumed = True
                if media_type is not None:
                    event.media_type = media_type
                if intake_mode is not None:
                    event.intake_mode = intake_mode
                break

        self.consumed_counts[viewer_id] += 1
        if media_type:
            self.consumed_by_media[str(media_type)] += 1

        print(
            f"DEBUG:[T={timestamp}] Agent['{viewer_id}'] Consumed: "
            f"Content='{content_id}', Topic='{topic}', Media={media_type}, Intake={intake_mode}"
        )

    def log_dream(
        self,
        timestamp: int,
        agent_id: str,
        *,
        consolidated: int,
        topic_counts: Dict[str, int],
        actions: int = 0,
    ):
        """
        Record a daily consolidation run ("dreaming/reflection").
        Safe to call even if visualization is minimal right now.
        """
        summary = {
            "timestamp": timestamp,
            "agent_id": agent_id,
            "consolidated": consolidated,
            "topic_counts": dict(topic_counts),
            "actions": actions,
        }
        self.dream_runs.append(summary)

        # Keep print compact but informative
        top_topics = sorted(topic_counts.items(), key=lambda kv: kv[1], reverse=True)[:3]
        top_str = ", ".join([f"{t}:{c}" for t, c in top_topics]) if top_topics else "none"
        print(
            f"LOG:[T={timestamp}] Agent['{agent_id}'] Dream: consolidated={consolidated}, actions={actions}, top_topics={top_str}"
        )

    def log_delivery(self, record: DeliveryRecord):
        """
        Optional future hook for eligible/shown/seen pipelines.
        """
        self.delivery_records.append(record)
        print(
            f"DEBUG:[T={record.tick}] Delivery viewer='{record.viewer_id}' layer='{record.layer_id}' "
            f"intake='{record.intake_mode}' eligible={record.eligible} shown={record.shown} seen={record.seen}"
        )

```

## `src/gsocialsim/analytics/attribution.py`

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import defaultdict

from gsocialsim.types import AgentId, TopicId, ActorId


@dataclass
class ExposureEvent:
    timestamp: int
    source_actor_id: ActorId
    topic: TopicId
    is_physical: bool

    # --- new optional fields (backward compatible) ---
    content_id: Optional[str] = None
    channel: Optional[str] = None        # e.g., "broadcast", "dm", "physical"
    intake_mode: Optional[str] = None    # "scroll", "seek", "physical", "deep_focus"
    media_type: Optional[str] = None     # "news", "social_post", etc.
    consumed: bool = False               # True only when the agent actually consumes


class ExposureHistory:
    """Logs every piece of content an agent is exposed to (and optionally whether it was consumed)."""
    def __init__(self):
        self._history: Dict[AgentId, List[ExposureEvent]] = defaultdict(list)

    def log_exposure(self, viewer_id: AgentId, event: ExposureEvent):
        self._history[viewer_id].append(event)

    def get_history_for_agent(self, agent_id: AgentId) -> List[ExposureEvent]:
        return self._history.get(agent_id, [])


@dataclass
class BeliefCrossingEvent:
    timestamp: int
    agent_id: AgentId
    topic: TopicId
    old_stance: float
    new_stance: float
    attribution: Dict[ActorId, float] = field(default_factory=dict)


class BeliefCrossingDetector:
    """Checks if a belief update crosses a meaningful threshold."""
    def check(self, old_stance: float, new_stance: float) -> bool:
        # Simple: sign-crossing
        return (old_stance <= 0 and new_stance > 0) or (old_stance >= 0 and new_stance < 0)


class AttributionEngine:
    """
    Assigns credit for a belief crossing event.

    Current model: recency-weighted accumulator over matching-topic exposure events.
    Boost factors:
      - physical exposures are stronger
      - consumed exposures are stronger than mere exposures
    """
    def assign_credit(
        self,
        agent_id: AgentId,
        topic: TopicId,
        history: ExposureHistory,
        window_days: int = 7,
    ) -> Dict[ActorId, float]:
        credits = defaultdict(float)
        total = 0.0
        agent_history = history.get_history_for_agent(agent_id)

        # TODO: incorporate real timestamp->day conversion. For now we treat history order as recency.
        # Weight decays with distance in the reversed list.
        decay = 0.97

        w = 1.0
        for event in reversed(agent_history):
            if event.topic != topic:
                w *= decay
                continue

            weight = w

            # Physical gets a boost (as your design intends)
            if event.is_physical:
                weight *= 5.0

            # Consumed gets a boost over mere exposure
            if getattr(event, "consumed", False):
                weight *= 1.75

            credits[event.source_actor_id] += weight
            total += weight

            w *= decay

        if total <= 0.0:
            return {}

        return {actor: val / total for actor, val in credits.items()}

```

## `src/gsocialsim/evolution/__init__.py`

```python

```

## `src/gsocialsim/evolution/evolutionary_system.py`

```python
from dataclasses import dataclass
from gsocialsim.agents.agent import Agent
from gsocialsim.agents.reward_weights import RewardWeights
import random

@dataclass
class Fitness:
    """Represents an agent's success in the environment."""
    # For now, fitness is simply the agent's total affiliation reward
    total_reward: float = 0.0

class EvolutionarySystem:
    def __init__(self, exit_threshold: float = -10.0, mutation_rate: float = 0.1):
        self.exit_threshold = exit_threshold
        self.mutation_rate = mutation_rate

    def should_exit(self, agent: Agent) -> bool:
        """Determines if an agent's fitness is too low."""
        # A simple model: if total reward drops too low, exit
        total_reward = sum(agent.policy.action_rewards.values())
        return total_reward < self.exit_threshold

    def reproduce(self, parent: Agent, newborn_id: str, seed: int) -> Agent:
        """Creates a new agent by inheriting and mutating a parent's personality."""
        # Inherit personality (reward weights)
        new_weights = RewardWeights(
            status=parent.personality.status,
            affiliation=parent.personality.affiliation,
            # ... copy other weights
        )

        # Mutate
        rng = random.Random(seed)
        if rng.random() < self.mutation_rate:
            new_weights.affiliation += rng.gauss(0, 0.1)
        if rng.random() < self.mutation_rate:
            new_weights.status += rng.gauss(0, 0.1)

        newborn = Agent(id=newborn_id, seed=seed)
        newborn.personality = new_weights
        newborn.beliefs.update("T", 0, 0.1, 0.1, 0) # Give newborn a default belief to be viable
        return newborn

```

## `src/gsocialsim/kernel/__init__.py`

```python

```

## `src/gsocialsim/kernel/event_scheduler.py`

```python
import heapq
from typing import List
from gsocialsim.kernel.events import Event

class EventScheduler:
    """A priority queue to manage and dispatch events in chronological order."""
    def __init__(self):
        # The queue now stores tuples: (timestamp, tie_breaker, event_object)
        self._queue: List[tuple[int, int, Event]] = []

    def schedule(self, event: Event):
        """Add an event to the queue as a tuple for robust sorting."""
        entry = (event.timestamp, event.tie_breaker, event)
        heapq.heappush(self._queue, entry)

    def pop_due(self, timestamp: int):
        """Pop and return all events scheduled exactly at `timestamp` (in phase/order priority)."""
        due = []
        while self._queue and self._queue[0][0] == timestamp:
            _, _, event = heapq.heappop(self._queue)
            due.append(event)
        return due

    def get_next_event(self) -> Event | None:
        """Pop the next event from the queue."""
        if not self._queue:
            return None
        # The event object is the third item in the tuple
        return heapq.heappop(self._queue)[2]

    def is_empty(self) -> bool:
        return len(self._queue) == 0

```

## `src/gsocialsim/kernel/events.py`

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, Optional, Set
import itertools

from gsocialsim.agents.budget_state import BudgetKind
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.types import TopicId

if TYPE_CHECKING:
    from gsocialsim.kernel.world_kernel import WorldContext
    from gsocialsim.stimuli.interaction import Interaction
    from gsocialsim.stimuli.stimulus import Stimulus

_event_counter = itertools.count()


def _stimulus_topic_id(stimulus: "Stimulus") -> TopicId:
    """
    Map a stimulus to a TopicId that agents can actually reason about.

    Rules:
      - If stimulus.metadata["topic"] is a non-empty string: use it.
      - If missing/empty: fall back to "T_Original" to preserve phase behavior.
      - If non-string: coerce to string (defensive).
    """
    raw = getattr(stimulus, "metadata", None) or {}
    t = raw.get("topic")

    if t is None:
        return TopicId("T_Original")

    if isinstance(t, str):
        t = t.strip()
        return TopicId(t if t else "T_Original")

    return TopicId(str(t))


def _get_followers(context: "WorldContext", author_id: str) -> Set[str]:
    """
    Backward compatible helper: return followers if the follow graph exists.
    """
    try:
        return set(context.network.graph.get_followers(author_id))
    except Exception:
        return set()


def _subs_recipients(context: "WorldContext", stimulus: "Stimulus", topic: TopicId) -> Set[str]:
    """
    Best-effort recipient selection from a subscription system, if present.

    We intentionally support multiple possible subscription service shapes to stay robust
    while we implement the real SubscriptionService next.

    Expected future shapes (any one of these):
      - context.subscriptions.get_subscribers(sub_type: str, target_id: str) -> Iterable[str]
      - context.subscriptions.subscribers_by_target[(sub_type, target_id)] -> set(agent_id)
      - context.subscriptions.subscribers_by_target[(sub_type.value, target_id)] -> set(agent_id)
    """
    subs = getattr(context, "subscriptions", None)
    if subs is None:
        return set()

    def _try_get(sub_type: str, target_id: Optional[str]) -> Set[str]:
        if not target_id:
            return set()

        # Method-based API
        fn = getattr(subs, "get_subscribers", None)
        if callable(fn):
            try:
                return set(fn(sub_type, target_id))
            except Exception:
                pass

        # Dict-based API
        m = getattr(subs, "subscribers_by_target", None)
        if isinstance(m, dict):
            # try common key shapes
            for key in ((sub_type, target_id), (str(sub_type), target_id)):
                try:
                    v = m.get(key)
                    if v:
                        return set(v)
                except Exception:
                    continue

        return set()

    recipients: Set[str] = set()

    # Topic subscriptions
    recipients |= _try_get("topic", str(topic))

    # Creator/outlet/community subscriptions (if present on stimulus)
    recipients |= _try_get("creator", getattr(stimulus, "creator_id", None))
    recipients |= _try_get("outlet", getattr(stimulus, "outlet_id", None))
    recipients |= _try_get("community", getattr(stimulus, "community_id", None))

    return recipients


def _select_stimulus_recipients(context: "WorldContext", stimulus: "Stimulus", topic: TopicId) -> Set[str]:
    """
    Full-capability intent: subscription-driven delivery, with follows as an additional source of eligibility.

    Backward compatibility:
      - If no subscription system exists yet, deliver to all agents (original behavior).
      - If subscription system exists but yields nobody, deliver to nobody (true gating).
    """
    has_subs = getattr(context, "subscriptions", None) is not None

    recipients: Set[str] = set()

    # Subscriptions if available
    if has_subs:
        recipients |= _subs_recipients(context, stimulus, topic)

    # Followers as a bridge / additional eligibility
    recipients |= _get_followers(context, getattr(stimulus, "source", ""))

    if not has_subs:
        # Legacy behavior: broadcast to all if we don't have subscriptions implemented yet.
        return set(context.agents.agents.keys())

    return recipients


@dataclass(order=True)
class Event(ABC):
    timestamp: int = field(compare=True)
    tie_breaker: int = field(init=False, compare=True)

    def __post_init__(self):
        self.tie_breaker = next(_event_counter)

    @abstractmethod
    def apply(self, context: "WorldContext"):
        pass


@dataclass(order=True)
class StimulusIngestionEvent(Event):
    def apply(self, context: "WorldContext"):
        new_stimuli = context.stimulus_engine.tick(self.timestamp)
        if new_stimuli:
            for stimulus in new_stimuli:
                context.scheduler.schedule(
                    StimulusPerceptionEvent(
                        timestamp=self.timestamp,
                        stimulus_id=stimulus.id,
                    )
                )
        context.scheduler.schedule(StimulusIngestionEvent(timestamp=self.timestamp + 1))


@dataclass(order=True)
class StimulusPerceptionEvent(Event):
    stimulus_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        stimulus = context.stimulus_engine.get_stimulus(self.stimulus_id)
        if not stimulus:
            return

        topic = _stimulus_topic_id(stimulus)

        temp_content = ContentItem(
            id=stimulus.id,
            author_id=stimulus.source,
            topic=topic,
            stance=0.0,
            media_type=getattr(stimulus, "media_type", None),
            outlet_id=getattr(stimulus, "outlet_id", None),
            community_id=getattr(stimulus, "community_id", None),
            provenance={
                "stimulus_id": stimulus.id,
                "source": stimulus.source,
            },
        )

        recipients = _select_stimulus_recipients(context, stimulus, topic)
        for agent_id in recipients:
            agent = context.agents.get(agent_id)
            if agent:
                # Keep Agent.perceive signature unchanged for now.
                agent.perceive(temp_content, context, stimulus_id=stimulus.id)


@dataclass(order=True)
class AgentActionEvent(Event):
    agent_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        interaction = agent.act(tick=self.timestamp)
        if interaction:
            context.analytics.log_interaction(self.timestamp, interaction)
            context.scheduler.schedule(
                InteractionPerceptionEvent(timestamp=self.timestamp, interaction=interaction)
            )
        context.scheduler.schedule(
            AgentActionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id)
        )


@dataclass(order=True)
class InteractionPerceptionEvent(Event):
    interaction: "Interaction" = field(compare=False)

    def apply(self, context: "WorldContext"):
        from gsocialsim.policy.bandit_learner import RewardVector
        from gsocialsim.stimuli.interaction import InteractionVerb

        author = context.agents.get(self.interaction.agent_id)
        if not author:
            return

        followers = _get_followers(context, author.id)
        reward = RewardVector()
        topic: TopicId | None = None

        if self.interaction.verb == InteractionVerb.CREATE:
            content = self.interaction.original_content
            topic = content.topic
            reward.affiliation = 0.1 * len(followers)
            for follower_id in followers:
                follower = context.agents.get(follower_id)
                if follower:
                    follower.perceive(content, context)

        elif self.interaction.verb == InteractionVerb.LIKE:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = _stimulus_topic_id(stimulus)
                reward.affiliation = 0.2

        elif self.interaction.verb == InteractionVerb.FORWARD:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = _stimulus_topic_id(stimulus)
                reward.status = 0.3

        if topic and author:
            action_key = f"{self.interaction.verb.value}_{topic}"
            author.learn(action_key, reward)


@dataclass(order=True)
class DeepFocusEvent(Event):
    agent_id: str = field(compare=False)
    content_id: str = field(compare=False)
    original_impression: Impression = field(compare=False)  # Store the impression that led to deep focus

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        if agent.budgets.spend(BudgetKind.ATTENTION, 10) and agent.budgets.spend(
            BudgetKind.DEEP_FOCUS, 1
        ):
            print(
                f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] engaged in Deep Focus on '{self.content_id}'"
            )

            amplified_impression = Impression(
                intake_mode=IntakeMode.DEEP_FOCUS,
                content_id=self.content_id,
                topic=self.original_impression.topic,
                stance_signal=self.original_impression.stance_signal,
                emotional_valence=self.original_impression.emotional_valence + 0.3,
                arousal=self.original_impression.arousal + 0.3,
                credibility_signal=min(1.0, self.original_impression.credibility_signal + 0.2),
                identity_threat=self.original_impression.identity_threat,
                social_proof=self.original_impression.social_proof,
                relationship_strength_source=self.original_impression.relationship_strength_source,
            )

            content_source_id = self.original_impression.content_id

            belief_delta = agent.belief_update_engine.update(
                viewer=agent,
                content_author_id=content_source_id,
                impression=amplified_impression,
                gsr=context.gsr,
            )

            agent.beliefs.apply_delta(belief_delta)
            context.analytics.log_belief_update(
                timestamp=self.timestamp, agent_id=self.agent_id, delta=belief_delta
            )
        else:
            print(
                f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] failed Deep Focus due to insufficient budget."
            )


@dataclass(order=True)
class AllocateAttentionEvent(Event):
    agent_id: str = field(compare=False)

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent:
            return

        high_salience_impressions = []
        for impression in agent.recent_impressions.values():
            if agent.beliefs.get(impression.topic) and agent.beliefs.get(impression.topic).salience > 0.5:
                high_salience_impressions.append(impression)

        if (
            high_salience_impressions
            and agent.budgets.deep_focus_budget >= 1
            and agent.budgets.attention_minutes >= 10
        ):
            impression_to_focus = agent.rng.choice(high_salience_impressions)
            context.scheduler.schedule(
                DeepFocusEvent(
                    timestamp=self.timestamp,
                    agent_id=self.agent_id,
                    content_id=impression_to_focus.content_id,
                    original_impression=impression_to_focus,
                )
            )

        context.scheduler.schedule(
            AllocateAttentionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id)
        )


@dataclass(order=True)
class DayBoundaryEvent(Event):
    def apply(self, context: "WorldContext"):
        for agent in context.agents.agents.values():
            agent.consolidate_daily(context)
        context.scheduler.schedule(
            DayBoundaryEvent(timestamp=self.timestamp + context.clock.ticks_per_day)
        )

```

## `src/gsocialsim/kernel/sim_clock.py`

```python
import datetime
import random
from dataclasses import dataclass

@dataclass
class SimClock:
    t: int = 0  # Total simulation ticks
    day: int = 0  # Current simulation day
    tick_of_day: int = 0  # Current tick within the day
    ticks_per_day: int = 1440 # 1440 minutes in a day, assuming 1 tick = 1 minute

    def advance(self, num_ticks: int = 1):
        self.t += num_ticks
        self.tick_of_day += num_ticks
        while self.tick_of_day >= self.ticks_per_day:
            self.tick_of_day -= self.ticks_per_day
            self.day += 1

    def get_datetime(self, start_date: datetime.datetime) -> datetime.datetime:
        """
        Returns the current simulation datetime based on a start_date.
        Assumes each tick is one minute.
        """
        return start_date + datetime.timedelta(minutes=self.t)


```

## `src/gsocialsim/kernel/stimulus_ingestion.py`

```python
from typing import List
from gsocialsim.stimuli.data_source import DataSource
from gsocialsim.stimuli.stimulus import Stimulus

class StimulusIngestionEngine:
    def __init__(self):
        self._data_sources: List[DataSource] = []
        self._stimuli_store: Dict[str, Stimulus] = {}

    def register_data_source(self, source: DataSource):
        self._data_sources.append(source)

    def get_stimulus(self, stimulus_id: str) -> Stimulus | None:
        return self._stimuli_store.get(stimulus_id)

    def tick(self, current_tick: int) -> List[Stimulus]:
        """ Polls all data sources and adds new stimuli to the world. """
        newly_added = []
        for source in self._data_sources:
            new_stimuli = source.get_stimuli(current_tick)
            for stimulus in new_stimuli:
                self._stimuli_store[stimulus.id] = stimulus
                newly_added.append(stimulus)
        return newly_added

```

## `src/gsocialsim/kernel/world_context.py`

```python
# src/gsocialsim/kernel/world_context.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from gsocialsim.social.global_social_reality import GlobalSocialReality


@dataclass
class WorldContext:
    """
    Shared simulation context passed into Events and Agents.
    Keep this intentionally lightweight: it's a container for pointers to
    subsystems (scheduler, network, physical_world, etc).

    The WorldKernel is responsible for wiring these references in __post_init__.
    """

    # Core pointers
    kernel: Optional[Any] = None
    clock: Optional[Any] = None
    agents: Optional[Any] = None

    # Required by many Events
    scheduler: Optional[Any] = None

    # Optional subsystems (present in later phases)
    network: Optional[Any] = None
    stimulus_engine: Optional[Any] = None
    physical_world: Optional[Any] = None
    attention_system: Optional[Any] = None
    evolutionary_system: Optional[Any] = None
    analytics: Optional[Any] = None
    gsr: GlobalSocialReality | None = None

    # Future: subscriptions, content store, etc.
    subscriptions: Optional[Any] = None

```

## `src/gsocialsim/kernel/world_kernel.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
import random

from gsocialsim.agents.agent import Agent
from gsocialsim.analytics.analytics import Analytics
from gsocialsim.evolution.evolutionary_system import EvolutionarySystem
from gsocialsim.kernel.sim_clock import SimClock
from gsocialsim.kernel.event_scheduler import EventScheduler
from gsocialsim.kernel.world_context import WorldContext
from gsocialsim.kernel.stimulus_ingestion import StimulusIngestionEngine
from gsocialsim.kernel.events import (
    DayBoundaryEvent,
    StimulusIngestionEvent,
    AgentActionEvent,
    AllocateAttentionEvent,
)
from gsocialsim.networks.network_layer import NetworkLayer
from gsocialsim.physical.physical_world import PhysicalWorld
from gsocialsim.social.global_social_reality import GlobalSocialReality


@dataclass
class AgentPopulation:
    agents: Dict[str, Agent] = field(default_factory=dict)

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.id] = agent

    def replace(self, exited_agent_id: str, newborn_agent: Agent) -> None:
        if exited_agent_id in self.agents:
            del self.agents[exited_agent_id]
        self.add_agent(newborn_agent)

    def get(self, agent_id: str, default=None):
        return self.agents.get(agent_id, default)

    def __getitem__(self, agent_id: str) -> Agent:
        return self.agents[agent_id]

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self.agents

    def items(self):
        return self.agents.items()

    def keys(self):
        return self.agents.keys()

    def values(self):
        return self.agents.values()


@dataclass
class WorldKernel:
    seed: int
    clock: SimClock = field(default_factory=SimClock)
    rng: random.Random = field(init=False)

    agents: AgentPopulation = field(default_factory=AgentPopulation)
    analytics: Analytics = field(default_factory=Analytics)

    gsr: GlobalSocialReality = field(default_factory=GlobalSocialReality)

    network: NetworkLayer = field(default_factory=NetworkLayer)
    physical_world: PhysicalWorld = field(default_factory=PhysicalWorld)
    evolutionary_system: EvolutionarySystem = field(default_factory=EvolutionarySystem)
    stimulus_engine: StimulusIngestionEngine = field(default_factory=StimulusIngestionEngine)
    scheduler: EventScheduler = field(default_factory=EventScheduler)

    world_context: WorldContext = field(init=False)

    # Internal state: ensures we seed the run loop exactly once
    _started: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.world_context = WorldContext(
            analytics=self.analytics,
            gsr=self.gsr,
            network=self.network,
            clock=self.clock,
            physical_world=self.physical_world,
            evolutionary_system=self.evolutionary_system,
            stimulus_engine=self.stimulus_engine,
            scheduler=self.scheduler,
            agents=self.agents,
        )

    def _schedule_agent_loops(self, agent_id: str) -> None:
        """
        Schedule the recurring per-agent loop events for a given agent.
        """
        self.scheduler.schedule(AgentActionEvent(timestamp=self.clock.t, agent_id=agent_id))
        self.scheduler.schedule(AllocateAttentionEvent(timestamp=self.clock.t, agent_id=agent_id))

    def start(self) -> None:
        """
        Seeds the initial events to start the simulation.

        This is real functionality: a kernel that can step forward should
        have its run-loop seeded. We allow calling start() explicitly,
        but we also auto-start on first step() for a sane public API.
        """
        if self._started:
            return

        self._started = True

        # First day boundary at end of day 0 (relative to current clock)
        self.scheduler.schedule(DayBoundaryEvent(timestamp=self.clock.t + self.clock.ticks_per_day))

        # Start ingestion immediately
        self.scheduler.schedule(StimulusIngestionEvent(timestamp=self.clock.t))

        # Start agent loops immediately for existing agents
        for agent_id in self.agents.agents.keys():
            self._schedule_agent_loops(agent_id)

    def step(self, num_ticks: int = 1) -> None:
        """
        Authoritative simulation advance.

        Guarantees:
          - The clock advances by exactly num_ticks (even if no events exist).
          - Events are applied in timestamp order.
          - No event with timestamp > target_tick is applied.
          - If the kernel hasn't started, it auto-starts once.
        """
        if num_ticks <= 0:
            return

        # Real functionality: stepping a kernel implies the run loop exists.
        if not self._started:
            self.start()

        target_tick = self.clock.t + num_ticks

        while True:
            next_event = self.scheduler.get_next_event()

            # No events left: advance time to the target and stop.
            if next_event is None:
                remaining = target_tick - self.clock.t
                if remaining > 0:
                    self.clock.advance(remaining)
                return

            # Event is at/after end of window: put it back, advance to target, stop.
            if next_event.timestamp >= target_tick:
                self.scheduler.schedule(next_event)
                remaining = target_tick - self.clock.t
                if remaining > 0:
                    self.clock.advance(remaining)
                return

            # Advance to event time
            delta = next_event.timestamp - self.clock.t
            if delta > 0:
                self.clock.advance(delta)

            # Apply event at current time
            next_event.apply(self.world_context)

```

## `src/gsocialsim/kernel/world_kernel_step.py`

```python
from __future__ import annotations

"""
Deprecated compatibility shim.

Older versions of the project used a manual per-tick loop in this module.
The authoritative runtime is now event-driven via WorldKernel.step().

If anything still imports WorldKernelStep or calls step() from here, it will
delegate to the WorldKernel implementation to keep day boundary ("dream") behavior correct.
"""

from dataclasses import dataclass
from typing import Optional

from gsocialsim.kernel.world_kernel import WorldKernel


@dataclass
class WorldKernelStep:
    kernel: WorldKernel

    def step(self, num_ticks: int = 1) -> None:
        self.kernel.step(num_ticks=num_ticks)

```

## `src/gsocialsim/networks/__init__.py`

```python

```

## `src/gsocialsim/networks/network_layer.py`

```python
from typing import Dict, Set, List
from dataclasses import dataclass, field

from gsocialsim.types import AgentId

@dataclass
class NetworkGraph:
    """
    A simple directed graph representing follow relationships.
    """
    # Key: AgentId of the follower
    # Value: Set of AgentIds being followed
    _following: Dict[AgentId, Set[AgentId]] = field(default_factory=dict)
    
    # Key: AgentId of the one being followed
    # Value: Set of AgentIds who are followers
    _followers: Dict[AgentId, Set[AgentId]] = field(default_factory=dict)

    def add_edge(self, follower: AgentId, followed: AgentId):
        """Adds a directed edge from follower to followed."""
        self._following.setdefault(follower, set()).add(followed)
        self._followers.setdefault(followed, set()).add(follower)
    
    def get_followers(self, agent_id: AgentId) -> List[AgentId]:
        return list(self._followers.get(agent_id, []))

    def get_following(self, agent_id: AgentId) -> List[AgentId]:
        return list(self._following.get(agent_id, []))

@dataclass
class NetworkLayer:
    """
    A minimal social network layer for Phase 3.
    For now, it just holds the graph.
    """
    graph: NetworkGraph = field(default_factory=NetworkGraph)

```

## `src/gsocialsim/physical/__init__.py`

```python

```

## `src/gsocialsim/physical/physical_world.py`

```python
from dataclasses import dataclass, field
from typing import Dict, List
from gsocialsim.types import AgentId, TopicId

@dataclass
class Place:
    id: str
    size: int
    topic_bias: Dict[TopicId, float] = field(default_factory=dict)

@dataclass
class Schedule:
    # A simple schedule mapping a tick of the day to a Place id
    daily_plan: Dict[int, str] = field(default_factory=dict)

@dataclass
class PhysicalWorld:
    places: Dict[str, Place] = field(default_factory=dict)
    schedules: Dict[AgentId, Schedule] = field(default_factory=dict)

    def get_co_located_agents(self, tick_of_day: int) -> List[List[AgentId]]:
        """Finds groups of agents in the same place at the same time."""
        agents_by_place: Dict[str, List[AgentId]] = {}
        for agent_id, schedule in self.schedules.items():
            current_place_id = schedule.daily_plan.get(tick_of_day)
            if current_place_id:
                agents_by_place.setdefault(current_place_id, []).append(agent_id)
        
        # Return groups of 2 or more agents
        return [group for group in agents_by_place.values() if len(group) > 1]

```

## `src/gsocialsim/policy/__init__.py`

```python

```

## `src/gsocialsim/policy/action_policy.py`

```python
import random
from typing import Optional, TYPE_CHECKING

from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import ContentId

if TYPE_CHECKING:
    from gsocialsim.agents.agent import Agent

class ActionPolicy:
    """
    Phase 4: A simple policy that decides if and how an agent should act.
    """
    def should_act(self, agent: "Agent") -> bool:
        """
        Determines if an agent should take an action on this tick.
        A simple probabilistic model to ensure most agents are lurkers.
        """
        # For now, a 1% chance to act on any given tick
        return agent.rng.random() < 0.01

    def generate_action(self, agent: "Agent", tick: int) -> Optional[ContentItem]:
        """
        If an agent decides to act, this generates the action.
        For Phase 4, the only action is creating a ContentItem.
        """
        if not self.should_act(agent) or not agent.beliefs.topics:
            return None

        # Choose a random topic the agent has a belief about
        topic_id = agent.rng.choice(list(agent.beliefs.topics.keys()))
        belief = agent.beliefs.get(topic_id)

        # Create content that reflects the agent's own belief stance
        new_content_id = ContentId(f"C_{agent.id}_{tick}")
        return ContentItem(
            id=new_content_id,
            author_id=agent.id,
            topic=topic_id,
            stance=belief.stance
        )

```

## `src/gsocialsim/policy/bandit_learner.py`

```python
from collections import defaultdict
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

from gsocialsim.policy.action_policy import ActionPolicy
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from gsocialsim.stimuli.content_item import ContentItem

if TYPE_CHECKING:
    from gsocialsim.agents.agent import Agent


# -----------------------------
# Reward Vector
# -----------------------------
@dataclass
class RewardVector:
    status: float = 0.0
    affiliation: float = 0.0

    def __add__(self, other: "RewardVector") -> "RewardVector":
        return RewardVector(
            status=self.status + other.status,
            affiliation=self.affiliation + other.affiliation,
        )

    def weighted_sum(self, weights: RewardWeights) -> float:
        return (
            self.status * weights.status
            + self.affiliation * weights.affiliation
        )


# -----------------------------
# Bandit Learner Policy
# -----------------------------
class BanditLearner(ActionPolicy):
    """
    Epsilon-greedy bandit over *topics* (arms).

    Design decision:
    - CREATE actions are keyed ONLY by topic.
    - LIKE / FORWARD are keyed by verb + target id.
    """

    def __init__(self, epsilon: float = 0.2):
        self.epsilon = epsilon
        self.action_counts: dict[str, int] = defaultdict(int)
        self.action_rewards: dict[str, RewardVector] = defaultdict(RewardVector)

    # -------------------------
    # Learning
    # -------------------------
    def learn(self, action_key: str, reward_vector: RewardVector) -> None:
        """
        Update reward statistics for an action key.

        action_key:
          - For CREATE: str(topic_id)
          - For others: verb_targetid
        """
        self.action_counts[action_key] += 1
        self.action_rewards[action_key] = (
            self.action_rewards[action_key] + reward_vector
        )

    # -------------------------
    # Action Generation
    # -------------------------
    def _get_possible_actions(self, agent: "Agent", tick: int) -> list[Interaction]:
        actions: list[Interaction] = []

        # CREATE actions (one per belief topic)
        for topic, belief in agent.beliefs.topics.items():
            content = ContentItem(
                id=f"C_{agent.id}_{tick}",
                author_id=agent.id,
                topic=topic,
                stance=belief.stance,
            )
            actions.append(
                Interaction(
                    agent_id=agent.id,
                    verb=InteractionVerb.CREATE,
                    original_content=content,
                )
            )

        # Reactive actions
        for content_id in agent.recent_impressions.keys():
            actions.append(
                Interaction(
                    agent_id=agent.id,
                    verb=InteractionVerb.LIKE,
                    target_stimulus_id=content_id,
                )
            )
            actions.append(
                Interaction(
                    agent_id=agent.id,
                    verb=InteractionVerb.FORWARD,
                    target_stimulus_id=content_id,
                )
            )

        return actions

    def _action_key(self, action: Interaction) -> str:
        """
        Canonical key for learning/scoring.
        """
        if action.verb == InteractionVerb.CREATE:
            return str(action.original_content.topic)
        return f"{action.verb.value}_{action.target_stimulus_id}"

    def generate_interaction(
        self, agent: "Agent", tick: int
    ) -> Optional[Interaction]:

        possible_actions = self._get_possible_actions(agent, tick)
        if not possible_actions:
            return None

        # ---------------------
        # Exploration
        # ---------------------
        if agent.rng.random() < self.epsilon:
            return agent.rng.choice(possible_actions)

        # ---------------------
        # Exploitation
        # ---------------------
        best_action: Optional[Interaction] = None
        best_score = float("-inf")

        for action in possible_actions:
            key = self._action_key(action)
            n = self.action_counts[key]
            if n == 0:
                continue

            avg_reward = (
                self.action_rewards[key].weighted_sum(agent.personality)
                / n
            )

            if avg_reward > best_score:
                best_score = avg_reward
                best_action = action

        # ---------------------
        # Deterministic fallback
        # ---------------------
        if best_action is None:
            if self.epsilon == 0.0:
                # Deterministic ordering when exploiting
                return max(
                    possible_actions,
                    key=self._action_key,
                )
            return agent.rng.choice(possible_actions)

        return best_action

```

## `src/gsocialsim/social/__init__.py`

```python

```

## `src/gsocialsim/social/global_social_reality.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
import random

from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.relationship_vector import RelationshipVector


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


@dataclass
class TopicReality:
    """
    Global "outside-the-agent" state for a topic.

    truth: objective ground-truth strength in [0, 1]
    salience: visibility / availability in [0, 1]
    institutional_stance: optional stance in [-1, 1] (future use)
    volatility: how fast salience decays (higher = faster)
    """
    truth: float = 0.5
    salience: float = 0.0
    institutional_stance: float = 0.0
    volatility: float = 0.02


@dataclass
class GlobalSocialReality:
    """
    Global social reality includes:
      1) Latent dyadic relationship vectors between agent pairs (symmetric).
      2) Topic-level external reality (truth + salience), which agents observe imperfectly.
    """

    # --- (1) Relationships ---
    # Key is a sorted tuple of two AgentIds to ensure R(u,v) == R(v,u)
    _relations: Dict[Tuple[AgentId, AgentId], RelationshipVector] = field(default_factory=dict)

    # --- (2) Topic reality ---
    topics: Dict[TopicId, TopicReality] = field(default_factory=dict)
    default_truth: float = 0.5
    default_volatility: float = 0.02

    # ----------------------------
    # Relationships API (unchanged)
    # ----------------------------
    def _get_key(self, u: AgentId, v: AgentId) -> Tuple[AgentId, AgentId]:
        """Creates a canonical key for a pair of agents."""
        if u == v:
            raise ValueError("Cannot have a relationship with oneself.")
        return tuple(sorted((u, v)))

    def get_relationship(self, u: AgentId, v: AgentId) -> RelationshipVector:
        """
        Gets the relationship between two agents.
        If no relationship exists, it creates and returns a default one.
        """
        key = self._get_key(u, v)
        if key not in self._relations:
            self._relations[key] = RelationshipVector()
        return self._relations[key]

    def set_relationship(self, u: AgentId, v: AgentId, vector: RelationshipVector) -> None:
        """Sets a specific relationship vector for a pair of agents."""
        key = self._get_key(u, v)
        self._relations[key] = vector

    # ----------------------------
    # Topic reality API (new)
    # ----------------------------
    def ensure_topic(self, topic: TopicId) -> TopicReality:
        tr = self.topics.get(topic)
        if tr is None:
            tr = TopicReality(truth=self.default_truth, salience=0.0, volatility=self.default_volatility)
            self.topics[topic] = tr
        return tr

    def truth(self, topic: TopicId) -> float:
        return self.ensure_topic(topic).truth

    def set_truth(self, topic: TopicId, value: float) -> None:
        self.ensure_topic(topic).truth = _clamp01(value)

    def salience(self, topic: TopicId) -> float:
        return self.ensure_topic(topic).salience

    def set_salience(self, topic: TopicId, value: float) -> None:
        self.ensure_topic(topic).salience = _clamp01(value)

    def bump_salience(self, topic: TopicId, delta: float) -> None:
        tr = self.ensure_topic(topic)
        tr.salience = _clamp01(tr.salience + delta)

    def decay(self) -> None:
        """Decay salience over time (call on DayBoundaryEvent, etc.)."""
        for tr in self.topics.values():
            tr.salience = _clamp01(tr.salience * (1.0 - tr.volatility))

    def observe_truth(
        self,
        topic: TopicId,
        *,
        rng: Optional[random.Random] = None,
        noise_std: float = 0.08,
        attention_gain: float = 1.0,
    ) -> float:
        """
        Noisy observation of objective truth in [0, 1].
        Higher attention_gain => less noise.
        """
        r = rng or random
        tr = self.ensure_topic(topic)
        std = max(1e-6, noise_std / max(1e-6, attention_gain))
        return _clamp01(tr.truth + r.gauss(0.0, std))

    def observe_salience(
        self,
        topic: TopicId,
        *,
        rng: Optional[random.Random] = None,
        noise_std: float = 0.05,
    ) -> float:
        r = rng or random
        tr = self.ensure_topic(topic)
        return _clamp01(tr.salience + r.gauss(0.0, noise_std))

```

## `src/gsocialsim/social/relationship_vector.py`

```python
from dataclasses import dataclass, field
from typing import Dict
from gsocialsim.types import TopicId

@dataclass
class RelationshipVector:
    """
    Represents the latent social relationship between two agents.
    For Phase 3, we only focus on 'trust'. Other fields are placeholders.
    """
    affinity: float = 0.5
    trust: float = 0.5  # [0,1] - The most important factor for Phase 3
    intimacy: float = 0.5
    conflict: float = 0.0
    reciprocity: float = 0.5
    status_delta: float = 0.0
    topic_alignment: Dict[TopicId, float] = field(default_factory=dict)

```

## `src/gsocialsim/stimuli/__init__.py`

```python

```

## `src/gsocialsim/stimuli/content_item.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from gsocialsim.types import ContentId, ActorId, TopicId
from gsocialsim.stimuli.stimulus import MediaType


@dataclass
class ContentItem:
    """
    A representation of a piece of content an agent can perceive.

    Backward compatible with the original minimal fields:
      - id, author_id, topic, stance, is_identity_threatening

    New capability:
      - media_type: used for consume vs interact weighting
      - outlet_id/community_id: supports subscription targeting in future layers
      - provenance: optional metadata chain (stimulus id, transform chain, etc.)
    """
    id: ContentId
    author_id: ActorId
    topic: TopicId
    stance: float  # [-1.0, +1.0]
    is_identity_threatening: bool = False

    # --- new / optional (safe defaults) ---
    media_type: MediaType = MediaType.UNKNOWN
    outlet_id: Optional[str] = None
    community_id: Optional[str] = None
    provenance: Dict[str, Any] = field(default_factory=dict)

```

## `src/gsocialsim/stimuli/data_source.py`

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import csv

from gsocialsim.stimuli.stimulus import Stimulus, MediaType


class DataSource(ABC):
    """Abstract base class for any source of external data."""

    @abstractmethod
    def get_stimuli(self, tick: int) -> List[Stimulus]:
        """Returns a list of all stimuli that should be injected at a given tick."""
        raise NotImplementedError


def _clean_opt_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        return v if v else None
    # defensive: coerce non-strings to string
    s = str(v).strip()
    return s if s else None


class CsvDataSource(DataSource):
    """
    A concrete data source that reads from a CSV file.

    Required columns:
      - id
      - tick
      - source
      - content_text

    Optional columns:
      - topic
      - media_type       (news, social_post, video, meme, longform, forum_thread)
      - creator_id       (for subscription targeting)
      - outlet_id        (for subscription targeting)
      - community_id     (for subscription targeting)

    Notes:
      - All optional fields are safe: missing columns are simply treated as None.
      - The Stimulus class also mirrors some values into stimulus.metadata to keep the
        CSV format flexible and backward compatible.
    """

    def __init__(self, file_path: str):
        self.stimuli_by_tick: Dict[int, List[Stimulus]] = {}

        with open(file_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)

            # Normalize header names defensively (CSV authors make mistakes).
            # We keep original keys but also allow case-insensitive matching.
            fieldnames = reader.fieldnames or []
            lower_to_actual = {fn.lower(): fn for fn in fieldnames}

            def get(row: Dict[str, Any], key: str) -> Any:
                actual = lower_to_actual.get(key.lower(), key)
                return row.get(actual)

            for row in reader:
                tick_raw = get(row, "tick")
                if tick_raw is None:
                    continue
                tick = int(tick_raw)

                stimulus_id = str(get(row, "id"))
                source = str(get(row, "source"))
                content_text = str(get(row, "content_text"))

                topic = _clean_opt_str(get(row, "topic"))
                media_type_raw = _clean_opt_str(get(row, "media_type"))
                creator_id = _clean_opt_str(get(row, "creator_id"))
                outlet_id = _clean_opt_str(get(row, "outlet_id"))
                community_id = _clean_opt_str(get(row, "community_id"))

                # Keep metadata flexible and compatible with existing code paths.
                metadata: Dict[str, Any] = {"topic": topic}
                if media_type_raw is not None:
                    metadata["media_type"] = media_type_raw
                if creator_id is not None:
                    metadata["creator_id"] = creator_id
                if outlet_id is not None:
                    metadata["outlet_id"] = outlet_id
                if community_id is not None:
                    metadata["community_id"] = community_id

                stimulus = Stimulus(
                    id=stimulus_id,
                    source=source,
                    tick=tick,
                    content_text=content_text,
                    media_type=MediaType.from_any(media_type_raw),
                    creator_id=creator_id,
                    outlet_id=outlet_id,
                    community_id=community_id,
                    topic_hint=topic,
                    metadata=metadata,
                )

                self.stimuli_by_tick.setdefault(tick, []).append(stimulus)

        print(
            f"Loaded {sum(len(s) for s in self.stimuli_by_tick.values())} stimuli from {file_path}"
        )

    def get_stimuli(self, tick: int) -> List[Stimulus]:
        return self.stimuli_by_tick.get(tick, [])

```

## `src/gsocialsim/stimuli/interaction.py`

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

@dataclass
class Interaction:
    """ Represents an agent's action, either creating original content or acting on a stimulus. """
    agent_id: str
    verb: "InteractionVerb"
    target_stimulus_id: Optional[str] = None
    original_content: Optional["ContentItem"] = None # Used for CREATE verb

class InteractionVerb(Enum):
    CREATE = "create"   # Original post
    LIKE = "like"
    FORWARD = "forward"
    COMMENT = "comment"
    REPLY = "reply"

```

## `src/gsocialsim/stimuli/stimulus.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class MediaType(str, Enum):
    """
    High-level media category for behavior weighting and feed semantics.

    Matches the design in project.md (news/social_post/video/meme/longform/forum_thread).
    """
    NEWS = "news"
    SOCIAL_POST = "social_post"
    VIDEO = "video"
    MEME = "meme"
    LONGFORM = "longform"
    FORUM_THREAD = "forum_thread"
    UNKNOWN = "unknown"

    @classmethod
    def from_any(cls, value: Any) -> "MediaType":
        if value is None:
            return cls.UNKNOWN
        if isinstance(value, MediaType):
            return value
        if isinstance(value, str):
            v = value.strip().lower()
            for mt in cls:
                if mt.value == v:
                    return mt
        return cls.UNKNOWN


@dataclass
class Stimulus:
    """
    A generic container for a piece of external data injected into the world.

    Backward compatible with the original fields:
      - id, source, tick, content_text, metadata

    New capability:
      - media_type: used for consumption vs interaction weighting
      - creator_id / outlet_id / community_id: supports subscription targeting
      - topic_hint: optional explicit topic string (still mirrors metadata["topic"])
    """

    # --- legacy / required ---
    id: str
    source: str  # e.g., "NewsOutletX", "SocialMediaFeedY", or creator/outlet identifier
    tick: int
    content_text: str

    # --- new / optional (safe defaults) ---
    media_type: MediaType = MediaType.UNKNOWN
    creator_id: Optional[str] = None
    outlet_id: Optional[str] = None
    community_id: Optional[str] = None
    topic_hint: Optional[str] = None

    # freeform extensibility
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Allow media_type to come from metadata or be passed as a string.
        if self.media_type is None or not isinstance(self.media_type, MediaType):
            self.media_type = MediaType.from_any(
                self.media_type if self.media_type is not None else self.metadata.get("media_type")
            )

        # If topic_hint wasn't provided, mirror from metadata (or vice versa).
        if self.topic_hint is None:
            t = self.metadata.get("topic")
            if isinstance(t, str):
                t = t.strip() or None
            self.topic_hint = t
        else:
            # normalize and keep metadata in sync
            if isinstance(self.topic_hint, str):
                self.topic_hint = self.topic_hint.strip() or None
            self.metadata.setdefault("topic", self.topic_hint)

        # Subscription-related IDs can live in metadata too (keeps CSV simple).
        if self.creator_id is None:
            v = self.metadata.get("creator_id")
            self.creator_id = v.strip() if isinstance(v, str) and v.strip() else None

        if self.outlet_id is None:
            v = self.metadata.get("outlet_id")
            self.outlet_id = v.strip() if isinstance(v, str) and v.strip() else None

        if self.community_id is None:
            v = self.metadata.get("community_id")
            self.community_id = v.strip() if isinstance(v, str) and v.strip() else None

        # If the source looks like a publisher and we have no explicit creator/outlet,
        # treat source as a generic "actor id" but don't override explicit fields.
        self.metadata.setdefault("source", self.source)

    @property
    def topic(self) -> Optional[str]:
        """Canonical topic accessor (preferred over direct metadata lookups)."""
        return self.topic_hint

    def to_debug_dict(self) -> Dict[str, Any]:
        """Helpful for logging/analytics without dumping huge metadata."""
        return {
            "id": self.id,
            "tick": self.tick,
            "source": self.source,
            "media_type": self.media_type.value if isinstance(self.media_type, MediaType) else str(self.media_type),
            "creator_id": self.creator_id,
            "outlet_id": self.outlet_id,
            "community_id": self.community_id,
            "topic": self.topic,
        }

```

## `src/gsocialsim/types.py`

```python
from typing import NewType

# Define common type aliases for clarity and future extension
AgentId = NewType("AgentId", str)
TopicId = NewType("TopicId", str)
ContentId = NewType("ContentId", str)
ActorId = NewType("ActorId", str) # Can be an AgentId or an institutional actor

```

## `src/gsocialsim/visualization/__init__.py`

```python
"""
Visualization package.

Importing this package registers all available exporters via side-effects
of their @register_exporter decorators.
"""

# Base + registry
from gsocialsim.visualization.exporter import (
    BaseExporter,
    ExportRequest,
    get_exporter,
    list_exporters,
    register_exporter,
    generate_influence_graph_html,
)

# Force-load built-in exporters so they register.
# Keep these imports at module-level on purpose.
from gsocialsim.visualization import exporter_full  # noqa: F401
from gsocialsim.visualization import exporter_agents_only  # noqa: F401
from gsocialsim.visualization import exporter_bipartite  # noqa: F401
from gsocialsim.visualization import exporter_threshold  # noqa: F401
from gsocialsim.visualization import exporter_agents_platform  # noqa: F401

```

## `src/gsocialsim/visualization/exporter.py`

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from pyvis.network import Network

from gsocialsim.kernel.world_kernel import WorldKernel


@dataclass(frozen=True)
class ExportRequest:
    """
    Common contract for all exporters.

    - kernel: WorldKernel
    - output_path: file to write (html)
    - extra: free-form knobs (thresholds, styles, etc.)
    """
    kernel: WorldKernel
    output_path: str = "influence_graph.html"
    extra: Dict[str, Any] = None


class BaseExporter(ABC):
    """
    Generic exporter contract. Inherit and implement render().
    All exporters must accept the same ExportRequest and write an HTML output.
    """
    name: str = "base"

    def __init__(self) -> None:
        pass

    @abstractmethod
    def render(self, req: ExportRequest) -> str:
        """
        Render a graph to req.output_path and return the output_path.
        """
        raise NotImplementedError

    # ---------- shared helpers ----------
    @staticmethod
    def _safe_set_options(net: Network, options_js: str) -> None:
        try:
            net.set_options(options_js)
        except Exception:
            # pyvis versions vary, defaults are acceptable if this fails
            pass

    @staticmethod
    def _node_exists(net: Network, node_id: str) -> bool:
        try:
            return node_id in net.get_nodes()
        except Exception:
            return False

    @classmethod
    def _ensure_node(
        cls,
        net: Network,
        node_id: str,
        *,
        label: Optional[str] = None,
        title: Optional[str] = None,
        color: Optional[str] = None,
        shape: Optional[str] = None,
        size: Optional[float] = None,
    ) -> None:
        if not node_id:
            return
        if cls._node_exists(net, node_id):
            return

        kwargs: Dict[str, Any] = {"label": label or node_id}
        if title is not None:
            kwargs["title"] = title
        if color is not None:
            kwargs["color"] = color
        if shape is not None:
            kwargs["shape"] = shape
        if size is not None:
            kwargs["size"] = size

        net.add_node(node_id, **kwargs)


# -----------------------------
# Registry (optional convenience)
# -----------------------------
_EXPORTERS: Dict[str, Type[BaseExporter]] = {}


def register_exporter(cls: Type[BaseExporter]) -> Type[BaseExporter]:
    _EXPORTERS[cls.name] = cls
    return cls


def get_exporter(name: str) -> BaseExporter:
    if name not in _EXPORTERS:
        raise ValueError(f"Unknown exporter '{name}'. Known: {sorted(_EXPORTERS.keys())}")
    return _EXPORTERS[name]()


def list_exporters() -> Dict[str, Type[BaseExporter]]:
    return dict(_EXPORTERS)


# -----------------------------
# Backward-compatible function
# -----------------------------
def generate_influence_graph_html(kernel: WorldKernel, output_path: str = "influence_graph.html") -> str:
    """
    Backward compatible entrypoint used by run_and_visualize.py today.
    Uses the 'full' exporter by default.

    Import is inside the function to avoid import-time cycles.
    """
    from gsocialsim.visualization.exporter_full import FullGraphExporter  # local import by design

    exporter = FullGraphExporter()
    req = ExportRequest(kernel=kernel, output_path=output_path, extra={})
    return exporter.render(req)

```

## `src/gsocialsim/visualization/exporter_agents_only.py`

```python
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple

from pyvis.network import Network

from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class AgentsOnlyExporter(BaseExporter):
    """
    Agents-only graph:
      - agents
      - external sources (only if they influence an agent)
      - follower edges
      - influence edges (source -> agent)
    """
    name = "agents_only"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        self._safe_set_options(net, """
        var options = {
          "physics": {
            "enabled": true,
            "stabilization": {"enabled": true, "iterations": 1200, "fit": true}
          }
        }
        """)

        agent_ids = set(kernel.agents.agents.keys())

        # Agent nodes
        for agent in kernel.agents.agents.values():
            self._ensure_node(net, str(agent.id), label=str(agent.id), color="#cccccc", shape="dot", size=18)

        # Follower edges
        following = kernel.world_context.network.graph._following
        for follower, followed_list in following.items():
            for followed in followed_list:
                if follower in agent_ids and followed in agent_ids:
                    net.add_edge(str(follower), str(followed), color="#cccccc", width=1, title="follows")

        # Influence edges
        influence_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1

        for (source, target), count in influence_counts.items():
            if target in agent_ids:
                if not self._node_exists(net, source) and source not in agent_ids:
                    self._ensure_node(net, source, label=source, color="#555555", shape="box", size=14, title=f"External actor: {source}")
                net.add_edge(source, target, color="#ff0000", width=min(10, 2 * count), title=f"Influenced {count} time(s)")

        net.save_graph(output_path)
        return output_path

```

## `src/gsocialsim/visualization/exporter_agents_platform.py`

```python
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple, Set

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class AgentsPlatformExporter(BaseExporter):
    """
    Agents + Platform aggregation:
      - Collapses all stimuli by source into one "platform/source" node
      - Interaction edges: agent -> source
      - Influence edges: (source actor or source node) -> agent

    extra knobs:
      - platform_prefix (str) default "SRC:"
    """
    name = "agents_platform"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path
        extra = req.extra or {}
        prefix = str(extra.get("platform_prefix", "SRC:"))

        def pid(source: str) -> str:
            return f"{prefix}{source}"

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        self._safe_set_options(net, """
        var options = {
          "physics": {
            "enabled": true,
            "stabilization": {"enabled": true, "iterations": 1300, "fit": true}
          }
        }
        """)

        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store

        # Agent nodes
        for agent in kernel.agents.agents.values():
            aid = str(agent.id)
            self._ensure_node(net, aid, label=aid, color="#cccccc", shape="dot", size=18)

        # Source/platform nodes
        sources: Set[str] = set()
        for stim in stimuli_store.values():
            if getattr(stim, "source", None):
                sources.add(str(stim.source))

        for s in sorted(sources):
            self._ensure_node(
                net,
                pid(s),
                label=s,
                color="#2aa198",
                shape="box",
                size=18,
                title=f"Platform/Source: {s}",
            )

        # Interaction aggregation agent -> source
        interaction_counts = defaultdict(int)
        for inter in kernel.world_context.analytics.interactions:
            if inter.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                stim = stimuli_store.get(str(inter.target_stimulus_id))
                if not stim:
                    continue
                s = str(getattr(stim, "source", "")).strip()
                if not s:
                    continue
                interaction_counts[(str(inter.agent_id), pid(s))] += 1

        max_c = max(interaction_counts.values()) if interaction_counts else 1
        for (aid, sid), c in interaction_counts.items():
            width = 1 + 6 * (c / max_c)
            net.add_edge(aid, sid, color="#99ff99", width=width, dashes=True, title=f"Interacted {c} time(s)")

        # Influence edges:
        # If influencer name matches an actual source label, connect source node -> agent, else external -> agent.
        influence_counts = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1

        for (src, tgt), c in influence_counts.items():
            if tgt not in kernel.agents.agents:
                continue

            if src in sources:
                net.add_edge(pid(src), tgt, color="#ff0000", width=min(10, 2 * c), title=f"Influenced {c} time(s)")
            else:
                if not self._node_exists(net, src) and src not in kernel.agents.agents:
                    self._ensure_node(net, src, label=src, color="#555555", shape="box", size=14, title=f"External actor: {src}")
                net.add_edge(src, tgt, color="#ff0000", width=min(10, 2 * c), title=f"Influenced {c} time(s)")

        net.save_graph(output_path)
        return output_path

```

## `src/gsocialsim/visualization/exporter_bipartite.py`

```python
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class BipartiteExporter(BaseExporter):
    """
    Bipartite layout (high readability):
      - agents on left
      - stimuli on right
      - follower edges optional (kept)
      - interactions agent->stimulus
      - influence edges source->agent (external sources appear as boxes)
    Uses hierarchical layout LR and physics off (no dancing).
    """
    name = "bipartite"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        self._safe_set_options(net, """
        var options = {
          "physics": {"enabled": false},
          "layout": {
            "hierarchical": {
              "enabled": true,
              "direction": "LR",
              "sortMethod": "directed",
              "nodeSpacing": 180,
              "levelSeparation": 220
            }
          }
        }
        """)

        # Nodes
        for agent in kernel.agents.agents.values():
            self._ensure_node(net, str(agent.id), label=str(agent.id), color="#cccccc", shape="dot", size=18)

        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store
        for stim in stimuli_store.values():
            self._ensure_node(net, str(stim.id), label=str(stim.id), color="#00cc66", shape="square", size=16, title=f"Source: {stim.source}")

        # Interaction edges
        interaction_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for interaction in kernel.world_context.analytics.interactions:
            if interaction.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                interaction_counts[(str(interaction.agent_id), str(interaction.target_stimulus_id))] += 1

        max_c = max(interaction_counts.values()) if interaction_counts else 1
        for (aid, sid), c in interaction_counts.items():
            if aid in kernel.agents.agents and sid in stimuli_store:
                width = 1 + 6 * (c / max_c)
                net.add_edge(aid, sid, color="#99ff99", width=width, title=f"Interacted {c} time(s)")

        # Influence edges (external -> agent)
        influence_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1

        for (source, target), c in influence_counts.items():
            if target in kernel.agents.agents:
                if not self._node_exists(net, source) and source not in kernel.agents.agents:
                    self._ensure_node(net, source, label=source, color="#555555", shape="box", size=14, title=f"External actor: {source}")
                net.add_edge(source, target, color="#ff0000", width=min(10, 2 * c), title=f"Influenced {c} time(s)")

        net.save_graph(output_path)
        return output_path

```

## `src/gsocialsim/visualization/exporter_full.py`

```python
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple, Any

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class FullGraphExporter(BaseExporter):
    """
    Full graph:
      - agents
      - stimuli
      - follower edges
      - interactions (agent -> stimulus)
      - influence edges (source -> agent), including external sources
    Stabilized physics to avoid the "jello".
    """
    name = "full"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        self._safe_set_options(net, """
        var options = {
          "physics": {
            "enabled": true,
            "barnesHut": {
              "gravitationalConstant": -25000,
              "centralGravity": 0.25,
              "springLength": 180,
              "springConstant": 0.04,
              "damping": 0.5,
              "avoidOverlap": 0.2
            },
            "stabilization": {
              "enabled": true,
              "iterations": 1500,
              "updateInterval": 50,
              "fit": true
            }
          },
          "interaction": {"hover": true, "tooltipDelay": 80}
        }
        """)

        # 1) Agent nodes
        for agent in kernel.agents.agents.values():
            primary_belief = max(agent.beliefs.topics.values(), key=lambda b: b.confidence, default=None)
            color, title, size = "#808080", f"Agent {agent.id}", 15
            if primary_belief:
                color = "#cccccc"
                if primary_belief.stance > 0.1:
                    color = "#0080ff"
                elif primary_belief.stance < -0.1:
                    color = "#ff4000"
                title += f"\nTopic: {primary_belief.topic}\nStance: {primary_belief.stance:.2f}"
                size += float(primary_belief.confidence) * 20
            self._ensure_node(net, str(agent.id), label=str(agent.id), color=color, title=title, size=size, shape="dot")

        # 2) Stimulus nodes
        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store
        for stimulus in stimuli_store.values():
            title = f"Stimulus: {stimulus.id}\nSource: {stimulus.source}\nContent: {stimulus.content_text}"
            self._ensure_node(net, str(stimulus.id), label=str(stimulus.id), color="#00cc66", title=title, shape="square", size=18)

        # 3) Follower edges
        following = kernel.world_context.network.graph._following
        for follower, followed_list in following.items():
            for followed in followed_list:
                if follower in kernel.agents.agents and followed in kernel.agents.agents:
                    net.add_edge(str(follower), str(followed), color="#cccccc", width=1, title="follows")

        # 4) Interaction edges (aggregated)
        interaction_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for interaction in kernel.world_context.analytics.interactions:
            if interaction.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                interaction_counts[(str(interaction.agent_id), str(interaction.target_stimulus_id))] += 1

        max_interaction_count = max(interaction_counts.values()) if interaction_counts else 1
        for (agent_id, stimulus_id), count in interaction_counts.items():
            if agent_id in kernel.agents.agents and stimulus_id in stimuli_store:
                width = 1 + 6 * (count / max_interaction_count)
                net.add_edge(agent_id, stimulus_id, color="#99ff99", width=width, dashes=True, title=f"Interacted {count} time(s)")

        # 5) Influence edges (with external nodes)
        influence_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1

        for (source, target), count in influence_counts.items():
            if target in kernel.agents.agents:
                if not self._node_exists(net, source):
                    self._ensure_node(
                        net,
                        source,
                        label=source,
                        color="#555555",
                        title=f"External actor: {source}",
                        shape="box",
                        size=14,
                    )
                net.add_edge(source, target, color="#ff0000", width=min(10, 2 * count), title=f"Influenced {count} time(s)")

        net.save_graph(output_path)
        return output_path

```

## `src/gsocialsim/visualization/exporter_threshold.py`

```python
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple, Set

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class ThresholdExporter(BaseExporter):
    """
    Threshold graph:
      - Start from full graph, but only include nodes/edges that exceed thresholds
      - Good for "only what influences / gets lots of visibility"
    extra knobs:
      - min_influence_edges (int) default 2
      - min_interaction_edges (int) default 2
      - min_node_visibility (int) default 5
    """
    name = "threshold"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path
        extra = req.extra or {}

        min_infl = int(extra.get("min_influence_edges", 2))
        min_int = int(extra.get("min_interaction_edges", 2))
        min_vis = int(extra.get("min_node_visibility", 5))

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        self._safe_set_options(net, """
        var options = {
          "physics": {
            "enabled": true,
            "stabilization": {"enabled": true, "iterations": 1400, "fit": true}
          }
        }
        """)

        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store

        # Aggregate interactions
        interaction_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for interaction in kernel.world_context.analytics.interactions:
            if interaction.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                interaction_counts[(str(interaction.agent_id), str(interaction.target_stimulus_id))] += 1

        # Aggregate influence
        influence_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1

        # Node visibility score
        vis: Dict[str, int] = defaultdict(int)
        for (src, tgt), c in influence_counts.items():
            vis[src] += c
            vis[tgt] += c
        for (aid, sid), c in interaction_counts.items():
            vis[aid] += c
            vis[sid] += c

        allowed_nodes: Set[str] = {nid for nid, v in vis.items() if v >= min_vis}

        # Add agent nodes (if visible)
        for agent in kernel.agents.agents.values():
            aid = str(agent.id)
            if aid in allowed_nodes:
                self._ensure_node(net, aid, label=aid, color="#cccccc", shape="dot", size=18)

        # Add stimulus nodes (if visible)
        for stim_id, stim in stimuli_store.items():
            sid = str(stim_id)
            if sid in allowed_nodes:
                self._ensure_node(net, sid, label=sid, color="#00cc66", shape="square", size=16, title=f"Source: {stim.source}")

        # Add filtered interaction edges
        max_int = max(interaction_counts.values()) if interaction_counts else 1
        for (aid, sid), c in interaction_counts.items():
            if c < min_int:
                continue
            if aid in allowed_nodes and sid in allowed_nodes and sid in stimuli_store and aid in kernel.agents.agents:
                width = 1 + 6 * (c / max_int)
                net.add_edge(aid, sid, color="#99ff99", width=width, dashes=True, title=f"Interacted {c} time(s)")

        # Add filtered influence edges
        for (src, tgt), c in influence_counts.items():
            if c < min_infl:
                continue
            if tgt not in kernel.agents.agents:
                continue
            # allow external src even if not in allowed_nodes (if it is the influencer)
            if tgt not in allowed_nodes:
                continue
            if src not in allowed_nodes and src not in kernel.agents.agents:
                # If an external source is strongly influencing, include it
                allowed_nodes.add(src)

            if not self._node_exists(net, src) and src not in kernel.agents.agents:
                self._ensure_node(net, src, label=src, color="#555555", shape="box", size=14, title=f"External actor: {src}")
            if not self._node_exists(net, tgt):
                self._ensure_node(net, tgt, label=tgt, color="#cccccc", shape="dot", size=18)

            net.add_edge(src, tgt, color="#ff0000", width=min(10, 2 * c), title=f"Influenced {c} time(s)")

        net.save_graph(output_path)
        return output_path

```

## `stimuli.csv`

```text
id,tick,source,topic,content_text
news1,10,NewsOutlet,T_Science,A major scientific breakthrough has been announced.
news2,50,RivalNews,T_Science,A competing report raises doubts about the recent breakthrough.
meme1,100,UserA,T_Memes,"That feeling when you realize it's Friday, lol"

sci1,15,ScienceDaily,T_Science,Peer review highlights key limitations in the breakthrough study.
sci2,20,UniLab,T_Science,Researchers publish replication results with mixed outcomes.
sci3,25,ScienceDaily,T_Science,Explainer: what the breakthrough actually claims and what it does not.
sci4,30,UniLab,T_Science,New dataset released to validate claims independently.
sci5,35,ScienceDaily,T_Science,Interview: lead author responds to criticism.

pol1,40,NewsOutlet,T_Politics,Lawmakers call for hearings on research funding priorities.
pol2,45,RivalNews,T_Politics,Opposition says the hearings are political theater.
pol3,55,CapitolWatch,T_Politics,Bill introduced to increase transparency in grants.
pol4,60,CapitolWatch,T_Politics,Committee schedules public testimony next week.
pol5,65,NewsOutlet,T_Politics,Debate escalates over who benefits from the new policy.

eco1,70,MarketWire,T_Economy,Markets react to the news with modest volatility.
eco2,75,MarketWire,T_Economy,Analysts: impact may be overstated in the short term.
eco3,80,FinBlog,T_Economy,Thread: how hype cycles distort investment decisions.
eco4,85,MarketWire,T_Economy,Report: funding reallocations could reshape the sector.
eco5,90,FinBlog,T_Economy,Opinion: focus on fundamentals not narratives.

cult1,95,TrendFeed,T_Culture,Influencers argue the story proves "experts are out of touch."
cult2,105,TrendFeed,T_Culture,Viral clip sparks debate about scientific literacy.
cult3,110,PodcasterX,T_Culture,Hot take: institutions cannot be trusted anymore.
cult4,115,PodcasterX,T_Culture,Counterpoint: skepticism is healthy but facts matter.
cult5,120,TrendFeed,T_Culture,Community notes provide corrections and sources.

meme2,125,UserB,T_Memes,"Me reading the comments: 'I will not engage' (engages anyway)."
meme3,130,UserC,T_Memes,"Breaking: my confidence is 1.0 and my evidence is vibes."
meme4,135,UserD,T_Memes,"When your model overfits and you call it 'intuition'."
meme5,140,UserE,T_Memes,"Trust me bro, I ran it once."

sports1,145,SportsDesk,T_Sports,Upset win sparks celebration and trash talk.
sports2,150,SportsDesk,T_Sports,Analysts debate whether the win was luck or skill.
sports3,155,FanAccount,T_Sports,"Hot take: refs decided the game."
sports4,160,FanAccount,T_Sports,Replay breakdown thread goes viral.
sports5,165,SportsDesk,T_Sports,Coach addresses controversy in press conference.

sec1,170,InfosecNews,T_Security,Security researchers disclose a new vulnerability class.
sec2,175,InfosecNews,T_Security,Patch guidance issued with mitigations and timelines.
sec3,180,ForumUser,T_Security,"This will be exploited in the wild within 72 hours."
sec4,185,InfosecNews,T_Security,Early telemetry suggests opportunistic scanning.
sec5,190,ForumUser,T_Security,"If you are unpatched you are already compromised."

mix1,195,NewsOutlet,T_Original,Summary: what we know so far and what is still uncertain.
mix2,200,RivalNews,T_Original,Opinion: the story is being misframed by both sides.
mix3,205,NewsOutlet,T_Original,Fact check: common claims circulating are inaccurate.
mix4,210,TrendFeed,T_Original,Compilation: reactions across platforms and communities.
mix5,215,ScienceDaily,T_Original,Update: new evidence clarifies earlier ambiguities.

```

## `tests/test_attention_system.py`

```python
import unittest
from unittest.mock import Mock, patch
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.kernel.events import DeepFocusEvent, AllocateAttentionEvent
from gsocialsim.agents.impression import Impression, IntakeMode

class TestAttentionSystem(unittest.TestCase):

    def test_salience_triggers_deep_focus(self):
        """
        Verify that a high-salience impression in an agent's memory
        correctly triggers the scheduling of a DeepFocusEvent.
        """
        print("\n--- Test: Salience Triggers Deep Focus ---")
        
        # --- Setup ---
        kernel = WorldKernel(seed=1001)
        agent = Agent(id=AgentId("test_agent"), seed=1002)
        agent.budgets.deep_focus_budget = 5
        agent.budgets.attention_minutes = 100
        kernel.agents.add_agent(agent)

        # 1. Create a belief with high salience
        high_salience_topic = TopicId("T_IMPORTANT")
        agent.beliefs.update(high_salience_topic, stance=0.5, confidence=0.5, salience=0.9, knowledge=0.5)

        # 2. Add an impression related to that topic to the agent's memory
        impression = Impression(
            intake_mode=IntakeMode.SCROLL,
            content_id="important_stimulus",
            topic=high_salience_topic,
            stance_signal=0.6
        )
        agent.recent_impressions["important_stimulus"] = impression
        
        # --- Execution ---
        # Directly call the apply method of the event
        allocate_event = AllocateAttentionEvent(timestamp=1, agent_id=agent.id)
        allocate_event.apply(kernel.world_context)

        # --- Verification ---
        # Check the scheduler's queue for a DeepFocusEvent
        found_event = False
        while not kernel.scheduler.is_empty():
            event = kernel.scheduler.get_next_event()
            if isinstance(event, DeepFocusEvent):
                found_event = True
                self.assertEqual(event.agent_id, agent.id)
                self.assertEqual(event.content_id, "important_stimulus")
                break # Stop once we've found it

        self.assertTrue(found_event, "A DeepFocusEvent should have been scheduled for the high-salience topic.")
        print("Verified: High salience correctly schedules a DeepFocusEvent.")

if __name__ == '__main__':
    unittest.main()
```

## `tests/test_belief_model.py`

```python
import unittest
from unittest.mock import patch
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.relationship_vector import RelationshipVector
from gsocialsim.agents.impression import Impression, IntakeMode
from gsocialsim.agents.belief_update_engine import BeliefUpdateEngine

class TestBeliefModel(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=909)
        self.viewer = Agent(id=AgentId("viewer"), seed=910)
        self.source = Agent(id=AgentId("source"), seed=911)
        self.topic = TopicId("T_Bias")
        self.kernel.agents.add_agent(self.viewer)
        self.kernel.agents.add_agent(self.source)
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.source.id, RelationshipVector(trust=1.0))

    def test_confirmation_bias(self):
        print("\n--- Test: Confirmation Bias ---")
        impression = Impression(IntakeMode.SCROLL, "c1", self.topic, 0.3)
        engine = self.viewer.belief_update_engine

        # Baseline (opposing) - multiplier should be 1.0
        self.viewer.beliefs.update(self.topic, stance=-0.1, confidence=0.5, salience=0, knowledge=0)
        with patch.object(engine, 'update', wraps=engine.update) as spy:
            delta_base = spy(self.viewer, self.source.id, impression, self.kernel.world_context.gsr)
            # We can't directly inspect the multiplier, so we check the output
            expected_base_change = (0.3 - (-0.1)) * 0.10 * 1.0 # stance_diff * base_influence * multiplier
            self.assertAlmostEqual(delta_base.stance_delta, expected_base_change)
            print(f"Baseline stance change (no bias): {delta_base.stance_delta:.4f}")

        # Confirmation (aligned) - multiplier should be 1.5
        self.viewer.beliefs.update(self.topic, stance=0.1, confidence=0.5, salience=0, knowledge=0)
        with patch.object(engine, 'update', wraps=engine.update) as spy:
            delta_confirm = spy(self.viewer, self.source.id, impression, self.kernel.world_context.gsr)
            expected_confirm_change = (0.3 - 0.1) * 0.10 * 1.5 # stance_diff * base_influence * multiplier
            self.assertAlmostEqual(delta_confirm.stance_delta, expected_confirm_change)
            print(f"Confirming stance change (with bias): {delta_confirm.stance_delta:.4f}")
        
        print("Verified: Confirmation bias logic is applying the correct multiplier.")

    def test_backfire_effect(self):
        print("\n--- Test: Backfire Effect ---")
        self.viewer.beliefs.update(self.topic, stance=0.8, confidence=0.9, salience=0, knowledge=0)
        impression_threatening = Impression(IntakeMode.SCROLL, "c2", self.topic, -0.8)
        setattr(impression_threatening, '_is_threatening_hack', True)

        initial_stance = self.viewer.beliefs.get(self.topic).stance
        delta = self.viewer.belief_update_engine.update(self.viewer, self.source.id, impression_threatening, self.kernel.world_context.gsr)
        
        self.assertGreater(delta.stance_delta, 0, "Stance delta should be positive (repulsion).")
        print("Verified: Backfire effect works.")

if __name__ == '__main__':
    unittest.main()
```

## `tests/test_daily_consolidation_and_consumption.py`

```python
import pytest

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.stimuli.content_item import ContentItem


def _seed_agent_with_topic(agent: Agent, topic: str):
    agent.budgets.action_budget = 9999
    agent.beliefs.update(TopicId(topic), stance=0.0, confidence=0.5, salience=0.2, knowledge=0.2)


def test_day_boundary_triggers_dream():
    k = WorldKernel(seed=123)
    a = Agent(id=AgentId("A"), seed=1)
    _seed_agent_with_topic(a, "T_Test")
    k.agents.add_agent(a)

    # Start and run past one day boundary.
    k.start()
    k.step(k.clock.ticks_per_day + 1)

    dream_runs = getattr(k.analytics, "dream_runs", [])
    assert len(dream_runs) >= 1, "Expected at least one dream run after day boundary"


def test_exposure_vs_consumption_split_is_recorded():
    k = WorldKernel(seed=123)
    a = Agent(id=AgentId("A"), seed=7)
    _seed_agent_with_topic(a, "T_Test")
    k.agents.add_agent(a)

    # No need to run the whole scheduler; call perceive directly through the agent,
    # but we do want analytics initialized in kernel context.
    k.start()

    # Create a bunch of content items; the attention system will assign default media/intake.
    # Agent RNG is seeded, so this result is deterministic.
    for i in range(50):
        c = ContentItem(
            id=f"C{i}",
            author_id="SOURCE",
            topic=TopicId("T_Test"),
            text="hello world",
        )
        a.perceive(c, k.world_context, is_physical=False)

    exp = getattr(k.analytics, "exposure_counts", {}).get(a.id, 0)
    con = getattr(k.analytics, "consumed_counts", {}).get(a.id, 0)

    assert exp == 50, "Exposure should be logged for every perceive()"
    assert 0 <= con <= exp, "Consumed count must be bounded by exposures"
    assert con != exp, "With probabilistic consumption, not all exposures should be consumed"

```

## `tests/test_event_system.py`

```python
import unittest
from unittest.mock import Mock
from gsocialsim.kernel.event_scheduler import EventScheduler
from gsocialsim.kernel.events import (
    Event,
    StimulusIngestionEvent,
    DayBoundaryEvent,
    AgentActionEvent,
)

class TestEventSystem(unittest.TestCase):

    def test_event_scheduler_tie_breaking(self):
        """
        Verify that the EventScheduler correctly orders and dispatches
        different event types that are scheduled for the exact same timestamp.
        """
        print("--- Test: Event Scheduler Tie-Breaking ---")
        scheduler = EventScheduler()
        
        # Schedule three different event types for the same timestamp (t=0)
        # Their tie-breaker values will be 0, 1, 2 respectively.
        e1 = StimulusIngestionEvent(timestamp=0)
        e2 = DayBoundaryEvent(timestamp=0)
        e3 = AgentActionEvent(timestamp=0, agent_id="A1")

        scheduler.schedule(e1)
        scheduler.schedule(e2)
        scheduler.schedule(e3)

        # Retrieve the events. They should come out in the order they were added
        # because the tie-breaker maintains insertion order for same-timestamp events.
        out1 = scheduler.get_next_event()
        out2 = scheduler.get_next_event()
        out3 = scheduler.get_next_event()

        self.assertIsInstance(out1, StimulusIngestionEvent, "First event should be StimulusIngestionEvent")
        self.assertIsInstance(out2, DayBoundaryEvent, "Second event should be DayBoundaryEvent")
        self.assertIsInstance(out3, AgentActionEvent, "Third event should be AgentActionEvent")
        print("Verified: Events with the same timestamp are dispatched in a stable, predictable order.")

    def test_event_apply_calls(self):
        """ Verify that the event's apply method is called by the kernel. """
        # This is a conceptual test of the main loop
        mock_event = Mock(spec=Event)
        mock_event.timestamp = 0
        
        mock_context = Mock()
        
        # Manually call apply to simulate the kernel's behavior
        mock_event.apply(mock_context)
        
        # Verify that the apply method was called exactly once
        mock_event.apply.assert_called_once_with(mock_context)

if __name__ == '__main__':


    unittest.main()

```

## `tests/test_learning_policy.py`

```python
import unittest
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.types import AgentId
from gsocialsim.stimuli.data_source import CsvDataSource
from gsocialsim.stimuli.interaction import InteractionVerb

class TestLearningPolicy(unittest.TestCase):

    def test_personality_driven_learning(self):
        """
        Verify that agents with different personalities learn to prefer
        different actions based on the rewards they receive.
        """
        print("\n--- Test: Personality-Driven Learning (Bandit) ---")
        
        # --- Setup ---
        kernel = WorldKernel(seed=808)
        
        # Agent Affiliation: High affiliation weight, low status
        agent_aff = Agent(id=AgentId("AffiliationSeeker"), seed=809)
        agent_aff.personality = RewardWeights(affiliation=1.0, status=0.1)

        # Agent Status: High status weight, low affiliation
        agent_status = Agent(id=AgentId("StatusSeeker"), seed=810)
        agent_status.personality = RewardWeights(affiliation=0.1, status=1.0)
        
        # Viewer agent to generate rewards
        viewer = Agent(id=AgentId("Viewer"), seed=811)

        for agent in [agent_aff, agent_status, viewer]:
            agent.budgets.action_budget = 1000 # Give plenty of budget
            kernel.agents.add_agent(agent)
            
        # Viewer follows both agents
        kernel.world_context.network.graph.add_edge(viewer.id, agent_aff.id)
        kernel.world_context.network.graph.add_edge(viewer.id, agent_status.id)
        
        # Load a stimulus for them to interact with
        csv_source = CsvDataSource(file_path="stimuli.csv")
        kernel.world_context.stimulus_engine.register_data_source(csv_source)

        # --- Learning Phase ---
        print("Running learning phase...")
        kernel.start()
        kernel.step(200) # Run long enough for stimuli to be seen and actions to be learned

        # --- Verification Phase ---
        print("Running verification phase (exploitation only)...")
        # Disable exploration to see what the agents have learned
        agent_aff.policy.epsilon = 0.0
        agent_status.policy.epsilon = 0.0
        
        aff_actions = {"LIKE": 0, "FORWARD": 0, "CREATE": 0}
        status_actions = {"LIKE": 0, "FORWARD": 0, "CREATE": 0}

        # Run for more ticks and count the exploited actions
        for i in range(100):
            # We need to manually run the action part of the loop for this test
            interaction_aff = agent_aff.act(tick=200 + i)
            if interaction_aff:
                aff_actions[interaction_aff.verb.name] += 1
            
            interaction_status = agent_status.act(tick=200 + i)
            if interaction_status:
                status_actions[interaction_status.verb.name] += 1
        
        print(f"AffiliationSeeker actions: {aff_actions}")
        print(f"StatusSeeker actions: {status_actions}")

        # --- Assertions ---
        # The affiliation seeker should have learned that LIKEs are best
        self.assertGreater(aff_actions["LIKE"], aff_actions["FORWARD"],
                           "AffiliationSeeker should prefer LIKE over FORWARD.")
                           
        # The status seeker should have learned that FORWARDs are best
        self.assertGreater(status_actions["FORWARD"], status_actions["LIKE"],
                           "StatusSeeker should prefer FORWARD over LIKE.")

        print("Verified: Agents successfully learned personality-driven behaviors.")

if __name__ == '__main__':
    unittest.main()

```

## `tests/test_phase1.py`

```python
import unittest
import datetime
from gsocialsim.kernel.world_kernel import WorldKernel, AgentPopulation
from gsocialsim.kernel.sim_clock import SimClock
from gsocialsim.agents.agent import Agent

class TestPhase1(unittest.TestCase):

    def test_world_kernel_initialization_and_clock_advance(self):
        print("""
--- Test: WorldKernel Initialization and Clock Advance ---""")
        seed = 42
        kernel = WorldKernel(seed=seed)

        self.assertIsInstance(kernel.clock, SimClock)
        self.assertEqual(kernel.clock.t, 0)
        self.assertEqual(kernel.clock.day, 0)
        self.assertIsInstance(kernel.agents, AgentPopulation)
        self.assertEqual(len(kernel.agents.agents), 0)

        initial_datetime = kernel.clock.get_datetime(datetime.datetime(2026, 1, 1))
        print(f"Initial simulation datetime: {initial_datetime}")

        ticks_to_advance = 100
        kernel.step(ticks_to_advance)

        self.assertEqual(kernel.clock.t, ticks_to_advance)
        self.assertEqual(kernel.clock.day, 0) # 100 minutes is less than a day (1440 min)
        self.assertEqual(kernel.clock.tick_of_day, 100)

        advanced_datetime = kernel.clock.get_datetime(datetime.datetime(2026, 1, 1))
        print(f"Simulation datetime after {ticks_to_advance} ticks: {advanced_datetime}")
        self.assertEqual(advanced_datetime, initial_datetime + datetime.timedelta(minutes=ticks_to_advance))
        print("Clock advanced successfully.")

    def test_agent_creation_and_population_management(self):
        print("""
--- Test: Agent Creation and Population Management ---""")
        seed = 123
        kernel = WorldKernel(seed=seed)

        agent1 = Agent(id="agent_001", seed=seed + 1)
        agent2 = Agent(id="agent_002", seed=seed + 2)

        agent1.beliefs.update("T1", 0, 0, 0, 0) # Give a belief to prevent IndexError
        agent2.beliefs.update("T1", 0, 0, 0, 0)
        kernel.agents.add_agent(agent1)
        kernel.agents.add_agent(agent2)

        self.assertEqual(len(kernel.agents.agents), 2)
        self.assertIn("agent_001", kernel.agents.agents)
        self.assertIn("agent_002", kernel.agents.agents)
        self.assertEqual(kernel.agents.get("agent_001"), agent1)
        print(f"Agent 'agent_001' created and added to population. Initial identity vector: {agent1.identity.identity_vector[0:3]}...")
        print(f"Agent 'agent_002' created and added to population. Initial belief topics: {agent2.beliefs.topics}")

        # Verify that agent states are initialized (even if empty)
        self.assertIsInstance(agent1.identity, type(Agent(id='temp', seed=0).identity))
        self.assertIsInstance(agent1.beliefs, type(Agent(id='temp', seed=0).beliefs))
        self.assertIsInstance(agent1.emotion, type(Agent(id='temp', seed=0).emotion))
        self.assertIsInstance(agent1.budgets, type(Agent(id='temp', seed=0).budgets))
        self.assertIsInstance(agent1.personality, type(Agent(id='temp', seed=0).personality))
        print("Agent states (identity, beliefs, emotion, budgets, personality) are initialized.")

        # Run a few steps and ensure agent state doesn't change (as no logic implemented)
        initial_agent1_identity_vector = list(agent1.identity.identity_vector)
        initial_agent2_belief_topics = dict(agent2.beliefs.topics)

        kernel.step(50)
        self.assertEqual(agent1.identity.identity_vector, initial_agent1_identity_vector)
        self.assertEqual(agent2.beliefs.topics, initial_agent2_belief_topics)
        print("Agent states remained unchanged after simulation steps (as expected for Phase 1).")

    def test_daily_budget_regeneration_initialization(self):
        print("""
--- Test: Daily Budget Regeneration Initialization ---""")
        agent_id = "test_budget_agent"
        agent_seed = 99
        agent = Agent(id=agent_id, seed=agent_seed)

        # Before regeneration, budgets are 0 (default)
        self.assertEqual(agent.budgets.attention_minutes, 0.0)
        self.assertEqual(agent.budgets.action_budget, 0.0)

        # Manually call regen_daily to test initial functionality
        agent.budgets.regen_daily()
        print(f"Budgets after first regeneration: Attention={agent.budgets.attention_minutes:.2f}, Action={agent.budgets.action_budget:.2f}")

        # Budgets should now be non-zero due to random generation
        self.assertGreater(agent.budgets.attention_minutes, 0)
        self.assertGreater(agent.budgets.action_budget, 0)
        print("Budgets regenerated successfully.")

if __name__ == '__main__':
    unittest.main()

```

## `tests/test_phase10.py`

```python
# tests/test_phase10.py
import statistics
import unittest

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.policy.bandit_learner import RewardVector


class TestPhase10(unittest.TestCase):
    def _expected_value_for_action(self, agent: Agent, action_key: str) -> float:
        """
        Current BanditLearner stores:
          - action_counts[action_key]
          - action_rewards[action_key] as a RewardVector SUM (not average)

        Expected scalar value (as used in exploitation) is:
          (sum_reward_vector.weighted_sum(personality) / count)
        """
        policy = agent.policy
        cnt = policy.action_counts.get(action_key, 0)
        if cnt <= 0:
            return 0.0
        sum_vec = policy.action_rewards[action_key]
        return sum_vec.weighted_sum(agent.personality) / cnt

    def test_evolutionary_pressure(self):
        """
        Current model behavior check (not evolutionary selection yet):
        Under a status-rewarding environment, agents with higher 'status' personality
        weight should learn a higher expected value for the SAME action key.

        IMPORTANT: BanditLearner keys actions as "<verb>_<topic>", e.g. "create_T".
        So we train on that exact key.
        """
        print("\n--- Test: Selection Pressure via Learning (Current Model) ---")
        _ = WorldKernel(seed=707)  # kernel not strictly required for this test, but fine to construct

        topic = "T"
        action_key = f"create_{topic}"

        # Create an initial population with random personalities
        agents: list[Agent] = []
        for i in range(20):
            agent = Agent(id=AgentId(f"agent_{i}"), seed=708 + i)
            agent.personality = RewardWeights(
                affiliation=agent.rng.random(),
                status=agent.rng.random(),
            )
            # Ensure there is at least one topic so "create_T" is a plausible action
            agent.beliefs.update(topic, 1, 1, 1, 1)
            agents.append(agent)

        initial_avg_status = statistics.mean(a.personality.status for a in agents)
        print(f"Initial average 'status' personality weight: {initial_avg_status:.2f}")

        # Environment: reward is an affine function of personality.status
        # high status -> positive reward, low status -> negative reward
        for _ in range(500):
            for agent in agents:
                reward_val = agent.personality.status * 0.1 - 0.05
                agent.learn(action_key, RewardVector(status=reward_val))

        # Compare learned values between high-status and low-status subsets
        agents_sorted = sorted(agents, key=lambda a: a.personality.status)
        low = agents_sorted[:5]
        high = agents_sorted[-5:]

        low_vals = [self._expected_value_for_action(a, action_key) for a in low]
        high_vals = [self._expected_value_for_action(a, action_key) for a in high]

        low_mean = statistics.mean(low_vals)
        high_mean = statistics.mean(high_vals)

        print(f"Mean learned value (low-status 5):  {low_mean:.4f}")
        print(f"Mean learned value (high-status 5): {high_mean:.4f}")

        self.assertGreater(
            high_mean,
            low_mean,
            "Under a status-rewarding environment, higher-status agents should learn a higher value for action 'create_T'."
        )


if __name__ == "__main__":
    unittest.main()

```

## `tests/test_phase2.py`

```python
import unittest
import io
from contextlib import redirect_stdout

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import AgentId, ContentId, TopicId, ActorId


class TestPhase2(unittest.TestCase):

    def setUp(self):
        """Set up a standard world and agent for tests."""
        self.seed = 42
        self.kernel = WorldKernel(seed=self.seed)
        self.agent = Agent(id=AgentId("agent_001"), seed=self.seed + 1)
        self.kernel.agents.add_agent(self.agent)
        self.topic = TopicId("T1")

    def test_agent_forms_new_belief(self):
        """
        Verify that an agent with no prior belief forms a new one
        after being exposed to content.
        """
        print("\n--- Test: Agent Forms New Belief ---")
        # Agent starts with no belief on the topic
        self.assertIsNone(self.agent.beliefs.get(self.topic))
        print(f"Agent '{self.agent.id}' starts with no belief on topic '{self.topic}'.")

        # Create a piece of content
        content = ContentItem(
            id=ContentId("C1"),
            author_id=ActorId("author_01"),
            topic=self.topic,
            stance=0.8
        )
        print(f"Agent perceives content '{content.id}' with stance {content.stance}.")

        # Capture the log output
        f = io.StringIO()
        with redirect_stdout(f):
            self.agent.perceive(content, self.kernel.world_context)
        log_output = f.getvalue()

        # Check the agent's belief state
        new_belief = self.agent.beliefs.get(self.topic)
        self.assertIsNotNone(new_belief)
        self.assertAlmostEqual(new_belief.stance, 0.4)  # 0.8 * 0.5 trust
        self.assertAlmostEqual(new_belief.confidence, 0.05)  # 0.1 * 0.5 trust
        print(f"Agent's new belief: Stance={new_belief.stance:.2f}, Confidence={new_belief.confidence:.2f}")

        # Check if the event was logged (updated to current logging format)
        self.assertIn("DEBUG:", log_output)
        self.assertIn(f"Agent['{self.agent.id}']", log_output)
        self.assertIn(f"Topic='{self.topic}'", log_output)
        self.assertIn("BeliefUpdate:", log_output)
        self.assertIn("StanceΔ=0.4000", log_output)
        print("Belief formation was logged successfully.")

    def test_agent_updates_existing_belief(self):
        """
        Verify that an agent with an existing belief modifies it
        after being exposed to new content.
        """
        print("\n--- Test: Agent Updates Existing Belief ---")
        # Agent starts with a contrary belief
        self.agent.beliefs.update(
            topic_id=self.topic,
            stance=-0.5,
            confidence=0.5,
            salience=0.0,
            knowledge=0.0
        )
        initial_belief = self.agent.beliefs.get(self.topic)
        print(
            f"Agent '{self.agent.id}' starts with belief: "
            f"Stance={initial_belief.stance:.2f}, Confidence={initial_belief.confidence:.2f}"
        )

        # Create a piece of content with an opposing stance
        content = ContentItem(
            id=ContentId("C2"),
            author_id=ActorId("author_02"),
            topic=self.topic,
            stance=1.0
        )
        print(f"Agent perceives content '{content.id}' with stance {content.stance}.")

        # Capture log output
        f = io.StringIO()
        with redirect_stdout(f):
            self.agent.perceive(content, self.kernel.world_context)
        log_output = f.getvalue()

        # Check the agent's belief state
        updated_belief = self.agent.beliefs.get(self.topic)
        self.assertIsNotNone(updated_belief)

        # Expected stance update: -0.5 + (1.0 - (-0.5)) * 0.05 = -0.425
        self.assertAlmostEqual(updated_belief.stance, -0.425)

        # Expected confidence update: 0.5 + 0.01 = 0.51
        self.assertAlmostEqual(updated_belief.confidence, 0.51)
        print(f"Agent's updated belief: Stance={updated_belief.stance:.2f}, Confidence={updated_belief.confidence:.2f}")

        # Check if the event was logged correctly (updated to current logging format)
        self.assertIn("DEBUG:", log_output)
        self.assertIn("BeliefUpdate:", log_output)
        self.assertIn(f"StanceΔ={0.075:.4f}", log_output)
        self.assertIn(f"ConfΔ={0.01:.4f}", log_output)
        print("Belief update was logged successfully.")


if __name__ == '__main__':
    unittest.main()

```

## `tests/test_phase3.py`

```python
import unittest
import io
from contextlib import redirect_stdout

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import AgentId, ContentId, TopicId, ActorId
from gsocialsim.social.relationship_vector import RelationshipVector

class TestPhase3(unittest.TestCase):

    def setUp(self):
        """Set up a world with three agents: a viewer, a trusted author, and an untrusted author."""
        self.kernel = WorldKernel(seed=101)
        
        self.viewer = Agent(id=AgentId("viewer"), seed=102)
        self.trusted_author = Agent(id=AgentId("trusted_author"), seed=103)
        self.untrusted_author = Agent(id=AgentId("untrusted_author"), seed=104)

        self.kernel.agents.add_agent(self.viewer)
        self.kernel.agents.add_agent(self.trusted_author)
        self.kernel.agents.add_agent(self.untrusted_author)

        # Establish trust relationships
        # Viewer -> Trusted Author: High trust
        high_trust_vector = RelationshipVector(trust=0.9)
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.trusted_author.id, high_trust_vector)

        # Viewer -> Untrusted Author: Low trust
        low_trust_vector = RelationshipVector(trust=0.1)
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.untrusted_author.id, low_trust_vector)

        self.topic = TopicId("T3")

    def test_influence_is_scaled_by_trust(self):
        """
        Verify that belief updates are stronger from a trusted source than an untrusted one.
        """
        print("\n--- Test: Influence Scaled by Trust ---")
        # Viewer starts with a neutral belief
        self.viewer.beliefs.update(self.topic, stance=0.0, confidence=0.5, salience=0, knowledge=0)
        initial_stance = self.viewer.beliefs.get(self.topic).stance
        print(f"Viewer starts with belief: Stance={initial_stance:.2f}")

        # --- Case 1: Exposure to content from a TRUSTED author ---
        trusted_content = ContentItem(id=ContentId("C_trust"), author_id=self.trusted_author.id, topic=self.topic, stance=1.0)
        
        self.viewer.perceive(trusted_content, self.kernel.world_context)
        belief_after_trusted = self.viewer.beliefs.get(self.topic)
        
        print(f"After trusted content, viewer belief is: Stance={belief_after_trusted.stance:.4f}")
        # Change = (1.0 - 0.0) * 0.10 * 0.9 (trust) = 0.09
        self.assertAlmostEqual(belief_after_trusted.stance, 0.09)
        stance_change_trusted = belief_after_trusted.stance - initial_stance

        # --- Case 2: Reset and expose to content from an UNTRUSTED author ---
        self.viewer.beliefs.update(self.topic, stance=0.0, confidence=0.5, salience=0, knowledge=0) # Reset stance
        initial_stance_untrusted = self.viewer.beliefs.get(self.topic).stance
        untrusted_content = ContentItem(id=ContentId("C_untrust"), author_id=self.untrusted_author.id, topic=self.topic, stance=1.0)
        
        self.viewer.perceive(untrusted_content, self.kernel.world_context)
        belief_after_untrusted = self.viewer.beliefs.get(self.topic)

        print(f"After untrusted content, viewer belief is: Stance={belief_after_untrusted.stance:.4f}")
        # Change = (1.0 - 0.0) * 0.10 * 0.1 (trust) = 0.01
        self.assertAlmostEqual(belief_after_untrusted.stance, 0.01)
        stance_change_untrusted = belief_after_untrusted.stance - initial_stance_untrusted

        # --- Verification ---
        self.assertGreater(stance_change_trusted, stance_change_untrusted)
        print(f"Verified: Stance change from trusted source ({stance_change_trusted:.4f}) > from untrusted source ({stance_change_untrusted:.4f})")

    def test_new_belief_confidence_scaled_by_trust(self):
        """
        Verify that confidence in a newly formed belief is scaled by the source's trust.
        """
        print("\n--- Test: New Belief Confidence Scaled by Trust ---")
        # Viewer starts with no belief on the topic
        self.assertIsNone(self.viewer.beliefs.get(self.topic))

        # --- Case 1: Exposure to content from a TRUSTED author ---
        trusted_content = ContentItem(id=ContentId("C_trust"), author_id=self.trusted_author.id, topic=self.topic, stance=0.7)
        self.viewer.perceive(trusted_content, self.kernel.world_context)
        belief_from_trusted = self.viewer.beliefs.get(self.topic)
        
        print(f"New belief from trusted source: Confidence={belief_from_trusted.confidence:.4f}")
        # New confidence = 0.1 * 0.9 (trust) = 0.09
        self.assertAlmostEqual(belief_from_trusted.confidence, 0.09)

        # --- Case 2: Reset and expose to content from an UNTRUSTED author ---
        self.viewer.beliefs.topics.pop(self.topic) # Reset belief
        self.assertIsNone(self.viewer.beliefs.get(self.topic))
        untrusted_content = ContentItem(id=ContentId("C_untrust"), author_id=self.untrusted_author.id, topic=self.topic, stance=0.7)
        self.viewer.perceive(untrusted_content, self.kernel.world_context)
        belief_from_untrusted = self.viewer.beliefs.get(self.topic)

        print(f"New belief from untrusted source: Confidence={belief_from_untrusted.confidence:.4f}")
        # New confidence = 0.1 * 0.1 (trust) = 0.01
        self.assertAlmostEqual(belief_from_untrusted.confidence, 0.01)

        # --- Verification ---
        self.assertGreater(belief_from_trusted.confidence, belief_from_untrusted.confidence)
        print("Verified: Confidence in new belief is higher from a trusted source.")

if __name__ == '__main__':
    unittest.main()

```

## `tests/test_phase4.py`

```python
import unittest
import io
from contextlib import redirect_stdout

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId

class TestPhase4(unittest.TestCase):

    def setUp(self):
        """
        Set up a world with a simple influence chain: A -> B -> C
        Agent A follows B, Agent B follows C.
        """
        self.kernel = WorldKernel(seed=202)
        
        self.agent_A = Agent(id=AgentId("A"), seed=203)
        self.agent_B = Agent(id=AgentId("B"), seed=204)
        self.agent_C = Agent(id=AgentId("C"), seed=205)

        self.kernel.agents.add_agent(self.agent_A)
        self.kernel.agents.add_agent(self.agent_B)
        self.kernel.agents.add_agent(self.agent_C)

        # A follows B
        self.kernel.world_context.network.graph.add_edge(
            follower=self.agent_A.id,
            followed=self.agent_B.id
        )
        # B follows C
        self.kernel.world_context.network.graph.add_edge(
            follower=self.agent_B.id,
            followed=self.agent_C.id
        )
        
        self.agent_A.budgets.action_budget = 10
        self.agent_B.budgets.action_budget = 10
        self.agent_C.budgets.action_budget = 10

    def test_autonomous_influence_chain(self):
        """
        Verify that a belief can propagate autonomously from C to B to A.
        """
        print("\n--- Test: Autonomous Influence Chain ---")
        # Seed Agent C with a strong, confident belief.
        self.topic = TopicId("T4_Chain")
        self.agent_C.beliefs.update(self.topic, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)
        print(f"Initial state: A.stance=N/A, B.stance=N/A, C.stance={self.agent_C.beliefs.get(self.topic).stance:.2f}")

        # Ensure A and B start with no belief
        self.assertIsNone(self.agent_A.beliefs.get(self.topic))
        self.assertIsNone(self.agent_B.beliefs.get(self.topic))

        # Run the simulation for enough ticks for actions to occur and propagate
        # With a 1% action chance, 300 ticks should be sufficient for C and then B to post.
        f = io.StringIO()
        with redirect_stdout(f):
            self.kernel.step(300)
        log_output = f.getvalue()

        # --- Verification ---
        print("\n--- Verifying Final States ---")
        belief_A = self.agent_A.beliefs.get(self.topic)
        belief_B = self.agent_B.beliefs.get(self.topic)
        belief_C = self.agent_C.beliefs.get(self.topic)

        # 1. C's belief should be unchanged (it's the source)
        self.assertAlmostEqual(belief_C.stance, 1.0)
        print(f"Final C Stance: {belief_C.stance:.4f} (Correct)")

        # 2. B must have been influenced by C
        self.assertIsNotNone(belief_B, "Agent B was not influenced, no belief formed.")
        self.assertGreater(belief_B.stance, 0, "Agent B's stance should have moved towards C's.")
        print(f"Final B Stance: {belief_B.stance:.4f} (Influenced by C)")
        
        # 3. A must have been influenced by B
        self.assertIsNotNone(belief_A, "Agent A was not influenced, no belief formed.")
        self.assertGreater(belief_A.stance, 0, "Agent A's stance should have moved towards B's.")
        print(f"Final A Stance: {belief_A.stance:.4f} (Influenced by B)")

        # 4. The influence on A should be less than on B, as it's second-hand
        self.assertLess(belief_A.stance, belief_B.stance, "A's stance should be less extreme than B's.")
        print("Verified: Influence propagated autonomously and diluted down the chain.")

        # 5. Check logs for the chain of events
        self.assertIn(f"Agent['B'] BeliefUpdate: Topic='{self.topic}'", log_output, "Log shows no belief update for B")
        self.assertIn(f"Agent['A'] BeliefUpdate: Topic='{self.topic}'", log_output, "Log shows no belief update for A")
        print("Verified: Log files show updates for both A and B.")

if __name__ == '__main__':
    unittest.main()

```

## `tests/test_phase5.py`

```python
import unittest
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId

class TestPhase5(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=303)
        self.agent = Agent(id=AgentId("budget_agent"), seed=304)
        # Give the agent a belief so it has something to post about
        self.agent.beliefs.update(TopicId("T5"), 1.0, 1.0, 1.0, 1.0)
        self.agent.budgets.action_budget = 2.0 # Start with a known budget
        self.kernel.agents.add_agent(self.agent)

    def test_budget_depletion_and_regeneration(self):
        """
        Verify that an agent stops acting when its budget is depleted
        and resumes after the daily budget regeneration.
        """
        print("\n--- Test: Budget Depletion and Regeneration ---")
        
        # Give the agent a small, fixed budget
        self.agent.budgets.action_budget = 2.0
        print(f"Agent starts with action_budget = {self.agent.budgets.action_budget}")

        # Mock the policy to make the test deterministic
        self.agent.policy.should_act = lambda agent: True

        # --- Depletion Phase ---
        # Agent should now post on every tick until budget is gone
        posts_in_first_day = 0
        for _ in range(2): # Should run exactly twice
            content = self.agent.act(self.kernel.clock.t)
            if content:
                posts_in_first_day += 1
        
        self.assertEqual(posts_in_first_day, 2, "Agent should have posted exactly twice before running out of budget.")
        self.assertEqual(self.agent.budgets.action_budget, 0, "Agent's action budget should be zero.")
        print("Agent successfully depleted its action budget and stopped posting.")

        # --- Regeneration Phase ---
        # Run the kernel long enough to cross a day boundary
        ticks_to_new_day = self.kernel.clock.ticks_per_day - self.kernel.clock.tick_of_day
        self.kernel.step(ticks_to_new_day + 1)
        
        self.assertGreater(self.agent.budgets.action_budget, 0, "Agent's action budget should have been regenerated.")
        print(f"After daily cycle, agent budget regenerated to: {self.agent.budgets.action_budget:.2f}")

        # Verify agent can act again
        can_act_again = False
        for _ in range(300):
             if self.agent.act(self.kernel.clock.t):
                 can_act_again = True
                 break
        
        self.assertTrue(can_act_again, "Agent should be able to act again after budget regeneration.")
        print("Agent can act again. Budget system is working.")

if __name__ == '__main__':
    unittest.main()

```

## `tests/test_phase6.py`

```python
import io
import unittest
from contextlib import redirect_stdout

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId, ContentId, ActorId
from gsocialsim.stimuli.content_item import ContentItem


class TestPhase6(unittest.TestCase):
    def setUp(self):
        self.kernel = WorldKernel(seed=505)

        self.agent_A = Agent(id=AgentId("agent_A"), seed=506)
        self.agent_B = Agent(id=AgentId("agent_B"), seed=507)

        # Seed B with a belief so it has something meaningful to communicate.
        self.topic = TopicId("T6_Physical")
        self.agent_B.beliefs.update(self.topic, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)

        self.kernel.agents.add_agent(self.agent_A)
        self.kernel.agents.add_agent(self.agent_B)

    def test_physical_influence(self):
        """
        Current model: "physical proximity influence" is tested by delivering a perception
        with is_physical=True to simulate a co-located interaction.
        We do NOT depend on the kernel to autonomously schedule meetings yet.
        """
        print("\n--- Test: Physical Layer Influence ---")

        # --- Run 1: No proximity / no delivery ---
        self.kernel.step(100)
        self.assertIsNone(self.agent_A.beliefs.get(self.topic), "Agent A should not have been influenced yet.")
        print("Verified: No influence without an interaction delivery event.")

        # --- Run 2: With physical proximity ---
        content = ContentItem(
            id=ContentId("C_phys_1"),
            author_id=ActorId(str(self.agent_B.id)),
            topic=self.topic,
            stance=1.0,
        )

        f = io.StringIO()
        with redirect_stdout(f):
            # Key point: is_physical=True triggers the physical amplification path (if implemented).
            self.agent_A.perceive(content, self.kernel.world_context, is_physical=True)

        belief_A = self.agent_A.beliefs.get(self.topic)
        self.assertIsNotNone(belief_A, "Agent A should have been influenced by physical proximity.")
        print(f"Agent A formed belief via physical proximity: stance={belief_A.stance:.3f}, conf={belief_A.confidence:.3f}")

        # Keep this assertion loose but meaningful.
        self.assertGreater(
            belief_A.confidence, 0.0,
            "Physical influence should result in a non-zero confidence belief."
        )


if __name__ == "__main__":
    unittest.main()

```

## `tests/test_phase7.py`

```python
import unittest
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.types import AgentId, TopicId

class TestPhase7(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=505)
        self.viewer = Agent(id=AgentId("viewer"), seed=506)
        self.source1 = Agent(id=AgentId("source1"), seed=507)
        self.source2 = Agent(id=AgentId("source2"), seed=508)
        self.kernel.agents.add_agent(self.viewer)
        self.kernel.agents.add_agent(self.source1)
        self.kernel.agents.add_agent(self.source2)
        
        self.topic = TopicId("T7_Attrib")
        self.viewer.beliefs.update(self.topic, -0.2, 0.5, 0, 0) # Start with a moderately negative belief

        # Set trust to 1.0 to ensure influence is strong enough to cross the threshold
        from gsocialsim.social.relationship_vector import RelationshipVector
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.source1.id, RelationshipVector(trust=1.0))
        self.kernel.world_context.gsr.set_relationship(self.viewer.id, self.source2.id, RelationshipVector(trust=1.0))


    def test_belief_crossing_and_attribution(self):
        """
        Verify that a belief crossing event is logged and that attribution
        is correctly assigned to the influencing sources.
        """
        print("\n--- Test: Belief Crossing and Attribution ---")
        
        # Capture log output across all relevant perceptions
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            # Exposure 1
            content1 = ContentItem("c1", self.source1.id, self.topic, 0.8)
            self.viewer.perceive(content1, self.kernel.world_context)
            
            # Exposure 2 (this one should trigger the crossing)
            content2 = ContentItem("c2", self.source2.id, self.topic, 1.0)
            self.viewer.perceive(content2, self.kernel.world_context)
            
        log_output = f.getvalue()

        self.assertIn("BeliefCrossing", log_output, "Belief crossing event was not logged.")
        self.assertIn(f"Topic='{self.topic}'", log_output)
        self.assertIn("Stance=-0.10->0.01", log_output, "Logged stance change is incorrect.")
        
        # Verify attribution
        self.assertIn("Attribution=", log_output)
        self.assertIn(f"'{self.source1.id}': 0.5", log_output)
        self.assertIn(f"'{self.source2.id}': 0.5", log_output)
        print("Verified: Belief crossing and attribution logged correctly.")

if __name__ == '__main__':
    unittest.main()

```

## `tests/test_phase8.py`

```python
import unittest

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.types import AgentId, TopicId


class TestPhase8(unittest.TestCase):

    def test_bandit_learner(self):
        """
        Verify that an agent learns to prefer actions that align with its personality.
        """
        print("\n--- Test: Reinforcement Learning (Bandit) ---")
        kernel = WorldKernel(seed=606)

        # Agent with personality that strongly values affiliation
        agent = Agent(id=AgentId("learner"), seed=607)
        agent.personality = RewardWeights(affiliation=1.0, status=0.0)

        # Agent has two topics to talk about
        good_topic = TopicId("T_good")
        bad_topic = TopicId("T_bad")
        agent.beliefs.update(good_topic, 1, 1, 1, 1)
        agent.beliefs.update(bad_topic, 1, 1, 1, 1)
        agent.budgets.action_budget = 1000  # Give plenty of budget

        kernel.agents.add_agent(agent)

        # Mock the decision to act to make the test deterministic
        agent.policy.should_act = lambda agent: True

        # Mock the reward generation to give affiliation reward only for the good topic
        original_learn = agent.learn

        def mock_learn(topic, reward_vector):
            # The bandit uses epsilon-greedy, so we need to run it for a bit to learn
            if topic == good_topic:
                reward_vector.affiliation = 1.0
            else:
                reward_vector.affiliation = -1.0  # Give negative reward for the bad topic
            original_learn(topic, reward_vector)

        agent.learn = mock_learn

        # Run the simulation for many steps to allow for learning
        for i in range(100):  # More than enough to learn
            interaction = agent.act(kernel.clock.t + i)
            if interaction:
                # New model: Agent.act returns an Interaction envelope.
                # For CREATE, the topic is on the original_content.
                self.assertIsNotNone(interaction.original_content, "Expected CREATE interaction to include original_content.")
                from gsocialsim.policy.bandit_learner import RewardVector
                agent.learn(interaction.original_content.topic, RewardVector())

        # After learning, disable exploration (epsilon=0) to check exploitation
        agent.policy.epsilon = 0.0
        post_counts = {good_topic: 0, bad_topic: 0}

        for i in range(100):
            interaction = agent.act(kernel.clock.t + i)
            if interaction:
                self.assertIsNotNone(interaction.original_content, "Expected CREATE interaction to include original_content.")
                post_counts[interaction.original_content.topic] += 1

        self.assertGreater(
            post_counts[good_topic],
            post_counts[bad_topic],
            "Agent should have learned to prefer the rewarding topic."
        )
        self.assertEqual(
            post_counts[bad_topic],
            0,
            "Agent should not choose the negatively rewarded topic in exploitation mode."
        )
        print(f"Verified: Agent learned to prefer the good topic. Posts (good/bad): {post_counts[good_topic]}/{post_counts[bad_topic]}")


if __name__ == '__main__':
    unittest.main()

```

## `threshold.html`

```html
<html>
    <head>
        <meta charset="utf-8">
        
            <script>function neighbourhoodHighlight(params) {
  // console.log("in nieghbourhoodhighlight");
  allNodes = nodes.get({ returnType: "Object" });
  // originalNodes = JSON.parse(JSON.stringify(allNodes));
  // if something is selected:
  if (params.nodes.length > 0) {
    highlightActive = true;
    var i, j;
    var selectedNode = params.nodes[0];
    var degrees = 2;

    // mark all nodes as hard to read.
    for (let nodeId in allNodes) {
      // nodeColors[nodeId] = allNodes[nodeId].color;
      allNodes[nodeId].color = "rgba(200,200,200,0.5)";
      if (allNodes[nodeId].hiddenLabel === undefined) {
        allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }
    var connectedNodes = network.getConnectedNodes(selectedNode);
    var allConnectedNodes = [];

    // get the second degree nodes
    for (i = 1; i < degrees; i++) {
      for (j = 0; j < connectedNodes.length; j++) {
        allConnectedNodes = allConnectedNodes.concat(
          network.getConnectedNodes(connectedNodes[j])
        );
      }
    }

    // all second degree nodes get a different color and their label back
    for (i = 0; i < allConnectedNodes.length; i++) {
      // allNodes[allConnectedNodes[i]].color = "pink";
      allNodes[allConnectedNodes[i]].color = "rgba(150,150,150,0.75)";
      if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[allConnectedNodes[i]].label =
          allNodes[allConnectedNodes[i]].hiddenLabel;
        allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // all first degree nodes get their own color and their label back
    for (i = 0; i < connectedNodes.length; i++) {
      // allNodes[connectedNodes[i]].color = undefined;
      allNodes[connectedNodes[i]].color = nodeColors[connectedNodes[i]];
      if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
        allNodes[connectedNodes[i]].label =
          allNodes[connectedNodes[i]].hiddenLabel;
        allNodes[connectedNodes[i]].hiddenLabel = undefined;
      }
    }

    // the main node gets its own color and its label back.
    // allNodes[selectedNode].color = undefined;
    allNodes[selectedNode].color = nodeColors[selectedNode];
    if (allNodes[selectedNode].hiddenLabel !== undefined) {
      allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
      allNodes[selectedNode].hiddenLabel = undefined;
    }
  } else if (highlightActive === true) {
    // console.log("highlightActive was true");
    // reset all nodes
    for (let nodeId in allNodes) {
      // allNodes[nodeId].color = "purple";
      allNodes[nodeId].color = nodeColors[nodeId];
      // delete allNodes[nodeId].color;
      if (allNodes[nodeId].hiddenLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
        allNodes[nodeId].hiddenLabel = undefined;
      }
    }
    highlightActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    // console.log("Nothing was selected");
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        // console.log(allNodes[nodeId]);
        // allNodes[nodeId].color = {};
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function filterHighlight(params) {
  allNodes = nodes.get({ returnType: "Object" });
  // if something is selected:
  if (params.nodes.length > 0) {
    filterActive = true;
    let selectedNodes = params.nodes;

    // hiding all nodes and saving the label
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = true;
      if (allNodes[nodeId].savedLabel === undefined) {
        allNodes[nodeId].savedLabel = allNodes[nodeId].label;
        allNodes[nodeId].label = undefined;
      }
    }

    for (let i=0; i < selectedNodes.length; i++) {
      allNodes[selectedNodes[i]].hidden = false;
      if (allNodes[selectedNodes[i]].savedLabel !== undefined) {
        allNodes[selectedNodes[i]].label = allNodes[selectedNodes[i]].savedLabel;
        allNodes[selectedNodes[i]].savedLabel = undefined;
      }
    }

  } else if (filterActive === true) {
    // reset all nodes
    for (let nodeId in allNodes) {
      allNodes[nodeId].hidden = false;
      if (allNodes[nodeId].savedLabel !== undefined) {
        allNodes[nodeId].label = allNodes[nodeId].savedLabel;
        allNodes[nodeId].savedLabel = undefined;
      }
    }
    filterActive = false;
  }

  // transform the object into an array
  var updateArray = [];
  if (params.nodes.length > 0) {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  } else {
    for (let nodeId in allNodes) {
      if (allNodes.hasOwnProperty(nodeId)) {
        updateArray.push(allNodes[nodeId]);
      }
    }
    nodes.update(updateArray);
  }
}

function selectNode(nodes) {
  network.selectNodes(nodes);
  neighbourhoodHighlight({ nodes: nodes });
  return nodes;
}

function selectNodes(nodes) {
  network.selectNodes(nodes);
  filterHighlight({nodes: nodes});
  return nodes;
}

function highlightFilter(filter) {
  let selectedNodes = []
  let selectedProp = filter['property']
  if (filter['item'] === 'node') {
    let allNodes = nodes.get({ returnType: "Object" });
    for (let nodeId in allNodes) {
      if (allNodes[nodeId][selectedProp] && filter['value'].includes((allNodes[nodeId][selectedProp]).toString())) {
        selectedNodes.push(nodeId)
      }
    }
  }
  else if (filter['item'] === 'edge'){
    let allEdges = edges.get({returnType: 'object'});
    // check if the selected property exists for selected edge and select the nodes connected to the edge
    for (let edge in allEdges) {
      if (allEdges[edge][selectedProp] && filter['value'].includes((allEdges[edge][selectedProp]).toString())) {
        selectedNodes.push(allEdges[edge]['from'])
        selectedNodes.push(allEdges[edge]['to'])
      }
    }
  }
  selectNodes(selectedNodes)
}</script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            
            
            
            
            
            

        
<center>
<h1></h1>
</center>

<!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
<script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
          crossorigin="anonymous"
        />
        <script
          src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf"
          crossorigin="anonymous"
        ></script>


        <center>
          <h1></h1>
        </center>
        <style type="text/css">

             #mynetwork {
                 width: 100%;
                 height: 100vh;
                 background-color: #ffffff;
                 border: 1px solid lightgray;
                 position: relative;
                 float: left;
             }

             

             

             
        </style>
    </head>


    <body>
        <div class="card" style="width: 100%">
            
            
            <div id="mynetwork" class="card-body"></div>
        </div>

        
        

        <script type="text/javascript">

              // initialize global variables.
              var edges;
              var nodes;
              var allNodes;
              var allEdges;
              var nodeColors;
              var originalNodes;
              var network;
              var container;
              var options, data;
              var filter = {
                  item : '',
                  property : '',
                  value : []
              };

              

              

              // This method is responsible for drawing the graph, returns the drawn network
              function drawGraph() {
                  var container = document.getElementById('mynetwork');

                  

                  // parsing and collecting nodes and edges from the python
                  nodes = new vis.DataSet([{"color": "#cccccc", "id": "A", "label": "A", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "B", "label": "B", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "C (Source)", "label": "C (Source)", "shape": "dot", "size": 18}, {"color": "#cccccc", "id": "D (Lurker)", "label": "D (Lurker)", "shape": "dot", "size": 18}, {"color": "#00cc66", "id": "news1", "label": "news1", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "sci1", "label": "sci1", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}, {"color": "#00cc66", "id": "sci2", "label": "sci2", "shape": "square", "size": 16, "title": "Source: UniLab"}, {"color": "#00cc66", "id": "sci3", "label": "sci3", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}, {"color": "#00cc66", "id": "sci4", "label": "sci4", "shape": "square", "size": 16, "title": "Source: UniLab"}, {"color": "#00cc66", "id": "sci5", "label": "sci5", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}, {"color": "#00cc66", "id": "pol1", "label": "pol1", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "pol2", "label": "pol2", "shape": "square", "size": 16, "title": "Source: RivalNews"}, {"color": "#00cc66", "id": "news2", "label": "news2", "shape": "square", "size": 16, "title": "Source: RivalNews"}, {"color": "#00cc66", "id": "pol3", "label": "pol3", "shape": "square", "size": 16, "title": "Source: CapitolWatch"}, {"color": "#00cc66", "id": "pol4", "label": "pol4", "shape": "square", "size": 16, "title": "Source: CapitolWatch"}, {"color": "#00cc66", "id": "pol5", "label": "pol5", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "eco1", "label": "eco1", "shape": "square", "size": 16, "title": "Source: MarketWire"}, {"color": "#00cc66", "id": "eco2", "label": "eco2", "shape": "square", "size": 16, "title": "Source: MarketWire"}, {"color": "#00cc66", "id": "eco3", "label": "eco3", "shape": "square", "size": 16, "title": "Source: FinBlog"}, {"color": "#00cc66", "id": "eco4", "label": "eco4", "shape": "square", "size": 16, "title": "Source: MarketWire"}, {"color": "#00cc66", "id": "eco5", "label": "eco5", "shape": "square", "size": 16, "title": "Source: FinBlog"}, {"color": "#00cc66", "id": "cult1", "label": "cult1", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "meme1", "label": "meme1", "shape": "square", "size": 16, "title": "Source: UserA"}, {"color": "#00cc66", "id": "cult2", "label": "cult2", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "cult3", "label": "cult3", "shape": "square", "size": 16, "title": "Source: PodcasterX"}, {"color": "#00cc66", "id": "cult4", "label": "cult4", "shape": "square", "size": 16, "title": "Source: PodcasterX"}, {"color": "#00cc66", "id": "cult5", "label": "cult5", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "meme2", "label": "meme2", "shape": "square", "size": 16, "title": "Source: UserB"}, {"color": "#00cc66", "id": "meme3", "label": "meme3", "shape": "square", "size": 16, "title": "Source: UserC"}, {"color": "#00cc66", "id": "meme4", "label": "meme4", "shape": "square", "size": 16, "title": "Source: UserD"}, {"color": "#00cc66", "id": "meme5", "label": "meme5", "shape": "square", "size": 16, "title": "Source: UserE"}, {"color": "#00cc66", "id": "sports1", "label": "sports1", "shape": "square", "size": 16, "title": "Source: SportsDesk"}, {"color": "#00cc66", "id": "sports2", "label": "sports2", "shape": "square", "size": 16, "title": "Source: SportsDesk"}, {"color": "#00cc66", "id": "sports3", "label": "sports3", "shape": "square", "size": 16, "title": "Source: FanAccount"}, {"color": "#00cc66", "id": "sports4", "label": "sports4", "shape": "square", "size": 16, "title": "Source: FanAccount"}, {"color": "#00cc66", "id": "sports5", "label": "sports5", "shape": "square", "size": 16, "title": "Source: SportsDesk"}, {"color": "#00cc66", "id": "sec1", "label": "sec1", "shape": "square", "size": 16, "title": "Source: InfosecNews"}, {"color": "#00cc66", "id": "sec2", "label": "sec2", "shape": "square", "size": 16, "title": "Source: InfosecNews"}, {"color": "#00cc66", "id": "sec3", "label": "sec3", "shape": "square", "size": 16, "title": "Source: ForumUser"}, {"color": "#00cc66", "id": "sec4", "label": "sec4", "shape": "square", "size": 16, "title": "Source: InfosecNews"}, {"color": "#00cc66", "id": "sec5", "label": "sec5", "shape": "square", "size": 16, "title": "Source: ForumUser"}, {"color": "#00cc66", "id": "mix1", "label": "mix1", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "mix2", "label": "mix2", "shape": "square", "size": 16, "title": "Source: RivalNews"}, {"color": "#00cc66", "id": "mix3", "label": "mix3", "shape": "square", "size": 16, "title": "Source: NewsOutlet"}, {"color": "#00cc66", "id": "mix4", "label": "mix4", "shape": "square", "size": 16, "title": "Source: TrendFeed"}, {"color": "#00cc66", "id": "mix5", "label": "mix5", "shape": "square", "size": 16, "title": "Source: ScienceDaily"}]);
                  edges = new vis.DataSet([{"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "news1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 157 time(s)", "to": "sci1", "width": 7.0}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "sci3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 26 time(s)", "to": "sci3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 136 time(s)", "to": "news1", "width": 6.197452229299364}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 5 time(s)", "to": "news1", "width": 1.1910828025477707}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sci4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 29 time(s)", "to": "sci2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sci5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 133 time(s)", "to": "pol3", "width": 6.082802547770701}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 32 time(s)", "to": "news2", "width": 2.2229299363057327}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "pol3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "pol3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 29 time(s)", "to": "sci1", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "pol2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "eco3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "eco4", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 51 time(s)", "to": "pol1", "width": 2.949044585987261}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "news2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 28 time(s)", "to": "sci2", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "sci1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 29 time(s)", "to": "sci5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "eco3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 30 time(s)", "to": "cult4", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "sci2", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "cult5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "meme3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 30 time(s)", "to": "eco4", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "meme2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "meme1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "meme3", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "cult1", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "eco4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "eco2", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "meme2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sci2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "cult3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "eco2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "meme2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "cult4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "pol4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "meme5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "pol2", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 6 time(s)", "to": "sports2", "width": 1.2292993630573248}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "sports2", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "cult1", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 28 time(s)", "to": "meme4", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "cult3", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "pol3", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 30 time(s)", "to": "sports3", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "sci1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "pol5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "sports5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "pol4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "mix2", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sec5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 29 time(s)", "to": "eco5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "sec2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "pol2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 25 time(s)", "to": "sci3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sec1", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "cult3", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 12 time(s)", "to": "sports4", "width": 1.4585987261146496}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "pol5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "sec5", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "sec3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sports4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "mix1", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "news2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "mix5", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sports3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 29 time(s)", "to": "mix5", "width": 2.1082802547770703}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sec1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "meme5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "cult5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sports5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "mix3", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "cult4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sports1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "eco1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 23 time(s)", "to": "sec4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "meme3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 5 time(s)", "to": "mix1", "width": 1.1910828025477707}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "sec2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "mix4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "mix1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 22 time(s)", "to": "sec1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "cult2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 30 time(s)", "to": "cult2", "width": 2.1464968152866244}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 26 time(s)", "to": "sports5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 26 time(s)", "to": "meme5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "cult4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 10 time(s)", "to": "mix3", "width": 1.3821656050955413}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "mix3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "meme4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sec4", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "sec3", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "meme3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "sec2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sec3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 3 time(s)", "to": "mix2", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "eco3", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "sports3", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "cult2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "eco3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 4 time(s)", "to": "sec5", "width": 1.1528662420382165}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "news1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "sec4", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 28 time(s)", "to": "sci5", "width": 2.0700636942675157}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 3 time(s)", "to": "cult5", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 2 time(s)", "to": "pol4", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "eco5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sports4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "mix2", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "eco5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "sports2", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 24 time(s)", "to": "mix5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 3 time(s)", "to": "pol4", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "meme1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "cult5", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "mix4", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "mix3", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "pol1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 2 time(s)", "to": "sec4", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 24 time(s)", "to": "eco2", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "cult3", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 13 time(s)", "to": "sec2", "width": 1.4968152866242037}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 26 time(s)", "to": "meme4", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sec5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 27 time(s)", "to": "eco1", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "cult2", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 4 time(s)", "to": "meme1", "width": 1.1528662420382165}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "pol2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 3 time(s)", "to": "sports5", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "meme5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 23 time(s)", "to": "pol5", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "eco1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 25 time(s)", "to": "sci4", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 2 time(s)", "to": "eco5", "width": 1.0764331210191083}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 26 time(s)", "to": "sci5", "width": 1.9936305732484076}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 24 time(s)", "to": "meme1", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "sports2", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 3 time(s)", "to": "sci3", "width": 1.1146496815286624}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 24 time(s)", "to": "sec3", "width": 1.9171974522292994}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 25 time(s)", "to": "sports1", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 22 time(s)", "to": "cult1", "width": 1.8407643312101911}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 27 time(s)", "to": "sports4", "width": 2.031847133757962}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 25 time(s)", "to": "pol5", "width": 1.9554140127388535}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "eco2", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 11 time(s)", "to": "mix5", "width": 1.4203821656050954}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 23 time(s)", "to": "cult1", "width": 1.8789808917197452}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 10 time(s)", "to": "sec1", "width": 1.3821656050955413}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 10 time(s)", "to": "mix4", "width": 1.3821656050955413}]);

                  nodeColors = {};
                  allNodes = nodes.get({ returnType: "Object" });
                  for (nodeId in allNodes) {
                    nodeColors[nodeId] = allNodes[nodeId].color;
                  }
                  allEdges = edges.get({ returnType: "Object" });
                  // adding nodes and edges to the graph
                  data = {nodes: nodes, edges: edges};

                  var options = {"physics": {"enabled": true, "stabilization": {"enabled": true, "iterations": 1400, "fit": true}}};

                  


                  

                  network = new vis.Network(container, data, options);

                  

                  

                  


                  

                  return network;

              }
              drawGraph();
        </script>
    </body>
</html>
```

<details>
<summary>📁 Final Project Structure</summary>

```
📁 diagrams/
    📄 agent_runtime_state_machine.uml
    📄 class_diagram.uml
    📄 component_diagram.uml
    📄 sequence_diagram.uml
📁 requirements/
📁 src/
    📁 gsocialsim/
        📁 agents/
            📄 __init__.py
            📄 agent.py
            📄 attention_system.py
            📄 belief_state.py
            📄 belief_update_engine.py
            📄 budget_state.py
            📄 emotion_state.py
            📄 identity_state.py
            📄 impression.py
            📄 reward_weights.py
        📁 analytics/
            📄 __init__.py
            📄 analytics.py
            📄 attribution.py
        📁 evolution/
            📄 __init__.py
            📄 evolutionary_system.py
        📁 kernel/
            📄 __init__.py
            📄 event_scheduler.py
            📄 events.py
            📄 sim_clock.py
            📄 stimulus_ingestion.py
            📄 world_context.py
            📄 world_kernel.py
            📄 world_kernel_step.py
        📁 networks/
            📄 __init__.py
            📄 network_layer.py
        📁 physical/
            📄 __init__.py
            📄 physical_world.py
        📁 policy/
            📄 __init__.py
            📄 action_policy.py
            📄 bandit_learner.py
        📁 social/
            📄 __init__.py
            📄 global_social_reality.py
            📄 relationship_vector.py
        📁 stimuli/
            📄 __init__.py
            📄 content_item.py
            📄 data_source.py
            📄 interaction.py
            📄 stimulus.py
        📁 visualization/
            📄 __init__.py
            📄 exporter.py
            📄 exporter_agents_only.py
            📄 exporter_agents_platform.py
            📄 exporter_bipartite.py
            📄 exporter_full.py
            📄 exporter_threshold.py
        📄 __init__.py
        📄 types.py
    📁 gsocialsim.egg-info/
        📄 dependency_links.txt
        📄 PKG-INFO
        📄 SOURCES.txt
        📄 top_level.txt
📁 tests/
    📄 test_attention_system.py
    📄 test_belief_model.py
    📄 test_daily_consolidation_and_consumption.py
    📄 test_event_system.py
    📄 test_learning_policy.py
    📄 test_phase1.py
    📄 test_phase10.py
    📄 test_phase2.py
    📄 test_phase3.py
    📄 test_phase4.py
    📄 test_phase5.py
    📄 test_phase6.py
    📄 test_phase7.py
    📄 test_phase8.py
📄 agents_only.html
📄 bipartite.html
📄 fix_event_phase_init.patch
📄 gsocialsim-logo.png
📄 influence_graph.html
📄 LICENSE
📄 phase_patch.py
📄 platform.html
📄 PRD.md
📄 project.md
📄 pyproject.toml
📄 README.md
📄 requirements.txt
📄 run_and_visualize.py
📄 run_stimulus_sim.py
📄 stimuli.csv
📄 threshold.html
```

</details>
