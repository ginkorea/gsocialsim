import uuid
from fastapi import APIRouter, HTTPException

from ..core.schemas import PARAM_SCHEMA, get_param_groups, get_defaults, PresetConfig

router = APIRouter(prefix="/api", tags=["params"])

# Set by main.py
store = None


@router.get("/params/schema")
async def get_schema():
    groups = get_param_groups()
    return {
        "groups": {
            name: [p.model_dump() for p in params]
            for name, params in groups.items()
        },
        "defaults": get_defaults(),
    }


@router.get("/presets")
async def list_presets():
    return await store.list_presets()


@router.post("/presets")
async def create_preset(preset: PresetConfig):
    preset_id = preset.id or uuid.uuid4().hex[:12]
    await store.create_preset(preset_id, preset.name, preset.config.model_dump())
    return {"id": preset_id, "name": preset.name}


@router.get("/presets/{preset_id}")
async def get_preset(preset_id: str):
    p = await store.get_preset(preset_id)
    if not p:
        raise HTTPException(status_code=404, detail="Preset not found")
    return p
