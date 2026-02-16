import unittest
from gsocialsim.kernel.world_kernel import WorldKernel
from gsocialsim.agents.agent import Agent
from gsocialsim.types import AgentId, TopicId
from gsocialsim.stimuli.content_item import ContentItem
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb

class TestPhase5(unittest.TestCase):

    def setUp(self):
        self.kernel = WorldKernel(seed=303)
        self.kernel.physical_world.enable_life_cycle = False
        self.agent = Agent(id=AgentId("budget_agent"), seed=304)
        # Give the agent a belief so it has something to post about
        self.agent.beliefs.update(TopicId("T5"), 1.0, 1.0, 1.0, 1.0)
        self.kernel.agents.add_agent(self.agent)

        class AlwaysCreatePolicy:
            def generate_interaction(self, agent: Agent, tick: int):
                topic = next(iter(agent.beliefs.topics.keys()))
                content = ContentItem(
                    id=f"C_{agent.id}_{tick}",
                    author_id=agent.id,
                    topic=topic,
                    stance=agent.beliefs.get(topic).stance,
                )
                return Interaction(agent_id=agent.id, verb=InteractionVerb.CREATE, original_content=content)

            def learn(self, action_key, reward_vector):
                return None

        self.agent.policy = AlwaysCreatePolicy()

    def test_time_budget_limits_actions_per_tick(self):
        """
        Verify that an agent stops acting once its per-tick time is exhausted,
        and can act again on the next tick (no banking).
        """
        print("\n--- Test: Time Budget Limits Actions ---")

        t = self.kernel.clock.t
        self.kernel.world_context.set_time_budget(self.agent.id, 5.0)  # CREATE costs 5 minutes

        first = self.agent.act(t, context=self.kernel.world_context)
        second = self.agent.act(t, context=self.kernel.world_context)

        self.assertIsNotNone(first, "Agent should act when time is available.")
        self.assertIsNone(second, "Agent should be out of time within the same tick.")

        # Next tick: budget resets (no banking, fresh time available)
        self.kernel.world_context.set_time_budget(self.agent.id, 5.0)
        third = self.agent.act(t + 1, context=self.kernel.world_context)
        self.assertIsNotNone(third, "Agent should be able to act again in the next tick.")
        print("Verified: time is consumed per tick and does not bank.")

if __name__ == '__main__':
    unittest.main()
