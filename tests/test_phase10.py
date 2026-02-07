import unittest
import statistics
from src.gsocialsim.kernel.world_kernel import WorldKernel
from src.gsocialsim.agents.agent import Agent
from src.gsocialsim.agents.reward_weights import RewardWeights
from src.gsocialsim.types import AgentId

class TestPhase10(unittest.TestCase):

    def test_evolutionary_pressure(self):
        """
        Verify that over a long run, the average personality of the population
        evolves to match the environmental pressures.
        """
        print("\n--- Test: Evolutionary Selection ---")
        kernel = WorldKernel(seed=707)
        
        # Create an environment that ONLY rewards status-seeking behavior
        kernel.evolutionary_system.exit_threshold = -1.0 # Exit if reward is negative

        # Create an initial population with random personalities
        initial_population = []
        for i in range(10):
            agent = Agent(id=AgentId(f"agent_{i}"), seed=708 + i)
            agent.personality = RewardWeights(
                affiliation=agent.rng.random(),
                status=agent.rng.random()
            )
            # Give a belief to act on
            agent.beliefs.update("T", 1, 1, 1, 1)
            initial_population.append(agent)
            kernel.agents.add_agent(agent)

        initial_avg_status = statistics.mean(p.personality.status for p in initial_population)
        print(f"Initial average 'status' personality weight: {initial_avg_status:.2f}")

        # --- Main Simulation Loop ---
        # In this loop, we manually provide rewards to simulate the environment
        for i in range(5 * kernel.clock.ticks_per_day): # Run for 5 days
            current_tick = kernel.clock.t
            
            # Action/Perception is simplified: every agent just acts and gets a reward
            for agent in list(kernel.agents.agents.values()):
                from src.gsocialsim.policy.bandit_learner import RewardVector
                # The ENVIRONMENT rewards status-seeking behavior.
                # Here, we simulate that by giving a high reward if the agent chooses to "post about status".
                # For simplicity, we'll just use the personality as a proxy for the *action choice*.
                reward_val = agent.personality.status * 0.1 - 0.05 # high status personality gets positive reward
                agent.learn("T", RewardVector(status=reward_val))

            # Step the kernel to trigger daily/evolutionary checks
            kernel.step(1)

        # --- Verification ---
        final_population = kernel.agents.agents.values()
        final_avg_status = statistics.mean(p.personality.status for p in final_population)
        
        print(f"Final average 'status' personality weight: {final_avg_status:.2f}")
        self.assertGreater(final_avg_status, initial_avg_status, "The average 'status' weight in the population should have evolved upwards.")
        print("Verified: Population has evolved to better suit the environment.")


if __name__ == '__main__':
    unittest.main()
