from __future__ import annotations
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class ParamType(str, Enum):
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    BOOL = "bool"


class ParamDef(BaseModel):
    name: str
    display_name: str
    group: str
    type: ParamType
    default: Any
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    description: str = ""
    choices: Optional[list[str]] = None


# All 96+ parameters organized by group
PARAM_SCHEMA: list[ParamDef] = [
    # --- Simulation ---
    ParamDef(name="ticks", display_name="Ticks", group="Simulation", type=ParamType.INT, default=96, min=1, max=9600, step=1, description="Number of simulation ticks (96 per day)"),
    ParamDef(name="agents", display_name="Agents", group="Simulation", type=ParamType.INT, default=100, min=2, max=10000, step=1, description="Number of agents in the simulation"),
    ParamDef(name="seed", display_name="Random Seed", group="Simulation", type=ParamType.INT, default=123, min=0, max=999999, step=1, description="Random number generator seed"),
    ParamDef(name="network_mode", display_name="Network Mode", group="Simulation", type=ParamType.STRING, default="groups", description="Network construction mode", choices=["groups", "random", "geo"]),
    ParamDef(name="avg_following", display_name="Avg Following", group="Simulation", type=ParamType.INT, default=12, min=1, max=500, step=1, description="Average number of accounts each agent follows"),
    ParamDef(name="analytics_mode", display_name="Analytics Mode", group="Simulation", type=ParamType.STRING, default="summary", description="Analytics logging mode", choices=["summary", "detailed"]),

    # --- Belief Dynamics ---
    ParamDef(name="inertia_rho", display_name="Inertia (rho)", group="Belief Dynamics", type=ParamType.FLOAT, default=0.85, min=0.0, max=1.0, step=0.01, description="Momentum decay factor [0,1]. Higher = more persistent momentum"),
    ParamDef(name="learning_rate_base", display_name="Learning Rate", group="Belief Dynamics", type=ParamType.FLOAT, default=0.10, min=0.001, max=1.0, step=0.01, description="Base learning rate for stance updates"),
    ParamDef(name="rebound_k", display_name="Rebound K", group="Belief Dynamics", type=ParamType.FLOAT, default=0.05, min=0.0, max=1.0, step=0.01, description="Spring constant pulling stance toward core value"),
    ParamDef(name="critical_velocity_threshold", display_name="Critical Velocity", group="Belief Dynamics", type=ParamType.FLOAT, default=0.1, min=0.0, max=1.0, step=0.01, description="Momentum threshold for nonlinear boost"),
    ParamDef(name="critical_kappa", display_name="Critical Kappa", group="Belief Dynamics", type=ParamType.FLOAT, default=2.0, min=0.1, max=10.0, step=0.1, description="Nonlinear gain multiplier above critical velocity"),
    ParamDef(name="evidence_decay_lambda", display_name="Evidence Decay", group="Belief Dynamics", type=ParamType.FLOAT, default=0.90, min=0.0, max=1.0, step=0.01, description="Evidence decay per tick"),
    ParamDef(name="evidence_threshold", display_name="Evidence Threshold", group="Belief Dynamics", type=ParamType.FLOAT, default=0.5, min=0.0, max=5.0, step=0.1, description="Minimum evidence to update belief"),
    ParamDef(name="trust_exponent_gamma", display_name="Trust Exponent", group="Belief Dynamics", type=ParamType.FLOAT, default=2.0, min=0.1, max=10.0, step=0.1, description="Trust scaling exponent (1=linear, >1=superlinear)"),
    ParamDef(name="habituation_alpha", display_name="Habituation Alpha", group="Belief Dynamics", type=ParamType.FLOAT, default=0.05, min=0.0, max=1.0, step=0.01, description="Habituation decay rate per exposure"),
    ParamDef(name="bounded_confidence_tau", display_name="Bounded Confidence", group="Belief Dynamics", type=ParamType.FLOAT, default=1.5, min=0.1, max=5.0, step=0.1, description="Stance difference threshold for rejection"),

    # --- Kernel ---
    ParamDef(name="mutual_trust_weight", display_name="Mutual Trust Weight", group="Kernel", type=ParamType.FLOAT, default=0.2, min=0.0, max=1.0, step=0.01, description="Weight for mutual connection trust boost"),
    ParamDef(name="offline_contacts_per_tick", display_name="Offline Contacts", group="Kernel", type=ParamType.INT, default=2, min=0, max=20, step=1, description="Offline contacts per tick"),
    ParamDef(name="offline_base_prob", display_name="Offline Base Prob", group="Kernel", type=ParamType.FLOAT, default=0.6, min=0.0, max=1.0, step=0.01, description="Base probability of offline interaction"),
    ParamDef(name="discovery_min_per_tick", display_name="Discovery Min", group="Kernel", type=ParamType.INT, default=1, min=0, max=20, step=1, description="Minimum discovery items per tick"),
    ParamDef(name="discovery_max_per_tick", display_name="Discovery Max", group="Kernel", type=ParamType.INT, default=3, min=0, max=50, step=1, description="Maximum discovery items per tick"),
    ParamDef(name="discovery_pool_size", display_name="Discovery Pool Size", group="Kernel", type=ParamType.INT, default=200, min=10, max=5000, step=10, description="Size of content discovery pool"),

    # --- Feed Algorithm ---
    ParamDef(name="recency_weight", display_name="Recency Weight", group="Feed Algorithm", type=ParamType.FLOAT, default=0.4, min=0.0, max=1.0, step=0.01, description="Weight for content recency in feed ranking"),
    ParamDef(name="engagement_weight", display_name="Engagement Weight", group="Feed Algorithm", type=ParamType.FLOAT, default=0.45, min=0.0, max=1.0, step=0.01, description="Weight for engagement score in feed ranking"),
    ParamDef(name="proximity_weight", display_name="Proximity Weight", group="Feed Algorithm", type=ParamType.FLOAT, default=0.1, min=0.0, max=1.0, step=0.01, description="Weight for social proximity in feed ranking"),
    ParamDef(name="mutual_weight", display_name="Mutual Weight", group="Feed Algorithm", type=ParamType.FLOAT, default=0.05, min=0.0, max=1.0, step=0.01, description="Weight for mutual connections in feed ranking"),

    # --- Broadcast Feed ---
    ParamDef(name="candidate_window_ticks", display_name="Candidate Window", group="Broadcast Feed", type=ParamType.INT, default=96, min=1, max=960, step=1, description="Lookback window in ticks for content candidates"),
    ParamDef(name="max_candidates", display_name="Max Candidates", group="Broadcast Feed", type=ParamType.INT, default=500, min=10, max=5000, step=10, description="Maximum candidate pool size"),
    ParamDef(name="max_shown", display_name="Max Shown", group="Broadcast Feed", type=ParamType.INT, default=20, min=1, max=100, step=1, description="Maximum items shown per feed refresh"),

    # --- Media Diet ---
    ParamDef(name="saturation_k", display_name="Saturation K", group="Media Diet", type=ParamType.FLOAT, default=3.0, min=0.1, max=20.0, step=0.1, description="Media saturation curve parameter (higher = faster saturation)"),
]


def get_param_groups() -> dict[str, list[ParamDef]]:
    groups: dict[str, list[ParamDef]] = {}
    for p in PARAM_SCHEMA:
        groups.setdefault(p.group, []).append(p)
    return groups


def get_defaults() -> dict[str, Any]:
    return {p.name: p.default for p in PARAM_SCHEMA}


# --- Request/Response Models ---

class DataSourceConfig(BaseModel):
    source_type: str = "csv"
    filename: Optional[str] = None
    path: Optional[str] = None  # resolved by backend before run


class SimulationConfig(BaseModel):
    ticks: int = 96
    agents: int = 100
    seed: int = 123
    network_mode: str = "groups"
    avg_following: int = 12
    analytics_mode: str = "summary"
    # Belief Dynamics
    influence_dynamics: dict[str, float] = Field(default_factory=dict)
    # Kernel
    kernel: dict[str, Any] = Field(default_factory=dict)
    # Feed Queue
    feed_queue: dict[str, float] = Field(default_factory=dict)
    # Broadcast Feed
    broadcast_feed: dict[str, Any] = Field(default_factory=dict)
    # Media Diet
    media_diet: dict[str, float] = Field(default_factory=dict)
    # Data Source
    data_source: Optional[DataSourceConfig] = None


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunInfo(BaseModel):
    id: str
    config: SimulationConfig
    status: RunStatus = RunStatus.PENDING
    created_at: str = ""
    ticks_completed: int = 0
    total_ticks: int = 0
    metrics: dict[str, Any] = Field(default_factory=dict)


class PresetConfig(BaseModel):
    id: Optional[str] = None
    name: str
    config: SimulationConfig


class StudyConfig(BaseModel):
    name: str
    base_config: SimulationConfig
    search_space: dict[str, dict[str, Any]]
    objectives: list[dict[str, str]]
    sampler: str = "tpe"
    n_trials: int = 20
    n_parallel: int = 1


class StudyStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class StudyInfo(BaseModel):
    id: str
    name: str
    status: StudyStatus = StudyStatus.RUNNING
    n_trials: int = 0
    completed_trials: int = 0
    best_value: Optional[float] = None
    best_params: dict[str, Any] = Field(default_factory=dict)
    trials: list[dict[str, Any]] = Field(default_factory=list)
