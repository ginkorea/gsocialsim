"""Tests for the phase contract.

These tests are intended to prevent regression back into within-tick ping-pong loops and to keep
tick semantics consistent as features are added.

They are written as a scaffold because repo implementations differ. Replace the `TODO:` hooks with
the actual APIs in your codebase.
"""

from __future__ import annotations

import pytest


# ----------------------------
# Helpers (adapt to your repo)
# ----------------------------

def _make_kernel(seed: int = 123):
    """Return a configured WorldKernel with deterministic seed.

    TODO: replace with:
        from gsocialsim.kernel.world_kernel import WorldKernel
        return WorldKernel(seed=seed)
    """
    raise NotImplementedError("TODO: implement _make_kernel() for your repo APIs")


def _add_two_agents(kernel):
    """Create two agents A and B with a simple relationship and budgets.

    TODO: create agents and add to kernel population
    Ensure they have sufficient attention to perceive at least one item per tick.
    """
    raise NotImplementedError("TODO: implement _add_two_agents()")


def _force_action_plan_post(kernel, agent_id: str, tick: int, content_text: str, topic: str = "T_Test"):
    """Force agent's ActionPlan[tick] to include an immediate post action.

    The action must be executed in ACT_BATCH(tick) and produce world-visible content
    (posted_by_tick[tick] / platform feed).
    """
    raise NotImplementedError("TODO: implement _force_action_plan_post()")


def _get_perceived_content_ids(kernel, agent_id: str, tick: int) -> set[str]:
    """Return the set of content IDs perceived by agent_id during PERCEIVE_BATCH(tick)."""
    raise NotImplementedError("TODO: implement _get_perceived_content_ids()")


def _force_reaction_reply_next_tick(kernel, agent_id: str, tick: int, target_content_id: str):
    """Force agent's ActionPlan[tick] to include a reply/react action targeting target_content_id."""
    raise NotImplementedError("TODO: implement _force_reaction_reply_next_tick()")


def _get_posts_created_by_agent(kernel, agent_id: str, tick: int) -> list[str]:
    """Return content IDs created/published by agent during ACT_BATCH(tick)."""
    raise NotImplementedError("TODO: implement _get_posts_created_by_agent()")


def _get_belief_snapshot(kernel, agent_id: str):
    """Return a serializable belief snapshot to compare equality across phases."""
    raise NotImplementedError("TODO: implement _get_belief_snapshot()")


def _step_one_tick(kernel):
    """Advance the kernel by exactly one tick.

    TODO: If your kernel uses sub-ticks, ensure this steps one tick boundary, not multiple.
    """
    raise NotImplementedError("TODO: implement _step_one_tick()")


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

    # TODO: inject a persuasive stimulus visible to B during PERCEIVE(0)
    # Example: kernel.world_context.stimulus_store.add(...)
    # Ensure B perceives it in tick 0.

    # Step tick 0: B perceives
    _step_one_tick(kernel)

    # Step tick 1: B may create internal monologue in ACT(1), then belief updates in CONSOLIDATE(1)
    b_belief_before = _get_belief_snapshot(kernel, agent_id="B")
    _step_one_tick(kernel)
    b_belief_after = _get_belief_snapshot(kernel, agent_id="B")

    assert b_belief_after != b_belief_before, "B belief should be able to change due to internal processing"
    b_posts = _get_posts_created_by_agent(kernel, agent_id="B", tick=1)
    assert not b_posts, "Silent thinker should not be required to post for belief change"


@pytest.mark.phase_contract
def test_budget_tradeoff_creation_reduces_perception_volume():
    """Spending time creating content in ACT(t) should reduce how much can be perceived in PERCEIVE(t)."""
    kernel = _make_kernel(seed=404)
    _add_two_agents(kernel)

    # TODO: configure A with low attention budget and force a high-cost creation action in ACT(0)
    # so A has little remaining budget for PERCEIVE(0).
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

    # TODO: If you expose hooks for stepping phases, validate belief snapshot unchanged during ACT/PERCEIVE.
    # If not, use event logs to ensure belief update events only occur in CONSOLIDATE.

    raise NotImplementedError(
        "TODO: implement using your kernel's phase stepping hooks or event log invariants."
    )
