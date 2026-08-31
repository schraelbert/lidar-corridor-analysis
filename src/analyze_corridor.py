import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask

from config import load_config, project_path


cfg = load_config()

chm_path = project_path(cfg["input"]["chm"])
corridor_path = project_path(cfg["outputs"]["corridor"])
thresholds = cfg["screening"]["height_thresholds_m"]

corridor = gpd.read_file(corridor_path)

with rasterio.open(chm_path) as src:
    corridor = corridor.to_crs(src.crs)

    data, _ = mask(
        src,
        corridor.geometry,
        crop=True,
        filled=False,
    )

    chm = data[0].compressed()

    pixel_area = abs(
        src.transform.a * src.transform.e
    )

print(f"Valid corridor pixels: {chm.size:,}")
print(f"Mean canopy height:     {np.mean(chm):.2f} m")
print(f"Median canopy height:   {np.median(chm):.2f} m")
print(f"P95 canopy height:      {np.percentile(chm, 95):.2f} m")
print(f"Maximum canopy height:  {np.max(chm):.2f} m")

for threshold in thresholds:
    count = np.sum(chm > threshold)
    pct = 100 * count / chm.size
    area = count * pixel_area

    print(
        f"> {threshold:2g} m: "
        f"{count:6,d} pixels, "
        f"{area:8.0f} m2, "
        f"{pct:5.1f}%"
    )