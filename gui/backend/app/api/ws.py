import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from ..core.parser import compute_metrics_from_tick_data

router = APIRouter()
log = logging.getLogger("gsocialsim.ws")

# Set by main.py
runner = None
store = None
tuning_engine = None


async def _ws_send(websocket: WebSocket, data: dict) -> bool:
    """Send JSON to WebSocket. Returns False if connection is closed."""
    try:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(data)
            return True
    except Exception:
        pass
    return False


@router.websocket("/ws/run/{run_id}")
async def ws_run(websocket: WebSocket, run_id: str):
    await websocket.accept()
    log.info("[ws %s] client connected", run_id)
    await _ws_send(websocket, {"type": "log", "message": f"WebSocket connected for run {run_id}"})

    run = runner.get_run(run_id)
    if not run:
        log.error("[ws %s] run not found", run_id)
        await _ws_send(websocket, {"type": "error", "message": f"Run {run_id} not found"})
        return

    await _ws_send(websocket, {"type": "log", "message": f"Run config: ticks={run.config.ticks} agents={run.config.agents} seed={run.config.seed}"})
    ds = run.config.data_source
    if ds and ds.filename:
        await _ws_send(websocket, {"type": "log", "message": f"Data source: {ds.filename} (path={ds.path})"})
    else:
        await _ws_send(websocket, {"type": "log", "message": "WARNING: No data source configured for this run"})

    await _ws_send(websocket, {"type": "log", "message": "Launching C++ process (setup may take 30-60s)..."})

    tick_history = []
    heartbeat_active = True

    async def heartbeat():
        """Send periodic keepalive pings while the C++ process is running."""
        count = 0
        while heartbeat_active:
            await asyncio.sleep(5)
            if not heartbeat_active:
                break
            count += 1
            await _ws_send(websocket, {
                "type": "log",
                "message": f"[heartbeat] Process running... ({count * 5}s elapsed)",
            })

    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        async for item in runner.stream_output(run_id):
            item_type = item.pop("_type", "tick")

            if item_type == "status":
                # Non-JSON line from C++ (setup messages, errors, etc.)
                ok = await _ws_send(websocket, {"type": "log", "message": f"[cpp] {item['message']}"})
                if not ok:
                    log.info("[ws %s] client gone during status send, continuing process", run_id)
            elif item_type == "tick":
                tick_history.append(item)
                tick = item.get("tick", "?")
                total = item.get("total", "?")
                await _ws_send(websocket, {"type": "log", "message": f"Tick {tick}/{total}"})
                ok = await _ws_send(websocket, {"type": "tick", "data": item})
                if not ok:
                    log.info("[ws %s] client gone during tick send", run_id)

        heartbeat_active = False
        heartbeat_task.cancel()

        metrics = compute_metrics_from_tick_data(tick_history)
        run = runner.get_run(run_id)
        status = run.status.value if run else "completed"
        await store.update_run_status(run_id, status, len(tick_history), metrics)
        await _ws_send(websocket, {"type": "log", "message": f"Simulation complete: {len(tick_history)} ticks, status={status}"})
        await _ws_send(websocket, {"type": "complete", "metrics": metrics, "status": status})
    except WebSocketDisconnect:
        log.info("[ws %s] client disconnected", run_id)
    except Exception as e:
        log.error("[ws %s] error: %s", run_id, e, exc_info=True)
        await _ws_send(websocket, {"type": "error", "message": str(e)})
    finally:
        heartbeat_active = False
        heartbeat_task.cancel()


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
