from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.types import AgentId, TopicId
from src.gsocialsim.visualization.exporter import generate_influence_graph_html
from src.gsocialsim.social.relationship_vector import RelationshipVector
from src.gsocialsim.stimuli.data_source import CsvDataSource

def setup_and_run_simulation(kernel: WorldKernel, num_ticks: int):
    """
    Sets up a scenario with agents and external stimuli, runs the simulation,
    and returns the kernel state.
    """
    print("Setting up simulation scenario...")
    # --- Create Agents and Network ---
    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C (Source)"), seed=3)
    agent_D = Agent(id=AgentId("D (Lurker)"), seed=4)
    
    agents = [agent_A, agent_B, agent_C, agent_D]
    for a in agents:
        a.budgets.action_budget = 100
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)
    graph.add_edge(follower=agent_D.id, followed=agent_A.id) # D follows A

    # --- Setup Trust ---
    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9))
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6))

    # --- Setup Initial Belief ---
    topic = TopicId("T_Original")
    agent_C.beliefs.update(topic, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)
    
    # --- Register Data Source ---
    csv_source = CsvDataSource(file_path="stimuli.csv")
    kernel.world_context.stimulus_engine.register_data_source(csv_source)
    print("Scenario setup complete.")

    # --- Run Simulation ---
    print(f"\nRunning simulation for {num_ticks} ticks...")
    kernel.step(num_ticks)
    print("Simulation finished.\n")


if __name__ == "__main__":
    # --- 1. Initialize & Run ---
    sim_kernel = WorldKernel(seed=101)
    # Run long enough for stimuli at ticks 10, 50, 100 to appear and be acted upon
    setup_and_run_simulation(sim_kernel, num_ticks=200)

    # --- 2. Generate Visualization ---
    generate_influence_graph_html(sim_kernel)