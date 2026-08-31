from pathlib import Path

import geopandas as gpd
from shapely.geometry import LineString

out = Path("data/processed")
out.mkdir(parents=True, exist_ok=True)

line = LineString([
    (601680, 6649250),
    (602320, 6649740),
])

centerline = gpd.GeoDataFrame(
    {"name": ["synthetic_corridor"]},
    geometry=[line],
    crs="EPSG:25832",
)

corridor = centerline.copy()
corridor["geometry"] = corridor.buffer(20)

centerline.to_file(out / "corridor_centerline.gpkg", driver="GPKG")
corridor.to_file(out / "corridor_buffer.gpkg", driver="GPKG")

print(f"Centerline length: {line.length:.1f} m")
print("Corridor width: 40 m")