from typing import Dict, Tuple
from dataclasses import dataclass, field
from src.gsocialsim.types import AgentId
from src.gsocialsim.social.relationship_vector import RelationshipVector

@dataclass
class GlobalSocialReality:
    """
    Manages the latent relationship vectors between all pairs of agents.
    """
    # Key is a sorted tuple of two AgentIds to ensure R(u,v) == R(v,u)
    _relations: Dict[Tuple[AgentId, AgentId], RelationshipVector] = field(default_factory=dict)

    def _get_key(self, u: AgentId, v: AgentId) -> Tuple[AgentId, AgentId]:
        """Creates a canonical key for a pair of agents."""
        if u == v:
            raise ValueError("Cannot have a relationship with oneself.")
        return tuple(sorted((u, v)))

    def get_relationship(self, u: AgentId, v: AgentId) -> RelationshipVector:
        """
        Gets the relationship between two agents.
        If no relationship exists, it creates and returns a default one.
        """
        key = self._get_key(u, v)
        if key not in self._relations:
            self._relations[key] = RelationshipVector()
        return self._relations[key]

    def set_relationship(self, u: AgentId, v: AgentId, vector: RelationshipVector):
        """Sets a specific relationship vector for a pair of agents."""
        key = self._get_key(u, v)
        self._relations[key] = vector
