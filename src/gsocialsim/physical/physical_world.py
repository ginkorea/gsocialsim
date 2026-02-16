from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import random

from gsocialsim.types import AgentId, TopicId

@dataclass
class Place:
    id: str
    size: int
    topic_bias: Dict[TopicId, float] = field(default_factory=dict)

class LifePhase(Enum):
    SLEEP = "sleep"
    WORK = "work"
    LEISURE = "leisure"


@dataclass
class Schedule:
    # Mapping of tick-of-day to Place id
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
class PhysicalWorld:
    places: Dict[str, Place] = field(default_factory=dict)
    schedules: Dict[AgentId, Schedule] = field(default_factory=dict)
    enable_life_cycle: bool = True
    grid_size: int = 10
    life_profile: LifeProfile = field(default_factory=LifeProfile)
    agent_homes: Dict[AgentId, str] = field(default_factory=dict)
    agent_workplaces: Dict[AgentId, str] = field(default_factory=dict)
    agent_social_factors: Dict[AgentId, float] = field(default_factory=dict)

    def ensure_grid(self) -> None:
        if self.places:
            return
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                pid = f"{x}_{y}"
                self.places[pid] = Place(id=pid, size=10)

    def _clamp_tick(self, t: int, ticks_per_day: int) -> int:
        return max(0, min(ticks_per_day - 1, int(t)))

    def _sample_tick(self, rng: random.Random, mean: int, std: float, ticks_per_day: int) -> int:
        return self._clamp_tick(int(round(rng.gauss(mean, std))), ticks_per_day)

    def _sample_duration(self, rng: random.Random, mean: int, std: float, ticks_per_day: int) -> int:
        return max(1, min(ticks_per_day, int(round(rng.gauss(mean, std)))))

    def _pick_place(self, rng: random.Random) -> str:
        x = rng.randrange(self.grid_size)
        y = rng.randrange(self.grid_size)
        return f"{x}_{y}"

    def ensure_agent(self, agent_id: AgentId, rng: random.Random, ticks_per_day: int) -> None:
        if agent_id in self.schedules:
            return
        self.ensure_grid()
        if agent_id not in self.agent_homes:
            self.agent_homes[agent_id] = self._pick_place(rng)
        if agent_id not in self.agent_workplaces:
            self.agent_workplaces[agent_id] = self._pick_place(rng)
        if agent_id not in self.agent_social_factors:
            sf = rng.gauss(self.life_profile.social_time_factor_mean, self.life_profile.social_time_factor_std)
            self.agent_social_factors[agent_id] = max(0.1, min(1.0, sf))
        self.schedules[agent_id] = self._build_schedule(rng, ticks_per_day, agent_id)

    def _build_schedule(self, rng: random.Random, ticks_per_day: int, agent_id: AgentId) -> Schedule:
        prof = self.life_profile
        sleep_start = self._sample_tick(rng, prof.sleep_start_mean, prof.sleep_start_std, ticks_per_day)
        sleep_dur = self._sample_duration(rng, prof.sleep_duration_mean, prof.sleep_duration_std, ticks_per_day)
        work_start = self._sample_tick(rng, prof.work_start_mean, prof.work_start_std, ticks_per_day)
        work_dur = self._sample_duration(rng, prof.work_duration_mean, prof.work_duration_std, ticks_per_day)

        schedule = Schedule()
        home = self.agent_homes[agent_id]
        work = self.agent_workplaces[agent_id]

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
                schedule.daily_plan[t] = self._pick_place(rng)
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
        """Finds groups of agents in the same place at the same time."""
        agents_by_place: Dict[str, List[AgentId]] = {}
        for agent_id, schedule in self.schedules.items():
            current_place_id = schedule.daily_plan.get(tick_of_day)
            if current_place_id:
                agents_by_place.setdefault(current_place_id, []).append(agent_id)

        # Return groups of 2 or more agents
        return [group for group in agents_by_place.values() if len(group) > 1]
