from gsocialsim.physical.geo_world import (
    GeoWorld as PhysicalWorld,
    GeoLocation,
    LifePhase,
    LifeProfile,
    Schedule,
)

__all__ = [
    "PhysicalWorld",
    "GeoWorld",
    "GeoLocation",
    "LifePhase",
    "LifeProfile",
    "Schedule",
]

# Backward-compatible alias
GeoWorld = PhysicalWorld
