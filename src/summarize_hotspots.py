import pandas as pd


INPUT = "data/processed/corridor_profile.csv"
OUTPUT = "data/processed/top_hotspots.csv"
TOP_N = 10


df = pd.read_csv(INPUT)

top = (
    df.sort_values("p95_m", ascending=False)
      .head(TOP_N)
      .copy()
)

top.insert(
    0,
    "rank",
    range(1, len(top) + 1)
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
    OUTPUT,
    index=False,
    float_format="%.2f"
)

print(top.to_string(index=False))
print()
print(f"Saved: {OUTPUT}")