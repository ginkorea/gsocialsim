#include <iostream>

#include "kernel.h"
#include "utils.h"

int main(int argc, char** argv) {
    (void)argc;
    (void)argv;

    WorldKernel kernel;
    kernel.ingest_fn = [](int t, WorldContext& ctx) {
        // placeholder: push a dummy stimulus for visibility
        Stimulus s;
        s.id = "stim_" + std::to_string(t);
        s.tick = t;
        s.source = "SOURCE";
        s.content_text = "placeholder";
        s.topic_hint = "T_Original";
        s.stance_hint = 0.1;
        ctx.stimuli_by_tick[t].push_back(s);
    };
    kernel.act_fn = [](int t, WorldContext& ctx) {
        // placeholder: post one dummy content
        Content c;
        c.id = "content_" + std::to_string(t);
        c.author_id = "AGENT";
        c.topic = "T_Original";
        c.stance = -0.1;
        ctx.posted_by_tick[t].push_back(c);
    };
    kernel.perceive_fn = [](int, WorldContext&) {};
    kernel.consolidate_fn = [](int, WorldContext&) {};

    kernel.step(3);

    std::cout << "gsocialsim_cpp: kernel ran 3 ticks\n";
    return 0;
}
