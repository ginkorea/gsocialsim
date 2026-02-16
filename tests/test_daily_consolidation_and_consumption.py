import pytest

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.stimuli.content_item import ContentItem


def _seed_agent_with_topic(agent: Agent, topic: str):
    agent.budgets.action_bank = 9999.0
    agent.budgets.action_budget = 9999.0
    agent.beliefs.update(TopicId(topic), stance=0.0, confidence=0.5, salience=0.2, knowledge=0.2)


def test_day_boundary_triggers_dream():
    k = WorldKernel(seed=123)
    k.physical_world.enable_life_cycle = False
    a = Agent(id=AgentId("A"), seed=1)
    _seed_agent_with_topic(a, "T_Test")
    k.agents.add_agent(a)

    # Ensure at least one consumed impression before the day boundary
    a.budgets.attention_bank_minutes = 1000.0
    a.budgets.reset_for_tick()
    c = ContentItem(id="C_seed", author_id="SRC", topic=TopicId("T_Test"), stance=0.0)
    a.perceive(c, k.world_context, is_physical=False)

    # Start and run past one day boundary.
    k.start()
    k.step(k.clock.ticks_per_day + 1)

    dream_runs = getattr(k.analytics, "dream_runs", [])
    assert len(dream_runs) >= 1, "Expected at least one dream run after day boundary"


def test_exposure_vs_consumption_split_is_recorded():
    k = WorldKernel(seed=123)
    k.physical_world.enable_life_cycle = False
    a = Agent(id=AgentId("A"), seed=7)
    _seed_agent_with_topic(a, "T_Test")
    a.budgets.attention_minutes = 1000.0
    a.budgets.attention_bank_minutes = 1000.0
    k.agents.add_agent(a)

    # No need to run the whole scheduler; call perceive directly through the agent,
    # but we do want analytics initialized in kernel context.
    k.start()

    # Create a bunch of content items; the attention system will assign default media/intake.
    # Agent RNG is seeded, so this result is deterministic.
    for i in range(50):
        c = ContentItem(
            id=f"C{i}",
            author_id="SOURCE",
            topic=TopicId("T_Test"),
            stance=0.0,
        )
        a.perceive(c, k.world_context, is_physical=False)

    exp = getattr(k.analytics, "exposure_counts", {}).get(a.id, 0)
    con = getattr(k.analytics, "consumed_counts", {}).get(a.id, 0)

    assert exp == 50, "Exposure should be logged for every perceive()"
    assert 0 <= con <= exp, "Consumed count must be bounded by exposures"
    assert con != exp, "With probabilistic consumption, not all exposures should be consumed"
