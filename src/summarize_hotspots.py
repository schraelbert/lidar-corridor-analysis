import pandas as pd

from config import load_config, project_path


cfg = load_config()

input_path = project_path(
    cfg["outputs"]["profile_csv"]
)

output_path = project_path(
    cfg["outputs"]["hotspot_csv"]
)

top_n = cfg["screening"]["top_n"]
metric = cfg["screening"]["hotspot_metric"]

df = pd.read_csv(input_path)

top = (
    df.sort_values(
        metric,
        ascending=False,
    )
    .head(top_n)
    .copy()
)

top.insert(
    0,
    "rank",
    range(1, len(top) + 1),
)

columns = [
    "rank",
    "distance_m",
    "start_m",
    "end_m",
    "mean_m",
    "p95_m",
    "max_m",
]

top = top[columns]

top.to_csv(
    output_path,
    index=False,
    float_format="%.2f",
)

print(top.to_string(index=False))
print()
print(f"Saved: {output_path}")