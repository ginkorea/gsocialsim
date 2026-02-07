from collections import defaultdict
from pyvis.network import Network
from src.gsocialsim.kernel.world_kernel import WorldKernel

def generate_influence_graph_html(kernel: WorldKernel, output_path: str = "influence_graph.html"):
    """
    Generates an interactive HTML graph visualizing the social network and the flow of influence.

    - Nodes: Agents, colored by their stance on the most salient topic.
    - Gray Edges: Follower relationships (potential for influence).
    - Red Edges: Actual belief crossings (realized influence), weighted by frequency.
    """
    print(f"Generating visualization... output to '{output_path}'")
    net = Network(height="100vh", width="100%", directed=True, notebook=False, cdn_resources='remote')

    # --- 1. Add Agent Nodes ---
    all_agents = list(kernel.agents.agents.values())
    for agent in all_agents:
        primary_belief = max(agent.beliefs.topics.values(), key=lambda b: b.confidence, default=None)
        color = "#808080" # Default gray
        title = f"Agent {agent.id}"
        size = 15

        if primary_belief:
            if primary_belief.stance > 0.1:
                color = "#0080ff" # Blue for positive
            elif primary_belief.stance < -0.1:
                color = "#ff4000" # Red for negative
            else:
                color = "#cccccc" # Light gray for neutral
            
            title += (
                f"\nTopic: {primary_belief.topic}"
                f"\nStance: {primary_belief.stance:.2f}"
                f"\nConfidence: {primary_belief.confidence:.2f}"
            )
            size += primary_belief.confidence * 20

        net.add_node(agent.id, label=agent.id, color=color, title=title, size=size)

    # --- 2. Add Follower Edges (Potential Influence) ---
    network_graph = kernel.world_context.network.graph
    # Using _following directly as get_following is not on the NetworkGraph class
    for follower, followed_list in network_graph._following.items():
        for followed in followed_list:
            if follower in kernel.agents.agents and followed in kernel.agents.agents:
                net.add_edge(follower, followed, color="#cccccc", width=1)

    # --- 3. Add Influence Edges (Realized Influence) ---
    influence_counts = defaultdict(int)
    for crossing in kernel.world_context.analytics.crossings:
        for source_id, weight in crossing.attribution.items():
            if weight > 0: # Only count credited sources
                influence_counts[(source_id, crossing.agent_id)] += 1
    
    for (source, target), count in influence_counts.items():
         if source in kernel.agents.agents and target in kernel.agents.agents:
            net.add_edge(source, target, color="#ff0000", width=2 * count, title=f"Influenced {count} time(s)")

    # --- 4. Generate HTML ---
    net.show_buttons(filter_=['physics'])
    net.save_graph(output_path)
    print("Visualization generated successfully.")