from dataclasses import dataclass, field
from typing import Dict, List
from gsocialsim.types import AgentId, TopicId

@dataclass
class Place:
    id: str
    size: int
    topic_bias: Dict[TopicId, float] = field(default_factory=dict)

@dataclass
class Schedule:
    # A simple schedule mapping a tick of the day to a Place id
    daily_plan: Dict[int, str] = field(default_factory=dict)

@dataclass
class PhysicalWorld:
    places: Dict[str, Place] = field(default_factory=dict)
    schedules: Dict[AgentId, Schedule] = field(default_factory=dict)

    def get_co_located_agents(self, tick_of_day: int) -> List[List[AgentId]]:
        """Finds groups of agents in the same place at the same time."""
        agents_by_place: Dict[str, List[AgentId]] = {}
        for agent_id, schedule in self.schedules.items():
            current_place_id = schedule.daily_plan.get(tick_of_day)
            if current_place_id:
                agents_by_place.setdefault(current_place_id, []).append(agent_id)
        
        # Return groups of 2 or more agents
        return [group for group in agents_by_place.values() if len(group) > 1]
