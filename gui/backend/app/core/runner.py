import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, AsyncIterator, Optional

from .schemas import SimulationConfig, RunInfo, RunStatus


class SimulationRunner:
    def __init__(self, cpp_binary: str, stimuli_csv: str, data_dir: str, max_concurrent: int = 4):
        self.cpp_binary = cpp_binary
        self.stimuli_csv = stimuli_csv
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._processes: dict[str, asyncio.subprocess.Process] = {}
        self._runs: dict[str, RunInfo] = {}

    def _build_command(self, config: SimulationConfig, config_path: str, run_dir: str) -> list[str]:
        cmd = [
            self.cpp_binary,
            "--ticks", str(config.ticks),
            "--agents", str(config.agents),
            "--seed", str(config.seed),
            "--network-mode", config.network_mode,
            "--avg-following", str(config.avg_following),
            "--stream-json",
            "--export-state",
            "--export-dir", run_dir,
            "--config", config_path,
        ]
        # Per-run data source takes priority, then global default
        stimuli_path = ""
        if config.data_source and config.data_source.path:
            stimuli_path = config.data_source.path
        elif self.stimuli_csv:
            stimuli_path = self.stimuli_csv

        if stimuli_path:
            cmd.extend(["--stimuli", stimuli_path])
        return cmd

    def _write_config_json(self, config: SimulationConfig, path: str):
        cfg: dict[str, Any] = {}
        if config.influence_dynamics:
            cfg["influence_dynamics"] = config.influence_dynamics
        if config.kernel:
            cfg["kernel"] = config.kernel
        if config.feed_queue:
            cfg["feed_queue"] = config.feed_queue
        if config.broadcast_feed:
            cfg["broadcast_feed"] = config.broadcast_feed
        Path(path).write_text(json.dumps(cfg, indent=2))

    async def start_run(self, config: SimulationConfig) -> RunInfo:
        run_id = uuid.uuid4().hex[:12]
        run_dir = str(self.data_dir / run_id)
        Path(run_dir).mkdir(parents=True, exist_ok=True)

        config_path = str(Path(run_dir) / "config.json")
        self._write_config_json(config, config_path)

        cmd = self._build_command(config, config_path, run_dir)

        run = RunInfo(
            id=run_id,
            config=config,
            status=RunStatus.PENDING,
            created_at=datetime.now(timezone.utc).isoformat(),
            total_ticks=config.ticks,
        )
        self._runs[run_id] = run
        return run

    async def _launch(self, run_id: str) -> asyncio.subprocess.Process:
        run = self._runs[run_id]
        run_dir = str(self.data_dir / run_id)
        config_path = str(Path(run_dir) / "config.json")
        cmd = self._build_command(run.config, config_path, run_dir)

        await self._semaphore.acquire()
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            self._processes[run_id] = proc
            run.status = RunStatus.RUNNING
            return proc
        except Exception:
            self._semaphore.release()
            raise

    async def stream_output(self, run_id: str) -> AsyncIterator[dict]:
        proc = await self._launch(run_id)
        run = self._runs[run_id]
        try:
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break
                text = line.decode("utf-8", errors="replace").strip()
                if not text or not text.startswith("{"):
                    continue
                try:
                    data = json.loads(text)
                    run.ticks_completed = data.get("tick", 0)
                    yield data
                except json.JSONDecodeError:
                    continue

            await proc.wait()
            if proc.returncode == 0:
                run.status = RunStatus.COMPLETED
            else:
                stderr = await proc.stderr.read()
                run.status = RunStatus.FAILED
                run.metrics["error"] = stderr.decode("utf-8", errors="replace")[:500]
        except asyncio.CancelledError:
            proc.terminate()
            run.status = RunStatus.CANCELLED
        finally:
            self._processes.pop(run_id, None)
            self._semaphore.release()

    async def cancel_run(self, run_id: str):
        proc = self._processes.get(run_id)
        if proc:
            proc.terminate()
            run = self._runs.get(run_id)
            if run:
                run.status = RunStatus.CANCELLED

    def get_run(self, run_id: str) -> Optional[RunInfo]:
        return self._runs.get(run_id)

    def get_results(self, run_id: str) -> Optional[dict]:
        state_path = self.data_dir / run_id / "state.json"
        if state_path.exists():
            return json.loads(state_path.read_text())
        return None

    def list_runs(self) -> list[RunInfo]:
        return list(self._runs.values())
