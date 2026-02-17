from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class BipartiteExporter(BaseExporter):
    """
    Bipartite layout (high readability):
      - agents on left
      - stimuli on right
      - follower edges optional (kept)
      - interactions agent->stimulus
      - influence edges source->agent (external sources appear as boxes)
    Uses hierarchical layout LR and physics off (no dancing).
    """
    name = "bipartite"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path

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
          "physics": {"enabled": false},
          "layout": {
            "hierarchical": {
              "enabled": true,
              "direction": "LR",
              "sortMethod": "directed",
              "nodeSpacing": 180,
              "levelSeparation": 220
            }
          }
        }
        """)

        # Nodes
        for agent in kernel.agents.agents.values():
            self._ensure_node(net, str(agent.id), label=str(agent.id), color="#cccccc", shape="dot", size=18)

        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store
        for stim in stimuli_store.values():
            self._ensure_node(net, str(stim.id), label=str(stim.id), color="#00cc66", shape="square", size=16, title=f"Source: {stim.source}")

        # Interaction edges
        interaction_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for interaction in kernel.world_context.analytics.interactions:
            if interaction.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                interaction_counts[(str(interaction.agent_id), str(interaction.target_stimulus_id))] += 1

        max_c = max(interaction_counts.values()) if interaction_counts else 1
        for (aid, sid), c in interaction_counts.items():
            if aid in kernel.agents.agents and sid in stimuli_store:
                width = 1 + 6 * (c / max_c)
                net.add_edge(aid, sid, color="#99ff99", width=width, title=f"Interacted {c} time(s)")

        # Influence edges (external -> agent)
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

        for (source, target), c in influence_counts.items():
            if target in kernel.agents.agents:
                if not self._node_exists(net, source) and source not in kernel.agents.agents:
                    self._ensure_node(net, source, label=source, color="#555555", shape="box", size=14, title=f"External actor: {source}")
                key = (source, target)
                color = "#ff0000"
                if influence_sign_count.get(key, 0) > 0:
                    color = self._influence_color(influence_sign[key])
                net.add_edge(source, target, color=color, width=min(10, 2 * c), title=f"Influenced {c} time(s)")

        net.save_graph(output_path)
        self._freeze_after_stabilization(output_path)
        return output_path
