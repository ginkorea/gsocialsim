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

    @staticmethod
    def _influence_color(sign: int) -> str:
        if sign > 0:
            return "#2ca02c"
        if sign < 0:
            return "#d62728"
        return "#999999"

    @classmethod
    def _layout_settings(cls, extra: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        extra = extra or {}
        try:
            spread = float(extra.get("layout_spread", 1.35))
        except Exception:
            spread = 1.35
        try:
            seed = int(extra.get("layout_seed", 42))
        except Exception:
            seed = 42
        physics = bool(extra.get("layout_physics", True))
        spread = max(0.5, min(3.0, spread))
        return {"spread": spread, "seed": seed, "physics": physics}

    @classmethod
    def _apply_stable_layout(
        cls,
        net: Network,
        *,
        enable_physics: bool = False,
        spread: float = 1.35,
        seed: int = 42,
    ) -> None:
        spread = max(0.5, min(3.0, float(spread)))
        grav = -20000.0 * spread
        spring_length = 220.0 * spread
        central_gravity = 0.15 / spread
        options_js = f"""
        var options = {{
          "layout": {{
            "improvedLayout": true,
            "randomSeed": {seed}
          }},
          "interaction": {{
            "hover": true,
            "tooltipDelay": 80,
            "navigationButtons": true
          }},
          "edges": {{
            "smooth": {{
              "enabled": true,
              "type": "continuous",
              "roundness": 0.18
            }}
          }},
          "physics": {{
            "enabled": {str(enable_physics).lower()},
            "barnesHut": {{
              "gravitationalConstant": {grav},
              "centralGravity": {central_gravity},
              "springLength": {spring_length},
              "springConstant": 0.03,
              "damping": 0.8,
              "avoidOverlap": 0.2
            }},
            "stabilization": {{
              "enabled": true,
              "iterations": 2000,
              "updateInterval": 50,
              "fit": true
            }},
            "minVelocity": 0.1,
            "maxVelocity": 30
          }}
        }}
        """
        cls._safe_set_options(net, options_js)

    @staticmethod
    def _freeze_after_stabilization(output_path: str) -> None:
        try:
            with open(output_path, "r", encoding="utf-8") as fh:
                lines = fh.readlines()
        except Exception:
            return

        inject_line = (
            "network.once(\"stabilizationIterationsDone\", function () { "
            "network.setOptions({physics: false}); });\n"
        )
        if any(inject_line.strip() in line for line in lines):
            return

        for i, line in enumerate(lines):
            if "var network = new vis.Network" in line:
                lines.insert(i + 1, inject_line)
                break

        try:
            with open(output_path, "w", encoding="utf-8") as fh:
                fh.writelines(lines)
        except Exception:
            return

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
