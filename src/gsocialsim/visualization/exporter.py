from collections import defaultdict
from pyvis.network import Network
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.stimuli.interaction import InteractionVerb

def generate_influence_graph_html(kernel: WorldKernel, output_path: str = "influence_graph.html"):
    """
    Generates an interactive HTML graph with aggregated and scaled interaction edges.
    """
    print(f"Generating visualization... output to '{output_path}'")
    net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources='remote')

    # --- 1. Add Agent & Stimulus Nodes ---
    # (This logic remains the same)
    for agent in kernel.agents.agents.values():
        primary_belief = max(agent.beliefs.topics.values(), key=lambda b: b.confidence, default=None)
        color, title, size = "#808080", f"Agent {agent.id}", 15
        if primary_belief:
            color = "#cccccc"
            if primary_belief.stance > 0.1: color = "#0080ff"
            elif primary_belief.stance < -0.1: color = "#ff4000"
            title += f"\nTopic: {primary_belief.topic}\nStance: {primary_belief.stance:.2f}"
            size += primary_belief.confidence * 20
        net.add_node(agent.id, label=agent.id, color=color, title=title, size=size, shape="dot")

    for stimulus in kernel.world_context.stimulus_engine._stimuli_store.values():
        title = f"Stimulus: {stimulus.id}\nSource: {stimulus.source}\nContent: {stimulus.content_text}"
        net.add_node(stimulus.id, label=stimulus.id, color="#00cc66", title=title, shape="square", size=25)

    # --- 2. Add Follower Edges ---
    # (This logic remains the same)
    for follower, followed_list in kernel.world_context.network.graph._following.items():
        for followed in followed_list:
            if follower in kernel.agents.agents and followed in kernel.agents.agents:
                net.add_edge(follower, followed, color="#cccccc", width=1)

    # --- 3. Aggregate and Scale Interaction Edges ---
    interaction_counts = defaultdict(int)
    for interaction in kernel.world_context.analytics.interactions:
        if interaction.verb in [InteractionVerb.LIKE, InteractionVerb.FORWARD]:
            interaction_counts[(interaction.agent_id, interaction.target_stimulus_id)] += 1
    
    max_interaction_count = max(interaction_counts.values()) if interaction_counts else 1
    
    for (agent_id, stimulus_id), count in interaction_counts.items():
        if agent_id in kernel.agents.agents and stimulus_id in kernel.world_context.stimulus_engine._stimuli_store:
            # Scale width from 1 to 10 based on interaction frequency
            relative_width = 1 + 9 * (count / max_interaction_count)
            net.add_edge(
                agent_id, stimulus_id,
                color="#99ff99", width=relative_width, dashes=True,
                title=f"Interacted {count} time(s)"
            )

    # --- 4. Add Influence Edges ---
    # (This logic remains the same)
    influence_counts = defaultdict(int)
    for crossing in kernel.world_context.analytics.crossings:
        for source_id, weight in crossing.attribution.items():
            if weight > 0: influence_counts[(source_id, crossing.agent_id)] += 1
    
    for (source, target), count in influence_counts.items():
        if target in kernel.agents.agents:
            net.add_edge(source, target, color="#ff0000", width=2 * count, title=f"Influenced {count} time(s)")

    # --- 5. Generate HTML ---
    net.show_buttons(filter_=['physics'])
    net.save_graph(output_path)
    print("Visualization generated successfully.")