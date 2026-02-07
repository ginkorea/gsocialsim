from typing import Any
import datetime

class Analytics:
    """
    Phase 2: A simple logger that prints events to standard output.
    """
    def log_belief_update(self, timestamp: int, agent_id: str, delta: Any):
        # Using 'Any' for delta to avoid circular dependency with BeliefDelta for now
        # This can be properly typed later with an interface.
        print(
            f"LOG:[T={timestamp}] Agent['{agent_id}'] BeliefUpdate: "
            f"Topic='{delta.topic_id}', StanceΔ={delta.stance_delta:.4f}, ConfΔ={delta.confidence_delta:.4f}"
        )
