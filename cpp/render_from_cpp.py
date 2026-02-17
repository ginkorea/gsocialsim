#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python" / "src"))

from gsocialsim.analytics.analytics import Analytics
from gsocialsim.analytics.attribution import BeliefCrossingEvent
from gsocialsim.agents.belief_state import BeliefStore
from gsocialsim.agents.belief_update_engine import BeliefDelta
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from gsocialsim.stimuli.stimulus import Stimulus
from gsocialsim.visualization.exporter import ExportRequest, get_exporter, list_exporters


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def parse_payload(payload: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in payload.split("|"):
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        out[k] = v
    return out


def read_state(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"state file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def build_kernel(
    state_path: Path,
    analytics_path: Path,
    *,
    crossing_require_existing: bool,
    crossing_min_abs: float,
    crossing_min_delta: float,
) -> SimpleNamespace:
    state = read_state(state_path)

    analytics = Analytics(enable_debug_logging=False)
    agents: dict[str, SimpleNamespace] = {}

    def get_agent(aid: str) -> SimpleNamespace:
        agent = agents.get(aid)
        if agent is None:
            agent = SimpleNamespace(id=aid, beliefs=BeliefStore())
            agents[aid] = agent
        return agent

    agent_meta: dict[str, dict[str, float]] = {}
    for entry in state.get("agents", []):
        if isinstance(entry, str):
            aid = entry
            if aid:
                get_agent(aid)
            continue
        if isinstance(entry, dict):
            aid = entry.get("id")
            if not aid:
                continue
            get_agent(aid)
            meta: dict[str, float] = {}
            if "political_lean" in entry:
                try:
                    meta["political_lean"] = float(entry["political_lean"])
                except Exception:
                    pass
            if "partisanship" in entry:
                try:
                    meta["partisanship"] = float(entry["partisanship"])
                except Exception:
                    pass
            if meta:
                agent_meta[aid] = meta

    content_nodes: dict[str, dict[str, str]] = {}

    if not analytics_path.exists():
        sys.stderr.write(f"warn: analytics file not found: {analytics_path}; rendering without analytics edges\n")
        analytics_path = None

    last_exposure_stance: dict[tuple[str, str, str], float] = {}
    if analytics_path is not None:
        with analytics_path.open("r", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                try:
                    tick = int(row[0])
                except Exception:
                    continue
                event_type = row[1].strip()
                payload = ",".join(row[2:]).strip() if len(row) > 2 else ""

                if event_type == "summary":
                    raise RuntimeError(
                        "analytics file is in summary mode; rerun with --analytics-mode detailed"
                    )

                data = parse_payload(payload)

                if event_type == "impression":
                    viewer = data.get("viewer")
                    author = data.get("author")
                    topic = data.get("topic")
                    content_id = data.get("content")
                    consumed = data.get("consumed", "0") in ("1", "true", "True")
                    stance_raw = data.get("stance")
                    stance_val = None
                    if stance_raw is not None:
                        try:
                            stance_val = float(stance_raw)
                        except Exception:
                            stance_val = None

                    if viewer and author and topic:
                        analytics.log_exposure(
                            viewer_id=viewer,
                            source_id=author,
                            topic=topic,
                            is_physical=False,
                            timestamp=tick,
                            content_id=content_id,
                        )
                        if consumed and content_id:
                            analytics.log_consumption(
                                viewer_id=viewer,
                                content_id=content_id,
                                topic=topic,
                                timestamp=tick,
                            )
                        if stance_val is not None:
                            last_exposure_stance[(viewer, author, topic)] = stance_val

                    if content_id:
                        content_nodes.setdefault(
                            content_id,
                            {"source": author or "unknown", "topic": topic or ""},
                        )

                elif event_type == "interaction":
                    agent_id = data.get("agent")
                    verb = data.get("verb")
                    if not agent_id or not verb:
                        continue
                    try:
                        verb_enum = InteractionVerb(verb)
                    except Exception:
                        continue
                    interaction = Interaction(
                        agent_id=agent_id,
                        verb=verb_enum,
                        target_stimulus_id=data.get("target"),
                        original_content=None,
                    )
                    analytics.log_interaction(tick, interaction)

                    content_id = data.get("content")
                    topic = data.get("topic")
                    if content_id:
                        content_nodes.setdefault(
                            content_id,
                            {"source": agent_id, "topic": topic or ""},
                        )

                elif event_type == "belief_delta":
                    agent_id = data.get("agent")
                    topic = data.get("topic")
                    if not agent_id or not topic:
                        continue
                    try:
                        stance_delta = float(data.get("stance_delta", "0") or 0.0)
                        conf_delta = float(data.get("confidence_delta", "0") or 0.0)
                    except Exception:
                        continue

                    agent = get_agent(agent_id)
                    store: BeliefStore = agent.beliefs
                    current = store.get(topic)
                    old_stance = current.stance if current else 0.0
                    new_stance = clamp(old_stance + stance_delta, -1.0, 1.0)

                    if crossing_require_existing and current is None:
                        pass
                    elif abs(new_stance) < crossing_min_abs:
                        pass
                    elif abs(new_stance - old_stance) < crossing_min_delta:
                        pass
                    elif analytics.crossing_detector.check(old_stance, new_stance):
                        attribution = analytics.attribution_engine.assign_credit(
                            agent_id=agent_id,
                            topic=topic,
                            history=analytics.exposure_history,
                        )
                        event = BeliefCrossingEvent(
                            timestamp=tick,
                            agent_id=agent_id,
                            topic=topic,
                            old_stance=old_stance,
                            new_stance=new_stance,
                            attribution=attribution,
                        )
                        edge_signs: dict[str, int] = {}
                        for src in attribution.keys():
                            stance = last_exposure_stance.get((agent_id, str(src), topic))
                            if stance is None:
                                continue
                            old_dist = abs(old_stance - stance)
                            new_dist = abs(new_stance - stance)
                            if new_dist < old_dist:
                                edge_signs[str(src)] = 1
                            elif new_dist > old_dist:
                                edge_signs[str(src)] = -1
                            else:
                                edge_signs[str(src)] = 0
                        if edge_signs:
                            setattr(event, "edge_signs", edge_signs)
                        analytics.log_belief_crossing(event)

                    store.apply_delta(
                        BeliefDelta(
                            topic_id=topic,
                            stance_delta=stance_delta,
                            confidence_delta=conf_delta,
                        )
                    )

    stimuli_store: dict[str, Stimulus] = {}
    for stim in state.get("stimuli", []):
        try:
            stim_id = stim.get("id")
            if not stim_id:
                continue
            stimuli_store[stim_id] = Stimulus(
                id=stim_id,
                source=stim.get("source", "unknown"),
                tick=int(stim.get("tick", 0)),
                content_text=stim.get("content_text", ""),
                topic_hint=stim.get("topic"),
            )
        except Exception:
            continue

    for cid, info in content_nodes.items():
        if cid in stimuli_store:
            continue
        stimuli_store[cid] = Stimulus(
            id=cid,
            source=info.get("source", "unknown"),
            tick=0,
            content_text="",
            topic_hint=info.get("topic") or None,
        )

    following: dict[str, list[str]] = {}
    for edge in state.get("following", []):
        follower = edge.get("follower")
        followed = edge.get("followed")
        if not follower or not followed:
            continue
        following.setdefault(follower, []).append(followed)

    for aid, meta in agent_meta.items():
        agent = agents.get(aid)
        if not agent:
            continue
        lean = meta.get("political_lean")
        if lean is not None:
            agent.beliefs.update("T_POLITICAL_LEAN", float(lean), 1.0, 0.0, 0.0)

    agents_obj = SimpleNamespace(agents=agents)
    world_context = SimpleNamespace(
        analytics=analytics,
        stimulus_engine=SimpleNamespace(_stimuli_store=stimuli_store),
        network=SimpleNamespace(graph=SimpleNamespace(_following=following)),
    )
    kernel = SimpleNamespace(agents=agents_obj, world_context=world_context)
    return kernel


def main() -> None:
    exporters = list_exporters()
    exporter_names = [name for name in exporters.keys() if name != "geo_map"]

    p = argparse.ArgumentParser(description="Render Python visualizations from C++ exports.")
    p.add_argument("--state", type=str, default="reports/state.json", help="Path to C++ state.json")
    p.add_argument("--analytics", type=str, default="reports/analytics.csv", help="Path to C++ analytics.csv")
    p.add_argument("--viz", type=str, default="full", choices=exporter_names, help="Visualization type")
    p.add_argument("--out", type=str, default="reports/influence_graph.html", help="Output HTML path")
    p.add_argument("--min-influence-edges", type=int, default=2, help="threshold: min influence edge count")
    p.add_argument("--min-interaction-edges", type=int, default=2, help="threshold: min interaction edge count")
    p.add_argument("--min-node-visibility", type=int, default=5, help="threshold: min node visibility score")
    p.add_argument("--platform-prefix", type=str, default="SRC:", help="agents_platform: platform node id prefix")
    p.add_argument("--layout-spread", type=float, default=1.35, help="Layout spread multiplier (higher = more spread)")
    p.add_argument("--layout-seed", type=int, default=42, help="Layout random seed")
    p.add_argument(
        "--layout-physics",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Enable physics for initial stabilization (auto-frozen after)",
    )
    p.add_argument(
        "--crossing-require-existing",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Only count belief crossings when the agent already had a belief for that topic",
    )
    p.add_argument(
        "--crossing-min-abs",
        type=float,
        default=0.15,
        help="Minimum absolute stance required for a crossing to count",
    )
    p.add_argument(
        "--crossing-min-delta",
        type=float,
        default=0.05,
        help="Minimum stance change required for a crossing to count",
    )
    args = p.parse_args()

    kernel = build_kernel(
        Path(args.state),
        Path(args.analytics),
        crossing_require_existing=args.crossing_require_existing,
        crossing_min_abs=args.crossing_min_abs,
        crossing_min_delta=args.crossing_min_delta,
    )

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    extra = {
        "min_influence_edges": args.min_influence_edges,
        "min_interaction_edges": args.min_interaction_edges,
        "min_node_visibility": args.min_node_visibility,
        "platform_prefix": args.platform_prefix,
        "layout_spread": args.layout_spread,
        "layout_seed": args.layout_seed,
        "layout_physics": args.layout_physics,
    }
    exporter = get_exporter(args.viz)
    req = ExportRequest(kernel=kernel, output_path=args.out, extra=extra)
    exporter.render(req)


if __name__ == "__main__":
    main()
