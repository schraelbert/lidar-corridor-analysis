import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show

chm_path = "data/processed/chm_72.tif"
centerline_path = "data/processed/corridor_centerline.gpkg"
corridor_path = "data/processed/corridor_buffer.gpkg"

centerline = gpd.read_file(centerline_path)
corridor = gpd.read_file(corridor_path)

with rasterio.open(chm_path) as src:
    chm = src.read(1).astype(float)
    chm[chm == src.nodata] = np.nan

    fig, ax = plt.subplots(figsize=(10, 7))
    show(chm, transform=src.transform, ax=ax)

corridor.boundary.plot(ax=ax, linewidth=1.5)
centerline.plot(ax=ax, linewidth=1.5)

ax.set_title("Synthetic Corridor over Canopy Height Model")
ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")
plt.tight_layout()
plt.savefig("figures/corridor_over_chm.png", dpi=180)
plt.show()