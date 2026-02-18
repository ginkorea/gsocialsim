# CUDA Optimization Guide for Population Layer

## Overview

The Population Layer is designed with CUDA optimization in mind from the ground up. This document explains the data structure design decisions and how to implement the GPU backend in Phase 5.

## Key Design Principle: Struct-of-Arrays (SoA)

### Why SoA Instead of Array-of-Structs (AoS)?

**Bad (AoS)**:
```cpp
struct PopulationCell {
    string cell_id;
    int population;
    vector<SegmentMix> segments;
    map<TopicId, BeliefDistribution> beliefs;
};
vector<PopulationCell> cells;  // Pointer chasing, cache misses
```

**Good (SoA)**:
```cpp
struct PopulationCellArrays {
    vector<string> cell_ids;        // All cell IDs contiguous
    vector<int> populations;        // All populations contiguous
    vector<int> segment_offsets;    // Offset for variable-length data
    vector<int> segment_ids_flat;   // Flattened segment data
    // ... parallel arrays for all fields
};
```

### Benefits for GPU:
1. **Coalesced memory access**: Threads access adjacent elements
2. **SIMD-friendly**: Vectorized operations on parallel arrays
3. **No pointer chasing**: Everything in flat arrays
4. **Predictable memory layout**: Better cache utilization

---

## Data Structure Design

### PopulationCellArrays Layout

```cpp
// Cell metadata (1 entry per cell)
cell_ids:     ["cell_0", "cell_1", "cell_2", ...]
populations:  [1000,     2000,     1500,     ...]

// Segment mix (variable length per cell)
segment_mix_offsets: [0,   3,   7,   ...] // Where this cell's segments start
segment_mix_counts:  [3,   4,   2,   ...] // How many segments this cell has
segment_ids_flat:    [0,1,2, 1,2,3,4, 0,2, ...] // All segments flattened
segment_weights_flat:[0.5,0.3,0.2, 0.4,0.3,0.2,0.1, 0.6,0.4, ...]

// Beliefs (variable length per cell)
belief_offsets:       [0,   5,   12,  ...] // Where this cell's beliefs start
belief_counts:        [5,   7,   3,   ...] // How many topics this cell has
belief_topic_ids_flat:[0,1,2,3,4, 1,2,3,4,5,6,7, 0,2,5, ...]
belief_means_flat:    [0.5,-0.3,0.2,0.1,-0.4, ...]
belief_variances_flat:[0.1,0.2,0.15,0.1,0.2, ...]
belief_momentum_flat: [0.0,0.05,0.0,-0.03,0.01, ...]
```

### Memory Access Pattern

For cell `i`:
- Population: `populations[i]`
- Segments: `segment_ids_flat[segment_mix_offsets[i] ... segment_mix_offsets[i] + segment_mix_counts[i] - 1]`
- Beliefs: `belief_topic_ids_flat[belief_offsets[i] ... belief_offsets[i] + belief_counts[i] - 1]`

---

## CUDA Implementation Plan (Phase 5)

### Step 1: Create CUDA Kernel File

**File**: `cpp/src/population_cuda.cu`

```cuda
__global__ void update_belief_distributions_kernel(
    int num_cells,
    const int* populations,
    const int* segment_mix_offsets,
    const int* segment_mix_counts,
    const int* segment_ids_flat,
    const double* segment_weights_flat,
    const int* belief_offsets,
    const int* belief_counts,
    double* belief_means_flat,        // OUTPUT
    double* belief_variances_flat,    // OUTPUT
    double* belief_momentum_flat,     // OUTPUT
    // ... exposure data arrays
) {
    int cell_idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (cell_idx >= num_cells) return;

    // Access this cell's data
    int population = populations[cell_idx];
    int seg_start = segment_mix_offsets[cell_idx];
    int seg_count = segment_mix_counts[cell_idx];
    int belief_start = belief_offsets[cell_idx];
    int belief_count = belief_counts[cell_idx];

    // Process each belief for this cell
    for (int b = 0; b < belief_count; ++b) {
        int belief_idx = belief_start + b;

        // Compute segment-weighted update
        double weighted_update = 0.0;
        for (int s = 0; s < seg_count; ++s) {
            int seg_idx = segment_ids_flat[seg_start + s];
            double weight = segment_weights_flat[seg_start + s];
            // ... compute update contribution
            weighted_update += weight * /* segment influence */;
        }

        // Apply dynamics: inertia + rebound
        double momentum = belief_momentum_flat[belief_idx];
        double mean = belief_means_flat[belief_idx];

        momentum = 0.85 * momentum + 0.10 * weighted_update;
        double rebound = -0.05 * (mean - 0.0); // core_value = 0
        double new_mean = mean + momentum + rebound;

        // Clamp and write back
        belief_means_flat[belief_idx] = fmin(1.0, fmax(-1.0, new_mean));
        belief_momentum_flat[belief_idx] = momentum;
    }
}
```

### Step 2: Memory Transfer

```cpp
void PopulationUpdateEngine::update_all_cells_cuda(
    PopulationCellArrays& arrays,
    const std::vector<PopulationSegment>& segments) {

    // Allocate device memory
    int num_cells = arrays.num_cells();

    int* d_populations;
    int* d_segment_offsets;
    int* d_segment_counts;
    // ... allocate all arrays

    cudaMalloc(&d_populations, num_cells * sizeof(int));
    cudaMalloc(&d_segment_offsets, num_cells * sizeof(int));
    // ...

    // Copy to device
    cudaMemcpy(d_populations, arrays.populations.data(),
               num_cells * sizeof(int), cudaMemcpyHostToDevice);
    // ... copy all input arrays

    // Launch kernel
    int block_size = 256;
    int num_blocks = (num_cells + block_size - 1) / block_size;

    update_belief_distributions_kernel<<<num_blocks, block_size>>>(
        num_cells,
        d_populations,
        d_segment_offsets,
        // ... all device pointers
    );

    // Copy results back
    cudaMemcpy(arrays.belief_means_flat.data(), d_belief_means,
               arrays.belief_means_flat.size() * sizeof(double),
               cudaMemcpyDeviceToHost);
    // ... copy all output arrays

    // Free device memory
    cudaFree(d_populations);
    // ...
}
```

### Step 3: CMake CUDA Support

**Modify** `cpp/CMakeLists.txt`:

```cmake
project(gsocialsim_cpp LANGUAGES CXX CUDA)

set(CMAKE_CUDA_STANDARD 17)
set(CMAKE_CUDA_ARCHITECTURES 75 80 86)  # Turing, Ampere, Ada

add_executable(gsocialsim_cpp
    # ... existing sources
    src/population_cuda.cu  # CUDA kernel
)

target_compile_options(gsocialsim_cpp PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-Xcompiler -O3>
)
```

---

## Performance Expectations

### CPU Baseline
- 10,000 cells, 100 topics per cell
- 5 segments per cell
- 1000 exposures per cell per tick
- **Expected**: ~50ms per update

### GPU Target
- Same workload
- **Expected**: ~2-5ms per update
- **Speedup**: 10-25x

### Optimization Opportunities
1. **Shared memory**: Cache segment weights in shared memory
2. **Warp-level primitives**: Use warp shuffle for reductions
3. **Streams**: Overlap compute and memory transfer
4. **Unified memory**: Simplify memory management with managed memory

---

## Testing Strategy

### Validation
1. Run same workload on CPU and GPU
2. Compare results element-by-element (tolerance 1e-6)
3. Verify determinism (same seed → same results)

### Benchmarking
1. Measure CPU time: `update_all_cells_cpu()`
2. Measure GPU time: `update_all_cells_cuda()` including transfers
3. Report speedup and cells/second throughput

### Profiling
```bash
nvprof ./gsocialsim_cpp --agents 100000 --ticks 10
```

Look for:
- Kernel occupancy (target: >50%)
- Memory bandwidth utilization (target: >60%)
- SM utilization (target: >70%)

---

## Current Status

**Phase 4**: CPU implementation complete, data structures CUDA-ready
**Phase 5**: CUDA backend to be implemented

**Ready for GPU**:
- ✅ Struct-of-arrays layout
- ✅ Flat array representation
- ✅ Export/import pipeline
- ✅ Offset+count variable-length pattern
- ✅ No pointer chasing in hot path

**TODO for Phase 5**:
- [ ] Create population_cuda.cu
- [ ] Implement kernel launch wrapper
- [ ] Add CUDA to CMakeLists.txt
- [ ] Validate CPU/GPU equivalence
- [ ] Benchmark and optimize
