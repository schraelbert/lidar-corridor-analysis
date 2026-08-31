import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString

from config import load_config, project_path


cfg = load_config()

top_n = cfg["screening"]["top_n"]
metric = cfg["screening"]["hotspot_metric"]
half_width = cfg["corridor"]["width_m"] / 2.0

profile_path = project_path(
    cfg["outputs"]["profile_csv"]
)

centerline_path = project_path(
    cfg["outputs"]["centerline"]
)

output_path = project_path(
    cfg["outputs"]["hotspots"]
)

df = pd.read_csv(profile_path)
centerline_gdf = gpd.read_file(centerline_path)

line = centerline_gdf.geometry.iloc[0]

top = (
    df.sort_values(
        metric,
        ascending=False,
    )
    .head(top_n)
    .copy()
    .reset_index(drop=True)
)

records = []

for rank, row in top.iterrows():
    start = row["start_m"]
    end = row["end_m"]

    p0 = line.interpolate(start)
    p1 = line.interpolate(end)

    segment = LineString([p0, p1])

    hotspot = segment.buffer(
        half_width,
        cap_style=2,
    )

    records.append(
        {
            "rank": rank + 1,
            "start_m": start,
            "end_m": end,
            "distance_m": row["distance_m"],
            "mean_m": row["mean_m"],
            "p95_m": row["p95_m"],
            "max_m": row["max_m"],
            "geometry": hotspot,
        }
    )

hotspots = gpd.GeoDataFrame(
    records,
    crs=centerline_gdf.crs,
)

hotspots.to_file(
    output_path,
    layer="hotspots",
    driver="GPKG",
)

print(
    top[
        [
            "distance_m",
            "start_m",
            "end_m",
            "mean_m",
            "p95_m",
            "max_m",
        ]
    ].to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}",
    )
)

print()
print(
    f"Saved top {top_n} hotspot segments "
    f"ranked by {metric}:"
)
print(output_path)