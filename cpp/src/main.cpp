#include <iostream>

#include "kernel.h"

int main(int argc, char** argv) {
    (void)argc;
    (void)argv;

    WorldKernel kernel;
    kernel.ingest_fn = [](int t, WorldContext& ctx) {
        // placeholder: push a dummy stimulus id for visibility
        ctx.stimuli_by_tick[t].push_back(t);
    };
    kernel.act_fn = [](int t, WorldContext& ctx) {
        // placeholder: post one dummy content id
        ctx.posted_by_tick[t].push_back(1000 + t);
    };
    kernel.perceive_fn = [](int, WorldContext&) {};
    kernel.consolidate_fn = [](int, WorldContext&) {};

    kernel.step(3);

    std::cout << "gsocialsim_cpp: kernel ran 3 ticks\n";
    return 0;
}
