import uuid
from fastapi import APIRouter, HTTPException

from ..core.schemas import StudyConfig, StudyInfo

router = APIRouter(prefix="/api/studies", tags=["tuning"])

# Set by main.py
store = None
tuning_engine = None


@router.post("", response_model=StudyInfo)
async def create_study(config: StudyConfig):
    study_id = uuid.uuid4().hex[:12]
    study = StudyInfo(
        id=study_id,
        name=config.name,
        n_trials=config.n_trials,
    )
    await store.create_study(study_id, config.name, config.model_dump(), config.n_trials)
    # Start tuning in background
    import asyncio
    asyncio.create_task(tuning_engine.run_study(study_id, config))
    return study


@router.get("")
async def list_studies():
    return await store.list_studies()


@router.get("/{study_id}")
async def get_study(study_id: str):
    s = await store.get_study(study_id)
    if not s:
        raise HTTPException(status_code=404, detail="Study not found")
    return s
