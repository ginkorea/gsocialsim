from collections import defaultdict
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

from gsocialsim.policy.action_policy import ActionPolicy
from gsocialsim.agents.reward_weights import RewardWeights
from gsocialsim.stimuli.interaction import Interaction, InteractionVerb
from gsocialsim.stimuli.content_item import ContentItem

if TYPE_CHECKING:
    from gsocialsim.agents.agent import Agent


# -----------------------------
# Reward Vector
# -----------------------------
@dataclass
class RewardVector:
    status: float = 0.0
    affiliation: float = 0.0

    def __add__(self, other: "RewardVector") -> "RewardVector":
        return RewardVector(
            status=self.status + other.status,
            affiliation=self.affiliation + other.affiliation,
        )

    def weighted_sum(self, weights: RewardWeights) -> float:
        return (
            self.status * weights.status
            + self.affiliation * weights.affiliation
        )


# -----------------------------
# Bandit Learner Policy
# -----------------------------
class BanditLearner(ActionPolicy):
    """
    Epsilon-greedy bandit over *topics* (arms).

    Design decision:
    - CREATE actions are keyed ONLY by topic.
    - LIKE / FORWARD are keyed by verb + target id.
    """

    def __init__(self, epsilon: float = 0.2):
        self.epsilon = epsilon
        self.action_counts: dict[str, int] = defaultdict(int)
        self.action_rewards: dict[str, RewardVector] = defaultdict(RewardVector)

    # -------------------------
    # Learning
    # -------------------------
    def learn(self, action_key: str, reward_vector: RewardVector) -> None:
        """
        Update reward statistics for an action key.

        action_key:
          - For CREATE: str(topic_id)
          - For others: verb_targetid
        """
        self.action_counts[action_key] += 1
        self.action_rewards[action_key] = (
            self.action_rewards[action_key] + reward_vector
        )

    # -------------------------
    # Action Generation
    # -------------------------
    def _get_possible_actions(self, agent: "Agent", tick: int) -> list[Interaction]:
        actions: list[Interaction] = []

        # CREATE actions (one per belief topic)
        for topic, belief in agent.beliefs.topics.items():
            content = ContentItem(
                id=f"C_{agent.id}_{tick}",
                author_id=agent.id,
                topic=topic,
                stance=belief.stance,
            )
            actions.append(
                Interaction(
                    agent_id=agent.id,
                    verb=InteractionVerb.CREATE,
                    original_content=content,
                )
            )

        # Reactive actions
        for content_id in agent.recent_impressions.keys():
            actions.append(
                Interaction(
                    agent_id=agent.id,
                    verb=InteractionVerb.LIKE,
                    target_stimulus_id=content_id,
                )
            )
            actions.append(
                Interaction(
                    agent_id=agent.id,
                    verb=InteractionVerb.FORWARD,
                    target_stimulus_id=content_id,
                )
            )

        return actions

    def _action_key(self, action: Interaction) -> str:
        """
        Canonical key for learning/scoring.
        """
        if action.verb == InteractionVerb.CREATE:
            return str(action.original_content.topic)
        return f"{action.verb.value}_{action.target_stimulus_id}"

    def generate_interaction(
        self, agent: "Agent", tick: int
    ) -> Optional[Interaction]:

        possible_actions = self._get_possible_actions(agent, tick)
        if not possible_actions:
            return None

        # ---------------------
        # Exploration
        # ---------------------
        if agent.rng.random() < self.epsilon:
            return agent.rng.choice(possible_actions)

        # ---------------------
        # Exploitation
        # ---------------------
        best_action: Optional[Interaction] = None
        best_score = float("-inf")

        for action in possible_actions:
            key = self._action_key(action)
            n = self.action_counts[key]
            if n == 0:
                continue

            avg_reward = (
                self.action_rewards[key].weighted_sum(agent.personality)
                / n
            )

            if avg_reward > best_score:
                best_score = avg_reward
                best_action = action

        # ---------------------
        # Deterministic fallback
        # ---------------------
        if best_action is None:
            if self.epsilon == 0.0:
                # Deterministic ordering when exploiting
                return max(
                    possible_actions,
                    key=self._action_key,
                )
            return agent.rng.choice(possible_actions)

        return best_action
