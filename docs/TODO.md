# Model TODOs

This list is intentionally persistent. Update as items are implemented.

- [x] Multi-dimensional political identity (beyond 1D left/right).
- [x] Explicit group identity salience (race/sex/etc) plus mutable group affiliations.
- Network rewiring driven by trust changes (follow/unfollow, exposure shifts).
- Message framing (moral foundations / security / economic framing) as part of content.
- Heterogeneous media environments (source bias, ranking, platform incentives).
- Behavioral feedback loops (beliefs -> actions -> reinforcement).
- Context-dependent backfire (more nuanced triggers than a threshold).
- Optimize for massive simulations (define targets and thresholds).

## C++ Server Mode (Phase 14) — HIGH PRIORITY

Currently each GUI simulation run spawns a new C++ process with ~45s setup overhead (network generation is the bottleneck at 15-25s). The actual simulation runs in <1s for typical configs.

- [ ] Add `--server-mode` flag to C++ binary (persistent process, reads configs from stdin)
- [ ] Pre-load static data once at startup (stimulus CSV, geo population, segment templates)
- [ ] Stdin JSON protocol: `{"cmd": "run", ...params}` → stream tick JSON to stdout
- [ ] Per-run reset: clear agents, network graph, subscriptions between runs
- [ ] Update `runner.py` to manage persistent C++ process instead of spawn-per-run
- [ ] Add health check / ready protocol between Python backend and C++ process
- [ ] Parallel network generation with OpenMP (15-25s → 5-8s)

## GDELT Integration (Phase 15)

- [ ] Add `GdeltDataSource` to C++ alongside `CsvDataSource`
- [ ] GDELT 2.0 GKG API client (fetch events by date/country/topic)
- [ ] Transform GDELT events into `Stimulus` format
- [ ] Local cache for reproducibility
- [ ] Enable GDELT selector in GUI DataSourcePanel

## Optimize Targets (Massive Sim)

- Perception + belief update hot loop -> C first, CUDA later if batched arrays.
- Delivery fan-out / filtering -> C (fast recipient selection).
- Exposure history + attribution -> C (ring buffers), CUDA for large batch reductions.
- Feed ranking / scoring (if added) -> CUDA.
- Physical co-location / spatial queries -> C, CUDA if dense grid/large N.
