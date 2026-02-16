from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import random

from gsocialsim.agents.agent import Agent
from gsocialsim.analytics.analytics import Analytics
from gsocialsim.evolution.evolutionary_system import EvolutionarySystem
from gsocialsim.kernel.sim_clock import SimClock
from gsocialsim.kernel.event_scheduler import EventScheduler
from gsocialsim.kernel.world_context import WorldContext
from gsocialsim.kernel.stimulus_ingestion import StimulusIngestionEngine
from gsocialsim.networks.network_layer import NetworkLayer
from gsocialsim.physical.physical_world import PhysicalWorld
from gsocialsim.social.global_social_reality import GlobalSocialReality

from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.stimuli.stimulus import Stimulus


@dataclass
class AgentPopulation:
    agents: Dict[str, Agent] = field(default_factory=dict)

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.id] = agent

    def replace(self, exited_agent_id: str, newborn_agent: Agent) -> None:
        if exited_agent_id in self.agents:
            del self.agents[exited_agent_id]
        self.add_agent(newborn_agent)

    def get(self, agent_id: str, default=None):
        return self.agents.get(agent_id, default)

    def __getitem__(self, agent_id: str) -> Agent:
        return self.agents[agent_id]

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self.agents

    def items(self):
        return self.agents.items()

    def keys(self):
        return self.agents.keys()

    def values(self):
        return self.agents.values()


@dataclass
class WorldKernel:
    """
    PHASE CONTRACT KERNEL (authoritative runtime)

    Per tick t, MUST run exactly:
      1) INGEST(t)
      2) ACT_BATCH(t)
      3) PERCEIVE_BATCH(t)
      4) CONSOLIDATE(t)

    Invariants (enforced by ordering):
      - Reaction lag: PERCEIVE(t) cannot influence ACT(t). It can only influence ACT(t+1).
      - Same-tick visibility: content posted in ACT(t) may be perceived in PERCEIVE(t).
      - Belief updates applied only in CONSOLIDATE(t).
    """

    seed: int
    clock: SimClock = field(default_factory=SimClock)
    rng: random.Random = field(init=False)

    agents: AgentPopulation = field(default_factory=AgentPopulation)
    analytics: Analytics = field(default_factory=Analytics)
    gsr: GlobalSocialReality = field(default_factory=GlobalSocialReality)

    network: NetworkLayer = field(default_factory=NetworkLayer)
    physical_world: PhysicalWorld = field(default_factory=PhysicalWorld)
    evolutionary_system: EvolutionarySystem = field(default_factory=EvolutionarySystem)
    stimulus_engine: StimulusIngestionEngine = field(default_factory=StimulusIngestionEngine)

    # Scheduler retained for compatibility with older event-driven components,
    # but the phase contract kernel does NOT run intra-tick event loops.
    scheduler: EventScheduler = field(default_factory=EventScheduler)

    world_context: WorldContext = field(init=False)

    _started: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.world_context = WorldContext(
            kernel=self,
            analytics=self.analytics,
            gsr=self.gsr,
            network=self.network,
            clock=self.clock,
            physical_world=self.physical_world,
            evolutionary_system=self.evolutionary_system,
            stimulus_engine=self.stimulus_engine,
            scheduler=self.scheduler,
            agents=self.agents,
        )

        # IMPORTANT:
        # Do NOT install belief.apply_delta wrappers here.
        # Agent.perceive() already queues deltas via WorldContext unless in CONSOLIDATE.
        # A wrapper would risk double-queuing or phase ambiguity.
        # (Belief updates are applied only in CONSOLIDATE(t) below.)

    # -------------------------
    # Contract: kernel lifecycle
    # -------------------------

    def start(self) -> None:
        if self._started:
            return
        self._started = True
        self._seed_daily_budgets_if_needed()

    def step(self, num_ticks: int = 1) -> None:
        """
        Advance the simulation by num_ticks ticks.

        Strict contract loop:
          INGEST(t) -> ACT_BATCH(t) -> PERCEIVE_BATCH(t) -> CONSOLIDATE(t)
        """
        if num_ticks <= 0:
            return
        if not self._started:
            self.start()

        for _ in range(num_ticks):
            t = self.clock.t

            # Budgets reset at the start of tick t (contract)
            self._reset_tick_budgets(t)

            # 1) INGEST(t)
            self.world_context.begin_phase(t, "INGEST")
            self._ingest(t)

            # 2) ACT_BATCH(t)
            self.world_context.begin_phase(t, "ACT")
            self._act_batch(t)

            # 3) PERCEIVE_BATCH(t)
            self.world_context.begin_phase(t, "PERCEIVE")
            self._perceive_batch(t)

            # 4) CONSOLIDATE(t)
            self.world_context.begin_phase(t, "CONSOLIDATE")
            self._consolidate(t)

            # Clear buffers for this tick to keep memory bounded
            self.world_context.clear_tick_buffers(t)

            # Advance to next tick
            self.clock.advance(1)

    # -------------------------
    # Phase implementations
    # -------------------------

    def _ingest(self, t: int) -> None:
        """
        Pull exogenous stimuli for tick t and store in context buffer.
        """
        new_stimuli = self.stimulus_engine.tick(t) or []
        self.world_context.stimuli_by_tick[t] = list(new_stimuli)

    def _act_batch(self, t: int) -> None:
        """
        Execute actions for tick t.

        Reaction lag is enforced because this runs before PERCEIVE_BATCH(t).
        Agents act based on prior tick perceptions and internal state.
        """
        posted: List[ContentItem] = []

        for agent in self.agents.values():
            interaction = None
            try:
                interaction = agent.act(tick=t)
            except TypeError:
                # legacy signature support
                interaction = agent.act(self.world_context)

            if interaction:
                try:
                    self.analytics.log_interaction(t, interaction)
                except Exception:
                    pass

                # Same-tick visibility surface: created content is posted immediately
                content = getattr(interaction, "original_content", None)
                if content is not None and isinstance(content, ContentItem):
                    posted.append(content)

        self.world_context.posted_by_tick[t] = posted

    def _perceive_batch(self, t: int) -> None:
        """
        Deliver perceptions for tick t.

        Same-tick visibility:
          - exogenous stimuli ingested in INGEST(t)
          - posts published in ACT_BATCH(t)
        """
        for stimulus in self.world_context.stimuli_by_tick.get(t, []):
            self._deliver_stimulus(stimulus, t)

        for content in self.world_context.posted_by_tick.get(t, []):
            self._deliver_post(content, t)

    def _consolidate(self, t: int) -> None:
        """
        Apply queued belief deltas (the ONLY place canonical belief vectors may change).

        Also performs belief crossing detection here, since stance transitions only exist here
        under the contract.
        """
        queued = self.world_context.pop_all_belief_deltas()
        for agent_id, delta in queued:
            agent = self.agents.get(agent_id)
            if not agent:
                continue

            # Capture pre-stance for crossing detection
            topic = getattr(delta, "topic_id", getattr(delta, "topic", None))
            old_stance = None
            if topic is not None:
                b0 = agent.beliefs.get(topic)
                old_stance = b0.stance if b0 else 0.0

            try:
                agent.beliefs.apply_delta(delta)
            except Exception:
                continue

            # Applied delta log (canonical)
            try:
                self.analytics.log_belief_update(timestamp=t, agent_id=agent_id, delta=delta)
            except Exception:
                pass

            # Crossing detection (now legal because belief actually changed)
            try:
                if topic is not None:
                    b1 = agent.beliefs.get(topic)
                    new_stance = b1.stance if b1 else (old_stance if old_stance is not None else 0.0)

                    if old_stance is None:
                        old_stance = 0.0

                    if self.analytics.crossing_detector.check(old_stance, new_stance):
                        attribution = self.analytics.attribution_engine.assign_credit(
                            agent_id=agent_id,
                            topic=topic,
                            history=self.analytics.exposure_history,
                        )
                        from gsocialsim.analytics.attribution import BeliefCrossingEvent

                        crossing_event = BeliefCrossingEvent(
                            timestamp=t,
                            agent_id=agent_id,
                            topic=topic,
                            old_stance=old_stance,
                            new_stance=new_stance,
                            attribution=attribution,
                        )
                        self.analytics.log_belief_crossing(crossing_event)
            except Exception:
                pass

        # End-of-day boundary (96 ticks/day with contract clock)
        if getattr(self.clock, "ticks_per_day", 0) > 0 and (t + 1) % self.clock.ticks_per_day == 0:
            for agent in self.agents.values():
                try:
                    agent.consolidate_daily(self.world_context)
                except Exception:
                    pass

    # -------------------------
    # Delivery helpers
    # -------------------------

    def _deliver_stimulus(self, stimulus: Stimulus, t: int) -> None:
        meta = getattr(stimulus, "metadata", None) or {}
        raw_topic = meta.get("topic")
        if isinstance(raw_topic, str) and raw_topic.strip():
            topic = raw_topic.strip()
        else:
            topic = "T_Original"

        temp_content = ContentItem(
            id=stimulus.id,
            author_id=getattr(stimulus, "source", "unknown"),
            topic=topic,
            stance=0.0,
            media_type=getattr(stimulus, "media_type", None),
            outlet_id=getattr(stimulus, "outlet_id", None),
            community_id=getattr(stimulus, "community_id", None),
            provenance={"stimulus_id": stimulus.id, "source": getattr(stimulus, "source", "unknown")},
        )

        recipients = self._eligible_recipients_for_author(getattr(stimulus, "source", ""))
        for agent_id in recipients:
            agent = self.agents.get(agent_id)
            if not agent:
                continue
            self._mark_perceived(agent, t)
            agent.perceive(temp_content, self.world_context, stimulus_id=stimulus.id)

    def _deliver_post(self, content: ContentItem, t: int) -> None:
        recipients = self._eligible_recipients_for_author(getattr(content, "author_id", ""))
        for agent_id in recipients:
            agent = self.agents.get(agent_id)
            if not agent:
                continue
            self._mark_perceived(agent, t)
            agent.perceive(content, self.world_context)

    def _eligible_recipients_for_author(self, author_id: str) -> Set[str]:
        """
        Minimal realism:
          - If follow graph exists: author followers
          - Else: broadcast to all agents
        """
        try:
            followers = set(self.network.graph.get_followers(author_id))
            if followers:
                if author_id in self.agents.keys():
                    followers.add(author_id)
                return followers
        except Exception:
            pass

        return set(self.agents.keys())

    @staticmethod
    def _mark_perceived(agent: Agent, t: int) -> None:
        try:
            setattr(agent, "last_perception_tick", t)
        except Exception:
            pass

    # -------------------------
    # Budget reset
    # -------------------------

    def _reset_tick_budgets(self, t: int) -> None:
        """
        Budgets reset at start of each tick.
        (We keep compatibility with multiple budget API styles.)
        """
        for agent in self.agents.values():
            budgets = getattr(agent, "budgets", None)
            if budgets is None:
                continue

            for method_name in ("reset_for_tick", "reset_tick", "reset"):
                fn = getattr(budgets, method_name, None)
                if callable(fn):
                    try:
                        fn()
                        break
                    except Exception:
                        continue

    def _seed_daily_budgets_if_needed(self) -> None:
        """
        Seed daily budget banks once at startup if they are all empty.
        This avoids zeroing out per-tick allowances on the first tick.
        """
        for agent in self.agents.values():
            budgets = getattr(agent, "budgets", None)
            if budgets is None:
                continue

            # Skip if caller already configured any budgets.
            try:
                banks = (
                    float(getattr(budgets, "attention_bank_minutes", 0.0)),
                    float(getattr(budgets, "action_bank", 0.0)),
                    float(getattr(budgets, "deep_focus_bank", 0.0)),
                    float(getattr(budgets, "risk_bank", 0.0)),
                )
                per_tick = (
                    float(getattr(budgets, "attention_minutes", 0.0)),
                    float(getattr(budgets, "action_budget", 0.0)),
                    float(getattr(budgets, "deep_focus_budget", 0.0)),
                    float(getattr(budgets, "risk_budget", 0.0)),
                )
            except Exception:
                banks = (0.0, 0.0, 0.0, 0.0)
                per_tick = (0.0, 0.0, 0.0, 0.0)

            if any(v > 0.0 for v in banks) or any(v > 0.0 for v in per_tick):
                continue

            regen = getattr(budgets, "regen_daily", None)
            if callable(regen):
                try:
                    regen()
                except Exception:
                    pass
