import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask

chm_path = "data/processed/chm_72.tif"
corridor_path = "data/processed/corridor_buffer.gpkg"

corridor = gpd.read_file(corridor_path)

with rasterio.open(chm_path) as src:
    corridor = corridor.to_crs(src.crs)

    data, _ = mask(
        src,
        corridor.geometry,
        crop=True,
        filled=False
    )

    chm = data[0].compressed()

print(f"Valid corridor pixels: {chm.size:,}")
print(f"Mean canopy height:     {np.mean(chm):.2f} m")
print(f"Median canopy height:   {np.median(chm):.2f} m")
print(f"P95 canopy height:      {np.percentile(chm, 95):.2f} m")
print(f"Maximum canopy height:  {np.max(chm):.2f} m")

for threshold in [10, 15, 20, 25]:
    count = np.sum(chm > threshold)
    pct = 100 * count / chm.size
    area = count * 1.0  # 1 m x 1 m pixels

    print(
        f"> {threshold:2d} m: "
        f"{count:6,d} pixels, "
        f"{area:8.0f} m2, "
        f"{pct:5.1f}%"
    )