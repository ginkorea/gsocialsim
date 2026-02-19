import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..core.parser import compute_metrics_from_tick_data

router = APIRouter()

# Set by main.py
runner = None
store = None
tuning_engine = None


@router.websocket("/ws/run/{run_id}")
async def ws_run(websocket: WebSocket, run_id: str):
    await websocket.accept()
    tick_history = []
    try:
        async for tick_data in runner.stream_output(run_id):
            tick_history.append(tick_data)
            await websocket.send_json({"type": "tick", "data": tick_data})

        metrics = compute_metrics_from_tick_data(tick_history)
        run = runner.get_run(run_id)
        status = run.status.value if run else "completed"
        await store.update_run_status(run_id, status, len(tick_history), metrics)
        await websocket.send_json({"type": "complete", "metrics": metrics, "status": status})
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
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
