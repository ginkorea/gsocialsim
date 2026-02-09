from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from pyvis.network import Network

from gsocialsim.kernel.world_kernel import WorldKernel


@dataclass(frozen=True)
class ExportRequest:
    """
    Common contract for all exporters.

    - kernel: WorldKernel
    - output_path: file to write (html)
    - extra: free-form knobs (thresholds, styles, etc.)
    """
    kernel: WorldKernel
    output_path: str = "influence_graph.html"
    extra: Dict[str, Any] = None


class BaseExporter(ABC):
    """
    Generic exporter contract. Inherit and implement render().
    All exporters must accept the same ExportRequest and write an HTML output.
    """
    name: str = "base"

    def __init__(self) -> None:
        pass

    @abstractmethod
    def render(self, req: ExportRequest) -> str:
        """
        Render a graph to req.output_path and return the output_path.
        """
        raise NotImplementedError

    # ---------- shared helpers ----------
    @staticmethod
    def _safe_set_options(net: Network, options_js: str) -> None:
        try:
            net.set_options(options_js)
        except Exception:
            # pyvis versions vary, defaults are acceptable if this fails
            pass

    @staticmethod
    def _node_exists(net: Network, node_id: str) -> bool:
        try:
            return node_id in net.get_nodes()
        except Exception:
            return False

    @classmethod
    def _ensure_node(
        cls,
        net: Network,
        node_id: str,
        *,
        label: Optional[str] = None,
        title: Optional[str] = None,
        color: Optional[str] = None,
        shape: Optional[str] = None,
        size: Optional[float] = None,
    ) -> None:
        if not node_id:
            return
        if cls._node_exists(net, node_id):
            return

        kwargs: Dict[str, Any] = {"label": label or node_id}
        if title is not None:
            kwargs["title"] = title
        if color is not None:
            kwargs["color"] = color
        if shape is not None:
            kwargs["shape"] = shape
        if size is not None:
            kwargs["size"] = size

        net.add_node(node_id, **kwargs)


# -----------------------------
# Registry (optional convenience)
# -----------------------------
_EXPORTERS: Dict[str, Type[BaseExporter]] = {}


def register_exporter(cls: Type[BaseExporter]) -> Type[BaseExporter]:
    _EXPORTERS[cls.name] = cls
    return cls


def get_exporter(name: str) -> BaseExporter:
    if name not in _EXPORTERS:
        raise ValueError(f"Unknown exporter '{name}'. Known: {sorted(_EXPORTERS.keys())}")
    return _EXPORTERS[name]()


def list_exporters() -> Dict[str, Type[BaseExporter]]:
    return dict(_EXPORTERS)


# -----------------------------
# Backward-compatible function
# -----------------------------
def generate_influence_graph_html(kernel: WorldKernel, output_path: str = "influence_graph.html") -> str:
    """
    Backward compatible entrypoint used by run_and_visualize.py today.
    Uses the 'full' exporter by default.

    Import is inside the function to avoid import-time cycles.
    """
    from gsocialsim.visualization.exporter_full import FullGraphExporter  # local import by design

    exporter = FullGraphExporter()
    req = ExportRequest(kernel=kernel, output_path=output_path, extra={})
    return exporter.render(req)
