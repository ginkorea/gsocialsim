from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.types import AgentId, TopicId
from src.gsocialsim.visualization.exporter import generate_influence_graph_html
from src.gsocialsim.social.relationship_vector import RelationshipVector

def setup_simulation_scenario(kernel: WorldKernel):
    """
    Creates a small social network with a clear influence path.
    A -> B -> C, and D is a peripheral agent.
    A strongly trusts B. B moderately trusts C.
    """
    print("Setting up simulation scenario...")
    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C (Source)"), seed=3)
    agent_D = Agent(id=AgentId("D (Lurker)"), seed=4)
    
    agents = [agent_A, agent_B, agent_C, agent_D]
    for a in agents:
        a.budgets.action_budget = 100 # Give plenty of budget
        kernel.agents.add_agent(a)

    # --- Setup Social Graph ---
    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)

    # --- Setup Trust ---
    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9)) # A trusts B
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6)) # B trusts C

    # --- Setup Initial Belief ---
    topic = TopicId("T_Viz")
    agent_C.beliefs.update(topic, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)
    print("Scenario setup complete.")

if __name__ == "__main__":
    # --- 1. Initialize ---
    sim_kernel = WorldKernel(seed=101)
    setup_simulation_scenario(sim_kernel)

    # --- 2. Run Simulation ---
    print("\nRunning simulation...")
    # Run for enough ticks for influence to spread
    # With a 1% action chance, 500 ticks should be enough for several posts
    sim_kernel.step(500)
    print("Simulation finished.\n")

    # --- 3. Generate Visualization ---
    generate_influence_graph_html(sim_kernel)