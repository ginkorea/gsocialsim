import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .core.runner import SimulationRunner
from .core.store import Store
from .tuning.engine import OptunaEngine
from .api import runs, params, tuning, ws, datasources

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize store
    store = Store(settings.db_path)
    await store.init()

    # Initialize runner
    cpp_binary = settings.resolve_cpp_binary()
    stimuli_csv = settings.resolve_stimuli_csv()
    runner = SimulationRunner(
        cpp_binary=cpp_binary,
        stimuli_csv=stimuli_csv,
        data_dir=settings.run_data_dir,
        max_concurrent=settings.max_concurrent_runs,
    )

    # Initialize tuning engine
    engine = OptunaEngine(runner=runner, store=store)

    # Wire up dependencies
    runs.runner = runner
    runs.store = store
    params.store = store
    tuning.store = store
    tuning.tuning_engine = engine
    ws.runner = runner
    ws.store = store
    ws.tuning_engine = engine

    # Seed built-in presets
    await _seed_presets(store)

    print(f"gsocialsim GUI backend started")
    print(f"  C++ binary: {cpp_binary}")
    print(f"  Stimuli CSV: {stimuli_csv}")
    print(f"  DB: {settings.db_path}")

    yield

    await store.close()


app = FastAPI(
    title="gsocialsim GUI",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(runs.router)
app.include_router(params.router)
app.include_router(tuning.router)
app.include_router(ws.router)
app.include_router(datasources.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


async def _seed_presets(store: Store):
    """Seed built-in presets if they don't exist."""
    existing = await store.list_presets()
    existing_names = {p["name"] for p in existing}

    base = {
        "ticks": 96, "agents": 100, "seed": 123, "network_mode": "groups",
        "avg_following": 12, "analytics_mode": "summary",
        "influence_dynamics": {}, "kernel": {}, "feed_queue": {},
        "broadcast_feed": {}, "media_diet": {},
    }

    presets = [
        ("Default", {**base}),
        ("High Polarization", {
            **base,
            "influence_dynamics": {"rebound_k": 0.15, "bounded_confidence_tau": 0.5},
        }),
        ("Echo Chamber", {
            **base,
            "influence_dynamics": {"inertia_rho": 0.95},
            "feed_queue": {"mutual_weight": 0.3},
            "kernel": {"discovery_min_per_tick": 0},
        }),
        ("Open Discourse", {
            **base,
            "influence_dynamics": {"inertia_rho": 0.5, "bounded_confidence_tau": 3.0},
            "kernel": {"discovery_max_per_tick": 10},
        }),
        ("Rapid Dynamics", {
            **base,
            "influence_dynamics": {"evidence_threshold": 0.1, "learning_rate_base": 0.3},
        }),
        ("Large Scale", {
            **base, "agents": 5000, "ticks": 960,
        }),
    ]

    for name, config in presets:
        if name not in existing_names:
            preset_id = name.lower().replace(" ", "_")
            await store.create_preset(preset_id, name, config)
