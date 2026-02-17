from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple, Set

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class ThresholdExporter(BaseExporter):
    """
    Threshold graph:
      - Start from full graph, but only include nodes/edges that exceed thresholds
      - Good for "only what influences / gets lots of visibility"
    extra knobs:
      - min_influence_edges (int) default 2
      - min_interaction_edges (int) default 2
      - min_node_visibility (int) default 5
    """
    name = "threshold"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path
        extra = req.extra or {}

        min_infl = int(extra.get("min_influence_edges", 2))
        min_int = int(extra.get("min_interaction_edges", 2))
        min_vis = int(extra.get("min_node_visibility", 5))

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        layout = self._layout_settings(req.extra)
        self._apply_stable_layout(
            net,
            enable_physics=layout["physics"],
            spread=layout["spread"],
            seed=layout["seed"],
        )
        self._safe_set_options(net, """
        var options = {
          "physics": {
            "enabled": true,
            "stabilization": {"enabled": true, "iterations": 1400, "fit": true}
          }
        }
        """)

        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store

        # Aggregate interactions
        interaction_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for interaction in kernel.world_context.analytics.interactions:
            if interaction.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                interaction_counts[(str(interaction.agent_id), str(interaction.target_stimulus_id))] += 1

        # Aggregate influence
        influence_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        influence_sign: Dict[Tuple[str, str], int] = defaultdict(int)
        influence_sign_count: Dict[Tuple[str, str], int] = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1
                    edge_signs = getattr(crossing, "edge_signs", None)
                    if edge_signs and str(source_id) in edge_signs:
                        key = (str(source_id), str(crossing.agent_id))
                        influence_sign[key] += int(edge_signs[str(source_id)])
                        influence_sign_count[key] += 1

        # Node visibility score
        vis: Dict[str, int] = defaultdict(int)
        for (src, tgt), c in influence_counts.items():
            vis[src] += c
            vis[tgt] += c
        for (aid, sid), c in interaction_counts.items():
            vis[aid] += c
            vis[sid] += c

        allowed_nodes: Set[str] = {nid for nid, v in vis.items() if v >= min_vis}

        # Add agent nodes (if visible)
        for agent in kernel.agents.agents.values():
            aid = str(agent.id)
            if aid in allowed_nodes:
                self._ensure_node(net, aid, label=aid, color="#cccccc", shape="dot", size=18)

        # Add stimulus nodes (if visible)
        for stim_id, stim in stimuli_store.items():
            sid = str(stim_id)
            if sid in allowed_nodes:
                self._ensure_node(net, sid, label=sid, color="#00cc66", shape="square", size=16, title=f"Source: {stim.source}")

        # Add filtered interaction edges
        max_int = max(interaction_counts.values()) if interaction_counts else 1
        for (aid, sid), c in interaction_counts.items():
            if c < min_int:
                continue
            if aid in allowed_nodes and sid in allowed_nodes and sid in stimuli_store and aid in kernel.agents.agents:
                width = 1 + 6 * (c / max_int)
                net.add_edge(aid, sid, color="#99ff99", width=width, dashes=True, title=f"Interacted {c} time(s)")

        # Add filtered influence edges
        for (src, tgt), c in influence_counts.items():
            if c < min_infl:
                continue
            if tgt not in kernel.agents.agents:
                continue
            # allow external src even if not in allowed_nodes (if it is the influencer)
            if tgt not in allowed_nodes:
                continue
            if src not in allowed_nodes and src not in kernel.agents.agents:
                # If an external source is strongly influencing, include it
                allowed_nodes.add(src)

            if not self._node_exists(net, src) and src not in kernel.agents.agents:
                self._ensure_node(net, src, label=src, color="#555555", shape="box", size=14, title=f"External actor: {src}")
            if not self._node_exists(net, tgt):
                self._ensure_node(net, tgt, label=tgt, color="#cccccc", shape="dot", size=18)

            key = (src, tgt)
            color = "#ff0000"
            if influence_sign_count.get(key, 0) > 0:
                color = self._influence_color(influence_sign[key])
            net.add_edge(src, tgt, color=color, width=min(10, 2 * c), title=f"Influenced {c} time(s)")

        net.save_graph(output_path)
        self._freeze_after_stabilization(output_path)
        return output_path
