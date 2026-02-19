import csv
import json
from pathlib import Path
from typing import Any, Optional


def parse_state_json(run_dir: str) -> Optional[dict[str, Any]]:
    path = Path(run_dir) / "state.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def parse_analytics_csv(run_dir: str) -> list[dict[str, Any]]:
    path = Path(run_dir) / "analytics.csv"
    if not path.exists():
        return []
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def compute_polarization(leans: list[float]) -> float:
    if not leans:
        return 0.0
    n = len(leans)
    mean = sum(leans) / n
    variance = sum((x - mean) ** 2 for x in leans) / n
    return variance


def compute_metrics_from_tick_data(tick_history: list[dict]) -> dict[str, Any]:
    if not tick_history:
        return {}
    last = tick_history[-1]
    total_impressions = last.get("impressions", 0)
    total_consumed = last.get("consumed", 0)
    total_deltas = last.get("belief_deltas", 0)

    leans = last.get("leans", [])
    polarization = compute_polarization(leans)
    consumption_rate = total_consumed / max(total_impressions, 1)

    return {
        "total_impressions": total_impressions,
        "total_consumed": total_consumed,
        "total_belief_deltas": total_deltas,
        "polarization": round(polarization, 6),
        "consumption_rate": round(consumption_rate, 6),
        "final_tick": last.get("tick", 0),
    }
