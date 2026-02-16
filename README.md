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

## Overview

**gsocialsim** is a research framework for modeling **belief formation, influence propagation, attention dynamics, and evolutionary selection** in synthetic social ecosystems.

It is not a diffusion toy or a static agent-based model.

It is an **event-driven, multi-layer influence environment** designed to make belief change:

- rare
- attributable
- causal
- reproducible

---

## What This Simulator Is For

gsocialsim is built to answer questions like:

- Why do some beliefs spread while others die?
- How does influence *actually* propagate across networks and physical space?
- What role does attention scarcity play in persuasion?
- How do online and offline interactions interact?
- Which personalities survive under platform incentives?
- Who caused a belief crossing and through what pathway?

The output is not just adoption curves, but **causal influence graphs**.

---

## Core Architecture

### Event-Driven World Kernel

The simulation is driven by a centralized **WorldKernel**:

- discrete simulation clock
- deterministic phase ordering
- explicit event scheduling
- reproducible runs under fixed seeds

All social, physical, and cognitive processes are coordinated through the kernel.

---

### Persistent Agents

Agents are long-lived and stateful:

- belief vectors per topic
- per-tick time budget (minutes), no banking
- emotional and identity state
- political identity (lean + partisanship strength)
- personality-weighted reward preferences
- adaptive policies learned over time
 - dynamic trust on network edges

Agents optimize locally based on personality and experience, not global truth.

---

### Attention & Intake Modes

Agents consume information via explicit **intake modes**:

- **scroll** (passive feed exposure)
- **seek** (active information search)
- **physical** (in-person interaction)
- **deep_focus** (rare, expensive processing)

Attention is finite. Every exposure is a tradeoff.

Time is a hard constraint: perceiving and acting both consume minutes in the same tick.

---

### Stimuli & Content Pipeline

External data enters the world as **Stimuli**:

- typed media (news, post, meme, video, longform, forum)
- source, creator, outlet, or community identifiers
- optional topic hints
- provenance tracking

Stimuli are transformed into internal content items and logged as exposure events.

Optional neuromarketing fields:
- `primal_triggers` (e.g., `personal,contrast,tangible,memorable,visual,emotion`)
- `primal_intensity` in [0,1]

These are abstracted as a bounded persuasion multiplier.

---

### Belief Update & Crossing Detection

Beliefs evolve incrementally through exposure and interaction.

When a belief crosses a configured threshold:

- the event is detected
- prior and post states are recorded
- attribution is triggered
- causal credit is assigned

Belief change is not assumed. It must be *earned*.

---

## Politics & Identity

The model includes a lightweight political identity system:

- each agent has a `political_lean` in [-1, 1] and `partisanship` in [0, 1]
- topics can be marked with **political salience**
- politically salient topics can raise **identity threat** and increase resistance
- non-hostile disagreement can still reduce confidence and enable gradual belief change

Default political topic seeds live in `gsocialsim.social.politics.DEFAULT_POLITICAL_TOPICS`
and are used by `generate_agent(...)` to initialize left/right-leaning stances.

---

### Attribution Engine

Attribution reconstructs influence causality:

- configurable temporal windows
- exposure histories across channels
- tie strength and intake mode weighting
- multi-source credit assignment

The result is **who influenced whom, how, and when**.

---

### Dual Influence Layers

#### Online Layer
- directed social graph
- weighted relationships
- broadcast and direct interactions
- repeated exposure effects

#### Physical Layer
- places, schedules, and co-presence
- high-impact interactions
- small-world shortcuts
- amplified persuasion

Physical influence is explicitly modeled, not approximated.

---

## Literature Alignment (Selected)

We align mechanics to established findings. A short mapping and citations live in `docs/literature.md`.

Selected references:
- Kunda (1990), *Psychological Bulletin*
- Nickerson (1998), *Review of General Psychology*
- Hovland & Weiss (1951), *Public Opinion Quarterly*
- McPherson et al. (2001), *Annual Review of Sociology*
- Pettigrew & Tropp (2006), *Journal of Personality and Social Psychology*
- Iyengar et al. (2012), *Public Opinion Quarterly*
- Wood & Porter (2019), *Political Behavior*
- Renvoise & Morin (2007), *Neuromarketing*
- Morin & Renvoise (2018), *The Persuasion Code*

---

### Learning & Adaptation

Agents use contextual bandits to learn:

- which actions to take
- which channels to use
- how to allocate scarce attention

Reward is personality-weighted (status, affiliation, certainty, novelty, reinforcement).

---

### Evolutionary Dynamics

The population evolves:

- low-fitness agents are removed
- high-fitness agents reproduce
- offspring inherit traits with mutation
- diversity is preserved

You get belief **ecosystems**, not snapshots.

---

## Visualization

Multiple HTML exporters are included:

- **agents-only** (agent states, no platforms)
- **platform view** (agent-platform interactions)
- **bipartite** (agents ↔ content)
- **threshold view** (belief crossings only)
- **full graph** (everything)

Nodes represent agents or content.
Edges represent realized influence, not just potential.

---

## Running the Simulator

### Install

```bash
git clone https://github.com/ginkorea/gsocialsim.git
cd gsocialsim

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

### Run a Demo

```bash
python3 run_and_visualize.py
```

Outputs one or more HTML files (depending on exporter selection), e.g.:

```text
influence_graph.html
agents_only.html
bipartite.html
platform.html
threshold.html
```

Open them in a browser.

---

## Research Metrics

The system is designed to measure:

* belief conversion pathways
* influence efficiency
* influence concentration
* cascade shapes
* polarization drift
* personality survival rates
* platform selection effects
* physical vs online influence ratios

---

## Research Framing

gsocialsim is an **evolutionary attention-and-influence environment**:

* platforms define incentives
* personalities define reward
* learning defines adaptation
* evolution defines selection

The guiding question:

> Under which social and technical conditions do certain beliefs and behaviors survive, spread, and thrive, and what are the measurable mechanisms of influence that drive those outcomes?

---

## Project Structure

```
src/gsocialsim/
├── agents/          # agent state, beliefs, attention, personality
├── analytics/       # metrics and attribution
├── evolution/       # evolutionary system
├── kernel/          # event scheduling and world coordination
├── networks/        # social graph layers
├── physical/        # places, schedules, physical interaction
├── policy/          # learning and action selection
├── social/          # global social reality model
├── stimuli/         # external stimuli and content ingestion
├── visualization/   # HTML exporters
└── types.py
```

---

## Design Philosophy

> All models are wrong.
> Some monkeys are influential.

Minimal magic. Explicit mechanics. Measurable outcomes.

---

## License

MIT License. See `LICENSE`.

---

## Disclaimer

This framework models influence dynamics for research and defensive analysis.
It does not endorse manipulation campaigns.
Use responsibly.
