import argparse
import os
import urllib.parse
import urllib.request


WORLDPOP_IMAGE_SERVER = (
    "https://worldpop.arcgis.com/arcgis/rest/services/"
    "WorldPop_Total_Population_1km/ImageServer/exportImage"
)
WORLDPOP_EXTENT = (-180.0, -72.00041617728999, 179.99999856, 84.00791653201003)


def download(url: str, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"Downloading: {url}")
    print(f"Output: {out_path}")
    urllib.request.urlretrieve(url, out_path)
    print("Done.")


def build_export_url(
    *,
    bbox: str,
    size: str,
    time_value: str | None,
    fmt: str = "tiff",
    base_url: str = WORLDPOP_IMAGE_SERVER,
) -> str:
    params = {
        "bbox": bbox,
        "bboxSR": "4326",
        "size": size,
        "imageSR": "4326",
        "format": fmt,
        "f": "image",
    }
    if time_value:
        params["time"] = time_value
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def clamp_bbox(bbox: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    min_lat, min_lon, max_lat, max_lon = bbox
    min_x, min_y, max_x, max_y = WORLDPOP_EXTENT
    min_lon = max(min_lon, min_x)
    max_lon = min(max_lon, max_x)
    min_lat = max(min_lat, min_y)
    max_lat = min(max_lat, max_y)
    return min_lat, min_lon, max_lat, max_lon


def year_to_epoch_ms(year: int) -> int:
    # 00:00:00 UTC Jan 1 of the year
    import datetime

    dt = datetime.datetime(year, 1, 1, tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000)


def time_candidates(year: int, mode: str) -> list[str | None]:
    if mode == "none":
        return [None]
    if mode == "iso":
        return [f"{year}-01-01"]
    if mode == "ms":
        return [str(year_to_epoch_ms(year))]
    # auto
    return [str(year_to_epoch_ms(year)), f"{year}-01-01", None]


def main() -> None:
    p = argparse.ArgumentParser(description="Download WorldPop population GeoTIFF via ArcGIS export.")
    p.add_argument("--bbox", required=True, help="min_lat,min_lon,max_lat,max_lon")
    p.add_argument("--out", default="data/geo/worldpop.tif", help="Output file path (or prefix if tiled)")
    p.add_argument("--year", type=int, default=2020, help="Year (2000-2020)")
    p.add_argument("--size", default="4096,4096", help="Image size, max 4096x4096")
    p.add_argument("--tiles", default="", help="Optional tiling rows,cols (e.g., 2,4)")
    p.add_argument("--format", default="tiff", help="Output format (e.g., tiff, png)")
    p.add_argument(
        "--time-mode",
        default="auto",
        choices=["auto", "ms", "iso", "none"],
        help="Time parameter mode for ImageServer requests",
    )
    p.add_argument(
        "--base-url",
        default=WORLDPOP_IMAGE_SERVER,
        help="ArcGIS exportImage endpoint to use (defaults to worldpop.arcgis.com)",
    )
    args = p.parse_args()

    if args.tiles:
        if "," in args.tiles:
            rows, cols = [int(x) for x in args.tiles.split(",")]
        else:
            rows = cols = int(args.tiles)
        min_lat, min_lon, max_lat, max_lon = [float(x) for x in args.bbox.split(",")]
        min_lat, min_lon, max_lat, max_lon = clamp_bbox((min_lat, min_lon, max_lat, max_lon))
        lat_step = (max_lat - min_lat) / rows
        lon_step = (max_lon - min_lon) / cols
        for r in range(rows):
            for c in range(cols):
                tile_min_lat = min_lat + r * lat_step
                tile_max_lat = min_lat + (r + 1) * lat_step
                tile_min_lon = min_lon + c * lon_step
                tile_max_lon = min_lon + (c + 1) * lon_step
                bbox = f"{tile_min_lat},{tile_min_lon},{tile_max_lat},{tile_max_lon}"
                time_values = time_candidates(args.year, args.time_mode)
                out_path = args.out.replace(".tif", f"_r{r}_c{c}.tif")
                if os.path.exists(out_path):
                    print(f"File exists: {out_path}")
                    continue
                last_err = None
                for time_value in time_values:
                    url = build_export_url(
                        bbox=bbox,
                        size=args.size,
                        time_value=time_value,
                        fmt=args.format,
                        base_url=args.base_url,
                    )
                    try:
                        download(url, out_path)
                        last_err = None
                        break
                    except Exception as exc:
                        last_err = exc
                        if os.path.exists(out_path):
                            os.remove(out_path)
                if last_err is not None:
                    raise last_err
        return

    if os.path.exists(args.out):
        print(f"File exists: {args.out}")
        return

    min_lat, min_lon, max_lat, max_lon = [float(x) for x in args.bbox.split(",")]
    min_lat, min_lon, max_lat, max_lon = clamp_bbox((min_lat, min_lon, max_lat, max_lon))
    bbox = f"{min_lat},{min_lon},{max_lat},{max_lon}"
    last_err = None
    for time_value in time_candidates(args.year, args.time_mode):
        url = build_export_url(bbox=bbox, size=args.size, time_value=time_value, fmt=args.format, base_url=args.base_url)
        try:
            download(url, args.out)
            last_err = None
            break
        except Exception as exc:
            last_err = exc
            if os.path.exists(args.out):
                os.remove(args.out)
    if last_err is not None:
        raise last_err


if __name__ == "__main__":
    main()
