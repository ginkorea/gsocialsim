import random

from gsocialsim.physical.geo_world import GeoWorld
from gsocialsim.types import AgentId


def test_geo_world_bbox_sampling():
    gw = GeoWorld(h3_resolution=5, bbox=(0.0, 0.0, 1.0, 1.0))
    rng = random.Random(123)
    loc = gw.ensure_agent(AgentId("A"), rng, ticks_per_day=96)
    assert 0.0 <= loc.lat <= 1.0
    assert 0.0 <= loc.lon <= 1.0


def test_geo_world_schedule_consistency():
    gw = GeoWorld(h3_resolution=5, bbox=(0.0, 0.0, 5.0, 5.0))
    rng = random.Random(42)
    gw.ensure_agent(AgentId("A"), rng, ticks_per_day=96)
    loc1 = gw.get_agent_location(AgentId("A"), tick_of_day=10, rng=rng, ticks_per_day=96)
    loc2 = gw.get_agent_location(AgentId("A"), tick_of_day=10, rng=rng, ticks_per_day=96)
    assert loc1.cell_id == loc2.cell_id
