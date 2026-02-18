from __future__ import annotations

import pandas as pd

from src.automation.simulator import (
    explain_anomaly,
    build_cluster_profiles,
    automation_from_cluster,
    infer_sensor_columns,
)

def main():
    df = pd.read_csv("data/processed/features_with_models.csv")

    # --- Anomalies ---
    anomalies = df[df["is_anomaly"] == True].copy()
    anomalies = anomalies.sort_values("anomaly_score").head(10)

    print("\nTop 10 anomalies:")
    for _, r in anomalies.iterrows():
        print(r["window_start"], "-", explain_anomaly(r))

    # --- Cluster profiles (dynamic) ---
    sensor_cols = infer_sensor_columns(df)
    profiles = build_cluster_profiles(df, sensor_cols=sensor_cols)

    print("\nCluster profiles (summary):")
    for cid, p in profiles.items():
        print(
            f"cluster={cid} peak_hour={p.peak_hour} "
            f"top_sensor={p.top_sensor} mean_events={p.mean_total_events:.2f}"
        )

    # --- Automations derived from profiles ---
    print("\nSample automations (first 15 rows):")
    for _, r in df.head(15).iterrows():
        action = automation_from_cluster(int(r["cluster"]), profiles)
        print(r["window_start"], "-", action)

if __name__ == "__main__":
    main()
