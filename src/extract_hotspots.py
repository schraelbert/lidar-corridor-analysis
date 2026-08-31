import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString


TOP_N = 10
HALF_WIDTH = 20.0

profile_path = "data/processed/corridor_profile.csv"
centerline_path = "data/processed/corridor_centerline.gpkg"
output_path = "data/processed/corridor_hotspots.gpkg"

df = pd.read_csv(profile_path)
centerline_gdf = gpd.read_file(centerline_path)

line = centerline_gdf.geometry.iloc[0]

top = (
    df.sort_values("p95_m", ascending=False)
      .head(TOP_N)
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
    hotspot = segment.buffer(HALF_WIDTH, cap_style=2)

    records.append({
        "rank": rank + 1,
        "start_m": start,
        "end_m": end,
        "distance_m": row["distance_m"],
        "mean_m": row["mean_m"],
        "p95_m": row["p95_m"],
        "max_m": row["max_m"],
        "geometry": hotspot,
    })

hotspots = gpd.GeoDataFrame(
    records,
    crs=centerline_gdf.crs
)

hotspots.to_file(
    output_path,
    layer="hotspots",
    driver="GPKG"
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
        float_format=lambda x: f"{x:.2f}"
    )
)

print()
print(f"Saved top {TOP_N} hotspot segments to:")
print(output_path)