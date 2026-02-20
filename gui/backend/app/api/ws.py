import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..core.parser import compute_metrics_from_tick_data

router = APIRouter()
log = logging.getLogger("gsocialsim.ws")

# Set by main.py
runner = None
store = None
tuning_engine = None


@router.websocket("/ws/run/{run_id}")
async def ws_run(websocket: WebSocket, run_id: str):
    await websocket.accept()
    log.info("[ws %s] client connected", run_id)
    await _send_log(websocket, f"WebSocket connected for run {run_id}")

    run = runner.get_run(run_id)
    if not run:
        log.error("[ws %s] run not found", run_id)
        await _send_log(websocket, f"ERROR: run {run_id} not found in runner")
        await websocket.send_json({"type": "error", "message": f"Run {run_id} not found"})
        return

    await _send_log(websocket, f"Run config: ticks={run.config.ticks} agents={run.config.agents} seed={run.config.seed}")
    ds = run.config.data_source
    if ds and ds.filename:
        await _send_log(websocket, f"Data source: {ds.filename} (path={ds.path})")
    else:
        await _send_log(websocket, "WARNING: No data source configured for this run")

    await _send_log(websocket, "Launching C++ process...")

    tick_history = []
    try:
        async for tick_data in runner.stream_output(run_id):
            tick_history.append(tick_data)
            tick = tick_data.get("tick", "?")
            total = tick_data.get("total", "?")
            imp = tick_data.get("impressions", 0)
            con = tick_data.get("consumed", 0)
            n_leans = len(tick_data.get("leans", []))
            await _send_log(websocket, f"Tick {tick}/{total}: impressions={imp} consumed={con} agents={n_leans}")
            await websocket.send_json({"type": "tick", "data": tick_data})

        metrics = compute_metrics_from_tick_data(tick_history)
        run = runner.get_run(run_id)
        status = run.status.value if run else "completed"
        await store.update_run_status(run_id, status, len(tick_history), metrics)
        await _send_log(websocket, f"Simulation complete: {len(tick_history)} ticks, status={status}")
        await websocket.send_json({"type": "complete", "metrics": metrics, "status": status})
    except WebSocketDisconnect:
        log.info("[ws %s] client disconnected", run_id)
    except Exception as e:
        log.error("[ws %s] error: %s", run_id, e, exc_info=True)
        try:
            await _send_log(websocket, f"ERROR: {e}")
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass


async def _send_log(websocket: WebSocket, message: str):
    """Send a log message to the frontend via WebSocket."""
    try:
        await websocket.send_json({"type": "log", "message": message})
    except Exception:
        pass


@router.websocket("/ws/study/{study_id}")
async def ws_study(websocket: WebSocket, study_id: str):
    await websocket.accept()
    try:
        async for trial_data in tuning_engine.stream_trials(study_id):
            await websocket.send_json({"type": "trial", "data": trial_data})

        study = await store.get_study(study_id)
        await websocket.send_json({"type": "complete", "study": study})
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
