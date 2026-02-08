from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.visualization.exporter import generate_influence_graph_html
from gsocialsim.social.relationship_vector import RelationshipVector
from gsocialsim.stimuli.data_source import CsvDataSource


def setup_simulation_scenario(kernel: WorldKernel):
    print("Setting up simulation scenario...")

    agent_A = Agent(id=AgentId("A"), seed=1)
    agent_B = Agent(id=AgentId("B"), seed=2)
    agent_C = Agent(id=AgentId("C (Source)"), seed=3)
    agent_D = Agent(id=AgentId("D (Lurker)"), seed=4)

    agents = [agent_A, agent_B, agent_C, agent_D]

    # Topics we expect to see in stimuli.csv
    topics = [
        TopicId("T_Original"),
        TopicId("T_Science"),
        TopicId("T_Politics"),
        TopicId("T_Economy"),
        TopicId("T_Culture"),
        TopicId("T_Memes"),
        TopicId("T_Sports"),
        TopicId("T_Security"),
    ]

    for a in agents:
        # Robust budgets for longer runs and lots of stimuli
        a.budgets.action_budget = 5000

        # Seed beliefs for all topics so perception is never "topic-orphaned"
        for t in topics:
            a.beliefs.update(t, stance=0.0, confidence=0.5, salience=0.1, knowledge=0.1)

        kernel.agents.add_agent(a)

    graph = kernel.world_context.network.graph
    graph.add_edge(follower=agent_A.id, followed=agent_B.id)
    graph.add_edge(follower=agent_B.id, followed=agent_C.id)
    graph.add_edge(follower=agent_D.id, followed=agent_A.id)

    gsr = kernel.world_context.gsr
    gsr.set_relationship(agent_A.id, agent_B.id, RelationshipVector(trust=0.9))
    gsr.set_relationship(agent_B.id, agent_C.id, RelationshipVector(trust=0.6))

    # Source agent starts strongly opinionated on T_Original
    agent_C.beliefs.update(TopicId("T_Original"), stance=1.0, confidence=1.0, salience=1.0, knowledge=1.0)

    # External stimuli
    csv_source = CsvDataSource(file_path="stimuli.csv")
    kernel.world_context.stimulus_engine.register_data_source(csv_source)

    print("Scenario setup complete.")


if __name__ == "__main__":
    sim_kernel = WorldKernel(seed=101)
    setup_simulation_scenario(sim_kernel)

    sim_kernel.start()
    print("\nRunning simulation...")
    sim_kernel.step(250)
    print("Simulation finished.\n")

    generate_influence_graph_html(sim_kernel)
