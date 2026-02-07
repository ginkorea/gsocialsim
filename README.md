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

