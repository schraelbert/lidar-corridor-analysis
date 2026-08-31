import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from shapely.geometry import LineString

from config import load_config, project_path


cfg = load_config()

segment_length = cfg["corridor"]["segment_length_m"]
half_width = cfg["corridor"]["width_m"] / 2.0

chm_path = project_path(cfg["input"]["chm"])
centerline_path = project_path(cfg["outputs"]["centerline"])
out_csv = project_path(cfg["outputs"]["profile_csv"])

figure_path = project_path(
    "figures/corridor_profile.png"
)

centerline_gdf = gpd.read_file(centerline_path)

records = []

with rasterio.open(chm_path) as src:
    if centerline_gdf.crs != src.crs:
        centerline_gdf = centerline_gdf.to_crs(src.crs)

    line = centerline_gdf.geometry.iloc[0]

    distances = np.arange(
        0,
        line.length,
        segment_length,
    )

    for start in distances:
        end = min(
            start + segment_length,
            line.length,
        )

        p0 = line.interpolate(start)
        p1 = line.interpolate(end)

        segment = LineString([p0, p1])

        corridor_segment = segment.buffer(
            half_width,
            cap_style=2,
        )

        data, _ = mask(
            src,
            [corridor_segment],
            crop=True,
            filled=False,
        )

        values = data[0].compressed()

        if values.size == 0:
            continue

        records.append(
            {
                "distance_m": 0.5 * (start + end),
                "start_m": start,
                "end_m": end,
                "pixel_count": values.size,
                "mean_m": np.mean(values),
                "p95_m": np.percentile(values, 95),
                "max_m": np.max(values),
            }
        )

df = pd.DataFrame(records)

df.to_csv(
    out_csv,
    index=False,
)

print(df.head())
print()

print(f"Segments: {len(df)}")
print(f"Highest P95: {df['p95_m'].max():.2f} m")

print(
    "Highest-P95 location: "
    f"{df.loc[df['p95_m'].idxmax(), 'distance_m']:.1f} m"
)

print(
    f"Maximum canopy height: "
    f"{df['max_m'].max():.2f} m"
)

plt.figure(figsize=(11, 5))

plt.plot(
    df["distance_m"],
    df["mean_m"],
    label="Mean",
)

plt.plot(
    df["distance_m"],
    df["p95_m"],
    label="P95",
)

plt.plot(
    df["distance_m"],
    df["max_m"],
    label="Max",
)

plt.xlabel(
    "Distance along corridor centerline (m)"
)
plt.ylabel("Canopy height (m)")
plt.title("Longitudinal Vegetation Profile")

plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.show()