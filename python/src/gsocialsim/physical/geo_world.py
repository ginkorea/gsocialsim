from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import math
import random
import bisect

from gsocialsim.types import AgentId


try:
    import h3  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    h3 = None


@dataclass
class GeoLocation:
    cell_id: str
    lat: float
    lon: float
    country: Optional[str] = None
    admin1: Optional[str] = None
    admin2: Optional[str] = None


class LifePhase(Enum):
    SLEEP = "sleep"
    WORK = "work"
    LEISURE = "leisure"


@dataclass
class Schedule:
    # Mapping of tick-of-day to cell id
    daily_plan: Dict[int, str] = field(default_factory=dict)
    # Mapping of tick-of-day to life phase
    daily_phase: Dict[int, LifePhase] = field(default_factory=dict)


@dataclass
class LifeProfile:
    # All values in ticks (15 min each)
    sleep_start_mean: int = 88     # 22:00
    sleep_start_std: float = 4.0
    sleep_duration_mean: int = 32  # 8 hours
    sleep_duration_std: float = 2.0
    work_start_mean: int = 36      # 09:00
    work_start_std: float = 4.0
    work_duration_mean: int = 32   # 8 hours
    work_duration_std: float = 2.0
    social_time_factor_mean: float = 0.6
    social_time_factor_std: float = 0.2
    leisure_wander_prob: float = 0.2


@dataclass
class GeoPopulationSampler:
    h3_resolution: int
    bbox: Optional[Tuple[float, float, float, float]] = None  # (min_lat, min_lon, max_lat, max_lon)
    cell_weights: Dict[str, float] = field(default_factory=dict)
    cell_meta: Dict[str, Dict[str, str]] = field(default_factory=dict)
    total_weight: float = 0.0
    min_population: float = 1.0
    max_population: float = 1.0e12
    _cells: List[str] = field(default_factory=list, init=False)
    _cdf: List[float] = field(default_factory=list, init=False)

    def load_h3_population_csv(self, path: str) -> None:
        """
        Load pre-aggregated population weights by H3 cell.
        Expected columns: h3_cell, population|weight, country, admin1, admin2 (optional)
        """
        import csv

        self.cell_weights.clear()
        self.cell_meta.clear()
        self.total_weight = 0.0
        self._cells = []
        self._cdf = []

        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cell = (row.get("h3_cell") or row.get("cell") or "").strip()
                if not cell:
                    continue
                w_raw = row.get("population") or row.get("weight") or row.get("pop")
                try:
                    w = float(w_raw)
                except Exception:
                    continue
                if w <= 0:
                    continue
                if w < self.min_population or w > self.max_population:
                    continue
                self.cell_weights[cell] = self.cell_weights.get(cell, 0.0) + w
                self.total_weight += w
                meta = {
                    "country": (row.get("country") or "").strip(),
                    "admin1": (row.get("admin1") or "").strip(),
                    "admin2": (row.get("admin2") or "").strip(),
                }
                self.cell_meta[cell] = meta
        self._build_sampler()

    def _build_sampler(self) -> None:
        self._cells = list(self.cell_weights.keys())
        self._cdf = []
        acc = 0.0
        for cell in self._cells:
            acc += float(self.cell_weights[cell])
            self._cdf.append(acc)
        self.total_weight = acc

    def _fallback_cell_size_deg(self) -> float:
        # Rough mapping from resolution -> degrees for fallback grid.
        return 180.0 / (2 ** (self.h3_resolution + 2))

    def _fallback_cell_id(self, lat: float, lon: float) -> str:
        if self.bbox:
            min_lat, min_lon, max_lat, max_lon = self.bbox
        else:
            min_lat, min_lon, max_lat, max_lon = -90.0, -180.0, 90.0, 180.0
        size = self._fallback_cell_size_deg()
        i = int(math.floor((lat - min_lat) / size))
        j = int(math.floor((lon - min_lon) / size))
        return f"F{self.h3_resolution}_{i}_{j}"

    def latlon_to_cell(self, lat: float, lon: float) -> str:
        if h3 is not None:
            try:
                return h3.latlng_to_cell(lat, lon, self.h3_resolution)
            except Exception:
                pass
        return self._fallback_cell_id(lat, lon)

    def cell_to_point(self, cell_id: str, rng: random.Random) -> Tuple[float, float]:
        if h3 is not None and cell_id and not cell_id.startswith("F"):
            try:
                lat, lon = h3.cell_to_latlng(cell_id)
                return float(lat), float(lon)
            except Exception:
                pass
        # Fallback: return center of the implicit grid cell.
        if self.bbox:
            min_lat, min_lon, max_lat, max_lon = self.bbox
        else:
            min_lat, min_lon, max_lat, max_lon = -90.0, -180.0, 90.0, 180.0
        size = self._fallback_cell_size_deg()
        try:
            _, i_str, j_str = cell_id.split("_")
            i = int(i_str)
            j = int(j_str)
        except Exception:
            # random point inside bbox
            lat = rng.uniform(min_lat, max_lat)
            lon = rng.uniform(min_lon, max_lon)
            return lat, lon
        lat = min_lat + (i + 0.5) * size
        lon = min_lon + (j + 0.5) * size
        return max(-90.0, min(90.0, lat)), max(-180.0, min(180.0, lon))

    def sample_cell(self, rng: random.Random) -> str:
        if self._cdf and self.total_weight > 0.0:
            r = rng.random() * self.total_weight
            idx = bisect.bisect_left(self._cdf, r)
            if idx >= len(self._cells):
                idx = len(self._cells) - 1
            return self._cells[idx]

        # Uniform sample within bbox if no weights loaded.
        if self.bbox:
            min_lat, min_lon, max_lat, max_lon = self.bbox
        else:
            min_lat, min_lon, max_lat, max_lon = -90.0, -180.0, 90.0, 180.0
        lat = rng.uniform(min_lat, max_lat)
        lon = rng.uniform(min_lon, max_lon)
        return self.latlon_to_cell(lat, lon)

    def cell_metadata(self, cell_id: str) -> Dict[str, str]:
        return self.cell_meta.get(cell_id, {})


@dataclass
class GeoWorld:
    enable_life_cycle: bool = True
    h3_resolution: int = 6
    bbox: Optional[Tuple[float, float, float, float]] = None
    agent_scale: int = 10  # each agent represents this many people (default)
    population_csv_path: Optional[str] = "data/geo/h3_population.csv"
    life_profile: LifeProfile = field(default_factory=LifeProfile)
    schedules: Dict[AgentId, Schedule] = field(default_factory=dict)
    agent_home: Dict[AgentId, str] = field(default_factory=dict)
    agent_work: Dict[AgentId, str] = field(default_factory=dict)
    agent_home_geo: Dict[AgentId, GeoLocation] = field(default_factory=dict)
    agent_social_factors: Dict[AgentId, float] = field(default_factory=dict)
    population: GeoPopulationSampler = field(init=False)

    def __post_init__(self) -> None:
        self.population = GeoPopulationSampler(h3_resolution=self.h3_resolution, bbox=self.bbox)

    def set_resolution(self, res: int) -> None:
        self.h3_resolution = int(res)
        self.population.h3_resolution = int(res)

    def set_agent_scale(self, scale: int) -> None:
        try:
            self.agent_scale = max(1, int(scale))
        except Exception:
            self.agent_scale = 1

    def set_bbox(self, bbox: Optional[Tuple[float, float, float, float]]) -> None:
        self.bbox = bbox
        self.population.bbox = bbox

    def set_population_filter(self, *, min_population: float = 1.0, max_population: float = 1.0e12) -> None:
        self.population.min_population = float(min_population)
        self.population.max_population = float(max_population)

    def load_population_csv(self, path: Optional[str] = None) -> bool:
        import os
        p = path or self.population_csv_path
        if not p:
            return False
        if not os.path.exists(p):
            return False
        self.population.load_h3_population_csv(p)
        self.population_csv_path = p
        return True

    def _clamp_tick(self, t: int, ticks_per_day: int) -> int:
        return max(0, min(ticks_per_day - 1, int(t)))

    def _sample_tick(self, rng: random.Random, mean: int, std: float, ticks_per_day: int) -> int:
        return self._clamp_tick(int(round(rng.gauss(mean, std))), ticks_per_day)

    def _sample_duration(self, rng: random.Random, mean: int, std: float, ticks_per_day: int) -> int:
        return max(1, min(ticks_per_day, int(round(rng.gauss(mean, std)))))

    def _sample_location(self, rng: random.Random) -> GeoLocation:
        cell = self.population.sample_cell(rng)
        lat, lon = self.population.cell_to_point(cell, rng)
        meta = self.population.cell_metadata(cell)
        return GeoLocation(
            cell_id=cell,
            lat=lat,
            lon=lon,
            country=meta.get("country") or None,
            admin1=meta.get("admin1") or None,
            admin2=meta.get("admin2") or None,
        )

    def ensure_agent(self, agent_id: AgentId, rng: random.Random, ticks_per_day: int) -> GeoLocation:
        if agent_id in self.schedules:
            # return current home location if we have it
            home = self.agent_home.get(agent_id)
            if home:
                lat, lon = self.population.cell_to_point(home, rng)
                return GeoLocation(cell_id=home, lat=lat, lon=lon)
            return self._sample_location(rng)

        home_loc = self._sample_location(rng)
        work_loc = self._sample_location(rng)

        self.agent_home[agent_id] = home_loc.cell_id
        self.agent_work[agent_id] = work_loc.cell_id
        self.agent_home_geo[agent_id] = home_loc

        sf = rng.gauss(self.life_profile.social_time_factor_mean, self.life_profile.social_time_factor_std)
        self.agent_social_factors[agent_id] = max(0.1, min(1.0, sf))

        self.schedules[agent_id] = self._build_schedule(rng, ticks_per_day, agent_id)
        return home_loc

    def get_agent_home_location(self, agent_id: AgentId, rng: random.Random) -> GeoLocation:
        loc = self.agent_home_geo.get(agent_id)
        if loc:
            return loc
        home = self.agent_home.get(agent_id)
        if home:
            lat, lon = self.population.cell_to_point(home, rng)
            return GeoLocation(cell_id=home, lat=lat, lon=lon)
        return self._sample_location(rng)

    def get_agent_location(
        self,
        agent_id: AgentId,
        *,
        tick_of_day: Optional[int],
        rng: random.Random,
        ticks_per_day: int,
    ) -> GeoLocation:
        if tick_of_day is None:
            return self.get_agent_home_location(agent_id, rng)
        self.ensure_agent(agent_id, rng, ticks_per_day)
        schedule = self.schedules.get(agent_id)
        if not schedule:
            return self.get_agent_home_location(agent_id, rng)
        cell = schedule.daily_plan.get(tick_of_day) or self.agent_home.get(agent_id)
        if cell:
            lat, lon = self.population.cell_to_point(cell, rng)
            return GeoLocation(cell_id=cell, lat=lat, lon=lon)
        return self.get_agent_home_location(agent_id, rng)

    def _build_schedule(self, rng: random.Random, ticks_per_day: int, agent_id: AgentId) -> Schedule:
        prof = self.life_profile
        sleep_start = self._sample_tick(rng, prof.sleep_start_mean, prof.sleep_start_std, ticks_per_day)
        sleep_dur = self._sample_duration(rng, prof.sleep_duration_mean, prof.sleep_duration_std, ticks_per_day)
        work_start = self._sample_tick(rng, prof.work_start_mean, prof.work_start_std, ticks_per_day)
        work_dur = self._sample_duration(rng, prof.work_duration_mean, prof.work_duration_std, ticks_per_day)

        schedule = Schedule()
        home = self.agent_home[agent_id]
        work = self.agent_work[agent_id]

        def in_block(t: int, start: int, dur: int) -> bool:
            end = (start + dur) % ticks_per_day
            if dur >= ticks_per_day:
                return True
            if start <= end:
                return start <= t < end
            return t >= start or t < end

        for t in range(ticks_per_day):
            if in_block(t, sleep_start, sleep_dur):
                schedule.daily_phase[t] = LifePhase.SLEEP
                schedule.daily_plan[t] = home
                continue
            if in_block(t, work_start, work_dur):
                schedule.daily_phase[t] = LifePhase.WORK
                schedule.daily_plan[t] = work
                continue
            schedule.daily_phase[t] = LifePhase.LEISURE
            if rng.random() < prof.leisure_wander_prob:
                schedule.daily_plan[t] = self.population.sample_cell(rng)
            else:
                schedule.daily_plan[t] = home

        return schedule

    def get_phase(self, agent_id: AgentId, tick_of_day: int, rng: random.Random, ticks_per_day: int) -> LifePhase:
        if not self.enable_life_cycle:
            return LifePhase.LEISURE
        self.ensure_agent(agent_id, rng, ticks_per_day)
        schedule = self.schedules.get(agent_id)
        if not schedule:
            return LifePhase.LEISURE
        return schedule.daily_phase.get(tick_of_day, LifePhase.LEISURE)

    def get_available_minutes(
        self,
        agent_id: AgentId,
        tick_of_day: int,
        minutes_per_tick: float,
        rng: random.Random,
        ticks_per_day: int,
    ) -> float:
        if not self.enable_life_cycle:
            return float(minutes_per_tick)

        phase = self.get_phase(agent_id, tick_of_day, rng, ticks_per_day)
        base = 0.0
        if phase == LifePhase.SLEEP:
            base = 0.0
        elif phase == LifePhase.WORK:
            base = 2.0
        else:
            base = float(minutes_per_tick)

        sf = float(self.agent_social_factors.get(agent_id, 0.6))
        return max(0.0, base * sf)

    def get_co_located_agents(self, tick_of_day: int) -> List[List[AgentId]]:
        agents_by_cell: Dict[str, List[AgentId]] = {}
        for agent_id, schedule in self.schedules.items():
            current_cell = schedule.daily_plan.get(tick_of_day)
            if current_cell:
                agents_by_cell.setdefault(current_cell, []).append(agent_id)
        return [group for group in agents_by_cell.values() if len(group) > 1]

    def sample_demographics(self, rng: random.Random) -> Dict[str, str]:
        # Global fallback. Override with real data when available.
        sex = rng.choices(["female", "male", "nonbinary"], weights=[0.49, 0.49, 0.02], k=1)[0]
        age_group = rng.choices(
            ["0-17", "18-29", "30-44", "45-64", "65+"],
            weights=[0.30, 0.22, 0.22, 0.20, 0.06],
            k=1,
        )[0]
        return {"sex": sex, "age_group": age_group}

    def sample_group_affiliations(self, rng: random.Random) -> Dict[str, float]:
        groups = {}
        for g in ("religious", "union", "military", "immigrant", "student", "parent", "community_org", "professional"):
            if rng.random() < 0.25:
                groups[g] = max(0.0, min(1.0, rng.gauss(0.6, 0.2)))
        return groups
