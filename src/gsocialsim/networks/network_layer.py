from typing import Dict, Set, List
from dataclasses import dataclass, field

from src.gsocialsim.types import AgentId

@dataclass
class NetworkGraph:
    """
    A simple directed graph representing follow relationships.
    """
    # Key: AgentId of the follower
    # Value: Set of AgentIds being followed
    _following: Dict[AgentId, Set[AgentId]] = field(default_factory=dict)
    
    # Key: AgentId of the one being followed
    # Value: Set of AgentIds who are followers
    _followers: Dict[AgentId, Set[AgentId]] = field(default_factory=dict)

    def add_edge(self, follower: AgentId, followed: AgentId):
        """Adds a directed edge from follower to followed."""
        self._following.setdefault(follower, set()).add(followed)
        self._followers.setdefault(followed, set()).add(follower)
    
    def get_followers(self, agent_id: AgentId) -> List[AgentId]:
        return list(self._followers.get(agent_id, []))

    def get_following(self, agent_id: AgentId) -> List[AgentId]:
        return list(self._following.get(agent_id, []))

@dataclass
class NetworkLayer:
    """
    A minimal social network layer for Phase 3.
    For now, it just holds the graph.
    """
    graph: NetworkGraph = field(default_factory=NetworkGraph)
