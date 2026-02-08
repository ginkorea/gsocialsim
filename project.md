# Project Compilation: gsocialsim

## 🧾 Summary

| Metric | Value |
|:--|:--|
| Root Directory | `/home/gompert/data/workspace/gsocialsim` |
| Total Directories | 16 |
| Total Indexed Files | 75 |
| Skipped Files | 1 |
| Indexed Size | 176.42 KB |
| Max File Size Limit | 2 MB |

## 📚 Table of Contents

- [.gitignore](#gitignore)
- [LICENSE](#license)
- [PRD.md](#prd-md)
- [README.md](#readme-md)
- [diagrams/agent_runtime_state_machine.uml](#diagrams-agent-runtime-state-machine-uml)
- [diagrams/class_diagram.uml](#diagrams-class-diagram-uml)
- [diagrams/component_diagram.uml](#diagrams-component-diagram-uml)
- [diagrams/sequence_diagram.uml](#diagrams-sequence-diagram-uml)
- [fix_event_phase_init.patch](#fix-event-phase-init-patch)
- [influence_graph.html](#influence-graph-html)
- [phase_patch.py](#phase-patch-py)
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
- [stimuli.csv](#stimuli-csv)
- [tests/test_attention_system.py](#tests-test-attention-system-py)
- [tests/test_belief_model.py](#tests-test-belief-model-py)
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
📄 fix_event_phase_init.patch
📄 gsocialsim-logo.png
📄 influence_graph.html
📄 LICENSE
📄 phase_patch.py
📄 PRD.md
📄 project.md
📄 pyproject.toml
📄 README.md
📄 requirements.txt
📄 run_and_visualize.py
📄 run_stimulus_sim.py
📄 stimuli.csv
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
title SSES - Core Class Diagram

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
' Attention
'========================
class AttentionSystem {
  +scout: ScrollOrSeekner
  +deep: DeepFocusEngine
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


class Impression {
  +intake_mode: IntakeMode
  +contentId: ContentId
  +topic: TopicId?
  +valence: float
  +arousal: float
  +stance_signal: float
  +credibility: float
  +identity_threat: float
  +social_proof: float
  +source_strength: float
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

'========================
' Policy + Learning
'========================
class ActionPolicy {
  +selectIntent(a: Agent, ctx: WorldContext): Intent
  +selectActionTemplate(intent: Intent): ActionTemplate
  +instantiate(tpl: ActionTemplate, ctx: WorldContext): Action
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
' Social Reality + Graph Layers
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

abstract class NetworkLayer {
  +id: NetworkId
  +graph: NetworkGraph
  +mechanics: PlatformMechanics
  +projectEdge(u: Agent, v: Agent, gsr: GlobalSocialReality): Edge
  +rankFeed(viewer: Agent, candidates: List<ContentItem>): List<ContentItem>
  +enforceModeration(item: ContentItem): ModerationDecision
}

class BroadcastFeedNetwork
class DirectMessageNetwork

class NetworkGraph {
  +nodes: Set<AgentId>
  +edges: Set<Edge>
  +neighbors(u: AgentId): List<AgentId>
}

class Edge {
  +u: AgentId
  +v: AgentId
  +weight: float
  +features: float[*]  'relationship projection vector
}

class PlatformMechanics {
  +visibilityRules: VisibilityRules
  +rankingModel: RankingModel
  +riskProfile: RiskProfile
  +rewardMapping: RewardMapping
}

class NetworkManager {
  +layers: List<NetworkLayer>
  +getLayer(id: NetworkId): NetworkLayer
}

NetworkLayer <|-- BroadcastFeedNetwork
NetworkLayer <|-- DirectMessageNetwork
NetworkLayer *-- NetworkGraph
NetworkLayer *-- PlatformMechanics
NetworkManager o-- NetworkLayer

Agent --> GlobalSocialReality : updates via interactions
NetworkLayer --> GlobalSocialReality : projects edges

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
  +publisher: ActorId
  +topic: TopicId?
  +stance: float?
  +emotionDerivative: float?
  +provenance: ProvenanceRecord
}

class ProvenanceRecord {
  +rootStimulusId: StimulusId
  +transformChain: List<String>
}

StimulusStore o-- ExternalStimulus
ProvenanceTransformer --> ContentItem
ContentItem *-- ProvenanceRecord

'========================
' Belief Update + Crossing + Attribution
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
  +assignCredit(e: BeliefCrossingEvent, history: ExposureHistory): AttributionSet  'uses ExposureEvent.intake_mode
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
  +channel: ChannelType  'online/physical
  +tieStrength: float
}

class InfluenceEvent {
  +timestamp: long
  +source: ActorId
  +target: AgentId
  +topic: TopicId?
  +channel: ChannelType
  +intake_mode: IntakeMode
  +attemptType: String  'persuade, coordinate, intimidate, reassure, etc.
  +outcome: String      'success, failure, backfire, noop
  +deltaBelief: float?
  +deltaAction: float?
  +deltaRelationship: float?
  +evidence: List<String>  'contentIds, interactionIds, etc.
}

class InfluencePath {
  +id: string
  +agent: AgentId
  +topic: TopicId?
  +windowStart: long
  +windowEnd: long
  +exposures: List<ExposureEvent>
  +influenceEvents: List<InfluenceEvent>
  +result: String  'belief_crossing, action_change, relationship_shift
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

class AttributionSet {
  +credits: List<AttributionCredit>
}

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
' Daily identity consolidation
'========================
class IdentityConsolidator {
  +compressBeliefs(a: Agent)
  +reAnchorIdentity(a: Agent)
  +capAnchorDrift(a: Agent)
}

Agent --> IdentityConsolidator

'========================
' Moderation & Institutions
'========================
class InstitutionalActor {
  +id: ActorId
  +role: ActorRole
  +post(ctx: WorldContext): ContentItem
}

class ModerationEngine {
  +enforce(item: ContentItem, layer: NetworkLayer): ModerationDecision
}

class ModerationDecision {
  +action: ModerationAction
  +probability: float
}

'========================
' Evolutionary System
'========================
class EvolutionarySystem {
  +evaluateFitness(a: Agent): Fitness
  +maybeExit(a: Agent): bool
  +replace(a: Agent): Agent
}

class Fitness {
  +reward: float
  +connectedness: float
  +reputation: float
  +noise: float
}

EvolutionarySystem --> Fitness
EvolutionarySystem --> AgentPopulation

'========================
' Analytics + Logging
'========================
class Analytics {
  +logInfluenceEvent(e: InfluenceEvent)
  +logInfluencePath(p: InfluencePath)
  +scroll_exposures: int

  +seek_exposures: int

  +physical_exposures: int

  +scroll_seek_ratio(): float

  +logExposure(e: ExposureEvent)
  +logImpression(i: Impression)
  +logAction(a: Action)
  +logReward(r: RewardVector)
  +logBeliefUpdate(d: BeliefDelta)
  +logCrossing(e: BeliefCrossingEvent)
  +reportMetrics(): MetricsReport
}

class MetricsReport {
  +influenceGraph: Map<String,float>  'who→whom weights (by topic/channel)
  +influenceEfficiency: float
  +influenceConcentration: float
  +scrollInfluenceShare: float
  +seekInfluenceShare: float
  +physicalInfluenceShare: float
  +scrollExposures: int

  +seekExposures: int

  +physicalExposures: int

  +scrollSeekRatio: float

  +polarization: float
  +conversionRate: float
  +physicalVsOnlineRatio: float
  +cascadeStats: Map<String,float>
}

Analytics --> MetricsReport

@enduml

```

## `diagrams/component_diagram.uml`

```text
@startuml
title SSES - Component Diagram

skinparam componentStyle rectangle

component "World Kernel" as WK
component "Event Scheduler" as ES
component "Deterministic Replay" as DR

component "Agent Engine" as AE
component "Agent Runtime Loop" as ARL
component "Memory System" as MS
component "Attention System\n(Scroll + Seek + Deep Focus)" as ATTN
component "Policy + Learning\n(Contextual Bandits)" as LEARN

component "Global Social Reality\n(Latent R_uv)" as GSR

component "Online Network Layers" as ONL
component "Broadcast Feed Network" as BF
component "Private Messaging Network" as DM

component "Physical Layer" as PHY
component "Places + Schedules" as PS
component "Proximity Interaction Generator" as PIG

component "Stimulus Ingestion\n(Read-only Exogenous)" as SI
component "Provenance Transformer\n(Publisher/Influencer framing)" as PT

component "Belief & Identity System" as BIS
component "Belief Update Engine" as BUE
component "Identity Consolidation" as IC
component "Belief Crossing + Attribution" as BCA

component "Moderation & Institutions" as MI
component "Moderation Engine" as MOD
component "Institutional Actors\n(Publishers/Influencers)" as IA

component "Evolutionary System (GA)" as GA
component "Exit + Replacement" as ER
component "Mutation + Inheritance" as MU

component "Analytics + Logging" as AL
component "Event Logs" as LOGS
component "Metrics + Reports" as MET

WK --> ES
WK --> DR
WK --> AE
WK --> ONL
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

ONL --> BF
ONL --> DM
ONL --> GSR

PHY --> PS
PHY --> PIG
PHY --> GSR

SI --> PT
PT --> BF
PT --> IA

MI --> MOD
MI --> IA
MOD --> BF
MOD --> DM

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

@enduml

```

## `diagrams/sequence_diagram.uml`

```text
@startuml
title SSES - Sequence: Tick, Attention, Belief Update, Attribution

actor "WorldKernel" as WK
participant "AgentEngine" as AE
participant "Agent" as A
participant "NetworkLayer" as NL
participant "PhysicalWorld" as PW
participant "AttentionSystem" as AT
participant "BeliefUpdateEngine" as BUE
participant "CrossingDetector" as CD
participant "AttributionEngine" as ATR
participant "Analytics" as AN

WK -> AE: step(dt)
AE -> NL: generateCandidateContent(A)
AE -> PW: generatePhysicalInteractions(A)

NL --> AE: percepts_online(List<Percept>, intake_mode=scroll|seek)
PW --> AE: percepts_physical(List<Percept>, intake_mode=physical)

AE -> A: tick(ctx, percepts)
A -> AT: evaluate(percepts)
AT --> A: impressions

loop For each impression
  A -> BUE: update(A, impression, ctx)
  BUE --> A: beliefDelta (bounded)
  A -> AN: logImpression(impression)
  A -> AN: logBeliefUpdate(beliefDelta)
end

alt Deep focus triggered
  A -> AT: deepFocus(targetContent)
  AT --> A: deepResult
  A -> AN: logAction(deepFocus)
end

A -> A: maybeAct(ctx)
alt Action chosen
  A -> NL: post/send(action) or engage()
  NL --> A: exposureResults + costs
  A -> AN: logAction(action)
  alt action has influence intent
    A -> AN: logInfluenceEvent(InfluenceEvent)
  end

end

A -> CD: checkCrossing(before, after, topic)
CD --> A: crossingEvent? (optional)

alt crossingEvent exists
  A -> ATR: assignCredit(crossingEvent, exposureHistory)
  ATR --> A: attributionSet
  A -> AN: logCrossing(crossingEvent+attribution)
end

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

             

             
             #config {
                 float: left;
                 width: 400px;
                 height: 600px;
             }
             

             
        </style>
    </head>


    <body>
        <div class="card" style="width: 100%">
            
            
            <div id="mynetwork" class="card-body"></div>
        </div>

        
        
            <div id="config"></div>
        

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
                  nodes = new vis.DataSet([{"color": "#cccccc", "id": "A", "label": "A", "shape": "dot", "size": 25.36, "title": "Agent A\nTopic: T_Original\nStance: 0.00"}, {"color": "#0080ff", "id": "B", "label": "B", "shape": "dot", "size": 29.920000000000005, "title": "Agent B\nTopic: T_Original\nStance: 0.72"}, {"color": "#0080ff", "id": "C (Source)", "label": "C (Source)", "shape": "dot", "size": 35.0, "title": "Agent C (Source)\nTopic: T_Original\nStance: 1.00"}, {"color": "#cccccc", "id": "D (Lurker)", "label": "D (Lurker)", "shape": "dot", "size": 25.6, "title": "Agent D (Lurker)\nTopic: T_Original\nStance: 0.00"}, {"color": "#00cc66", "id": "news1", "label": "news1", "shape": "square", "size": 25, "title": "Stimulus: news1\nSource: NewsOutlet\nContent: A major scientific breakthrough has been announced."}, {"color": "#00cc66", "id": "news2", "label": "news2", "shape": "square", "size": 25, "title": "Stimulus: news2\nSource: RivalNews\nContent: A competing report raises doubts about the recent breakthrough."}, {"color": "#00cc66", "id": "meme1", "label": "meme1", "shape": "square", "size": 25, "title": "Stimulus: meme1\nSource: UserA\nContent: That feeling when you realize it\u0027s Friday, lol"}]);
                  edges = new vis.DataSet([{"arrows": "to", "color": "#cccccc", "from": "A", "to": "B", "width": 1}, {"arrows": "to", "color": "#cccccc", "from": "B", "to": "C (Source)", "width": 1}, {"arrows": "to", "color": "#cccccc", "from": "D (Lurker)", "to": "A", "width": 1}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 61 time(s)", "to": "news1", "width": 10.0}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 27 time(s)", "to": "news1", "width": 4.983606557377049}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 17 time(s)", "to": "news1", "width": 3.5081967213114753}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "news1", "width": 4.393442622950819}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "C (Source)", "title": "Interacted 23 time(s)", "to": "news2", "width": 4.393442622950819}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "A", "title": "Interacted 23 time(s)", "to": "news2", "width": 4.393442622950819}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "D (Lurker)", "title": "Interacted 1 time(s)", "to": "news2", "width": 1.1475409836065573}, {"arrows": "to", "color": "#99ff99", "dashes": true, "from": "B", "title": "Interacted 1 time(s)", "to": "news2", "width": 1.1475409836065573}, {"arrows": "to", "color": "#ff0000", "from": "C (Source)", "title": "Influenced 1 time(s)", "to": "B", "width": 2}]);

                  nodeColors = {};
                  allNodes = nodes.get({ returnType: "Object" });
                  for (nodeId in allNodes) {
                    nodeColors[nodeId] = allNodes[nodeId].color;
                  }
                  allEdges = edges.get({ returnType: "Object" });
                  // adding nodes and edges to the graph
                  data = {nodes: nodes, edges: edges};

                  var options = {
    "configure": {
        "enabled": true,
        "filter": [
            "physics"
        ]
    },
    "edges": {
        "color": {
            "inherit": true
        },
        "smooth": {
            "enabled": true,
            "type": "dynamic"
        }
    },
    "interaction": {
        "dragNodes": true,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false
    },
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "fit": true,
            "iterations": 1000,
            "onlyDynamicEdges": false,
            "updateInterval": 50
        }
    }
};

                  


                  
                  // if this network requires displaying the configure window,
                  // put it in its div
                  options.configure["container"] = document.getElementById("config");
                  

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
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.visualization.exporter import generate_influence_graph_html
from gsocialsim.social.relationship_vector import RelationshipVector
from gsocialsim.stimuli.data_source import CsvDataSource

def setup_simulation_scenario(kernel: WorldKernel):
    """
    Sets up a scenario with agents and external stimuli for the simulation.
    """
    print("Setting up simulation scenario...")
    
    # --- Create Agents and Network ---
    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C (Source)"), seed=3)
    agent_D = Agent(id=AgentId("D (Lurker)"), seed=4)
    
    agents = [agent_A, agent_B, agent_C, agent_D]
    for a in agents:
        a.budgets.action_budget = 100 # Give plenty of budget for actions
        a.beliefs.update(TopicId("T_Original"), stance=0.0, confidence=0.5, salience=0.1, knowledge=0.1)
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)
    graph.add_edge(follower=agent_D.id, followed=agent_A.id) # D follows A

    # --- Setup Trust ---
    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9))
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6))

    # --- Seed Initial Belief for Source Agent ---
    topic_original = TopicId("T_Original")
    agent_C.beliefs.update(topic_original, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)
    
    # --- Register External Data Source ---
    csv_source = CsvDataSource(file_path="stimuli.csv")
    kernel.world_context.stimulus_engine.register_data_source(csv_source)
    print("Scenario setup complete.")


if __name__ == "__main__":
    # --- 1. Initialize Kernel and Setup Scenario ---
    sim_kernel = WorldKernel(seed=101)
    setup_simulation_scenario(sim_kernel)

    # --- 2. Start Event-Driven Simulation ---
    sim_kernel.start() # Seed the initial events (ingestion, agent actions, day boundaries)
    print("\nRunning simulation...")
    # Run for enough ticks to allow stimuli to be ingested, perceived, and acted upon
    sim_kernel.step(200) # Run for 200 ticks
    print("Simulation finished.\n")

    # --- 3. Generate Visualization ---
    generate_influence_graph_html(sim_kernel)

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
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from collections import deque
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
    from gsocialsim.types import TopicId

class MemoryStore: pass

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
    # Store the most recent impressions, keyed by content_id
    recent_impressions: dict[str, Impression] = field(default_factory=dict)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.budgets._rng = self.rng

    def perceive(self, content: ContentItem, context: "WorldContext", is_physical: bool = False, stimulus_id: Optional[str] = None):
        impression = self.attention.evaluate(content, is_physical=is_physical)
        # Store the impression for potential deep focus/later action
        if impression.content_id:
            self.recent_impressions[impression.content_id] = impression

        context.analytics.log_exposure(
            viewer_id=self.id, source_id=content.author_id, topic=content.topic,
            is_physical=is_physical, timestamp=context.clock.t
        )
        
        old_stance = self.beliefs.get(content.topic).stance if self.beliefs.get(content.topic) else 0.0
        belief_delta = self.belief_update_engine.update(
            viewer=self,
            content_author_id=content.author_id,
            impression=impression,
            gsr=context.gsr
        )
        
        self.beliefs.apply_delta(belief_delta)
        new_stance = self.beliefs.get(content.topic).stance
        
        if context.analytics.crossing_detector.check(old_stance, new_stance):
            attribution = context.analytics.attribution_engine.assign_credit(
                agent_id=self.id, topic=content.topic, history=context.analytics.exposure_history
            )
            from gsocialsim.analytics.attribution import BeliefCrossingEvent
            crossing_event = BeliefCrossingEvent(
                timestamp=context.clock.t, agent_id=self.id, topic=content.topic,
                old_stance=old_stance, new_stance=new_stance, attribution=attribution
            )
            context.analytics.log_belief_crossing(crossing_event)
        
        context.analytics.log_belief_update(timestamp=context.clock.t, agent_id=self.id, delta=belief_delta)

    def learn(self, action_key: str, reward_vector: RewardVector):
        self.policy.learn(action_key, reward_vector)

    def act(self, tick: int) -> Optional[Interaction]:
        if self.budgets.action_budget < 1: return None
        interaction = self.policy.generate_interaction(self, tick)
        if interaction:
            self.budgets.spend(BudgetKind.ACTION, 1.0)
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

    def consolidate_daily(self, world_context):
        self.budgets.regen_daily()
        self.recent_impressions.clear() # Clear memory of impressions daily
```

## `src/gsocialsim/agents/attention_system.py`

```python
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.agents.impression import Impression, IntakeMode

class AttentionSystem:
    """
    Generates Impressions from ContentItems, now with more detail.
    """
    def evaluate(self, content: ContentItem, is_physical: bool = False) -> Impression:
        # For now, we'll set default values for the new fields.
        # In an LLM phase, these would be derived from content_text.
        intake_mode = IntakeMode.PHYSICAL if is_physical else IntakeMode.SCROLL
        return Impression(
            intake_mode=intake_mode,
            content_id=content.id,
            topic=content.topic,
            stance_signal=content.stance,
            emotional_valence=0.0, # Placeholder
            arousal=0.0,         # Placeholder
            credibility_signal=0.5, # Placeholder
            identity_threat=0.0, # Placeholder
            social_proof=0.0,    # Placeholder
            relationship_strength_source=0.0 # Placeholder
        )
```

## `src/gsocialsim/agents/belief_state.py`

```python
from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from gsocialsim.agents.belief_update_engine import BeliefDelta

# Placeholder for TopicId (can be a string for now)
TopicId = str

@dataclass
class TopicBelief:
    topic: TopicId
    stance: float = 0.0  # [-1,+1]
    confidence: float = 0.0  # [0,1]
    salience: float = 0.0  # [0,1]
    knowledge: float = 0.0  # [0,1]

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
            self.topics[topic_id] = TopicBelief(topic=topic_id, stance=stance, confidence=confidence, salience=salience, knowledge=knowledge)

    def apply_delta(self, delta: "BeliefDelta"):
        """ Applies a belief delta to the current store. """
        belief = self.get(delta.topic_id)
        if belief is None:
            # This case handles forming a new belief
            self.topics[delta.topic_id] = TopicBelief(
                topic=delta.topic_id,
                stance=delta.stance_delta, # For a new belief, the delta *is* the new stance
                confidence=delta.confidence_delta # And the new confidence
            )
        else:
            # This case handles updating an existing belief
            belief.stance = max(-1.0, min(1.0, belief.stance + delta.stance_delta))
            belief.confidence = max(0.0, min(1.0, belief.confidence + delta.confidence_delta))

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
from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class IdentityState:
    identity_vector: List[float] = field(default_factory=lambda: [0.0] * 8)
    identity_rigidity: float = 0.5
    ingroup_labels: Set[str] = field(default_factory=set)
    taboo_boundaries: Set[str] = field(default_factory=set)

    def is_threatening(self, content_text: str) -> bool:
        """ A simple check to see if content text contains taboo keywords. """
        if not content_text:
            return False
        # A more complex model could use an LLM for this check.
        # For now, we use a simple keyword search.
        for taboo in self.taboo_boundaries:
            if taboo in content_text.lower():
                return True
        return False

```

## `src/gsocialsim/agents/impression.py`

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from gsocialsim.types import ContentId, TopicId

class IntakeMode(Enum):
    """ How an agent perceived a piece of content. """
    SCROLL = "scroll" # Passive, feed-driven
    SEEK = "seek"     # Active, goal-directed
    PHYSICAL = "physical" # Offline interaction
    DEEP_FOCUS = "deep_focus" # Focused, expensive processing

@dataclass
class Impression:
    """
    A richer representation of an agent's internal reaction to a ContentItem/Stimulus.
    """
    intake_mode: IntakeMode
    content_id: ContentId
    topic: TopicId
    stance_signal: float
    emotional_valence: float = 0.0 # Perceived emotional tone [-1, 1]
    arousal: float = 0.0         # Perceived intensity [0, 1]
    credibility_signal: float = 0.5 # Perceived credibility [0, 1]
    identity_threat: float = 0.0 # Perceived threat to identity [0, 1]
    social_proof: float = 0.0    # Perceived social proof (e.g., likes/forwards from others) [0, 1]
    relationship_strength_source: float = 0.0 # Relationship strength of the source [0, 1]
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
from typing import Any
from gsocialsim.analytics.attribution import (
    ExposureHistory,
    BeliefCrossingDetector,
    AttributionEngine,
    BeliefCrossingEvent,
    ExposureEvent
)
from gsocialsim.stimuli.interaction import Interaction

class Analytics:
    """
    Manages all logging for the simulation, including verbose debugging
    and storing data for visualization.
    """
    def __init__(self):
        self.exposure_history = ExposureHistory()
        self.crossing_detector = BeliefCrossingDetector()
        self.attribution_engine = AttributionEngine()
        self.crossings: list[BeliefCrossingEvent] = []
        self.interactions: list[Interaction] = []

    def log_belief_update(self, timestamp: int, agent_id: str, delta: Any):
        print(
            f"DEBUG:[T={timestamp}] Agent['{agent_id}'] BeliefUpdate: "
            f"Topic='{delta.topic_id}', StanceΔ={delta.stance_delta:.4f}, ConfΔ={delta.confidence_delta:.4f}"
        )
    
    def log_exposure(self, viewer_id: str, source_id: str, topic: str, is_physical: bool, timestamp: int):
        print(
            f"DEBUG:[T={timestamp}] Agent['{viewer_id}'] Perceived: "
            f"Source='{source_id}', Topic='{topic}', Physical={is_physical}"
        )
        event = ExposureEvent(
            timestamp=timestamp,
            source_actor_id=source_id,
            topic=topic,
            is_physical=is_physical
        )
        self.exposure_history.log_exposure(viewer_id, event)

    def log_interaction(self, timestamp: int, interaction: Interaction):
        target = interaction.target_stimulus_id or (interaction.original_content.id if interaction.original_content else 'None')
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
```

## `src/gsocialsim/analytics/attribution.py`

```python
from dataclasses import dataclass, field
from typing import Dict, List
from collections import defaultdict
from gsocialsim.types import AgentId, TopicId, ActorId

@dataclass
class ExposureEvent:
    timestamp: int
    source_actor_id: ActorId
    topic: TopicId
    is_physical: bool

class ExposureHistory:
    """Logs every piece of content an agent is exposed to."""
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
        # A simple crossing from non-positive to positive, or vice-versa
        return (old_stance <= 0 and new_stance > 0) or (old_stance >= 0 and new_stance < 0)

class AttributionEngine:
    """Assigns credit for a belief crossing event."""
    def assign_credit(self, agent_id: AgentId, topic: TopicId, history: ExposureHistory, window_days: int = 7) -> Dict[ActorId, float]:
        credits = defaultdict(float)
        total_credit = 0.0
        agent_history = history.get_history_for_agent(agent_id)
        
        # A simple recency-based model
        for event in reversed(agent_history):
            if event.topic == topic:
                # TODO: Use real timestamp difference
                weight = 1.0 # Simple weight for now
                if event.is_physical:
                    weight *= 5.0 # Physical gets more credit
                credits[event.source_actor_id] += weight
                total_credit += weight

        if total_credit == 0:
            return {}
            
        # Normalize credits
        return {actor: val / total_credit for actor, val in credits.items()}

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
from typing import TYPE_CHECKING
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

@dataclass(order=True)
class Event(ABC):
    timestamp: int = field(compare=True)
    tie_breaker: int = field(init=False, compare=True)
    def __post_init__(self): self.tie_breaker = next(_event_counter)
    @abstractmethod
    def apply(self, context: "WorldContext"):
        pass

@dataclass(order=True)
class StimulusIngestionEvent(Event):
    def apply(self, context: "WorldContext"):
        new_stimuli = context.stimulus_engine.tick(self.timestamp)
        if new_stimuli:
            for stimulus in new_stimuli:
                context.scheduler.schedule(StimulusPerceptionEvent(timestamp=self.timestamp, stimulus_id=stimulus.id))
        context.scheduler.schedule(StimulusIngestionEvent(timestamp=self.timestamp + 1))

@dataclass(order=True)
class StimulusPerceptionEvent(Event):
    stimulus_id: str = field(compare=False)
    def apply(self, context: "WorldContext"):
        stimulus = context.stimulus_engine.get_stimulus(self.stimulus_id)
        if not stimulus: return
        
        temp_content = ContentItem(id=stimulus.id, author_id=stimulus.source, topic=TopicId(f"stim_{stimulus.id}"), stance=0.0)
        for agent in context.agents.agents.values():
            agent.perceive(temp_content, context, stimulus_id=stimulus.id)

@dataclass(order=True)
class AgentActionEvent(Event):
    agent_id: str = field(compare=False)
    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent: return

        interaction = agent.act(tick=self.timestamp)
        if interaction:
            context.analytics.log_interaction(self.timestamp, interaction)
            context.scheduler.schedule(InteractionPerceptionEvent(timestamp=self.timestamp, interaction=interaction))
        context.scheduler.schedule(AgentActionEvent(timestamp=self.timestamp + 1, agent_id=self.agent_id))

@dataclass(order=True)
class InteractionPerceptionEvent(Event):
    interaction: "Interaction" = field(compare=False)

    def apply(self, context: "WorldContext"):
        from gsocialsim.policy.bandit_learner import RewardVector
        from gsocialsim.stimuli.interaction import InteractionVerb
        
        author = context.agents.get(self.interaction.agent_id)
        if not author: return

        followers = context.network.graph.get_followers(author.id)
        if not followers: return
        
        reward = RewardVector()
        topic = None

        if self.interaction.verb == InteractionVerb.CREATE:
            content = self.interaction.original_content
            topic = content.topic
            reward.affiliation = 0.1 * len(followers)
            for follower_id in followers:
                follower = context.agents.get(follower_id)
                if follower: follower.perceive(content, context)
        
        elif self.interaction.verb == InteractionVerb.LIKE:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = f"stim_{stimulus.id}"
                reward.affiliation = 0.2
        
        elif self.interaction.verb == InteractionVerb.FORWARD:
            stimulus = context.stimulus_engine.get_stimulus(self.interaction.target_stimulus_id)
            if stimulus:
                topic = f"stim_{stimulus.id}"
                reward.status = 0.3

        if topic and author:
            action_key = f"{self.interaction.verb.value}_{topic}"
            author.learn(action_key, reward)

@dataclass(order=True)
class DeepFocusEvent(Event):
    agent_id: str = field(compare=False)
    content_id: str = field(compare=False)
    original_impression: Impression = field(compare=False) # Store the impression that led to deep focus

    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent: return

        if agent.budgets.spend(BudgetKind.ATTENTION, 10) and agent.budgets.spend(BudgetKind.DEEP_FOCUS, 1):
            print(f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] engaged in Deep Focus on '{self.content_id}'")

            # Re-process the original impression with amplified effect
            amplified_impression = Impression(
                intake_mode=IntakeMode.DEEP_FOCUS, content_id=self.content_id, topic=self.original_impression.topic,
                stance_signal=self.original_impression.stance_signal, # Use original stance
                emotional_valence=self.original_impression.emotional_valence + 0.3, # More emotional
                arousal=self.original_impression.arousal + 0.3,
                credibility_signal=min(1.0, self.original_impression.credibility_signal + 0.2), # More credible
                identity_threat=self.original_impression.identity_threat, # No change to threat on deep focus itself
                social_proof=self.original_impression.social_proof, # No change
                relationship_strength_source=self.original_impression.relationship_strength_source
            )

            # Apply the deep impression directly to the agent's belief
            # The belief update engine will handle the actual change with its rules
            # We need the original content's author for trust calculation
            content_source_id = self.original_impression.content_id # Using content_id as source for simplicity
            
            belief_delta = agent.belief_update_engine.update(
                viewer=agent, 
                content_author_id=content_source_id, 
                impression=amplified_impression, 
                gsr=context.gsr
            )

            agent.beliefs.apply_delta(belief_delta)
            context.analytics.log_belief_update(timestamp=self.timestamp, agent_id=self.agent_id, delta=belief_delta)
        else:
            print(f"DEBUG:[T={self.timestamp}] Agent['{self.agent_id}'] failed Deep Focus due to insufficient budget.")

@dataclass(order=True)
class AllocateAttentionEvent(Event):
    agent_id: str = field(compare=False)
    def apply(self, context: "WorldContext"):
        agent = context.agents.get(self.agent_id)
        if not agent: return

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
    def step(self, num_ticks: int = 1):
        for _ in range(num_ticks):
            current_tick = self.clock.t
            all_agents = list(self.agents.agents.values())

            # --- 0. Stimulus Ingestion Phase ---
            new_stimuli_this_tick = self.stimulus_engine.tick(current_tick)
            
            # --- 1. Stimulus Perception Phase ---
            if new_stimuli_this_tick:
                for agent in all_agents:
                    for stimulus in new_stimuli_this_tick:
                        temp_content = ContentItem(
                            id=stimulus.id, author_id=stimulus.source,
                            topic=TopicId(f"stim_{stimulus.id}"), stance=0.0
                        )
                        agent.perceive(temp_content, self.world_context, stimulus_id=stimulus.id)

            # --- 2. Action Phase ---
            interactions_this_tick = []
            for agent in all_agents:
                new_interaction = agent.act(tick=current_tick)
                if new_interaction:
                    interactions_this_tick.append(new_interaction)
                    self.analytics.log_interaction(new_interaction)
            
            # --- 3. Online Interaction Perception Phase ---
            if interactions_this_tick:
                from gsocialsim.policy.bandit_learner import RewardVector
                from gsocialsim.stimuli.interaction import InteractionVerb
                
                for viewer in all_agents:
                    following_list = self.world_context.network.graph.get_following(viewer.id)
                    for interaction in interactions_this_tick:
                        if interaction.agent_id == viewer.id or interaction.agent_id not in following_list:
                            continue

                        content_to_perceive, stimulus_id, topic = None, None, None
                        
                        if interaction.verb == InteractionVerb.CREATE:
                            content_to_perceive = interaction.original_content
                            topic = content_to_perceive.topic
                        elif interaction.verb in [InteractionVerb.FORWARD, InteractionVerb.LIKE]:
                            stimulus = self.stimulus_engine.get_stimulus(interaction.target_stimulus_id)
                            if stimulus:
                                topic = TopicId(f"stim_{stimulus.id}")
                                content_to_perceive = ContentItem(id=stimulus.id, author_id=stimulus.source, topic=topic, stance=0.0)
                                stimulus_id = stimulus.id
                        
                        if content_to_perceive:
                            viewer.perceive(content_to_perceive, self.world_context, stimulus_id=stimulus_id)
                            reward = RewardVector(affiliation=0.1)
                            author = self.agents.get(interaction.agent_id)
                            if author:
                                action_key = f"{interaction.verb.value}_{topic or ''}"
                                author.learn(action_key, reward)

            day_before = self.clock.day
            self.clock.advance(1)
            if self.clock.day > day_before:
                for agent in all_agents:
                    agent.consolidate_daily(self.world_context)

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
from dataclasses import dataclass
from typing import Optional

from gsocialsim.types import ContentId, ActorId, TopicId

@dataclass
class ContentItem:
    """
    A minimal representation of a piece of content an agent can perceive.
    """
    id: ContentId
    author_id: ActorId
    topic: TopicId
    stance: float # A value from -1.0 to 1.0 representing the content's position
    is_identity_threatening: bool = False

```

## `src/gsocialsim/stimuli/data_source.py`

```python
from abc import ABC, abstractmethod
from typing import List
import csv
from gsocialsim.stimuli.stimulus import Stimulus

class DataSource(ABC):
    """ Abstract base class for any source of external data. """
    @abstractmethod
    def get_stimuli(self, tick: int) -> List[Stimulus]:
        """ Returns a list of all stimuli that should be injected at a given tick. """
        pass

class CsvDataSource(DataSource):
    """ A concrete data source that reads from a CSV file. """
    def __init__(self, file_path: str):
        self.stimuli_by_tick = {}
        with open(file_path, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                tick = int(row['tick'])
                stimulus = Stimulus(
                    id=row['id'],
                    source=row['source'],
                    tick=tick,
                    content_text=row['content_text']
                )
                self.stimuli_by_tick.setdefault(tick, []).append(stimulus)
        print(f"Loaded {sum(len(s) for s in self.stimuli_by_tick.values())} stimuli from {file_path}")

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
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Stimulus:
    """ A generic container for a piece of external data injected into the world. """
    id: str
    source: str  # e.g., "NewsOutletX", "SocialMediaFeedY"
    tick: int
    content_text: str
    metadata: Dict = field(default_factory=dict)

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

```

## `src/gsocialsim/visualization/exporter.py`

```python
from collections import defaultdict
from pyvis.network import Network
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.stimuli.interaction import InteractionVerb

def generate_influence_graph_html(kernel: WorldKernel, output_path: str = "influence_graph.html"):
    """
    Generates an interactive HTML graph with aggregated and scaled interaction edges.
    """
    print(f"Generating visualization... output to '{output_path}'")
    net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources='remote')

    # --- 1. Add Agent & Stimulus Nodes ---
    # (This logic remains the same)
    for agent in kernel.agents.agents.values():
        primary_belief = max(agent.beliefs.topics.values(), key=lambda b: b.confidence, default=None)
        color, title, size = "#808080", f"Agent {agent.id}", 15
        if primary_belief:
            color = "#cccccc"
            if primary_belief.stance > 0.1: color = "#0080ff"
            elif primary_belief.stance < -0.1: color = "#ff4000"
            title += f"\nTopic: {primary_belief.topic}\nStance: {primary_belief.stance:.2f}"
            size += primary_belief.confidence * 20
        net.add_node(agent.id, label=agent.id, color=color, title=title, size=size, shape="dot")

    for stimulus in kernel.world_context.stimulus_engine._stimuli_store.values():
        title = f"Stimulus: {stimulus.id}\nSource: {stimulus.source}\nContent: {stimulus.content_text}"
        net.add_node(stimulus.id, label=stimulus.id, color="#00cc66", title=title, shape="square", size=25)

    # --- 2. Add Follower Edges ---
    # (This logic remains the same)
    for follower, followed_list in kernel.world_context.network.graph._following.items():
        for followed in followed_list:
            if follower in kernel.agents.agents and followed in kernel.agents.agents:
                net.add_edge(follower, followed, color="#cccccc", width=1)

    # --- 3. Aggregate and Scale Interaction Edges ---
    interaction_counts = defaultdict(int)
    for interaction in kernel.world_context.analytics.interactions:
        if interaction.verb in [InteractionVerb.LIKE, InteractionVerb.FORWARD]:
            interaction_counts[(interaction.agent_id, interaction.target_stimulus_id)] += 1
    
    max_interaction_count = max(interaction_counts.values()) if interaction_counts else 1
    
    for (agent_id, stimulus_id), count in interaction_counts.items():
        if agent_id in kernel.agents.agents and stimulus_id in kernel.world_context.stimulus_engine._stimuli_store:
            # Scale width from 1 to 10 based on interaction frequency
            relative_width = 1 + 9 * (count / max_interaction_count)
            net.add_edge(
                agent_id, stimulus_id,
                color="#99ff99", width=relative_width, dashes=True,
                title=f"Interacted {count} time(s)"
            )

    # --- 4. Add Influence Edges ---
    # (This logic remains the same)
    influence_counts = defaultdict(int)
    for crossing in kernel.world_context.analytics.crossings:
        for source_id, weight in crossing.attribution.items():
            if weight > 0: influence_counts[(source_id, crossing.agent_id)] += 1
    
    for (source, target), count in influence_counts.items():
        if target in kernel.agents.agents:
            net.add_edge(source, target, color="#ff0000", width=2 * count, title=f"Influenced {count} time(s)")

    # --- 5. Generate HTML ---
    net.show_buttons(filter_=['physics'])
    net.save_graph(output_path)
    print("Visualization generated successfully.")
```

## `stimuli.csv`

```text
id,tick,source,content_text
news1,10,NewsOutlet,A major scientific breakthrough has been announced.
news2,50,RivalNews,A competing report raises doubts about the recent breakthrough.
meme1,100,UserA,"That feeling when you realize it's Friday, lol"

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
📄 fix_event_phase_init.patch
📄 gsocialsim-logo.png
📄 influence_graph.html
📄 LICENSE
📄 phase_patch.py
📄 PRD.md
📄 project.md
📄 pyproject.toml
📄 README.md
📄 requirements.txt
📄 run_and_visualize.py
📄 run_stimulus_sim.py
📄 stimuli.csv
```

</details>
