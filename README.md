# gsocialsim

**gsocialsim** (Global Social Simulation) is a research framework for simulating
**human-like social behavior, belief formation, and influence mechanics** across
both **online social networks** and **offline physical interactions**.

The system is designed to study not only *why beliefs propagate or survive*, but
**how influence actually works**: who influences whom, through which channels,
under what incentives, and with what measurable downstream effects.

This repository currently contains the **complete design specification** for
gsocialsim, including a full Product Requirements Document (PRD) and UML
diagrams covering architecture, agents, cognition, influence, and evolution.

---

## Core Research Questions

gsocialsim is built to answer questions such as:

- How does influence differ between **scrolling**, **seeking**, and **physical interaction**?
- Who actually causes belief change, and how can attribution be measured?
- Why do some influence attempts succeed, fail, or backfire?
- How do platform mechanics shape influence efficiency and concentration?
- Under what conditions does influence become centralized vs distributed?
- Why does offline influence dominate belief crossings despite limited reach?

Influence is treated as a **first-class object**, not an emergent side effect.

---

## Design Principles

- **Persistent agents**, not request/response bots  
- **Unequal attention and action budgets** (heavy-tailed by design)  
- **Scroll vs Seek vs Physical** as distinct cognitive intake modes  
- **Belief change is rare, bounded, and attributable**  
- **Physical interactions dominate belief crossings**  
- **Most agents lurk; a small elite produces most content**  
- **Evolutionary selection**, not optimization to a single outcome  
- **Deterministic replay** under fixed seeds  

The system is explicitly **not** designed for real-world persuasion or deployment.

---

## Repository Contents

```

gsocialsim/
├── README.md
├── PRD.md
└── diagrams/
├── component_diagram.uml
├── class_diagram.uml
├── sequence_diagram.uml
└── agent_runtime_state_machine.uml

```

### Key Files

- **PRD.md**  
  Full product and research requirements, including:
  - Agent cognition and budgets
  - Belief and identity modeling
  - Influence attribution
  - Evolutionary dynamics
  - Required logs and metrics

- **UML Diagrams**
  - **Component Diagram** – system architecture
  - **Class Diagram** – agents, beliefs, influence events, analytics
  - **Sequence Diagram** – runtime flow and influence logging
  - **State Machine** – persistent agent cognition loop

---

## Influence Modeling (Explicit)

Influence is modeled directly via:

- **InfluenceEvent**
  - Attempts, successes, failures, backfires
  - Source, target, topic, channel, intake mode
- **InfluencePath**
  - Ordered exposure → influence → outcome chains
- **Attribution Engine**
  - Sliding windows
  - Mode-split credit (scroll / seek / physical)
  - Strong-tie and physical multipliers
- **Metrics**
  - Influence graph (who → whom)
  - Influence efficiency
  - Influence concentration (Gini / top-k)
  - Scroll vs seek vs physical influence share

This allows analysis of **mechanisms**, not just outcomes.

---

## Status

- **Design:** Complete (v1 design freeze)
- **Implementation:** Forthcoming
- **Scope:** Research and simulation only

---

## Non-Goals

- No live interaction with real social platforms
- No real-world persuasion or deployment
- No free-form AGI cognition
- No single “correct” belief model
- No claim of predictive accuracy for real societies

---

## License

License to be added (recommended: Apache-2.0).

---

## Author Notes

This project treats social systems as **evolutionary attention-and-influence
environments**, where:

- Platforms define incentives  
- Personalities define reward  
- Learning defines adaptation  
- Evolution defines selection  

If you are interested in agent-based modeling, social influence, or
computational social science beyond toy diffusion models, this project is
intended to be a serious foundation.
```

