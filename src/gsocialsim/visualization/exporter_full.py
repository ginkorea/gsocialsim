from __future__ import annotations

from collections import defaultdict
from typing import Dict, Tuple, Any

from pyvis.network import Network

from gsocialsim.stimuli.interaction import InteractionVerb
from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class FullGraphExporter(BaseExporter):
    """
    Full graph:
      - agents
      - stimuli
      - follower edges
      - interactions (agent -> stimulus)
      - influence edges (source -> agent), including external sources
    Stabilized physics to avoid the "jello".
    """
    name = "full"

    def render(self, req: ExportRequest) -> str:
        kernel = req.kernel
        output_path = req.output_path

        net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources="remote")
        self._safe_set_options(net, """
        var options = {
          "physics": {
            "enabled": true,
            "barnesHut": {
              "gravitationalConstant": -25000,
              "centralGravity": 0.25,
              "springLength": 180,
              "springConstant": 0.04,
              "damping": 0.5,
              "avoidOverlap": 0.2
            },
            "stabilization": {
              "enabled": true,
              "iterations": 1500,
              "updateInterval": 50,
              "fit": true
            }
          },
          "interaction": {"hover": true, "tooltipDelay": 80}
        }
        """)

        # 1) Agent nodes
        for agent in kernel.agents.agents.values():
            primary_belief = max(agent.beliefs.topics.values(), key=lambda b: b.confidence, default=None)
            color, title, size = "#808080", f"Agent {agent.id}", 15
            if primary_belief:
                color = "#cccccc"
                if primary_belief.stance > 0.1:
                    color = "#0080ff"
                elif primary_belief.stance < -0.1:
                    color = "#ff4000"
                title += f"\nTopic: {primary_belief.topic}\nStance: {primary_belief.stance:.2f}"
                size += float(primary_belief.confidence) * 20
            self._ensure_node(net, str(agent.id), label=str(agent.id), color=color, title=title, size=size, shape="dot")

        # 2) Stimulus nodes
        stimuli_store = kernel.world_context.stimulus_engine._stimuli_store
        for stimulus in stimuli_store.values():
            title = f"Stimulus: {stimulus.id}\nSource: {stimulus.source}\nContent: {stimulus.content_text}"
            self._ensure_node(net, str(stimulus.id), label=str(stimulus.id), color="#00cc66", title=title, shape="square", size=18)

        # 3) Follower edges
        following = kernel.world_context.network.graph._following
        for follower, followed_list in following.items():
            for followed in followed_list:
                if follower in kernel.agents.agents and followed in kernel.agents.agents:
                    net.add_edge(str(follower), str(followed), color="#cccccc", width=1, title="follows")

        # 4) Interaction edges (aggregated)
        interaction_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for interaction in kernel.world_context.analytics.interactions:
            if interaction.verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                interaction_counts[(str(interaction.agent_id), str(interaction.target_stimulus_id))] += 1

        max_interaction_count = max(interaction_counts.values()) if interaction_counts else 1
        for (agent_id, stimulus_id), count in interaction_counts.items():
            if agent_id in kernel.agents.agents and stimulus_id in stimuli_store:
                width = 1 + 6 * (count / max_interaction_count)
                net.add_edge(agent_id, stimulus_id, color="#99ff99", width=width, dashes=True, title=f"Interacted {count} time(s)")

        # 5) Influence edges (with external nodes)
        influence_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for crossing in kernel.world_context.analytics.crossings:
            for source_id, weight in crossing.attribution.items():
                try:
                    w = float(weight)
                except Exception:
                    w = 0.0
                if w > 0:
                    influence_counts[(str(source_id), str(crossing.agent_id))] += 1

        for (source, target), count in influence_counts.items():
            if target in kernel.agents.agents:
                if not self._node_exists(net, source):
                    self._ensure_node(
                        net,
                        source,
                        label=source,
                        color="#555555",
                        title=f"External actor: {source}",
                        shape="box",
                        size=14,
                    )
                net.add_edge(source, target, color="#ff0000", width=min(10, 2 * count), title=f"Influenced {count} time(s)")

        net.save_graph(output_path)
        return output_path
