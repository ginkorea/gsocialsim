from __future__ import annotations

from typing import Any, Dict

from gsocialsim.visualization.exporter import BaseExporter, ExportRequest, register_exporter


@register_exporter
class GeoMapExporter(BaseExporter):
    """
    Plotly-based world map exporter using agent geo locations.
    """
    name: str = "geo_map"

    def render(self, req: ExportRequest) -> str:
        try:
            import plotly.graph_objects as go
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("plotly is required for geo_map exporter") from exc

        kernel = req.kernel
        geo = getattr(kernel, "physical_world", None)
        extra: Dict[str, Any] = req.extra or {}

        tick_of_day = extra.get("tick_of_day")
        edge_mode = str(extra.get("edge_mode", "crossing"))
        show_edges = bool(extra.get("show_edges", True))

        lats = []
        lons = []
        labels = []
        sizes = []

        for agent_id, agent in kernel.agents.items():
            if geo is None:
                continue
            loc = geo.get_agent_location(
                agent_id,
                tick_of_day=tick_of_day,
                rng=agent.rng,
                ticks_per_day=kernel.clock.ticks_per_day,
            )
            lats.append(loc.lat)
            lons.append(loc.lon)
            labels.append(str(agent_id))
            weight = float(getattr(agent, "agent_weight", 1.0))
            sizes.append(max(8.0, min(18.0, 8.0 + weight ** 0.5)))

        show_labels = len(labels) <= 50
        mode = "markers+text" if show_labels else "markers"

        data = [
            go.Scattergeo(
                lat=lats,
                lon=lons,
                text=labels if show_labels else None,
                hovertext=labels,
                hoverinfo="text",
                mode=mode,
                marker=dict(size=sizes, color="#d62728", opacity=0.85, line=dict(width=0.6, color="#ffffff")),
                textposition="top center",
                textfont=dict(size=10, color="#222222"),
                name="agents",
            )
        ]

        if show_edges:
            edges_lat = []
            edges_lon = []
            edge_weights: Dict[tuple[str, str], float] = {}

            if edge_mode == "crossing":
                for ev in kernel.analytics.crossings:
                    tgt = ev.agent_id
                    for src, w in ev.attribution.items():
                        if src in kernel.agents and tgt in kernel.agents:
                            edge_weights[(str(src), str(tgt))] = edge_weights.get((str(src), str(tgt)), 0.0) + float(w)
            if edge_mode != "crossing" or not edge_weights:
                for viewer_id in kernel.agents.keys():
                    history = kernel.analytics.exposure_history.get_history_for_agent(viewer_id)
                    for ev in history:
                        src = getattr(ev, "source_actor_id", None)
                        if not src or src not in kernel.agents:
                            continue
                        edge_weights[(str(src), str(viewer_id))] = edge_weights.get((str(src), str(viewer_id)), 0.0) + 1.0

            for (src, tgt), w in edge_weights.items():
                src_loc = geo.get_agent_location(
                    src,
                    tick_of_day=tick_of_day,
                    rng=kernel.agents[src].rng,
                    ticks_per_day=kernel.clock.ticks_per_day,
                )
                tgt_loc = geo.get_agent_location(
                    tgt,
                    tick_of_day=tick_of_day,
                    rng=kernel.agents[tgt].rng,
                    ticks_per_day=kernel.clock.ticks_per_day,
                )
                edges_lat += [src_loc.lat, tgt_loc.lat, None]
                edges_lon += [src_loc.lon, tgt_loc.lon, None]

            if edges_lat:
                data.append(
                    go.Scattergeo(
                        lat=edges_lat,
                        lon=edges_lon,
                        mode="lines",
                        line=dict(width=1, color="rgba(200,0,0,0.35)"),
                        name="influence",
                    )
                )

        fig = go.Figure(data=data)
        fig.update_layout(
            title="Geo Map",
            geo=dict(
                showland=True,
                landcolor="rgb(240,240,240)",
                showcountries=True,
                countrycolor="rgb(200,200,200)",
                showocean=True,
                oceancolor="rgb(230,245,255)",
            ),
            margin=dict(l=0, r=0, t=30, b=0),
        )

        fig.write_html(req.output_path, include_plotlyjs="cdn")
        return req.output_path
