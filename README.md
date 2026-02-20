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

## Cross-Border Information Flow

Content crossing national borders passes through a **reach vs credibility decomposition**:

- **Reach multiplier** `[0, 1]`: cultural distance decay, language accessibility, amplification budget
- **Credibility multiplier** `[0, 1]`: geopolitical tension, state affiliation penalty, viewer institutional trust

```
effective_influence = base_influence * reach_mult * credibility_mult
```

State propaganda from hostile countries has low credibility in target nations but can boost reach through amplification budgets and inauthentic accounts. Low institutional trust makes viewers more susceptible.

**Media diet** for diaspora agents enforces **budget conservation** (all media shares sum to 1.0) with a **saturation curve** that gives diminishing returns, making diversified media consumption more information-efficient.

**International actors** (BBC, RT, UN, Greenpeace, etc.) have formal **capability profiles** bounding production capacity, targeting precision, and credibility per country. State media has higher targeting but lower credibility ceiling than independent international media.

See **[GLOBAL_ARCHITECTURE.md](GLOBAL_ARCHITECTURE.md)** for the full multi-country design and **[INFLUENCE_MATH.md](INFLUENCE_MATH.md)** for the formal math.

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

## Web GUI — Control Panel & Hypertuning Dashboard

gsocialsim includes a full-stack web GUI for interactive simulation control, live visualization, and automated hyperparameter optimization.

```
┌─────────────────────────┐     WebSocket      ┌──────────────────────┐
│   React + Vite (5173)   │ ◄──────────────── │   FastAPI (8000)     │
│   Tailwind + Recharts   │ ──── REST API ──► │   Uvicorn + Optuna   │
└─────────────────────────┘                    └──────────┬───────────┘
                                                          │ subprocess
                                                          ▼
                                               ┌──────────────────────┐
                                               │  gsocialsim_cpp      │
                                               │  --stream-json       │
                                               └──────────────────────┘
```

### Features

- **Dashboard** — overview of recent runs, active simulations, quick-launch
- **Configuration** — visual parameter editor with sliders for 30+ params across 7 groups (Belief Dynamics, Kernel, Feed Algorithm, Broadcast Feed, Media Diet, Simulation), raw JSON editor, save/load presets
- **Data Source Management** — browse, inspect, and upload CSV stimuli files; preview first N rows; file metadata (row count, tick range, columns); per-run data source selection; extensible for future GDELT integration
- **Live Simulation** — real-time WebSocket streaming from C++ process, animated tick counter with radial progress, belief distribution chart (stacked area histogram), live metrics panel (impressions, consumed, belief deltas, polarization), collapsible simulation log with timestamped entries
- **Hyperparameter Tuning** — Optuna-powered optimization (TPE, CMA-ES, Random), search space editor, 5 objective functions (polarization, crossing rate, consumption rate, mean belief shift, influence Gini), live progress charts, trial table with "apply best" button
- **Results Explorer** — multi-run comparison, parameter diff highlighting, CSV/JSON export

### Built-in Presets

| Preset | Key changes | Purpose |
|---|---|---|
| Default | All C++ defaults | Baseline |
| High Polarization | rebound_k=0.15, bounded_confidence_tau=0.5 | Study echo chambers |
| Echo Chamber | inertia_rho=0.95, mutual_weight=0.3, discovery_min=0 | Isolated groups |
| Open Discourse | inertia_rho=0.5, bounded_confidence_tau=3.0, discovery_max=10 | Free information flow |
| Rapid Dynamics | evidence_threshold=0.1, learning_rate_base=0.3 | Fast belief change |
| Large Scale | agents=5000, ticks=960 (10 days) | Scale test |

### Running the GUI

**Quick start** (single command):

```bash
./gsocialsim-gui.sh               # start backend + frontend
./gsocialsim-gui.sh --install     # install deps first, then start
./gsocialsim-gui.sh --build       # rebuild C++ binary, then start
./gsocialsim-gui.sh --port 9000   # custom backend port
```

**Manual start** (two terminals):

```bash
# Terminal 1: Backend
source .gsocialsim/bin/activate  # or your venv
pip install -r gui/backend/requirements.txt
uvicorn gui.backend.app.main:app --reload --port 8000

# Terminal 2: Frontend
cd gui/frontend
npm install
npm run dev   # → http://localhost:5173
```

Open http://localhost:5173 in a browser.

### C++ Streaming Flags

The C++ engine supports two new flags for GUI integration:

```bash
# Stream JSON Lines to stdout (one per tick)
./cpp/build/gsocialsim_cpp --stimuli data/stimuli.csv --ticks 96 --agents 100 --stream-json

# Load parameter overrides from a JSON config file
./cpp/build/gsocialsim_cpp --stimuli data/stimuli.csv --ticks 96 --agents 100 --config params.json
```

Each `--stream-json` line contains: `tick`, `total`, `impressions`, `consumed`, `belief_deltas`, `leans[]`.

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
│   ├── cross_border.h      # Reach vs credibility decomposition
│   ├── media_diet.h        # Budget conservation and saturation model
│   ├── actor_capabilities.h # International actor capability profiles
│   ├── scenario_harness.h  # Deterministic scenario test framework
│   ├── population_layer.h  # Hex-grid population dynamics
│   ├── kernel.h            # World kernel and event scheduling
│   ├── json.hpp            # nlohmann/json (single-header, MIT)
│   └── ...
├── src/
│   ├── main.cpp            # CLI entry: --stream-json, --config, --export-state
│   ├── identity_space.cpp  # Country factory defaults (USA/IND/BRA/GBR/FRA)
│   ├── belief_dynamics.cpp # Physics-inspired belief update pipeline
│   ├── agent_demographics.cpp  # Similarity and influence weight
│   ├── cross_border.cpp    # CrossBorderFactors, language accessibility
│   ├── media_diet.cpp      # MediaDiet factories, saturation curve
│   ├── actor_capabilities.cpp  # 7 actor capability profiles
│   ├── scenario_harness.cpp    # 16 scenario tests
│   ├── population_layer.cpp    # Population-level belief dynamics
│   └── ...
└── test/
    ├── test_agent_demographics.cpp  # 14 tests for dimensional system
    └── test_global_architecture.cpp # 16 tests for global architecture

gui/                        # Web GUI (React + FastAPI)
├── backend/
│   ├── requirements.txt    # FastAPI, Uvicorn, Optuna, etc.
│   └── app/
│       ├── main.py         # FastAPI app, CORS, lifespan, preset seeding
│       ├── config.py       # App settings (binary path, limits)
│       ├── api/            # REST + WebSocket endpoints
│       │   ├── runs.py     # POST/GET/DELETE /api/runs
│       │   ├── params.py   # GET /api/params/schema, presets CRUD
│       │   ├── tuning.py   # POST/GET /api/studies
│       │   ├── ws.py       # WebSocket /ws/run/{id}, /ws/study/{id}
│       │   └── datasources.py # GET/POST /api/datasources (browse, upload CSV)
│       ├── core/           # Business logic
│       │   ├── runner.py   # Async subprocess runner for C++ binary
│       │   ├── schemas.py  # Pydantic models, 30+ param definitions
│       │   ├── store.py    # SQLite storage (runs, presets, studies)
│       │   ├── parser.py   # Output parsing, metrics computation
│       │   └── datasources.py # CSV scanning, inspection, validation
│       └── tuning/         # Optuna hyperparameter optimization
│           ├── engine.py   # Study management, trial loop
│           ├── objectives.py # 5 objective functions
│           └── spaces.py   # Search space → trial.suggest_* mapping
└── frontend/
    ├── vite.config.ts      # Vite + Tailwind + API proxy
    └── src/
        ├── components/     # UI components
        │   ├── config/     # ParamSlider, ParamGroup, ConfigPanel, PresetBar
        │   ├── simulation/ # TickCounter, BeliefChart, MetricsPanel, LiveView
        │   ├── tuning/     # SearchSpaceEditor, OptProgress, TrialTable
        │   ├── results/    # RunComparison, ParamDiff, ExportDialog
        │   └── layout/     # Sidebar, Header, Layout
        ├── pages/          # Dashboard, Config, Simulation, Tuning, Results
        ├── providers/      # SimulationProvider (app-level WebSocket context)
        ├── hooks/          # useWebSocket, useSimulation, useTuning, useParams
        ├── stores/         # Zustand: configStore, runStore, tuningStore
        └── lib/            # API client, types, utilities

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
