from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.types import AgentId, TopicId
from src.gsocialsim.visualization.exporter import generate_influence_graph_html
from src.gsocialsim.social.relationship_vector import RelationshipVector
from src.gsocialsim.stimuli.data_source import CsvDataSource

def setup_simulation_scenario(kernel: WorldKernel):
    """
    Sets up a scenario with agents and external stimuli for the simulation.
    """
    print("Setting up simulation scenario...")
    
    # --- Create Agents and Network ---
    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C (Source)"), seed=3)
    agent_D = Agent(id=AgentId("D (Lurker)"), seed=4)
    
    agents = [agent_A, agent_B, agent_C, agent_D]
    for a in agents:
        a.budgets.action_budget = 100 # Give plenty of budget for actions
        a.beliefs.update(TopicId("T_Original"), stance=0.0, confidence=0.5, salience=0.1, knowledge=0.1)
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)
    graph.add_edge(follower=agent_D.id, followed=agent_A.id) # D follows A

    # --- Setup Trust ---
    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9))
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6))

    # --- Seed Initial Belief for Source Agent ---
    topic_original = TopicId("T_Original")
    agent_C.beliefs.update(topic_original, stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)
    
    # --- Register External Data Source ---
    csv_source = CsvDataSource(file_path="stimuli.csv")
    kernel.world_context.stimulus_engine.register_data_source(csv_source)
    print("Scenario setup complete.")


if __name__ == "__main__":
    # --- 1. Initialize Kernel and Setup Scenario ---
    sim_kernel = WorldKernel(seed=101)
    setup_simulation_scenario(sim_kernel)

    # --- 2. Start Event-Driven Simulation ---
    sim_kernel.start() # Seed the initial events (ingestion, agent actions, day boundaries)
    print("\nRunning simulation...")
    # Run for enough ticks to allow stimuli to be ingested, perceived, and acted upon
    sim_kernel.step(200) # Run for 200 ticks
    print("Simulation finished.\n")

    # --- 3. Generate Visualization ---
    generate_influence_graph_html(sim_kernel)
