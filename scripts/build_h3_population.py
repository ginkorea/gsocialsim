import argparse
import csv
import glob
import math
import os

try:
    import rasterio
except Exception as exc:  # pragma: no cover
    raise SystemExit("rasterio is required: pip install -r requirements-geo.txt") from exc

try:
    import h3
except Exception as exc:  # pragma: no cover
    raise SystemExit("h3 is required: pip install -r requirements.txt") from exc


def iter_blocks(src, band=1):
    for _, window in src.block_windows(band):
        data = src.read(band, window=window, masked=True)
        if data is None:
            continue
        if data.mask.all():
            continue
        yield window, data


def main() -> None:
    p = argparse.ArgumentParser(description="Aggregate a population GeoTIFF into H3 cells.")
    p.add_argument("--tif", nargs="+", default=[], help="Path(s) to population GeoTIFF(s)")
    p.add_argument("--tif-dir", default="", help="Directory containing GeoTIFF tiles")
    p.add_argument("--out", default="data/geo/h3_population.csv", help="Output CSV path")
    p.add_argument("--res", type=int, default=6, help="H3 resolution")
    p.add_argument("--bbox", type=str, default="", help="Optional bbox min_lat,min_lon,max_lat,max_lon")
    p.add_argument("--min-pop", type=float, default=0.0, help="Skip pixels below this population")
    p.add_argument("--max-pop", type=float, default=1.0e7, help="Skip pixels above this population (nodata guard)")
    args = p.parse_args()

    tif_paths = list(args.tif)
    if args.tif_dir:
        tif_paths.extend(glob.glob(os.path.join(args.tif_dir, "*.tif")))
        tif_paths.extend(glob.glob(os.path.join(args.tif_dir, "*.tiff")))
    tif_paths = sorted(set(tif_paths))
    if not tif_paths:
        raise SystemExit("No GeoTIFFs provided. Use --tif or --tif-dir.")

    bbox = None
    if args.bbox:
        parts = [float(x) for x in args.bbox.split(",")]
        if len(parts) == 4:
            bbox = (parts[0], parts[1], parts[2], parts[3])

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    agg = {}
    for tif_path in tif_paths:
        print(f"Processing {tif_path}")
        with rasterio.open(tif_path) as src:
            transform = src.transform
            nodata = src.nodata
            scale = src.scales[0] if src.scales and len(src.scales) > 0 else 1.0
            offset = src.offsets[0] if src.offsets and len(src.offsets) > 0 else 0.0
            for window, data in iter_blocks(src):
                # window offsets
                row_off, col_off = int(window.row_off), int(window.col_off)
                rows, cols = data.shape
                for r in range(rows):
                    for c in range(cols):
                        v = data[r, c]
                        if v is None:
                            continue
                        try:
                            v = float(v)
                        except Exception:
                            continue
                        if math.isnan(v):
                            continue
                        if nodata is not None and v == nodata:
                            continue
                        v = v * scale + offset
                        if v <= args.min_pop or v > args.max_pop:
                            continue
                        row = row_off + r
                        col = col_off + c
                        lon, lat = rasterio.transform.xy(transform, row, col, offset="center")
                        if bbox:
                            min_lat, min_lon, max_lat, max_lon = bbox
                            if lat < min_lat or lat > max_lat or lon < min_lon or lon > max_lon:
                                continue
                        cell = h3.latlng_to_cell(lat, lon, args.res)
                        agg[cell] = agg.get(cell, 0.0) + float(v)

    with open(args.out, mode="w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["h3_cell", "population"])
        for cell, pop in agg.items():
            w.writerow([cell, f"{pop:.4f}"])

    print(f"Wrote {len(agg)} H3 cells to {args.out}")


if __name__ == "__main__":
    main()
