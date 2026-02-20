from fastapi import APIRouter, HTTPException

from ..core.schemas import SimulationConfig, RunInfo
from ..core.parser import compute_metrics_from_tick_data
from ..core.datasources import resolve_source_path

router = APIRouter(prefix="/api/runs", tags=["runs"])

# These will be set by main.py at startup
runner = None
store = None


@router.post("", response_model=RunInfo)
async def create_run(config: SimulationConfig):
    # Resolve data source filename to absolute path
    if config.data_source and config.data_source.filename:
        resolved = resolve_source_path(config.data_source.filename)
        if not resolved:
            raise HTTPException(422, f"Data source file not found: {config.data_source.filename}")
        config.data_source.path = str(resolved)

    run = await runner.start_run(config)
    await store.create_run(run.id, config.model_dump(), run.created_at, config.ticks)
    return run


@router.get("")
async def list_runs():
    return await store.list_runs()


@router.get("/{run_id}")
async def get_run(run_id: str):
    run = runner.get_run(run_id)
    if run:
        return run
    db_run = await store.get_run(run_id)
    if db_run:
        return db_run
    raise HTTPException(status_code=404, detail="Run not found")


@router.get("/{run_id}/results")
async def get_results(run_id: str):
    results = runner.get_results(run_id)
    if results:
        return results
    raise HTTPException(status_code=404, detail="Results not found")


@router.delete("/{run_id}")
async def cancel_run(run_id: str):
    await runner.cancel_run(run_id)
    await store.update_run_status(run_id, "cancelled")
    return {"status": "cancelled"}
