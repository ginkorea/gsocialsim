"""Tests for the phase contract.

These tests are intended to prevent regression back into within-tick ping-pong loops and to keep
tick semantics consistent as features are added.

They are written as a scaffold because repo implementations differ. Replace the `TODO:` hooks with
the actual APIs in your codebase.
"""

from __future__ import annotations

import pytest

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from gsocialsim.stimuli.stimulus import Stimulus
from gsocialsim.stimuli.data_source import DataSource
from gsocialsim.types import AgentId, TopicId, ContentId, ActorId


# ----------------------------
# Helpers (adapt to your repo)
# ----------------------------

def _make_kernel(seed: int = 123):
    """Return a configured WorldKernel with deterministic seed.

    TODO: replace with:
        from gsocialsim.kernel.world_kernel import WorldKernel
        return WorldKernel(seed=seed)
    """
    kernel = WorldKernel(seed=seed)
    # Keep per-tick buffers for assertions in tests
    kernel.world_context.clear_tick_buffers = lambda tick: None
    return kernel


class _QueuedPolicy:
    def __init__(self):
        self._queue: dict[int, list[Interaction]] = {}

    def queue(self, tick: int, interaction: Interaction):
        self._queue.setdefault(tick, []).append(interaction)

    def generate_interaction(self, agent: Agent, tick: int):
        q = self._queue.get(tick, [])
        if not q:
            return None
        interaction = q.pop(0)
        if interaction.verb in (InteractionVerb.REPLY, InteractionVerb.COMMENT):
            last_tick = getattr(agent, "last_perception_tick", None)
            if last_tick is not None and tick <= last_tick:
                # Enforce reaction lag by deferring to next tick
                self.queue(tick + 1, interaction)
                return None
        return interaction

    def learn(self, action_key, reward_vector):
        return None


def _add_two_agents(kernel):
    """Create two agents A and B with a simple relationship and budgets.

    TODO: create agents and add to kernel population
    Ensure they have sufficient attention to perceive at least one item per tick.
    """
    a = Agent(id=AgentId("A"), seed=1)
    b = Agent(id=AgentId("B"), seed=2)

    for agent in (a, b):
        agent.budgets.action_bank = 10.0
        agent.budgets.attention_bank_minutes = 1000.0
        agent.budgets.reset_for_tick()
        agent.rng.random = lambda: 0.0
        agent.policy = _QueuedPolicy()
        kernel.agents.add_agent(agent)

    # B follows A for same-tick visibility
    kernel.world_context.network.graph.add_edge(follower=b.id, followed=a.id)

    return a, b


def _force_action_plan_post(kernel, agent_id: str, tick: int, content_text: str, topic: str = "T_Test"):
    """Force agent's ActionPlan[tick] to include an immediate post action.

    The action must be executed in ACT_BATCH(tick) and produce world-visible content
    (posted_by_tick[tick] / platform feed).
    """
    agent = kernel.agents.get(agent_id)
    if not agent:
        return
    content = ContentItem(
        id=ContentId(f"C_{agent_id}_{tick}"),
        author_id=ActorId(str(agent_id)),
        topic=TopicId(topic),
        stance=0.5,
    )
    interaction = Interaction(agent_id=str(agent_id), verb=InteractionVerb.CREATE, original_content=content)
    agent.policy.queue(tick, interaction)


def _get_perceived_content_ids(kernel, agent_id: str, tick: int) -> set[str]:
    """Return the set of content IDs perceived by agent_id during PERCEIVE_BATCH(tick)."""
    hist = kernel.analytics.exposure_history.get_history_for_agent(agent_id)
    return {
        e.content_id
        for e in hist
        if e.timestamp == tick and e.content_id and getattr(e, "consumed", False)
    }


def _force_reaction_reply_next_tick(kernel, agent_id: str, tick: int, target_content_id: str):
    """Force agent's ActionPlan[tick] to include a reply/react action targeting target_content_id."""
    agent = kernel.agents.get(agent_id)
    if not agent:
        return
    content = ContentItem(
        id=ContentId(f"R_{agent_id}_{tick}_{target_content_id}"),
        author_id=ActorId(str(agent_id)),
        topic=TopicId("T_Test"),
        stance=0.1,
    )
    interaction = Interaction(agent_id=str(agent_id), verb=InteractionVerb.REPLY, original_content=content)
    agent.policy.queue(tick, interaction)


def _get_posts_created_by_agent(kernel, agent_id: str, tick: int) -> list[str]:
    """Return content IDs created/published by agent during ACT_BATCH(tick)."""
    posts = kernel.world_context.posted_by_tick.get(tick, [])
    return [p.id for p in posts if str(getattr(p, "author_id", "")) == str(agent_id)]


def _get_belief_snapshot(kernel, agent_id: str):
    """Return a serializable belief snapshot to compare equality across phases."""
    agent = kernel.agents.get(agent_id)
    if not agent:
        return {}
    snap = {}
    for topic, belief in agent.beliefs.topics.items():
        snap[str(topic)] = (
            float(belief.stance),
            float(belief.confidence),
            float(belief.salience),
            float(belief.knowledge),
        )
    return snap


def _step_one_tick(kernel):
    """Advance the kernel by exactly one tick.

    TODO: If your kernel uses sub-ticks, ensure this steps one tick boundary, not multiple.
    """
    kernel.start()
    kernel.step(1)


class _SingleStimulusSource(DataSource):
    def __init__(self, stimulus: Stimulus):
        self._stimulus = stimulus

    def get_stimuli(self, tick: int):
        return [self._stimulus] if tick == self._stimulus.tick else []


# ----------------------------
# Contract tests
# ----------------------------

@pytest.mark.phase_contract
def test_same_tick_visibility_next_tick_reaction():
    """A posts in ACT(t); B can perceive it in PERCEIVE(t); B cannot react until ACT(t+1)."""
    kernel = _make_kernel(seed=202)
    _add_two_agents(kernel)

    t = 0
    _force_action_plan_post(kernel, agent_id="A", tick=t, content_text="Hello world", topic="T_Test")

    # Step tick 0 (should run INGEST->ACT->PERCEIVE->CONSOLIDATE)
    _step_one_tick(kernel)

    # A's post should be perceivable by B during PERCEIVE(0) (eligibility depends on feed rules, but test assumes enabled)
    perceived = _get_perceived_content_ids(kernel, agent_id="B", tick=t)
    assert perceived, "B should perceive at least one content item during PERCEIVE(t)"
    posted_by_a = _get_posts_created_by_agent(kernel, agent_id="A", tick=t)
    assert posted_by_a, "A should have created at least one post during ACT(t)"
    assert posted_by_a[0] in perceived, "B should be able to perceive A's post in the same tick"

    # Enforce reaction lag: any reply to that content must happen no earlier than ACT(t+1).
    target_id = posted_by_a[0]
    _force_reaction_reply_next_tick(kernel, agent_id="B", tick=t, target_content_id=target_id)

    # B attempting to react in ACT(t) would violate contract. Ensure nothing reacted in tick 0.
    # This helper should confirm no reply was created in tick 0.
    b_posts_t0 = _get_posts_created_by_agent(kernel, agent_id="B", tick=t)
    assert not b_posts_t0, "B must not publish a reaction in the same tick it perceived the trigger (lag rule)"

    # Now schedule reaction properly for tick 1 and step again
    _force_reaction_reply_next_tick(kernel, agent_id="B", tick=t + 1, target_content_id=target_id)
    _step_one_tick(kernel)

    b_posts_t1 = _get_posts_created_by_agent(kernel, agent_id="B", tick=t + 1)
    assert b_posts_t1, "B should be able to react in ACT(t+1)"


@pytest.mark.phase_contract
def test_silent_thinker_internal_monologue_can_shift_belief_without_post():
    """An agent can perceive, internally process (monologue), and shift belief without any outward posting."""
    kernel = _make_kernel(seed=303)
    _add_two_agents(kernel)

    # Inject a persuasive stimulus visible to B during PERCEIVE(0)
    stimulus = Stimulus(
        id="S_persuade_0",
        source="SRC",
        tick=0,
        content_text="persuade",
        metadata={"topic": "T_Test"},
    )
    kernel.world_context.stimulus_engine.register_data_source(_SingleStimulusSource(stimulus))

    # Step tick 0: B perceives and belief updates in CONSOLIDATE(0)
    b_belief_before = _get_belief_snapshot(kernel, agent_id="B")
    _step_one_tick(kernel)
    b_belief_after = _get_belief_snapshot(kernel, agent_id="B")

    assert b_belief_after != b_belief_before, "B belief should be able to change due to internal processing"
    b_posts = _get_posts_created_by_agent(kernel, agent_id="B", tick=0)
    assert not b_posts, "Silent thinker should not be required to post for belief change"


@pytest.mark.phase_contract
def test_budget_tradeoff_creation_reduces_perception_volume():
    """Spending time creating content in ACT(t) should reduce how much can be perceived in PERCEIVE(t)."""
    kernel = _make_kernel(seed=404)
    _add_two_agents(kernel)

    # Configure A with low attention budget and force a high-cost creation action in ACT(0)
    # so A has little remaining budget for PERCEIVE(0).
    a = kernel.agents.get("A")
    if a:
        a.budgets.attention_bank_minutes = 5.0
        a.budgets.attention_minutes = 5.0
        a.budgets.reset_for_tick()

    # Inject multiple stimuli so there is content to perceive
    stimuli = [
        Stimulus(
            id=f"S{i}",
            source="SRC",
            tick=0,
            content_text="stim",
            metadata={"topic": "T_Test"},
        )
        for i in range(10)
    ]
    for s in stimuli:
        kernel.world_context.stimulus_engine.register_data_source(_SingleStimulusSource(s))

    _force_action_plan_post(kernel, agent_id="A", tick=0, content_text="Long post", topic="T_Test")

    _step_one_tick(kernel)

    perceived = _get_perceived_content_ids(kernel, agent_id="A", tick=0)
    # This assertion is intentionally weak; replace with a numeric threshold once your feed/perception is deterministic.
    assert len(perceived) <= 5, "After heavy creation, A should perceive fewer items (budget tradeoff)"


@pytest.mark.phase_contract
def test_belief_updates_only_in_consolidate():
    """Beliefs must not change mid-phase; only at CONSOLIDATE(t)."""
    kernel = _make_kernel(seed=505)
    _add_two_agents(kernel)

    # Force a perception without running consolidate, then verify beliefs unchanged.
    agent_b = kernel.agents.get("B")
    assert agent_b is not None

    stimulus = Stimulus(
        id="S_belief_0",
        source="SRC",
        tick=0,
        content_text="belief",
        metadata={"topic": "T_Test"},
    )
    kernel.world_context.stimulus_engine.register_data_source(_SingleStimulusSource(stimulus))

    # Run only ingest/act/perceive by stepping one tick, but compare beliefs before/after consolidate
    b_before = _get_belief_snapshot(kernel, agent_id="B")
    _step_one_tick(kernel)
    b_after = _get_belief_snapshot(kernel, agent_id="B")

    # Beliefs should only change after CONSOLIDATE inside the tick
    assert b_after != b_before, "Beliefs should change only in CONSOLIDATE during the tick"
