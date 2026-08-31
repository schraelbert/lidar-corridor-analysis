import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show

from config import load_config, project_path


cfg = load_config()

chm_path = project_path(cfg["input"]["chm"])
centerline_path = project_path(cfg["outputs"]["centerline"])
corridor_path = project_path(cfg["outputs"]["corridor"])

figure_path = project_path(
    "figures/corridor_over_chm.png"
)

centerline = gpd.read_file(centerline_path)
corridor = gpd.read_file(corridor_path)

with rasterio.open(chm_path) as src:
    if centerline.crs != src.crs:
        centerline = centerline.to_crs(src.crs)

    if corridor.crs != src.crs:
        corridor = corridor.to_crs(src.crs)

    chm = src.read(1).astype(float)

    if src.nodata is not None:
        chm[chm == src.nodata] = np.nan

    fig, ax = plt.subplots(figsize=(10, 7))

    show(
        chm,
        transform=src.transform,
        ax=ax,
    )

corridor.boundary.plot(
    ax=ax,
    linewidth=1.5,
)

centerline.plot(
    ax=ax,
    linewidth=1.5,
)

ax.set_title(
    "Synthetic Corridor over Canopy Height Model"
)
ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")

plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.show()