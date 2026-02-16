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

## Optimize Targets (Massive Sim)

- Perception + belief update hot loop -> C first, CUDA later if batched arrays.
- Delivery fan-out / filtering -> C (fast recipient selection).
- Exposure history + attribution -> C (ring buffers), CUDA for large batch reductions.
- Feed ranking / scoring (if added) -> CUDA.
- Physical co-location / spatial queries -> C, CUDA if dense grid/large N.
