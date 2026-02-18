from __future__ import annotations
import pandas as pd

from src.automation.simulator import (
    explain_anomaly,
    build_cluster_profiles,
    infer_sensor_columns,
)

from src.automation.routines import (
    compute_cluster_daily_stats,
    compute_routine_scores,
    suggest_automations,
)

def main():
    df = pd.read_csv("data/processed/features_with_models.csv")

    # --- Anomalies ---
    anomalies = df[(df["is_anomaly"] == True) & (df["total_events"] > 0)].copy()
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

    # --- routine stability modeling ---
    daily = compute_cluster_daily_stats(df)
    routines = compute_routine_scores(daily)
    suggestions = suggest_automations(routines, profiles)

    print("\nTop routine clusters:")
    print(routines.head(10)[["cluster","frequency","avg_peak_hour","std_peak_hour","stability_score"]])

    print("\nAutomation suggestions from stable routines:")
    print(suggestions.head(10)[["cluster","top_sensor","avg_peak_hour","frequency","stability_score","level","suggestion"]])

    # Build a quick lookup: cluster -> suggestion text
    suggestion_map = {int(r["cluster"]): (r["level"], r["suggestion"]) for _, r in suggestions.iterrows()}

    # --- routine-based automation suggestions (per-row demo) ---
    print("\nSample routine-based automations (one example per cluster):")
    sample = df.sort_values("window_start").groupby("cluster", as_index=False).head(1)

    for _, r in sample.sort_values("cluster").iterrows():
        cid = int(r["cluster"])
        level, action = suggestion_map.get(cid, ("MONITOR", "No suggestion"))

        routine_peak = routines.loc[routines["cluster"] == cid, "avg_peak_hour"].iloc[0]

        print(
            r["window_start"],
            "-",
            f"[{level}]",
            action,
            f"(cluster={cid}, routine_peak≈{routine_peak:.1f}h)"
        )


if __name__ == "__main__":
    main()
