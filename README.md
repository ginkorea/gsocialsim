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
- multi-dimensional political identity (economic/social/security/environment/culture)
- group identities (immutable demographics + mutable affiliations)
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

Beliefs evolve through an **11-step physics-inspired pipeline**:

1. **Trust gate** (superlinear): low trust yields near-zero influence
2. **Bounded confidence**: reject signals too far from current stance
3. **Habituation**: diminishing returns from repeated exposure
4. **Base influence**: trust x credibility x primal activation x proximity
5. **Identity defense**: backfire effect, confirmation bias, openness gating
6. **Evidence accumulation**: multi-hit gate -- single exposures rarely move beliefs
7. **Inertia and momentum**: persistent velocity with decay
8. **Critical velocity**: nonlinear gain once momentum builds (tipping point)
9. **Rebound force**: damped spring pulling toward core values
10. **Stance update**: combine momentum, learning rate, and rebound
11. **Confidence update**: confirming signals increase, opposing decrease

When a belief crosses a configured threshold, the event is detected, prior and post states are recorded, attribution is triggered, and causal credit is assigned.

Belief change is not assumed. It must be *earned*.

See **[INFLUENCE_MATH.md](INFLUENCE_MATH.md)** for complete formal notation, diagrams, and parameter tables.

---

## Dimensional Identity & Demographics

Agents carry rich demographic profiles (age, race/ethnicity, religion, education, income, gender, geography, political ideology) that drive **homophily-based influence weighting**.

All identity categories are embedded onto continuous coordinate spaces (1-5D per category) and similarity is computed through a unified codepath:

```
    similarity(a, b) = weighted_sum_d[ exp( -dist(a_d, b_d) / decay_d ) ]
```

Key design features:

- **Religion**: 2D (tradition family x devotional intensity). Protestant and Catholic are close; Catholic and Hindu are distant. Devotion partially compensates across traditions but does not override tradition distance.
- **Race/Ethnicity**: 2D, fully country-configurable. US uses White/Black/Hispanic/Asian boundaries. India maps to caste/community (upper_caste, OBC, dalit, tribal). Brazil uses the color spectrum (branco/pardo/preto).
- **Political Ideology**: 5D (economic, social, libertarian/authoritarian, cosmopolitan/nationalist, secular/religious governance). The strongest similarity factor.
- **Geography, Education, Gender, Income, Age**: 1D sliders, same exponential decay codepath.
- **Language**: 2D, optional. Active in multilingual countries (India).
- **Weights are country-configurable** and auto-normalize at runtime.

Factory defaults for USA, India, Brazil, UK, and France.

See **[INFLUENCE_MATH.md](INFLUENCE_MATH.md)** for the full mathematical specification with coordinate maps, distance spot-checks, and parameter tables.

---

## Politics & Identity

The model includes a multi-dimensional political identity system:

- **5-axis political identity**: economic left-right, social progressive-traditional, libertarian-authoritarian, cosmopolitan-nationalist, secular-religious governance
- **Scalar fallback**: single `political_ideology` in [-1, +1] is expanded to 5D via empirical correlations
- topics can be marked with **political salience**
- politically salient topics can raise **identity threat** and increase resistance
- non-hostile disagreement can still reduce confidence and enable gradual belief change

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

## Geo Data Pipeline

For global placement using real population weights, download WorldPop tiles and aggregate to H3.

Download WorldPop tiles (example 8x8 tiling). If you see HTTP 500 errors, reduce the tile size:

```bash
python scripts/geo_download_worldpop.py --year 2020 --bbox -60,-180,85,180 --tiles 8 --out data/geo/worldpop.tif
# Safer fallback for ArcGIS limits:
python scripts/geo_download_worldpop.py --year 2020 --bbox -60,-180,85,180 --tiles 8 --size 2048,2048 --out data/geo/worldpop.tif
```

Aggregate to H3:

```bash
python scripts/build_h3_population.py --tif-dir data/geo --res 6 --out data/geo/h3_population.csv
# If you see ocean leakage or huge weights, clamp pixel values:
python scripts/build_h3_population.py --tif-dir data/geo --res 6 --min-pop 1 --max-pop 10000000 --out data/geo/h3_population.csv
```

Then use `--geo-pop data/geo/h3_population.csv` with visualizers.

## Literature Alignment (Selected)

We align mechanics to established findings. A short mapping and citations live in `docs/literature.md`. The full mathematical specification with formal notation lives in **[INFLUENCE_MATH.md](INFLUENCE_MATH.md)**.

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

## Running the Simulator (C++ Primary)

### Install

```bash
git clone https://github.com/ginkorea/gsocialsim.git
cd gsocialsim

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

### Build (C++)

```bash
cmake -S cpp -B cpp/build
cmake --build cpp/build
```

### Run (C++)

```bash
./cpp/build/gsocialsim_cpp --stimuli stimuli.csv --ticks 288 --agents 1000 \
  --analytics --analytics-mode detailed --export-state
```

Outputs:

```text
reports/analytics.csv
reports/state.json
```

### Render Visuals (Python)

```bash
python3 cpp/render_from_cpp.py --viz full --out reports/influence_graph.html
```

Other visualizations:

```text
reports/influence_graph.html
reports/agents_only.html
reports/bipartite.html
reports/platform.html
reports/threshold.html
```

Open them in a browser.

### Legacy Python Demo

The original Python simulator is still available for reference:

```bash
python3 run_and_visualize.py
```

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
cpp/                        # C++ engine (primary)
├── include/
│   ├── agent.h             # Agent state, demographics, psychographics
│   ├── belief_dynamics.h   # 11-step influence dynamics engine
│   ├── identity_space.h    # Dimensional identity similarity system
│   ├── country.h           # Multi-country infrastructure
│   ├── population_layer.h  # Hex-grid population dynamics
│   ├── kernel.h            # World kernel and event scheduling
│   └── ...
├── src/
│   ├── identity_space.cpp  # Country factory defaults (USA/IND/BRA/GBR/FRA)
│   ├── belief_dynamics.cpp # Physics-inspired belief update pipeline
│   ├── agent_demographics.cpp  # Similarity and influence weight
│   ├── population_layer.cpp    # Population-level belief dynamics
│   └── ...
└── test/
    └── test_agent_demographics.cpp  # 14 tests for dimensional system

python/src/gsocialsim/      # Python visualization bridge
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

docs/
INFLUENCE_MATH.md            # Full mathematical specification
GLOBAL_ARCHITECTURE.md       # Multi-country simulation design
PRD.md                       # Product requirements document
ROADMAP.md                   # Implementation roadmap
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
