import asyncio
import json
from typing import Any, AsyncIterator

import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

from ..core.schemas import SimulationConfig, StudyConfig
from ..core.runner import SimulationRunner
from ..core.parser import compute_metrics_from_tick_data
from .spaces import suggest_param
from .objectives import compute_objective


# Map param name to which config sub-dict it belongs to
PARAM_GROUP_MAP = {
    "inertia_rho": "influence_dynamics",
    "learning_rate_base": "influence_dynamics",
    "rebound_k": "influence_dynamics",
    "critical_velocity_threshold": "influence_dynamics",
    "critical_kappa": "influence_dynamics",
    "evidence_decay_lambda": "influence_dynamics",
    "evidence_threshold": "influence_dynamics",
    "trust_exponent_gamma": "influence_dynamics",
    "habituation_alpha": "influence_dynamics",
    "bounded_confidence_tau": "influence_dynamics",
    "mutual_trust_weight": "kernel",
    "offline_contacts_per_tick": "kernel",
    "offline_base_prob": "kernel",
    "discovery_min_per_tick": "kernel",
    "discovery_max_per_tick": "kernel",
    "discovery_pool_size": "kernel",
    "recency_weight": "feed_queue",
    "engagement_weight": "feed_queue",
    "proximity_weight": "feed_queue",
    "mutual_weight": "feed_queue",
    "candidate_window_ticks": "broadcast_feed",
    "max_candidates": "broadcast_feed",
    "max_shown": "broadcast_feed",
    "saturation_k": "media_diet",
}


class OptunaEngine:
    def __init__(self, runner: SimulationRunner, store):
        self.runner = runner
        self.store = store
        self._study_queues: dict[str, asyncio.Queue] = {}
        self._studies: dict[str, optuna.Study] = {}

    async def run_study(self, study_id: str, config: StudyConfig):
        queue: asyncio.Queue = asyncio.Queue()
        self._study_queues[study_id] = queue

        directions = []
        for obj in config.objectives:
            d = obj.get("direction", "minimize")
            directions.append(optuna.study.StudyDirection.MINIMIZE if d == "minimize" else optuna.study.StudyDirection.MAXIMIZE)

        sampler = self._get_sampler(config.sampler)
        study = optuna.create_study(
            study_name=study_id,
            directions=directions,
            sampler=sampler,
        )
        self._studies[study_id] = study

        try:
            for trial_num in range(config.n_trials):
                trial = study.ask()
                suggested = {}
                for param_name, space in config.search_space.items():
                    suggested[param_name] = suggest_param(trial, param_name, space)

                # Merge suggested into base config
                trial_config = config.base_config.model_copy(deep=True)
                for param_name, value in suggested.items():
                    group = PARAM_GROUP_MAP.get(param_name)
                    if group == "influence_dynamics":
                        trial_config.influence_dynamics[param_name] = value
                    elif group == "kernel":
                        trial_config.kernel[param_name] = value
                    elif group == "feed_queue":
                        trial_config.feed_queue[param_name] = value
                    elif group == "broadcast_feed":
                        trial_config.broadcast_feed[param_name] = value
                    elif group == "media_diet":
                        trial_config.media_diet[param_name] = value
                    elif param_name == "ticks":
                        trial_config.ticks = int(value)
                    elif param_name == "agents":
                        trial_config.agents = int(value)

                # Run simulation
                run = await self.runner.start_run(trial_config)
                tick_history = []
                async for tick_data in self.runner.stream_output(run.id):
                    tick_history.append(tick_data)

                state = self.runner.get_results(run.id)

                # Compute objectives
                values = []
                for obj in config.objectives:
                    obj_name = obj["name"]
                    val = compute_objective(obj_name, tick_history, state)
                    values.append(val)

                study.tell(trial, values)

                trial_result = {
                    "trial_number": trial_num,
                    "params": suggested,
                    "values": values,
                    "objectives": [o["name"] for o in config.objectives],
                }
                await queue.put(trial_result)

                # Update store
                best_trial = study.best_trial if len(directions) == 1 else study.best_trials[0] if study.best_trials else None
                best_val = best_trial.values[0] if best_trial else None
                best_params = best_trial.params if best_trial else {}
                await self.store.update_study(study_id, "running", trial_num + 1, best_val, best_params)

            await self.store.update_study(study_id, "completed", config.n_trials,
                                          best_val, best_params)
        except Exception as e:
            await self.store.update_study(study_id, "failed", 0, None, {"error": str(e)})
        finally:
            await queue.put(None)  # Signal completion

    async def stream_trials(self, study_id: str) -> AsyncIterator[dict]:
        queue = self._study_queues.get(study_id)
        if not queue:
            return
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

    def get_importance(self, study_id: str) -> dict[str, float]:
        study = self._studies.get(study_id)
        if not study or len(study.trials) < 2:
            return {}
        try:
            return optuna.importance.get_param_importances(study)
        except Exception:
            return {}

    def _get_sampler(self, name: str):
        if name == "cmaes":
            return optuna.samplers.CmaEsSampler()
        elif name == "random":
            return optuna.samplers.RandomSampler()
        elif name == "grid":
            return optuna.samplers.GridSampler({})
        else:
            return optuna.samplers.TPESampler()
