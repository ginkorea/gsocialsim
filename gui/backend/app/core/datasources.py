import csv
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

# Project root: five levels up from this file (core → app → backend → gui → project)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
SOURCES_DIR = _PROJECT_ROOT / "data" / "sources"

REQUIRED_COLUMNS = {"tick", "source", "content_text", "topic"}


class DataSourceInfo(BaseModel):
    filename: str
    path: str
    size_bytes: int
    row_count: int
    tick_min: int
    tick_max: int
    columns: list[str]
    source_type: str = "csv"


def ensure_sources_dir() -> Path:
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    return SOURCES_DIR


def inspect_csv(path: Path) -> DataSourceInfo:
    """Read a CSV and extract metadata."""
    size_bytes = path.stat().st_size
    row_count = 0
    tick_min = float("inf")
    tick_max = float("-inf")
    columns: list[str] = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        columns = list(reader.fieldnames or [])
        for row in reader:
            row_count += 1
            tick_raw = row.get("tick", "").strip()
            if tick_raw:
                try:
                    t = int(float(tick_raw))
                    tick_min = min(tick_min, t)
                    tick_max = max(tick_max, t)
                except (ValueError, TypeError):
                    pass

    if tick_min == float("inf"):
        tick_min = 0
    if tick_max == float("-inf"):
        tick_max = 0

    return DataSourceInfo(
        filename=path.name,
        path=str(path),
        size_bytes=size_bytes,
        row_count=row_count,
        tick_min=int(tick_min),
        tick_max=int(tick_max),
        columns=columns,
    )


def validate_csv(path: Path) -> tuple[bool, Optional[str]]:
    """Check that required columns exist in the CSV header."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header is None:
                return False, "CSV file is empty"
            header_lower = {col.strip().lower() for col in header}
            missing = REQUIRED_COLUMNS - header_lower
            if missing:
                return False, f"Missing required columns: {', '.join(sorted(missing))}"
            return True, None
    except Exception as e:
        return False, str(e)


def scan_sources() -> list[DataSourceInfo]:
    """Scan known locations for CSV data source files."""
    seen: set[str] = set()
    results: list[DataSourceInfo] = []

    def _add(p: Path):
        resolved = str(p.resolve())
        if resolved in seen:
            return
        if not p.exists() or not p.is_file():
            return
        seen.add(resolved)
        try:
            info = inspect_csv(p)
            results.append(info)
        except Exception:
            pass

    # Primary: data/sources/ directory
    if SOURCES_DIR.exists():
        for f in sorted(SOURCES_DIR.glob("*.csv")):
            _add(f)

    # Legacy locations
    _add(_PROJECT_ROOT / "data" / "stimuli_test.csv")
    _add(_PROJECT_ROOT / "stimuli.csv")

    return results


def resolve_source_path(filename: str) -> Optional[Path]:
    """Find the absolute path for a data source filename."""
    candidates = [
        SOURCES_DIR / filename,
        _PROJECT_ROOT / "data" / filename,
        _PROJECT_ROOT / filename,
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            return c.resolve()
    return None
