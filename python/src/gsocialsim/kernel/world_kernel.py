from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import random
from concurrent.futures import ThreadPoolExecutor

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
from gsocialsim.agents.belief_update_engine import BeliefDelta
from gsocialsim.fast import perception as fast
from gsocialsim.util.perf import PerfTracker

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
    enable_timing: bool = False
    timing_level: str = "basic"
    enable_debug_logging: bool = True
    enable_parallel: bool = False
    parallel_workers: int = 0
    max_recipients_per_content: int = 0
    max_perceptions_per_tick: int = 0
    enable_batch_perception: bool = False
    enable_batch_all: bool = True
    perf: PerfTracker = field(default_factory=PerfTracker)

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
        try:
            setattr(self.analytics, "enable_debug_logging", bool(self.enable_debug_logging))
        except Exception:
            pass
        self.perf.set_enabled(self.enable_timing, level=self.timing_level)
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
        try:
            from gsocialsim.social.politics import seed_political_topics
            seed_political_topics(self.gsr)
        except Exception:
            pass
        # Seed trust values for existing follow edges.
        try:
            graph = getattr(self.network, "graph", None)
            if graph:
                following = getattr(graph, "_following", {}) or {}
                for follower, followed_set in following.items():
                    for followed in followed_set:
                        trust = getattr(graph, "get_edge_trust", lambda *_: None)(follower, followed)
                        if trust is not None:
                            rel = self.gsr.get_relationship(follower, followed)
                            try:
                                rel.trust = max(0.0, min(1.0, float(trust)))
                            except Exception:
                                rel.trust = max(0.0, min(1.0, rel.trust))
        except Exception:
            pass
        if getattr(self.physical_world, "enable_life_cycle", False):
            try:
                load_fn = getattr(self.physical_world, "load_population_csv", None)
                if callable(load_fn):
                    load_fn()
            except Exception:
                pass
            for agent in self.agents.values():
                try:
                    self.physical_world.ensure_agent(agent.id, agent.rng, self.clock.ticks_per_day)
                except Exception:
                    pass
                try:
                    scale = float(getattr(self.physical_world, "agent_scale", 1.0))
                    agent.agent_weight = max(1.0, scale)
                except Exception:
                    pass

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

        executor = None
        if self.enable_parallel and (self.parallel_workers or 0) > 1:
            executor = ThreadPoolExecutor(max_workers=self.parallel_workers)
        try:
            for _ in range(num_ticks):
                with self.perf.time("tick"):
                    t = self.clock.t

                    # Budgets reset at the start of tick t (contract)
                    with self.perf.time("tick/reset_budgets"):
                        self._reset_tick_budgets(t)

                    # 1) INGEST(t)
                    self.world_context.begin_phase(t, "INGEST")
                    with self.perf.time("phase/ingest"):
                        self._ingest(t)

                    # 2) ACT_BATCH(t)
                    self.world_context.begin_phase(t, "ACT")
                    with self.perf.time("phase/act_batch"):
                        self._act_batch(t, executor=executor)

                    # 3) PERCEIVE_BATCH(t)
                    self.world_context.begin_phase(t, "PERCEIVE")
                    with self.perf.time("phase/perceive_batch"):
                        self._perceive_batch(t, executor=executor)

                    # 4) CONSOLIDATE(t)
                    self.world_context.begin_phase(t, "CONSOLIDATE")
                    with self.perf.time("phase/consolidate"):
                        self._consolidate(t)

                    # Clear buffers for this tick to keep memory bounded
                    with self.perf.time("tick/clear_buffers"):
                        self.world_context.clear_tick_buffers(t)

                    # Advance to next tick
                    self.clock.advance(1)
        finally:
            if executor is not None:
                executor.shutdown(wait=True)

    # -------------------------
    # Phase implementations
    # -------------------------

    def _ingest(self, t: int) -> None:
        """
        Pull exogenous stimuli for tick t and store in context buffer.
        """
        new_stimuli = self.stimulus_engine.tick(t) or []
        self.world_context.stimuli_by_tick[t] = list(new_stimuli)

    def _act_batch(self, t: int, *, executor: Optional[ThreadPoolExecutor] = None) -> None:
        """
        Execute actions for tick t.

        Reaction lag is enforced because this runs before PERCEIVE_BATCH(t).
        Agents act based on prior tick perceptions and internal state.
        """
        posted: List[ContentItem] = []

        detailed = self.perf.enabled and self.perf.level == "detailed"
        agents = list(self.agents.values())
        plans: list = []
        if executor is not None:
            if detailed:
                with self.perf.time("act/agent"):
                    plans = list(executor.map(lambda a: a.plan_action(t, self.world_context), agents))
            else:
                plans = list(executor.map(lambda a: a.plan_action(t, self.world_context), agents))
        else:
            for agent in agents:
                if detailed:
                    with self.perf.time("act/agent"):
                        plans.append(agent.plan_action(t, self.world_context))
                else:
                    plans.append(agent.plan_action(t, self.world_context))

        for agent, plan in zip(agents, plans):
            interaction = agent.apply_planned_action(plan, self.world_context)

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

    def _perceive_batch(self, t: int, *, executor: Optional[ThreadPoolExecutor] = None) -> None:
        """
        Deliver perceptions for tick t.

        Same-tick visibility:
          - exogenous stimuli ingested in INGEST(t)
          - posts published in ACT_BATCH(t)
        """
        if self.enable_batch_all or self.enable_batch_perception or (self.max_perceptions_per_tick and self.max_perceptions_per_tick > 0):
            self._perceive_batch_agentcentric(t)
            return
        detailed = self.perf.enabled and self.perf.level == "detailed"
        for stimulus in self.world_context.stimuli_by_tick.get(t, []):
            if detailed:
                with self.perf.time("deliver/stimulus"):
                    self._deliver_stimulus(stimulus, t, executor=executor)
            else:
                self._deliver_stimulus(stimulus, t, executor=executor)

        for content in self.world_context.posted_by_tick.get(t, []):
            if detailed:
                with self.perf.time("deliver/post"):
                    self._deliver_post(content, t, executor=executor)
            else:
                self._deliver_post(content, t, executor=executor)

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

    def _stimulus_to_content(self, stimulus: Stimulus) -> ContentItem:
        meta = getattr(stimulus, "metadata", None) or {}
        raw_topic = meta.get("topic")
        if isinstance(raw_topic, str) and raw_topic.strip():
            topic = raw_topic.strip()
        else:
            topic = "T_Original"

        stance = 0.0
        raw_stance = getattr(stimulus, "stance_hint", None)
        if raw_stance is None:
            raw_stance = meta.get("stance")
        try:
            stance = float(raw_stance) if raw_stance is not None else 0.0
        except Exception:
            stance = 0.0
        if raw_stance is None:
            seed = hash(f"{stimulus.id}:{topic}") & 0xFFFFFFFF
            rng = random.Random(seed)
            stance = rng.uniform(-0.35, 0.35)
        stance = max(-1.0, min(1.0, stance))

        # Update per-topic political salience if provided
        try:
            pol = getattr(stimulus, "political_salience", None)
            if pol is None:
                pol = meta.get("political_salience")
            if pol is not None:
                pol_val = max(0.0, min(1.0, float(pol)))
                current = float(getattr(self.gsr.ensure_topic(topic), "political_salience", 0.0))
                self.gsr.set_political_salience(topic, max(current, pol_val))
        except Exception:
            pass

        return ContentItem(
            id=stimulus.id,
            author_id=getattr(stimulus, "source", "unknown"),
            topic=topic,
            stance=stance,
            content_text=getattr(stimulus, "content_text", None),
            identity_threat=getattr(stimulus, "identity_threat", None),
            primal_triggers=list(getattr(stimulus, "primal_triggers", []) or []),
            primal_intensity=getattr(stimulus, "primal_intensity", None),
            media_type=getattr(stimulus, "media_type", None),
            outlet_id=getattr(stimulus, "outlet_id", None),
            community_id=getattr(stimulus, "community_id", None),
            provenance={"stimulus_id": stimulus.id, "source": getattr(stimulus, "source", "unknown")},
        )

    def _perceive_batch_agentcentric(self, t: int) -> None:
        """
        Agent-centric batch perception:
        - Build content list for tick
        - For each agent, build a feed from followed authors + broadcast
        - Sample a bounded number of items per agent
        """
        detailed = self.perf.enabled and self.perf.level == "detailed"
        # Build content list for this tick
        content_items: List[ContentItem] = []
        if detailed:
            with self.perf.time("batch/build_content"):
                for stimulus in self.world_context.stimuli_by_tick.get(t, []):
                    content_items.append(self._stimulus_to_content(stimulus))
                content_items.extend(self.world_context.posted_by_tick.get(t, []))
        else:
            for stimulus in self.world_context.stimuli_by_tick.get(t, []):
                content_items.append(self._stimulus_to_content(stimulus))
            content_items.extend(self.world_context.posted_by_tick.get(t, []))

        if not content_items:
            return

        # Precompute author followers and content by author
        author_contents: Dict[str, List[ContentItem]] = {}
        broadcast_contents: List[ContentItem] = []
        if detailed:
            with self.perf.time("batch/index_authors"):
                for content in content_items:
                    author = str(getattr(content, "author_id", ""))
                    author_contents.setdefault(author, []).append(content)

                for author, items in author_contents.items():
                    try:
                        followers = set(self.network.graph.get_followers(author))
                    except Exception:
                        followers = set()
                    if not followers:
                        broadcast_contents.extend(items)
        else:
            for content in content_items:
                author = str(getattr(content, "author_id", ""))
                author_contents.setdefault(author, []).append(content)

            for author, items in author_contents.items():
                try:
                    followers = set(self.network.graph.get_followers(author))
                except Exception:
                    followers = set()
                if not followers:
                    broadcast_contents.extend(items)

        # Precompute following sets per agent
        following_map: Dict[str, List[str]] = {}
        if detailed:
            with self.perf.time("batch/following_map"):
                try:
                    for agent_id in self.agents.keys():
                        following_map[agent_id] = list(self.network.graph.get_following(agent_id))
                except Exception:
                    for agent_id in self.agents.keys():
                        following_map[agent_id] = []
        else:
            try:
                for agent_id in self.agents.keys():
                    following_map[agent_id] = list(self.network.graph.get_following(agent_id))
            except Exception:
                for agent_id in self.agents.keys():
                    following_map[agent_id] = []

        max_items = int(self.max_perceptions_per_tick) if self.max_perceptions_per_tick else 0

        if detailed:
            with self.perf.time("batch/agent_loop"):
                for agent_id, agent in self.agents.items():
                    remaining = self.world_context.time_remaining_by_agent.get(agent_id)
                    if remaining is not None and remaining <= 0.0:
                        continue

                    with self.perf.time("batch/agent_feed"):
                        feed: List[ContentItem] = []
                        feed.extend(broadcast_contents)

                        for author in following_map.get(agent_id, []):
                            items = author_contents.get(author)
                            if items:
                                feed.extend(items)

                        # Ensure self-authored posts are visible to the author.
                        own_items = author_contents.get(agent_id)
                        if own_items:
                            feed.extend(own_items)

                        if not feed:
                            continue

                        if max_items > 0 and len(feed) > max_items:
                            feed = agent.rng.sample(feed, max_items)

                    with self.perf.time("batch/agent_perceive"):
                        plans = []
                        idx_map = []
                        stance_signal = []
                        current_stance = []
                        has_belief = []
                        trust = []
                        credibility = []
                        primal_activation = []
                        identity_threat = []
                        is_self_source = []
                        identity_rigidity = []
                        is_physical = []

                        use_fast = fast.HAS_FAST
                        remaining_local = self.world_context.time_remaining_by_agent.get(agent_id)
                        if remaining_local is None:
                            remaining_local = 0.0
                        for content in feed:
                            if remaining_local <= 0.0:
                                break
                            plan = agent.plan_perception(content, self.world_context, compute_delta=not use_fast)
                            plans.append(plan)
                            if not plan.exposed:
                                continue
                            # Exposure cost always consumes time
                            if plan.exposure_cost > remaining_local:
                                break
                            remaining_local -= plan.exposure_cost

                            # If there's no time for consumption, downgrade to exposure-only
                            if plan.consumed_roll and plan.consumption_extra_cost > remaining_local:
                                plan.consumed_roll = False
                                plan.belief_delta = None
                                continue
                            if plan.consumed_roll:
                                remaining_local -= plan.consumption_extra_cost

                            if use_fast and plan.consumed_roll:
                                idx_map.append(len(plans) - 1)
                                stance_signal.append(float(plan.impression.stance_signal))
                                current_stance.append(float(plan.old_stance))
                                has_belief.append(bool(plan.has_belief))
                                rel = self.gsr.get_relationship(agent.id, content.author_id)
                                trust.append(float(getattr(rel, "trust", 0.0)))
                                credibility.append(float(getattr(plan.impression, "credibility_signal", 0.5)))
                                primal_activation.append(float(getattr(plan.impression, "primal_activation", 0.0)))
                                identity_threat.append(float(getattr(plan.impression, "identity_threat", 0.0)))
                                is_self_source.append(bool(getattr(plan.impression, "is_self_source", False)))
                                identity_rigidity.append(float(getattr(agent.identity, "identity_rigidity", 0.5)))
                                is_physical.append(bool(plan.is_physical))

                        if use_fast and idx_map:
                            import numpy as np

                            sd, cd = fast.compute_belief_deltas(
                                np.asarray(stance_signal, dtype=np.float32),
                                np.asarray(current_stance, dtype=np.float32),
                                np.asarray(has_belief, dtype=np.bool_),
                                np.asarray(trust, dtype=np.float32),
                                np.asarray(credibility, dtype=np.float32),
                                np.asarray(primal_activation, dtype=np.float32),
                                np.asarray(identity_threat, dtype=np.float32),
                                np.asarray(is_self_source, dtype=np.bool_),
                                np.asarray(identity_rigidity, dtype=np.float32),
                                np.asarray(is_physical, dtype=np.bool_),
                            )
                            for j, idx in enumerate(idx_map):
                                plan = plans[idx]
                                plan.belief_delta = BeliefDelta(
                                    topic_id=plan.content.topic,
                                    stance_delta=float(sd[j]),
                                    confidence_delta=float(cd[j]),
                                )

                        for plan in plans:
                            agent.apply_perception_plan(plan, self.world_context)
        else:
            for agent_id, agent in self.agents.items():
                remaining = self.world_context.time_remaining_by_agent.get(agent_id)
                if remaining is not None and remaining <= 0.0:
                    continue

                feed: List[ContentItem] = []
                feed.extend(broadcast_contents)

                for author in following_map.get(agent_id, []):
                    items = author_contents.get(author)
                    if items:
                        feed.extend(items)

                # Ensure self-authored posts are visible to the author.
                own_items = author_contents.get(agent_id)
                if own_items:
                    feed.extend(own_items)

                if not feed:
                    continue

                if max_items > 0 and len(feed) > max_items:
                    feed = agent.rng.sample(feed, max_items)

                for content in feed:
                    remaining = self.world_context.time_remaining_by_agent.get(agent_id)
                    if remaining is not None and remaining <= 0.0:
                        break
                    plan = agent.plan_perception(content, self.world_context)
                    agent.apply_perception_plan(plan, self.world_context)

    # -------------------------
    # Delivery helpers
    # -------------------------

    def _deliver_stimulus(self, stimulus: Stimulus, t: int, *, executor: Optional[ThreadPoolExecutor] = None) -> None:
        temp_content = self._stimulus_to_content(stimulus)

        recipients = self._eligible_recipients_for_author(getattr(stimulus, "source", ""))
        if self.max_recipients_per_content and len(recipients) > self.max_recipients_per_content:
            seed = hash(f"{stimulus.id}:{t}") & 0xFFFFFFFF
            rng = random.Random(seed)
            recipients = rng.sample(recipients, self.max_recipients_per_content)
        detailed = self.perf.enabled and self.perf.level == "detailed"
        agents = [self.agents.get(agent_id) for agent_id in recipients]
        agents = [a for a in agents if a is not None]
        if executor is not None:
            if detailed:
                with self.perf.time("perceive/agent"):
                    plans = list(
                        executor.map(
                            lambda a: a.plan_perception(
                                temp_content,
                                self.world_context,
                                stimulus_id=stimulus.id,
                            ),
                            agents,
                        )
                    )
            else:
                plans = list(
                    executor.map(
                        lambda a: a.plan_perception(
                            temp_content,
                            self.world_context,
                            stimulus_id=stimulus.id,
                        ),
                        agents,
                    )
                )
            for agent, plan in zip(agents, plans):
                remaining = self.world_context.time_remaining_by_agent.get(agent.id)
                if remaining is not None and remaining <= 0.0:
                    continue
                self._mark_perceived(agent, t)
                agent.apply_perception_plan(plan, self.world_context)
        else:
            for agent in agents:
                remaining = self.world_context.time_remaining_by_agent.get(agent.id)
                if remaining is not None and remaining <= 0.0:
                    continue
                self._mark_perceived(agent, t)
                if detailed:
                    with self.perf.time("perceive/agent"):
                        agent.perceive(temp_content, self.world_context, stimulus_id=stimulus.id)
                else:
                    agent.perceive(temp_content, self.world_context, stimulus_id=stimulus.id)

    def _deliver_post(self, content: ContentItem, t: int, *, executor: Optional[ThreadPoolExecutor] = None) -> None:
        recipients = self._eligible_recipients_for_author(getattr(content, "author_id", ""))
        if self.max_recipients_per_content and len(recipients) > self.max_recipients_per_content:
            seed = hash(f"{content.id}:{t}") & 0xFFFFFFFF
            rng = random.Random(seed)
            recipients = rng.sample(recipients, self.max_recipients_per_content)
        detailed = self.perf.enabled and self.perf.level == "detailed"
        agents = [self.agents.get(agent_id) for agent_id in recipients]
        agents = [a for a in agents if a is not None]
        if executor is not None:
            if detailed:
                with self.perf.time("perceive/agent"):
                    plans = list(executor.map(lambda a: a.plan_perception(content, self.world_context), agents))
            else:
                plans = list(executor.map(lambda a: a.plan_perception(content, self.world_context), agents))
            for agent, plan in zip(agents, plans):
                remaining = self.world_context.time_remaining_by_agent.get(agent.id)
                if remaining is not None and remaining <= 0.0:
                    continue
                self._mark_perceived(agent, t)
                agent.apply_perception_plan(plan, self.world_context)
        else:
            for agent in agents:
                remaining = self.world_context.time_remaining_by_agent.get(agent.id)
                if remaining is not None and remaining <= 0.0:
                    continue
                self._mark_perceived(agent, t)
                if detailed:
                    with self.perf.time("perceive/agent"):
                        agent.perceive(content, self.world_context)
                else:
                    agent.perceive(content, self.world_context)

    def _eligible_recipients_for_author(self, author_id: str) -> List[str]:
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
                return sorted(followers)
        except Exception:
            pass

        return sorted(self.agents.keys())

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
        Time budgets reset at start of each tick.
        """
        minutes_per_tick = float(getattr(self.clock, "seconds_per_tick", 900)) / 60.0
        for agent in self.agents.values():
            available = minutes_per_tick
            try:
                available = self.physical_world.get_available_minutes(
                    agent_id=agent.id,
                    tick_of_day=self.clock.tick_of_day,
                    minutes_per_tick=minutes_per_tick,
                    rng=agent.rng,
                    ticks_per_day=self.clock.ticks_per_day,
                )
            except Exception:
                available = minutes_per_tick

            try:
                self.world_context.set_time_budget(agent.id, available)
            except Exception:
                pass

            # Reflective time: some agents spend time thinking instead of acting/reading.
            try:
                prefs = getattr(agent, "activity", None)
                reflect = float(getattr(prefs, "reflect_propensity", 0.0)) if prefs else 0.0
                reflect = max(0.0, min(1.0, reflect))
                if reflect > 0.0:
                    reflect_cost = available * 0.2 * reflect
                    self.world_context.spend_time(agent.id, reflect_cost)
            except Exception:
                pass
