import geopandas as gpd
from shapely.geometry import LineString

from config import load_config, project_path


cfg = load_config()

start = cfg["corridor"]["start"]
end = cfg["corridor"]["end"]
width = cfg["corridor"]["width_m"]
half_width = width / 2.0

centerline_path = project_path(cfg["outputs"]["centerline"])
corridor_path = project_path(cfg["outputs"]["corridor"])

centerline_path.parent.mkdir(parents=True, exist_ok=True)

line = LineString([start, end])

centerline = gpd.GeoDataFrame(
    {"name": ["synthetic_corridor"]},
    geometry=[line],
    crs="EPSG:25832",
)

corridor = centerline.copy()
corridor["geometry"] = corridor.buffer(half_width)

centerline.to_file(
    centerline_path,
    driver="GPKG",
)

corridor.to_file(
    corridor_path,
    driver="GPKG",
)

print(f"Centerline length: {line.length:.1f} m")
print(f"Corridor width: {width:.1f} m")