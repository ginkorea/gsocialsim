from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple

from pyvis.network import Network

from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class AgentsOnlyExporter(BaseExporter):
    """
    Agents-only graph:
      - agents
      - external sources (only if they influence an agent)
      - follower edges
      - influence edges (source -> agent)
    """
    name = "agents_only"

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
          "physics": {
            "enabled": true,
            "stabilization": {"enabled": true, "iterations": 1200, "fit": true}
          }
        }
        """)

        agent_ids = set(kernel.agents.agents.keys())

        # Agent nodes
        for agent in kernel.agents.agents.values():
            self._ensure_node(net, str(agent.id), label=str(agent.id), color="#cccccc", shape="dot", size=18)

        # Follower edges
        following = kernel.world_context.network.graph._following
        for follower, followed_list in following.items():
            for followed in followed_list:
                if follower in agent_ids and followed in agent_ids:
                    net.add_edge(str(follower), str(followed), color="#cccccc", width=1, title="follows")

        # Influence edges
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

        for (source, target), count in influence_counts.items():
            if target in agent_ids:
                if not self._node_exists(net, source) and source not in agent_ids:
                    self._ensure_node(net, source, label=source, color="#555555", shape="box", size=14, title=f"External actor: {source}")
                key = (source, target)
                color = "#ff0000"
                if influence_sign_count.get(key, 0) > 0:
                    color = self._influence_color(influence_sign[key])
                net.add_edge(source, target, color=color, width=min(10, 2 * count), title=f"Influenced {count} time(s)")

        net.save_graph(output_path)
        self._freeze_after_stabilization(output_path)
        return output_path
