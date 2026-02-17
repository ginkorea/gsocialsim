# C++ Port Plan (Module-by-Module)

Goal: port Python features into a standalone C++ engine, one module at a time, with a clean
phase-contract kernel, deterministic runs, and batch-friendly execution.

## Module 0: Core Types
- Status: complete
- Contents: identifiers, basic structs, shared utilities
- Next: define `AgentId`, `TopicId`, `ContentId`, `Belief`, `Impression`, `Content`

## Module 1: Kernel (phase contract)
- Target: C++ `WorldKernel`
- Scope: clock, phase ordering, buffers, queue of belief deltas
- Output: deterministic step loop, no Python dependencies
- Status: complete

## Module 2: Agents
- Target: Agent state + behavior
- Scope: identity, beliefs, attention, policy, budgeted time
- Output: `plan_action`, `plan_perception`, `apply_*` in C++
- Status: complete

## Module 3: Stimuli Pipeline
- Target: CSV ingestion and stimuli scheduling
- Scope: parse CSV into tick-indexed stimuli, content build
- Status: complete

## Module 4: Social Graph + Trust
- Target: directed follower graph + trust updates
- Scope: follow edges, edge trust, global relationship state
- Status: complete

## Module 5: Physical World
- Target: geo schedules + time budgets
- Scope: location sampling, daily schedules, co-location inference

## Module 6: Analytics + Attribution
- Target: exposure history, belief crossing, attribution engine
- Scope: logging + bounded memory footprint

## Module 7: Visualization
- Target: keep in Python (initially)
- Scope: export C++ outputs to CSV/JSON; reuse existing HTML/Dash renderers
- Note: C++ should output structured logs to drive current visualizations

## Module 8: Performance + Parallelism
- Target: batch data structures + threading
- Scope: agent-centric batches, SIMD-friendly structures, optional OpenMP

## Integration Notes
- LLM integration will attach to the action/perception planning layer (Module 2).
- Keep LLM out of the hot loop; cache or batch calls.

## Build
- `cpp/CMakeLists.txt` builds `gsocialsim_cpp` executable.
