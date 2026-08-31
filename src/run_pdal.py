import json
import subprocess
import tempfile

from config import load_config, project_path


cfg = load_config()

tile = cfg["input"]["tile"]

raw_laz = project_path(
    f"data/raw/32-1-515-135-{tile}.laz"
)

dtm = project_path(
    f"data/processed/dtm_{tile}.tif"
)

hag = project_path(
    f"data/processed/hag_{tile}.laz"
)

chm = project_path(
    cfg["input"]["chm"]
)

dtm_resolution = cfg["processing"]["dtm_resolution_m"]
chm_resolution = cfg["processing"]["chm_resolution_m"]

def run_pipeline(pipeline):
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
    ) as f:
        json.dump(pipeline, f, indent=2)
        path = f.name

    print(f"Running PDAL pipeline: {path}")

    subprocess.run(
        ["pdal", "pipeline", path],
        check=True,
    )


def make_dtm():
    pipeline = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": str(raw_laz),
            },
            {
                "type": "filters.expression",
                "expression": "Classification == 2",
            },
            {
                "type": "writers.gdal",
                "filename": str(dtm),
                "resolution": dtm_resolution,
                "output_type": "min",
                "gdaldriver": "GTiff",
                "window_size": 3,
            },
        ]
    }

    run_pipeline(pipeline)


def make_hag():
    pipeline = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": str(raw_laz),
            },
            {
                "type": "filters.hag_dem",
                "raster": str(dtm),
            },
            {
                "type": "writers.las",
                "filename": str(hag),
                "extra_dims": "HeightAboveGround=float32",
                "compression": "laszip",
            },
        ]
    }

    run_pipeline(pipeline)


def make_chm():
    pipeline = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": str(hag),
            },
            {
                "type": "filters.expression",
                "expression": "HeightAboveGround >= 0",
            },
            {
                "type": "writers.gdal",
                "filename": str(chm),
                "dimension": "HeightAboveGround",
                "resolution": chm_resolution,
                "output_type": "max",
                "gdaldriver": "GTiff",
                "nodata": -9999,
            },
        ]
    }

    run_pipeline(pipeline)


if __name__ == "__main__":
    print(f"Tile: {tile}")
    print(f"Raw LAZ: {raw_laz}")

    make_dtm()
    make_hag()
    make_chm()

    print()
    print("PDAL processing complete.")
    print(f"DTM: {dtm}")
    print(f"HAG: {hag}")
    print(f"CHM: {chm}")