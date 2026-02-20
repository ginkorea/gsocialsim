import json
import aiosqlite
from pathlib import Path
from typing import Any, Optional


class Store:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._db: Optional[aiosqlite.Connection] = None

    async def init(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._db = await aiosqlite.connect(self.db_path)
        await self._db.execute("PRAGMA journal_mode=WAL")
        await self._db.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY,
                config TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                ticks_completed INTEGER DEFAULT 0,
                total_ticks INTEGER DEFAULT 0,
                metrics TEXT DEFAULT '{}'
            );
            CREATE TABLE IF NOT EXISTS presets (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                config TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS studies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                config TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'running',
                best_params TEXT DEFAULT '{}',
                best_value REAL,
                completed_trials INTEGER DEFAULT 0,
                n_trials INTEGER DEFAULT 0
            );
        """)
        await self._db.commit()

    async def close(self):
        if self._db:
            await self._db.close()

    # --- Runs ---

    async def create_run(self, run_id: str, config: dict, created_at: str, total_ticks: int):
        await self._db.execute(
            "INSERT INTO runs (id, config, status, created_at, total_ticks) VALUES (?, ?, 'pending', ?, ?)",
            (run_id, json.dumps(config), created_at, total_ticks),
        )
        await self._db.commit()

    async def update_run_status(self, run_id: str, status: str, ticks_completed: int = 0, metrics: Optional[dict] = None):
        if metrics:
            await self._db.execute(
                "UPDATE runs SET status=?, ticks_completed=?, metrics=? WHERE id=?",
                (status, ticks_completed, json.dumps(metrics), run_id),
            )
        else:
            await self._db.execute(
                "UPDATE runs SET status=?, ticks_completed=? WHERE id=?",
                (status, ticks_completed, run_id),
            )
        await self._db.commit()

    async def get_run(self, run_id: str) -> Optional[dict]:
        async with self._db.execute("SELECT * FROM runs WHERE id=?", (run_id,)) as cur:
            row = await cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0], "config": json.loads(row[1]), "status": row[2],
                "created_at": row[3], "ticks_completed": row[4],
                "total_ticks": row[5], "metrics": json.loads(row[6]),
            }

    async def list_runs(self) -> list[dict]:
        runs = []
        async with self._db.execute("SELECT id, config, status, created_at, ticks_completed, total_ticks, metrics FROM runs ORDER BY created_at DESC") as cur:
            async for row in cur:
                runs.append({
                    "id": row[0], "config": json.loads(row[1]), "status": row[2],
                    "created_at": row[3], "ticks_completed": row[4],
                    "total_ticks": row[5], "metrics": json.loads(row[6]),
                })
        return runs

    async def delete_run(self, run_id: str):
        await self._db.execute("DELETE FROM runs WHERE id=?", (run_id,))
        await self._db.commit()

    # --- Presets ---

    async def create_preset(self, preset_id: str, name: str, config: dict):
        await self._db.execute(
            "INSERT OR REPLACE INTO presets (id, name, config) VALUES (?, ?, ?)",
            (preset_id, name, json.dumps(config)),
        )
        await self._db.commit()

    async def get_preset(self, preset_id: str) -> Optional[dict]:
        async with self._db.execute("SELECT * FROM presets WHERE id=?", (preset_id,)) as cur:
            row = await cur.fetchone()
            if not row:
                return None
            return {"id": row[0], "name": row[1], "config": json.loads(row[2])}

    async def list_presets(self) -> list[dict]:
        presets = []
        async with self._db.execute("SELECT id, name, config FROM presets ORDER BY name") as cur:
            async for row in cur:
                presets.append({"id": row[0], "name": row[1], "config": json.loads(row[2])})
        return presets

    # --- Studies ---

    async def create_study(self, study_id: str, name: str, config: dict, n_trials: int):
        await self._db.execute(
            "INSERT INTO studies (id, name, config, status, n_trials) VALUES (?, ?, ?, 'running', ?)",
            (study_id, name, json.dumps(config), n_trials),
        )
        await self._db.commit()

    async def update_study(self, study_id: str, status: str, completed_trials: int = 0,
                           best_value: Optional[float] = None, best_params: Optional[dict] = None):
        await self._db.execute(
            "UPDATE studies SET status=?, completed_trials=?, best_value=?, best_params=? WHERE id=?",
            (status, completed_trials, best_value, json.dumps(best_params or {}), study_id),
        )
        await self._db.commit()

    async def get_study(self, study_id: str) -> Optional[dict]:
        async with self._db.execute("SELECT * FROM studies WHERE id=?", (study_id,)) as cur:
            row = await cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0], "name": row[1], "config": json.loads(row[2]),
                "status": row[3], "best_params": json.loads(row[4]),
                "best_value": row[5], "completed_trials": row[6], "n_trials": row[7],
            }

    async def list_studies(self) -> list[dict]:
        studies = []
        async with self._db.execute("SELECT id, name, status, completed_trials, n_trials, best_value FROM studies ORDER BY id DESC") as cur:
            async for row in cur:
                studies.append({
                    "id": row[0], "name": row[1], "status": row[2],
                    "completed_trials": row[3], "n_trials": row[4], "best_value": row[5],
                })
        return studies
