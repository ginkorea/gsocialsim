from collections import defaultdict
from pyvis.network import Network
from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.stimuli.interaction import InteractionVerb

def generate_influence_graph_html(kernel: WorldKernel, output_path: str = "influence_graph.html"):
    """
    Generates an interactive HTML graph visualizing agents, stimuli, and interactions.
    """
    print(f"Generating visualization... output to '{output_path}'")
    net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources='remote')

    # --- 1. Add Agent Nodes (Circles) ---
    all_agents = list(kernel.agents.agents.values())
    for agent in all_agents:
        primary_belief = max(agent.beliefs.topics.values(), key=lambda b: b.confidence, default=None)
        color, title, size = "#808080", f"Agent {agent.id}", 15
        if primary_belief:
            color = "#cccccc" # Neutral
            if primary_belief.stance > 0.1: color = "#0080ff" # Blue
            elif primary_belief.stance < -0.1: color = "#ff4000" # Red
            title += f"\nTopic: {primary_belief.topic}\nStance: {primary_belief.stance:.2f}"
            size += primary_belief.confidence * 20
        net.add_node(agent.id, label=agent.id, color=color, title=title, size=size, shape="dot")

    # --- 2. Add Stimulus Nodes (Squares) ---
    all_stimuli = kernel.world_context.stimulus_engine._stimuli_store.values()
    for stimulus in all_stimuli:
        title = f"Stimulus: {stimulus.id}\nSource: {stimulus.source}\nContent: {stimulus.content_text}"
        net.add_node(stimulus.id, label=stimulus.id, color="#00cc66", title=title, shape="square", size=25)

    # --- 3. Add Follower Edges (Potential Influence) ---
    for follower, followed_list in kernel.world_context.network.graph._following.items():
        for followed in followed_list:
            if follower in kernel.agents.agents and followed in kernel.agents.agents:
                net.add_edge(follower, followed, color="#cccccc", width=1)

    # --- 4. Add Interaction Edges (Likes/Forwards) ---
    for interaction in kernel.world_context.analytics.interactions:
        if interaction.verb in [InteractionVerb.LIKE, InteractionVerb.FORWARD]:
            if interaction.agent_id in kernel.agents.agents and interaction.target_stimulus_id in kernel.world_context.stimulus_engine._stimuli_store:
                net.add_edge(
                    interaction.agent_id,
                    interaction.target_stimulus_id,
                    color="#99ff99", width=2, dashes=True,
                    title=f"{interaction.verb.name.capitalize()}d"
                )

    # --- 5. Add Influence Edges (Realized Influence) ---
    influence_counts = defaultdict(int)
    for crossing in kernel.world_context.analytics.crossings:
        for source_id, weight in crossing.attribution.items():
            if weight > 0:
                influence_counts[(source_id, crossing.agent_id)] += 1
    
    for (source, target), count in influence_counts.items():
        # Source could be an agent or a stimulus source like "NewsOutlet"
        if target in kernel.agents.agents:
            net.add_edge(source, target, color="#ff0000", width=2 * count, title=f"Influenced {count} time(s)")

    net.show_buttons(filter_=['physics'])
    net.save_graph(output_path)
    print("Visualization generated successfully.")
