import argparse
from typing import Any, Dict

from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.social.relationship_vector import RelationshipVector
from gsocialsim.stimuli.data_source import CsvDataSource

# IMPORTANT: import the package to auto-register exporters
import gsocialsim.visualization as viz
from gsocialsim.visualization import ExportRequest, get_exporter, list_exporters, generate_influence_graph_html


def setup_simulation_scenario(kernel: WorldKernel, *, stimuli_csv: str = "stimuli.csv"):
    print("Setting up simulation scenario...")

    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C (Source)"), seed=3)
    agent_D = Agent(id=AgentId("D (Lurker)"), seed=4)

    agents = [agent_A, agent_B, agent_C, agent_D]

    topics = [
        TopicId("T_Original"),
        TopicId("T_Science"),
        TopicId("T_Politics"),
        TopicId("T_Economy"),
        TopicId("T_Culture"),
        TopicId("T_Memes"),
        TopicId("T_Sports"),
        TopicId("T_Security"),
    ]

    for a in agents:
        a.budgets.action_budget = 5000
        for t in topics:
            a.beliefs.update(t, stance=0.0, confidence=0.5, salience=0.1, knowledge=0.1)
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)
    graph.add_edge(follower=agent_D.id, followed=agent_A.id)

    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9))
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6))

    agent_C.beliefs.update(TopicId("T_Original"), stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)

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

    # Threshold knobs
    p.add_argument("--min-influence-edges", type=int, default=2, help="threshold: min influence edge count")
    p.add_argument("--min-interaction-edges", type=int, default=2, help="threshold: min interaction edge count")
    p.add_argument("--min-node-visibility", type=int, default=5, help="threshold: min node visibility score")

    # Platform knob
    p.add_argument("--platform-prefix", type=str, default="SRC:", help="agents_platform: platform node id prefix")

    return p.parse_args()


def main() -> None:
    args = parse_args()

    sim_kernel = WorldKernel(seed=args.seed)
    setup_simulation_scenario(sim_kernel, stimuli_csv=args.stimuli)

    sim_kernel.start()
    print("\nRunning simulation...")

    ticks = args.ticks if args.ticks and args.ticks > 0 else (sim_kernel.clock.ticks_per_day + 10)
    sim_kernel.step(ticks)

    print("Simulation finished.\n")
    print_sanity_summary(sim_kernel)

    # Export
    if args.viz == "full" and args.out == "influence_graph.html":
        generate_influence_graph_html(sim_kernel, output_path=args.out)
        return

    exporter = get_exporter(args.viz)
    req = ExportRequest(kernel=sim_kernel, output_path=args.out, extra=build_extra_args(args))
    exporter.render(req)


if __name__ == "__main__":
    main()
