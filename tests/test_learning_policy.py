import unittest
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.types import AgentId
from gsocialsim.stimuli.data_source import CsvDataSource
from gsocialsim.stimuli.interaction import InteractionVerb

class TestLearningPolicy(unittest.TestCase):

    def test_personality_driven_learning(self):
        """
        Verify that agents with different personalities learn to prefer
        different actions based on the rewards they receive.
        """
        print("\n--- Test: Personality-Driven Learning (Bandit) ---")
        
        # --- Setup ---
        kernel = WorldKernel(seed=808)
        
        # Agent Affiliation: High affiliation weight, low status
        agent_aff = Agent(id=AgentId("AffiliationSeeker"), seed=809)
        agent_aff.personality = RewardWeights(affiliation=1.0, status=0.1)

        # Agent Status: High status weight, low affiliation
        agent_status = Agent(id=AgentId("StatusSeeker"), seed=810)
        agent_status.personality = RewardWeights(affiliation=0.1, status=1.0)
        
        # Viewer agent to generate rewards
        viewer = Agent(id=AgentId("Viewer"), seed=811)

        for agent in [agent_aff, agent_status, viewer]:
            agent.budgets.action_budget = 1000 # Give plenty of budget
            kernel.agents.add_agent(agent)
            
        # Viewer follows both agents
        kernel.world_context.network.graph.add_edge(viewer.id, agent_aff.id)
        kernel.world_context.network.graph.add_edge(viewer.id, agent_status.id)
        
        # Load a stimulus for them to interact with
        csv_source = CsvDataSource(file_path="stimuli.csv")
        kernel.world_context.stimulus_engine.register_data_source(csv_source)

        # --- Learning Phase ---
        print("Running learning phase...")
        kernel.start()
        kernel.step(200) # Run long enough for stimuli to be seen and actions to be learned

        # --- Verification Phase ---
        print("Running verification phase (exploitation only)...")
        # Disable exploration to see what the agents have learned
        agent_aff.policy.epsilon = 0.0
        agent_status.policy.epsilon = 0.0
        
        aff_actions = {"LIKE": 0, "FORWARD": 0, "CREATE": 0}
        status_actions = {"LIKE": 0, "FORWARD": 0, "CREATE": 0}

        # Run for more ticks and count the exploited actions
        for i in range(100):
            # We need to manually run the action part of the loop for this test
            interaction_aff = agent_aff.act(tick=200 + i)
            if interaction_aff:
                aff_actions[interaction_aff.verb.name] += 1
            
            interaction_status = agent_status.act(tick=200 + i)
            if interaction_status:
                status_actions[interaction_status.verb.name] += 1
        
        print(f"AffiliationSeeker actions: {aff_actions}")
        print(f"StatusSeeker actions: {status_actions}")

        # --- Assertions ---
        # The affiliation seeker should have learned that LIKEs are best
        self.assertGreater(aff_actions["LIKE"], aff_actions["FORWARD"],
                           "AffiliationSeeker should prefer LIKE over FORWARD.")
                           
        # The status seeker should have learned that FORWARDs are best
        self.assertGreater(status_actions["FORWARD"], status_actions["LIKE"],
                           "StatusSeeker should prefer FORWARD over LIKE.")

        print("Verified: Agents successfully learned personality-driven behaviors.")

if __name__ == '__main__':
    unittest.main()
