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
        self.max_reactive_impressions: int = 40

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
    def _action_key(self, action: Interaction) -> str:
        """
        Canonical key for learning/scoring.
        """
        if action.verb == InteractionVerb.CREATE:
            return str(action.original_content.topic)
        return f"{action.verb.value}_{action.target_stimulus_id}"

    def _random_action(self, agent: "Agent", tick: int) -> Optional[Interaction]:
        topics = list(agent.beliefs.topics.items())
        impressions = list(agent.recent_impressions.keys())
        if self.max_reactive_impressions > 0 and len(impressions) > self.max_reactive_impressions:
            impressions = impressions[-self.max_reactive_impressions :]
        n_topics = len(topics)
        n_impressions = len(impressions)
        total = n_topics + 2 * n_impressions
        if total <= 0:
            return None

        idx = agent.rng.randrange(total)
        if idx < n_topics:
            topic, belief = topics[idx]
            content = ContentItem(
                id=f"C_{agent.id}_{tick}",
                author_id=agent.id,
                topic=topic,
                stance=belief.stance,
            )
            return Interaction(agent_id=agent.id, verb=InteractionVerb.CREATE, original_content=content)

        idx -= n_topics
        pair_idx = idx // 2
        if pair_idx >= n_impressions:
            return None
        verb = InteractionVerb.LIKE if (idx % 2) == 0 else InteractionVerb.FORWARD
        return Interaction(agent_id=agent.id, verb=verb, target_stimulus_id=impressions[pair_idx])

    def _deterministic_fallback(self, agent: "Agent", tick: int) -> Optional[Interaction]:
        best_key = None
        best_kind = None
        best_payload = None

        for topic, belief in agent.beliefs.topics.items():
            key = str(topic)
            if best_key is None or key > best_key:
                best_key = key
                best_kind = InteractionVerb.CREATE
                best_payload = (topic, belief.stance)

        impressions = list(agent.recent_impressions.keys())
        if self.max_reactive_impressions > 0 and len(impressions) > self.max_reactive_impressions:
            impressions = impressions[-self.max_reactive_impressions :]
        for content_id in impressions:
            for verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                key = f"{verb.value}_{content_id}"
                if best_key is None or key > best_key:
                    best_key = key
                    best_kind = verb
                    best_payload = content_id

        if best_kind is None:
            return None
        if best_kind == InteractionVerb.CREATE:
            topic, stance = best_payload
            content = ContentItem(
                id=f"C_{agent.id}_{tick}",
                author_id=agent.id,
                topic=topic,
                stance=stance,
            )
            return Interaction(agent_id=agent.id, verb=InteractionVerb.CREATE, original_content=content)
        return Interaction(agent_id=agent.id, verb=best_kind, target_stimulus_id=best_payload)

    def generate_interaction(
        self, agent: "Agent", tick: int
    ) -> Optional[Interaction]:

        # ---------------------
        # Exploration
        # ---------------------
        if agent.rng.random() < self.epsilon:
            return self._random_action(agent, tick)

        # ---------------------
        # Exploitation
        # ---------------------
        best_action: Optional[Interaction] = None
        best_score = float("-inf")

        # CREATE actions
        for topic, belief in agent.beliefs.topics.items():
            key = str(topic)
            n = self.action_counts.get(key, 0)
            if n == 0:
                continue
            avg_reward = self.action_rewards[key].weighted_sum(agent.personality) / n
            if avg_reward > best_score:
                best_score = avg_reward
                content = ContentItem(
                    id=f"C_{agent.id}_{tick}",
                    author_id=agent.id,
                    topic=topic,
                    stance=belief.stance,
                )
                best_action = Interaction(
                    agent_id=agent.id,
                    verb=InteractionVerb.CREATE,
                    original_content=content,
                )

        # Reactive actions
        impressions = list(agent.recent_impressions.keys())
        if self.max_reactive_impressions > 0 and len(impressions) > self.max_reactive_impressions:
            impressions = impressions[-self.max_reactive_impressions :]
        for content_id in impressions:
            for verb in (InteractionVerb.LIKE, InteractionVerb.FORWARD):
                key = f"{verb.value}_{content_id}"
                n = self.action_counts.get(key, 0)
                if n == 0:
                    continue
                avg_reward = self.action_rewards[key].weighted_sum(agent.personality) / n
                if avg_reward > best_score:
                    best_score = avg_reward
                    best_action = Interaction(
                        agent_id=agent.id,
                        verb=verb,
                        target_stimulus_id=content_id,
                    )

        # ---------------------
        # Deterministic fallback
        # ---------------------
        if best_action is None:
            if self.epsilon == 0.0:
                # Deterministic ordering when exploiting
                return self._deterministic_fallback(agent, tick)
            return self._random_action(agent, tick)

        return best_action
