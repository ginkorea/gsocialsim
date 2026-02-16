# gsocialsim Phase Contract (Tick Semantics)

This document defines the **non-negotiable execution contract** for `WorldKernel.step()`.

It is written to prevent “phase drift”, accidental within-tick ping-pong loops, and ambiguity about
when content becomes visible, when actions can respond, and when beliefs may update.

---

## 0) Core Definitions

- **Tick (`t`)**: a fixed wall-clock window of **900 seconds (15 minutes)**.
- **Two batch calls per tick**:
  1) **ACT_BATCH(t)** — execute actions selected previously
  2) **PERCEIVE_BATCH(t)** — gather new perceptions for next tick planning

- **Consolidation** happens at the end of the tick and is where belief updates are applied.

---

## 1) Required Phase Order (Per Tick)

A tick MUST run in this exact order:

1. **INGEST(t)**
2. **ACT_BATCH(t)**
3. **PERCEIVE_BATCH(t)**
4. **CONSOLIDATE(t)**

There MUST NOT be additional agent decision loops inside the tick.

---

## 2) Reaction Lag Rule (No Ping-Pong)

### Hard invariant
**An agent may NOT execute an action in tick `t` that was selected because of something perceived in `PERCEIVE_BATCH(t)`.**

Equivalently:
- **Perceive(t) → Plan(t+1) → Act(t+1)**

This forbids infinite back-and-forth inside a tick and ensures cascades propagate in discrete 15-minute waves.

---

## 3) Same-Tick Visibility (Immediate Posting is Allowed)

Content **published** during **ACT_BATCH(t)** MAY be eligible to appear in other agents’ **PERCEIVE_BATCH(t)**,
subject to platform feed rules.

This enables:
- “post immediately” personalities
- fast same-tick audience exposure

But reactions to that exposure must still obey the **Reaction Lag Rule** and occur no earlier than **ACT_BATCH(t+1)**.

---

## 4) Generation vs Posting

During **ACT_BATCH(t)** an agent can produce three kinds of “generated content”:

### A) Posted content (public, visible)
- Becomes a `ContentItem` and is **published immediately** to the world/platform.
- MAY be perceivable by others during `PERCEIVE_BATCH(t)`.

### B) Draft content (private outbox)
- Stored as `OutboxDraft` (not visible to others).
- MAY be published later (preferably in a future ACT batch; publishing at CONSOLIDATE is allowed only if explicitly defined).

### C) Internal artifacts (private cognition)
- Stored as `InternalArtifact` (e.g., monologue, rehearsal, private notes).
- Never visible to others unless later transformed into a draft/post by policy.

This supports “read + think + do nothing” agents (silent majority), and separates cognition from expression.

---

## 5) Belief Update Timing

Belief state changes MUST be applied only in **CONSOLIDATE(t)**.

- During PERCEIVE and ACT, agents may compute deltas, traces, and drafts,
  but the canonical belief vector must remain unchanged until CONSOLIDATE runs.

---

## 6) Budget Semantics

Each agent has a per-tick time budget (minutes).

Costs are time-based, not just “counts”.

### Time budget rules
- Budget resets at the start of tick `t`.
- Unused time is not banked.
- Perception and action both spend from the same budget.

Opportunity cost is required:
- spending time on creation reduces time for perception in the same tick.

---

## 7) Minimal Data Structures (Contract Surface)

These names are conceptual; code may differ, but semantics must hold.

### Agent-side
- `ActionPlan[t]`: a list of scheduled actions to execute in `ACT_BATCH(t)`.
- `PerceptionSummary[t]`: exposures and selected cognitive traces produced in `PERCEIVE_BATCH(t)`.
- `outbox_drafts`: private drafts awaiting publication.
- `internal_artifacts`: private monologue/rehearsal artifacts.

### World-side
- `stimuli_by_tick[t]`: exogenous stimuli (e.g., GDELT batch) for tick `t`.
- `posted_by_tick[t]`: content published during `ACT_BATCH(t)`.

---

## 8) Platform Feed Eligibility Rules (Recommended)

To keep realism without complexity:

- **Direct actions** (DMs, direct replies, mentions): eligible for same-tick delivery to the target.
- **Broadcast feed**: eligible for same-tick inclusion probabilistically / by ranking,
  capped by the perceiving agent’s remaining attention budget.

---

## 9) Test Contract (Must Exist)

The following tests should be present and passing:

1. **Same-tick visibility, next-tick reaction**
   - A posts in ACT(t)
   - B can perceive it in PERCEIVE(t)
   - B cannot react until ACT(t+1)

2. **Silent thinker**
   - B perceives persuasive content in PERCEIVE(t)
   - B creates internal monologue in ACT(t+1)
   - B shifts belief in CONSOLIDATE(t+1) without posting

3. **Budget tradeoff**
   - Heavy creation in ACT(t) reduces perception in PERCEIVE(t)

4. **Belief updates only in CONSOLIDATE**
   - Belief vector unchanged during ACT/PERCEIVE; changes only after CONSOLIDATE

---

## 10) Reference Diagrams

### Tick lifecycle (high level)

```
INGEST(t) → ACT_BATCH(t) → PERCEIVE_BATCH(t) → CONSOLIDATE(t)
                    |                 |
                    |                 └─ produces PerceptionSummary[t]
                    └─ may publish content immediately (posted_by_tick[t])
```

### Causality and lag

```
PERCEIVE(t) → (plan at end of tick) → ActionPlan[t+1] → ACT(t+1)
```

If you ever see code that allows:
- `PERCEIVE(t)` to directly trigger `ACT(t)` behavior, or
- multiple act/perceive loops inside the tick,

then the phase contract has been violated.
