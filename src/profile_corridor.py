import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from shapely.geometry import LineString


SEGMENT_LENGTH = 10.0
HALF_WIDTH = 20.0

chm_path = "data/processed/chm_72.tif"
centerline_path = "data/processed/corridor_centerline.gpkg"

centerline_gdf = gpd.read_file(centerline_path)
line = centerline_gdf.geometry.iloc[0]

records = []

with rasterio.open(chm_path) as src:
    if centerline_gdf.crs != src.crs:
        centerline_gdf = centerline_gdf.to_crs(src.crs)
        line = centerline_gdf.geometry.iloc[0]

    distances = np.arange(0, line.length, SEGMENT_LENGTH)

    for start in distances:
        end = min(start + SEGMENT_LENGTH, line.length)

        p0 = line.interpolate(start)
        p1 = line.interpolate(end)

        segment = LineString([p0, p1])
        corridor_segment = segment.buffer(HALF_WIDTH, cap_style=2)

        data, _ = mask(
            src,
            [corridor_segment],
            crop=True,
            filled=False
        )

        values = data[0].compressed()

        if values.size == 0:
            continue

        records.append({
            "distance_m": 0.5 * (start + end),
            "start_m": start,
            "end_m": end,
            "pixel_count": values.size,
            "mean_m": np.mean(values),
            "p95_m": np.percentile(values, 95),
            "max_m": np.max(values),
        })


df = pd.DataFrame(records)

out_csv = "data/processed/corridor_profile.csv"
df.to_csv(out_csv, index=False)

print(df.head())
print()
print(f"Segments: {len(df)}")
print(f"Highest P95: {df['p95_m'].max():.2f} m")
print(
    "Highest-P95 location: "
    f"{df.loc[df['p95_m'].idxmax(), 'distance_m']:.1f} m"
)
print(f"Maximum canopy height: {df['max_m'].max():.2f} m")

plt.figure(figsize=(11, 5))

plt.plot(
    df["distance_m"],
    df["mean_m"],
    label="Mean"
)

plt.plot(
    df["distance_m"],
    df["p95_m"],
    label="P95"
)

plt.plot(
    df["distance_m"],
    df["max_m"],
    label="Max"
)

plt.xlabel("Distance along corridor centerline (m)")
plt.ylabel("Canopy height (m)")
plt.title("Longitudinal Vegetation Profile")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    "figures/corridor_profile.png",
    dpi=180
)

plt.show()