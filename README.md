# LiDAR Corridor Analysis

Exploratory airborne LiDAR processing, terrain modelling, and corridor-based geospatial analysis.

This project demonstrates a compact workflow for processing airborne laser-scanning data, deriving terrain and canopy-height products, constructing a synthetic corridor, and screening for high-vegetation segments.

## Workflow

```text
LAZ
 |
 v
Point-cloud inspection
 |
 v
Ground classification
 |
 v
Digital terrain model
 |
 v
Height above ground
 |
 v
Canopy height model
 |
 v
Synthetic corridor
 |
 v
Corridor statistics
 |
 v
Longitudinal vegetation profile
 |
 v
High-vegetation hotspot screening
```

## Environment

The analysis environment is containerized with Docker and built from conda-forge packages.

Main tools include:

* PDAL
* GDAL
* Python
* GeoPandas
* Rasterio
* laspy
* NumPy
* pandas
* matplotlib

Build the container:

```bash
docker build -t lidar-corridor-analysis .
```

Run it from the project directory:

```bash
docker run --rm -it \
  -v "$PWD:/workspace" \
  -w /workspace \
  lidar-corridor-analysis
```

## Data

The initial analysis uses airborne LiDAR data from Kartverket's national elevation-data service.

The current test data are referenced in:

* ETRS89 / UTM zone 32N
* EPSG:25832
* NN2000 vertical datum

The source point cloud contains official point classification, including classified ground points.

Raw LiDAR files are not included in the repository.

## Processing

The current workflow:

1. inspects LAZ metadata, coordinate reference information, and point classifications
2. extracts officially classified ground points
3. generates a 1 m digital terrain model
4. computes height above ground for the original point cloud
5. generates a 1 m canopy height model
6. creates a synthetic 40 m corridor
7. computes corridor-level canopy statistics
8. builds a longitudinal vegetation profile using 10 m segments
9. ranks high-vegetation hotspot segments using p95 canopy height

## Point Cloud

The first processed tile contains approximately 6.38 million points.

The source classification is dominated by:

* class 1: unclassified points
* class 2: ground points
* class 7: noise

Approximately 15% of the points are classified as ground.

The source data use:

* horizontal CRS: ETRS89 / UTM zone 32N
* horizontal EPSG code: 25832
* vertical reference: NN2000
* vertical EPSG code: 5941

## Digital Terrain Model

A 1 m digital terrain model is generated from the officially classified ground points.

For the current tile:

* minimum terrain elevation: 283.30 m
* maximum terrain elevation: 381.56 m
* mean terrain elevation: 342.62 m

The generated raster has full valid coverage over the processed tile.

## Height Above Ground

Height above ground is computed by sampling the terrain model for the original LiDAR point cloud.

For the current tile:

* point count: 6,376,095
* minimum height above ground: 0.00 m
* maximum height above ground: 36.05 m
* mean height above ground: 8.52 m
* median height above ground: 8.70 m
* p95 height above ground: 19.29 m
* p99 height above ground: 23.26 m

No values below -0.5 m were observed.

## Canopy Height Model

A 1 m canopy height model is generated using the maximum height-above-ground value within each raster cell.

For the current tile:

* minimum canopy height: 0.00 m
* maximum canopy height: 36.05 m
* mean canopy height: 14.47 m

## Synthetic Corridor

A synthetic corridor is constructed across the test tile.

Current geometry:

* centerline length: approximately 806 m
* corridor width: 40 m
* half-width: 20 m

The corridor is used as a controlled test geometry for vegetation analysis.

## Corridor Statistics

For the current synthetic corridor:

* valid corridor pixels: 33,499
* mean canopy height: 14.03 m
* median canopy height: 13.98 m
* p95 canopy height: 23.03 m
* maximum canopy height: 31.69 m

Canopy-height screening within the corridor shows:

* 76.0% of pixels above 10 m
* 44.1% of pixels above 15 m
* 15.9% of pixels above 20 m
* 2.1% of pixels above 25 m

## Longitudinal Vegetation Profile

The corridor centerline is divided into 10 m segments.

For each segment, the workflow computes:

* mean canopy height
* p95 canopy height
* maximum canopy height
* number of valid raster pixels

This produces a longitudinal vegetation profile showing how canopy structure changes along the corridor.

The strongest vegetation zones are concentrated in several distinct portions of the centerline rather than being uniformly distributed.

## High-Vegetation Hotspots

Hotspot segments are ranked using p95 canopy height.

The highest-ranked segment occurs near 803 m along the centerline.

For this segment:

* mean canopy height: 23.15 m
* p95 canopy height: 30.07 m
* maximum canopy height: 31.69 m

The current top-ranked hotspot segments are concentrated around:

* 90-130 m
* 620-690 m
* 790-806 m

The hotspot ranking is intended as a vegetation-screening metric.

It is not interpreted as an infrastructure-clearance assessment because no conductor geometry, tower geometry, sag model, or operational clearance threshold is included in the current workflow.

## Outputs

Generated products include:

* digital terrain model
* height-above-ground point cloud
* canopy height model
* synthetic corridor centerline
* synthetic corridor polygon
* corridor-level vegetation statistics
* longitudinal vegetation profile
* ranked hotspot segments
* hotspot GeoPackage
* hotspot summary CSV

Generated figures are stored under `figures/`.

Generated data products are stored under `data/processed/`.

Raw and processed data products are excluded from version control.

## Repository Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── figures/
├── pipelines/
│   ├── make_dtm.json
│   ├── make_hag.json
│   └── make_chm.json
├── src/
│   ├── analyze_corridor.py
│   ├── extract_hotspots.py
│   ├── make_corridor.py
│   ├── plot_corridor.py
│   ├── plot_hotspots.py
│   ├── profile_corridor.py
│   └── summarize_hotspots.py
├── Dockerfile
├── environment.yml
└── README.md
```

## Current Scope

The current implementation focuses on a single test tile and a synthetic corridor.

The workflow demonstrates:

* airborne LiDAR ingestion
* use of official ground classification
* terrain modelling
* canopy-height derivation
* corridor-based spatial analysis
* longitudinal vegetation profiling
* hotspot ranking

The project is intended as an exploratory and reproducible geospatial-processing workflow that can be extended to additional tiles and corridor geometries.

