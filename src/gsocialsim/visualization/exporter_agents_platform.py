from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple, Set

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class AgentsPlatformExporter(BaseExporter):
    """
    Agents + Platform aggregation:
      - Collapses all stimuli by source into one "platform/source" node
      - Interaction edges: agent -> source
      - Influence edges: (source actor or source node) -> agent

    extra knobs:
      - platform_prefix (str) default "SRC:"
    """
    name = "agents_platform"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path
        extra = req.extra or {}
        prefix = str(extra.get("platform_prefix", "SRC:"))

        def pid(source: str) -> str:
            return f"{prefix}{source}"

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        self._safe_set_options(net, """
        var options = {
          "physics": {
            "enabled": true,
            "stabilization": {"enabled": true, "iterations": 1300, "fit": true}
          }
        }
        """)

        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store

        # Agent nodes
        for agent in kernel.agents.agents.values():
            aid = str(agent.id)
            self._ensure_node(net, aid, label=aid, color="#cccccc", shape="dot", size=18)

        # Source/platform nodes
        sources: Set[str] = set()
        for stim in stimuli_store.values():
            if getattr(stim, "source", None):
                sources.add(str(stim.source))

        for s in sorted(sources):
            self._ensure_node(
                net,
                pid(s),
                label=s,
                color="#2aa198",
                shape="box",
                size=18,
                title=f"Platform/Source: {s}",
            )

        # Interaction aggregation agent -> source
        interaction_counts = defaultdict(int)
        for inter in kernel.world_context.analytics.interactions:
            if inter.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                stim = stimuli_store.get(str(inter.target_stimulus_id))
                if not stim:
                    continue
                s = str(getattr(stim, "source", "")).strip()
                if not s:
                    continue
                interaction_counts[(str(inter.agent_id), pid(s))] += 1

        max_c = max(interaction_counts.values()) if interaction_counts else 1
        for (aid, sid), c in interaction_counts.items():
            width = 1 + 6 * (c / max_c)
            net.add_edge(aid, sid, color="#99ff99", width=width, dashes=True, title=f"Interacted {c} time(s)")

        # Influence edges:
        # If influencer name matches an actual source label, connect source node -> agent, else external -> agent.
        influence_counts = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1

        for (src, tgt), c in influence_counts.items():
            if tgt not in kernel.agents.agents:
                continue

            if src in sources:
                net.add_edge(pid(src), tgt, color="#ff0000", width=min(10, 2 * c), title=f"Influenced {c} time(s)")
            else:
                if not self._node_exists(net, src) and src not in kernel.agents.agents:
                    self._ensure_node(net, src, label=src, color="#555555", shape="box", size=14, title=f"External actor: {src}")
                net.add_edge(src, tgt, color="#ff0000", width=min(10, 2 * c), title=f"Influenced {c} time(s)")

        net.save_graph(output_path)
        return output_path
