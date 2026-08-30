# LiDAR Corridor Analysis

An exploratory scientific-computing project for airborne LiDAR point-cloud processing, terrain modelling, and corridor-based geospatial analysis using Norwegian laser-scanning data.

## Planned workflow

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
Corridor extraction
 |
 v
Vegetation and object screening

## Environment

The analysis environment is fully containerized.

```bash
docker build -t lidar-corridor-analysis .

docker run --rm -it \
  -v "$PWD:/workspace" \
  -w /workspace \
  lidar-corridor-analysis
