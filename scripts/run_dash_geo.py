import argparse
from contextlib import nullcontext
from typing import Dict, Any, Tuple

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

from gsocialsim.kernel.world_kernel import WorldKernel
from run_and_visualize import setup_simulation_scenario


def _parse_bbox(raw: str) -> Tuple[float, float, float, float]:
    parts = [float(x) for x in raw.split(",")]
    if len(parts) != 4:
        raise ValueError("bbox must be min_lat,min_lon,max_lat,max_lon")
    return parts[0], parts[1], parts[2], parts[3]


def build_geo_figure(kernel: WorldKernel, tick_of_day: int, edge_mode: str, show_edges: bool) -> go.Figure:
    geo = getattr(kernel, "physical_world", None)
    perf = getattr(kernel, "perf", None)
    perf_enabled = bool(perf and getattr(perf, "enabled", False))

    lats = []
    lons = []
    labels = []
    sizes = []

    with (perf.time("dash/build_geo_figure") if perf_enabled else nullcontext()):
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

    if show_edges and geo is not None:
        edges_lat = []
        edges_lon = []
        edge_weights: Dict[tuple[str, str], float] = {}

        with (perf.time("dash/build_edges") if perf_enabled else nullcontext()):
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

            for (src, tgt), _w in edge_weights.items():
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
    return fig


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run gsocialsim and launch a Dash geo map.")
    p.add_argument("--seed", type=int, default=101, help="WorldKernel RNG seed.")
    p.add_argument("--stimuli", type=str, default="stimuli.csv", help="Path to stimuli CSV.")
    p.add_argument(
        "--ticks",
        type=int,
        default=0,
        help="Number of ticks to run. If 0, runs ticks_per_day+10 (guarantees day boundary).",
    )
    p.add_argument("--geo-res", type=int, default=None, help="H3 resolution for GeoWorld")
    p.add_argument("--geo-bbox", type=str, default=None, help="Geo bbox min_lat,min_lon,max_lat,max_lon")
    p.add_argument("--geo-pop", type=str, default=None, help="Path to H3 population CSV")
    p.add_argument("--edge-mode", type=str, default="crossing", help="crossing|exposure")
    p.add_argument(
        "--show-edges",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Show influence edges",
    )
    p.add_argument("--geo-min-pop", type=float, default=1.0, help="Min H3 population to include")
    p.add_argument("--geo-max-pop", type=float, default=1.0e12, help="Max H3 population to include")
    p.add_argument("--agents", type=int, default=4, help="Total agents to generate (min 4)")
    p.add_argument("--extra-agent-seed", type=int, default=1000, help="Seed for extra agent generation")
    p.add_argument("--port", type=int, default=8050, help="Dash server port")
    p.add_argument("--timing", action="store_true", help="Enable timing instrumentation")
    p.add_argument(
        "--timing-level",
        type=str,
        default="basic",
        choices=["basic", "detailed"],
        help="Timing detail level",
    )
    p.add_argument("--timing-top", type=int, default=20, help="Timing report top N rows")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    kernel = WorldKernel(seed=args.seed, enable_timing=args.timing, timing_level=args.timing_level)
    extra_agents = max(0, int(args.agents) - 4)
    setup_simulation_scenario(
        kernel,
        stimuli_csv=args.stimuli,
        extra_agents=extra_agents,
        extra_agent_seed=args.extra_agent_seed,
    )

    if args.geo_res is not None:
        kernel.physical_world.set_resolution(args.geo_res)
    kernel.physical_world.set_population_filter(min_population=args.geo_min_pop, max_population=args.geo_max_pop)
    if args.geo_bbox:
        kernel.physical_world.set_bbox(_parse_bbox(args.geo_bbox))
    if args.geo_pop:
        kernel.physical_world.load_population_csv(args.geo_pop)

    kernel.start()
    ticks = args.ticks if args.ticks and args.ticks > 0 else (kernel.clock.ticks_per_day + 10)
    kernel.step(ticks)
    if args.timing:
        print(kernel.perf.report(top=args.timing_top))

    app = Dash(__name__)
    ticks_per_day = kernel.clock.ticks_per_day

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Label("Tick of day"),
                    dcc.Slider(
                        id="tick-slider",
                        min=0,
                        max=ticks_per_day - 1,
                        step=1,
                        value=0,
                        marks={0: "0", ticks_per_day // 2: str(ticks_per_day // 2), ticks_per_day - 1: str(ticks_per_day - 1)},
                    ),
                ],
                style={"margin": "10px 20px"},
            ),
            html.Div(
                [
                    html.Label("Edge mode"),
                    dcc.Dropdown(
                        id="edge-mode",
                        options=[
                            {"label": "crossing", "value": "crossing"},
                            {"label": "exposure", "value": "exposure"},
                        ],
                        value=args.edge_mode,
                        clearable=False,
                    ),
                ],
                style={"width": "220px", "display": "inline-block", "margin": "0 20px"},
            ),
            html.Div(
                [
                    dcc.Checklist(
                        id="show-edges",
                        options=[{"label": "Show edges", "value": "show"}],
                        value=["show"] if args.show_edges else [],
                    )
                ],
                style={"display": "inline-block", "margin": "0 20px"},
            ),
            dcc.Graph(id="geo-graph", style={"height": "80vh"}),
        ]
    )

    @app.callback(
        Output("geo-graph", "figure"),
        Input("tick-slider", "value"),
        Input("edge-mode", "value"),
        Input("show-edges", "value"),
    )
    def _update_map(tick_of_day: int, edge_mode: str, show_edges_values: Any) -> go.Figure:
        show_edges = "show" in (show_edges_values or [])
        return build_geo_figure(kernel, tick_of_day, edge_mode, show_edges)

    app.run_server(debug=False, port=args.port)


if __name__ == "__main__":
    main()
