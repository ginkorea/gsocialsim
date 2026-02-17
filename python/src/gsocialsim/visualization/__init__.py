"""
Visualization package.

Importing this package registers all available exporters via side-effects
of their @register_exporter decorators.
"""

# Base + registry
from gsocialsim.visualization.exporter import (
    BaseExporter,
    ExportRequest,
    get_exporter,
    list_exporters,
    register_exporter,
    generate_influence_graph_html,
)

# Force-load built-in exporters so they register.
# Keep these imports at module-level on purpose.
from gsocialsim.visualization import exporter_full  # noqa: F401
from gsocialsim.visualization import exporter_agents_only  # noqa: F401
from gsocialsim.visualization import exporter_bipartite  # noqa: F401
from gsocialsim.visualization import exporter_threshold  # noqa: F401
from gsocialsim.visualization import exporter_agents_platform  # noqa: F401
from gsocialsim.visualization import exporter_geo_map  # noqa: F401
