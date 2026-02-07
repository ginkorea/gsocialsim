import random
from typing import Optional, TYPE_CHECKING

from src.gsocialsim.stimuli.content_item import ContentItem
from src.gsocialsim.types import ContentId

if TYPE_CHECKING:
    from src.gsocialsim.agents.agent import Agent

class ActionPolicy:
    """
    Phase 4: A simple policy that decides if and how an agent should act.
    """
    def should_act(self, agent: "Agent") -> bool:
        """
        Determines if an agent should take an action on this tick.
        A simple probabilistic model to ensure most agents are lurkers.
        """
        # For now, a 1% chance to act on any given tick
        return agent.rng.random() < 0.01

    def generate_action(self, agent: "Agent", tick: int) -> Optional[ContentItem]:
        """
        If an agent decides to act, this generates the action.
        For Phase 4, the only action is creating a ContentItem.
        """
        if not self.should_act(agent) or not agent.beliefs.topics:
            return None

        # Choose a random topic the agent has a belief about
        topic_id = agent.rng.choice(list(agent.beliefs.topics.keys()))
        belief = agent.beliefs.get(topic_id)

        # Create content that reflects the agent's own belief stance
        new_content_id = ContentId(f"C_{agent.id}_{tick}")
        return ContentItem(
            id=new_content_id,
            author_id=agent.id,
            topic=topic_id,
            stance=belief.stance
        )
