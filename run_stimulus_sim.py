from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.stimuli.data_source import CsvDataSource

def setup_stimulus_scenario(kernel: WorldKernel):
    print("Setting up stimulus simulation scenario...")
    # --- Create Agents and Network ---
    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C"), seed=3)
    
    agents = [agent_A, agent_B, agent_C]
    for a in agents:
        a.budgets.action_bank = 100.0
        a.budgets.attention_bank_minutes = 1000.0
        a.budgets.reset_for_tick()
        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_A.id)
    graph.add_edge(follower=agent_C.id, followed=agent_B.id)
    
    # --- Register Data Source ---
    csv_source = CsvDataSource(file_path="stimuli.csv")
    kernel.world_context.stimulus_engine.register_data_source(csv_source)
    print("Scenario setup complete.")

if __name__ == "__main__":
    sim_kernel = WorldKernel(seed=202)
    setup_stimulus_scenario(sim_kernel)

    sim_kernel.start()
    print("\nRunning simulation with external stimuli...")
    sim_kernel.step(150)
    print("Simulation finished.\n")

    print("--- Final Agent States ---")
    for agent in sim_kernel.agents.agents.values():
        print(f"Agent: {agent.id}")
        hist = sim_kernel.analytics.exposure_history.get_history_for_agent(agent.id)
        content_ids = [e.content_id for e in hist if e.content_id]
        if content_ids:
            preview = ", ".join(content_ids[:5])
            suffix = "..." if len(content_ids) > 5 else ""
            print(f"  Exposed to stimuli: {preview}{suffix}")
        else:
            print("  No stimuli exposures.")
