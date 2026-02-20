import csv
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File

from ..core.datasources import (
    DataSourceInfo,
    ensure_sources_dir,
    inspect_csv,
    resolve_source_path,
    scan_sources,
    validate_csv,
)

router = APIRouter(prefix="/api/datasources", tags=["datasources"])

MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB


@router.get("", response_model=list[DataSourceInfo])
async def list_datasources():
    return scan_sources()


@router.get("/{filename}", response_model=DataSourceInfo)
async def get_datasource(filename: str):
    path = resolve_source_path(filename)
    if not path:
        raise HTTPException(404, f"Data source not found: {filename}")
    return inspect_csv(path)


@router.get("/{filename}/preview")
async def preview_datasource(filename: str, rows: int = 5):
    path = resolve_source_path(filename)
    if not path:
        raise HTTPException(404, f"Data source not found: {filename}")

    result: list[dict[str, str]] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= rows:
                break
            result.append(dict(row))
    return result


@router.post("/upload", response_model=DataSourceInfo)
async def upload_datasource(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(422, "File must be a .csv file")

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "File too large (max 50MB)")

    dest = ensure_sources_dir() / file.filename
    dest.write_bytes(content)

    ok, err = validate_csv(dest)
    if not ok:
        dest.unlink(missing_ok=True)
        raise HTTPException(422, f"Invalid CSV: {err}")

    return inspect_csv(dest)
