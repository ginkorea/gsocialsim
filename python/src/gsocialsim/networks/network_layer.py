from typing import Dict, Set, List, Tuple, Optional
from dataclasses import dataclass, field

from gsocialsim.types import AgentId

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

    # Key: (follower, followed) tuple
    # Value: trust in [0,1]
    _edge_trust: Dict[Tuple[AgentId, AgentId], float] = field(default_factory=dict)

    def add_edge(self, follower: AgentId, followed: AgentId, trust: Optional[float] = None):
        """Adds a directed edge from follower to followed."""
        self._following.setdefault(follower, set()).add(followed)
        self._followers.setdefault(followed, set()).add(follower)
        if trust is None:
            trust = 0.5
        try:
            trust_val = max(0.0, min(1.0, float(trust)))
        except Exception:
            trust_val = 0.5
        self._edge_trust[(follower, followed)] = trust_val
    
    def get_followers(self, agent_id: AgentId) -> List[AgentId]:
        return list(self._followers.get(agent_id, []))

    def get_following(self, agent_id: AgentId) -> List[AgentId]:
        return list(self._following.get(agent_id, []))

    def get_edge_trust(self, follower: AgentId, followed: AgentId) -> Optional[float]:
        return self._edge_trust.get((follower, followed))

    def update_edge_trust(self, follower: AgentId, followed: AgentId, delta: float) -> Optional[float]:
        key = (follower, followed)
        if key not in self._edge_trust:
            return None
        try:
            v = float(self._edge_trust[key]) + float(delta)
        except Exception:
            v = self._edge_trust[key]
        v = max(0.0, min(1.0, v))
        self._edge_trust[key] = v
        return v

@dataclass
class NetworkLayer:
    """
    A minimal social network layer for Phase 3.
    For now, it just holds the graph.
    """
    graph: NetworkGraph = field(default_factory=NetworkGraph)
