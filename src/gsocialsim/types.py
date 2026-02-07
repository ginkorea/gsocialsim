from typing import NewType

# Define common type aliases for clarity and future extension
AgentId = NewType("AgentId", str)
TopicId = NewType("TopicId", str)
ContentId = NewType("ContentId", str)
ActorId = NewType("ActorId", str) # Can be an AgentId or an institutional actor
