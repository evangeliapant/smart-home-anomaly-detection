from __future__ import annotations
import pandas as pd

from src.automation.simulator import (
    explain_anomaly,
    build_cluster_profiles,
    automation_from_cluster,
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

    # --- Habit stability modeling ---
    daily = compute_cluster_daily_stats(df)
    habits = compute_routine_scores(daily)
    suggestions = suggest_automations(habits, profiles)

    print("\nTop habit clusters:")
    print(habits.head(10)[["cluster","frequency","avg_peak_hour","std_peak_hour","stability_score"]])

    print("\nAutomation suggestions from stable habits:")
    print(suggestions.head(10)[["cluster","top_sensor","avg_peak_hour","frequency","stability_score","suggestion"]])

    # --- Automations derived from profiles (per-row demo) ---
    print("\nSample automations (first 15 rows):")
    for _, r in df.head(15).iterrows():
        action = automation_from_cluster(int(r["cluster"]), profiles)
        print(r["window_start"], "-", action)

if __name__ == "__main__":
    main()
