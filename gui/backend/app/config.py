from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cpp_binary: str = ""
    stimuli_csv: str = ""
    db_path: str = "data/gsocialsim.db"
    run_data_dir: str = "data/runs"
    max_concurrent_runs: int = 4

    model_config = {"env_prefix": "GSOCIALSIM_"}

    def resolve_cpp_binary(self) -> str:
        if self.cpp_binary:
            return self.cpp_binary
        # Auto-detect from relative path
        candidates = [
            Path(__file__).resolve().parent.parent.parent.parent / "cpp" / "build" / "gsocialsim_cpp",
            Path.cwd() / "cpp" / "build" / "gsocialsim_cpp",
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        return "gsocialsim_cpp"

    def resolve_stimuli_csv(self) -> str:
        if self.stimuli_csv:
            return self.stimuli_csv
        candidates = [
            Path(__file__).resolve().parent.parent.parent.parent / "data" / "stimuli_test.csv",
            Path.cwd() / "data" / "stimuli_test.csv",
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        return ""


settings = Settings()
