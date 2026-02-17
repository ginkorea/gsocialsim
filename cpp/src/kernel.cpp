#include "kernel.h"

void WorldKernel::start() {
    if (started) return;
    started = true;
}

void WorldKernel::step(int num_ticks) {
    if (num_ticks <= 0) return;
    if (!started) start();

    for (int i = 0; i < num_ticks; ++i) {
        int t = clock.t;
        _reset_tick_budgets(t);

        context.begin_phase(t, "INGEST");
        _ingest(t);

        context.begin_phase(t, "ACT");
        _act_batch(t);

        context.begin_phase(t, "PERCEIVE");
        _perceive_batch(t);

        context.begin_phase(t, "CONSOLIDATE");
        _consolidate(t);

        context.clear_tick_buffers(t);
        clock.advance(1);
    }
}

void WorldKernel::_reset_tick_budgets(int /*t*/) {
    // Placeholder: Module 2/5 will implement time budgets.
}

void WorldKernel::_ingest(int t) {
    if (ingest_fn) {
        ingest_fn(t, context);
    }
}

void WorldKernel::_act_batch(int t) {
    if (act_fn) {
        act_fn(t, context);
    }
}

void WorldKernel::_perceive_batch(int t) {
    if (perceive_fn) {
        perceive_fn(t, context);
    }
}

void WorldKernel::_consolidate(int t) {
    if (consolidate_fn) {
        consolidate_fn(t, context);
    }
}
