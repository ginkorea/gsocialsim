import argparse
import random
from typing import Any, Dict

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.agents.generation import generate_agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.relationship_vector import RelationshipVector
from gsocialsim.stimuli.data_source import CsvDataSource

# IMPORTANT: import the package to auto-register exporters
import gsocialsim.visualization as viz
from gsocialsim.visualization import ExportRequest, get_exporter, list_exporters, generate_influence_graph_html


def _add_extra_agents(
    kernel: WorldKernel,
    topics: list[TopicId],
    *,
    extra_agents: int,
    seed: int,
    follow_min: int = 2,
    follow_max: int = 6,
) -> None:
    if extra_agents <= 0:
        return
    rng = random.Random(seed)
    graph = kernel.world_context.network.graph
    gsr = kernel.world_context.gsr

    for i in range(extra_agents):
        agent_id = AgentId(f"N{i+1}")
        if agent_id in kernel.agents:
            continue
        agent = generate_agent(agent_id=agent_id, seed=seed + i, topics=topics, rng=rng)
        kernel.agents.add_agent(agent)

        population_ids = [aid for aid in kernel.agents.keys() if aid != agent_id]
        if not population_ids:
            continue
        follow_count = min(len(population_ids), rng.randint(follow_min, follow_max))
        for target in rng.sample(population_ids, follow_count):
            trust = rng.uniform(0.2, 0.9)
            graph.add_edge(follower=agent_id, followed=target, trust=trust)
            gsr.set_relationship(agent_id, target, RelationshipVector(trust=trust))
            if rng.random() < 0.1:
                graph.add_edge(follower=target, followed=agent_id, trust=trust)


def setup_simulation_scenario(
    kernel: WorldKernel,
    *,
    stimuli_csv: str = "stimuli.csv",
    extra_agents: int = 0,
    extra_agent_seed: int = 1000,
):
    print("Setting up simulation scenario...")

    topics = [
        TopicId("T_Original"),
        TopicId("T_Science"),
        TopicId("T_POLITICS"),
        TopicId("T_ECONOMY"),
        TopicId("T_CULTURE"),
        TopicId("T_Memes"),
        TopicId("T_Sports"),
        TopicId("T_SECURITY"),
    ]

    agent_A = generate_agent(agent_id=AgentId("A"), seed=1, topics=topics)
    agent_B = generate_agent(agent_id=AgentId("B"), seed=2, topics=topics)
    agent_C = generate_agent(agent_id=AgentId("C (Source)"), seed=3, topics=topics)
    agent_D = generate_agent(agent_id=AgentId("D (Lurker)"), seed=4, topics=topics)

    agents = [agent_A, agent_B, agent_C, agent_D]

    # Enable life-cycle model on GeoWorld (H3 grid)
    kernel.physical_world.enable_life_cycle = True
    kernel.physical_world.h3_resolution = 6

    for a in agents:
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)
    graph.add_edge(follower=agent_D.id, followed=agent_A.id)

    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9))
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6))

    agent_C.beliefs.update(TopicId("T_Original"), stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)

    _add_extra_agents(kernel, topics, extra_agents=extra_agents, seed=extra_agent_seed)

    csv_source = CsvDataSource(file_path=stimuli_csv)
    kernel.world_context.stimulus_engine.register_data_source(csv_source)

    print("Scenario setup complete.")


def print_sanity_summary(kernel: WorldKernel):
    print("\n--- SANITY SUMMARY ---")
    analytics = kernel.analytics

    exposure_counts = getattr(analytics, "exposure_counts", {})
    consumed_counts = getattr(analytics, "consumed_counts", {})
    agent_ids = sorted(set(list(exposure_counts.keys()) + list(consumed_counts.keys())))

    if agent_ids:
        for aid in agent_ids:
            exp = exposure_counts.get(aid, 0)
            con = consumed_counts.get(aid, 0)
            print(f"Agent {aid}: exposures={exp}, consumed={con}")
    else:
        print("No exposure/consumption counters found (analytics too old?).")

    dream_runs = getattr(analytics, "dream_runs", [])
    print(f"dream_runs={len(dream_runs)}")
    if dream_runs:
        last = dream_runs[-1]
        print(
            f"last_dream: agent={last.get('agent_id')} "
            f"consolidated={last.get('consolidated')} actions={last.get('actions')}"
        )

    consumed_by_media = getattr(analytics, "consumed_by_media", None)
    if isinstance(consumed_by_media, dict) or hasattr(consumed_by_media, "items"):
        top = sorted(consumed_by_media.items(), key=lambda kv: kv[1], reverse=True)
        if top:
            print("consumed_by_media:", ", ".join([f"{k}={v}" for k, v in top[:8]]))

    print("--- END SUMMARY ---\n")


def build_extra_args(args: argparse.Namespace) -> Dict[str, Any]:
    extra: Dict[str, Any] = {}

    if args.viz == "threshold":
        extra["min_influence_edges"] = args.min_influence_edges
        extra["min_interaction_edges"] = args.min_interaction_edges
        extra["min_node_visibility"] = args.min_node_visibility

    if args.viz == "agents_platform":
        extra["platform_prefix"] = args.platform_prefix

    if args.viz == "geo_map":
        extra["edge_mode"] = args.geo_edge_mode
        extra["show_edges"] = bool(args.geo_show_edges)

    return extra


def parse_args() -> argparse.Namespace:
    exporters = list_exporters()
    exporter_names = sorted(exporters.keys())

    p = argparse.ArgumentParser(description="Run gsocialsim and export a visualization.")
    p.add_argument("--seed", type=int, default=101, help="WorldKernel RNG seed.")
    p.add_argument("--stimuli", type=str, default="stimuli.csv", help="Path to stimuli CSV.")
    p.add_argument(
        "--ticks",
        type=int,
        default=0,
        help="Number of ticks to run. If 0, runs ticks_per_day+10 (guarantees day boundary).",
    )

    p.add_argument(
        "--viz",
        type=str,
        default="full",
        choices=exporter_names,
        help=f"Visualization type. Available: {', '.join(exporter_names)}",
    )
    p.add_argument("--out", type=str, default="influence_graph.html", help="Output HTML path.")
    p.add_argument("--geo-res", type=int, default=None, help="H3 resolution for GeoWorld")
    p.add_argument("--geo-bbox", type=str, default=None, help="Geo bbox min_lat,min_lon,max_lat,max_lon")
    p.add_argument("--geo-pop", type=str, default=None, help="Path to H3 population CSV")
    p.add_argument("--geo-edge-mode", type=str, default="crossing", help="geo_map: crossing|exposure")
    p.add_argument(
        "--geo-show-edges",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="geo_map: show edges",
    )
    p.add_argument("--geo-min-pop", type=float, default=1.0, help="Min H3 population to include")
    p.add_argument("--geo-max-pop", type=float, default=1.0e12, help="Max H3 population to include")
    p.add_argument("--agents", type=int, default=4, help="Total agents to generate (min 4)")
    p.add_argument("--extra-agent-seed", type=int, default=1000, help="Seed for extra agent generation")

    # Threshold knobs
    p.add_argument("--min-influence-edges", type=int, default=2, help="threshold: min influence edge count")
    p.add_argument("--min-interaction-edges", type=int, default=2, help="threshold: min interaction edge count")
    p.add_argument("--min-node-visibility", type=int, default=5, help="threshold: min node visibility score")

    # Platform knob
    p.add_argument("--platform-prefix", type=str, default="SRC:", help="agents_platform: platform node id prefix")
    p.add_argument("--timing", action="store_true", help="Enable timing instrumentation")
    p.add_argument(
        "--timing-level",
        type=str,
        default="basic",
        choices=["basic", "detailed"],
        help="Timing detail level",
    )
    p.add_argument("--timing-top", type=int, default=20, help="Timing report top N rows")

    return p.parse_args()


def main() -> None:
    args = parse_args()

    sim_kernel = WorldKernel(seed=args.seed, enable_timing=args.timing, timing_level=args.timing_level)
    extra_agents = max(0, int(args.agents) - 4)
    setup_simulation_scenario(
        sim_kernel,
        stimuli_csv=args.stimuli,
        extra_agents=extra_agents,
        extra_agent_seed=args.extra_agent_seed,
    )

    if args.geo_res is not None:
        sim_kernel.physical_world.set_resolution(args.geo_res)
    sim_kernel.physical_world.set_population_filter(min_population=args.geo_min_pop, max_population=args.geo_max_pop)
    if args.geo_bbox:
        parts = [float(x) for x in args.geo_bbox.split(",")]
        if len(parts) == 4:
            sim_kernel.physical_world.set_bbox((parts[0], parts[1], parts[2], parts[3]))
    if args.geo_pop:
        sim_kernel.physical_world.load_population_csv(args.geo_pop)

    sim_kernel.start()
    print("\nRunning simulation...")

    ticks = args.ticks if args.ticks and args.ticks > 0 else (sim_kernel.clock.ticks_per_day + 10)
    sim_kernel.step(ticks)

    print("Simulation finished.\n")
    print_sanity_summary(sim_kernel)
    if args.timing:
        print(sim_kernel.perf.report(top=args.timing_top))

    # Export
    if args.viz == "full" and args.out == "influence_graph.html":
        generate_influence_graph_html(sim_kernel, output_path=args.out)
        return

    exporter = get_exporter(args.viz)
    req = ExportRequest(kernel=sim_kernel, output_path=args.out, extra=build_extra_args(args))
    exporter.render(req)


if __name__ == "__main__":
    main()
