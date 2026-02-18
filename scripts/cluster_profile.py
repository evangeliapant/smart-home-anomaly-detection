import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/features_with_models.csv")
df["window_start"] = pd.to_datetime(df["window_start"])
df["hour"] = df["window_start"].dt.hour + df["window_start"].dt.minute / 60

sensor_cols = [
    "Bathroom",
    "Bedroom",
    "DiningRoom",
    "Kitchen",
    "LivingRoom",
    "OutsideDoor"
]

print("\n==== CLUSTER PROFILES ====\n")

for k in sorted(df["cluster"].unique()):
    sub = df[df["cluster"] == k]

    mean_hour = round(sub["hour"].mean(), 2)
    peak_hour = sub["hour"].round().mode().iloc[0]

    top = sub[sensor_cols].mean().sort_values(ascending=False)

    print(f"\nCLUSTER {k}")
    print(f"count = {len(sub)}")
    print(f"mean_hour = {mean_hour}")
    print(f"peak_hour = {peak_hour}")
    print("\nTop sensors (mean activations per window):")
    print(top)
    print("-" * 40)