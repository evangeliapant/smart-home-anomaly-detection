from __future__ import annotations
import pandas as pd
import numpy as np

def compute_cluster_daily_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: features_with_models.csv-like DF with at least:
      window_start, cluster, total_events, n_sensors_active
    Output: per (date, cluster) stats.
    """
    x = df.copy()
    x["window_start"] = pd.to_datetime(x["window_start"])
    x["date"] = x["window_start"].dt.date
    x["hour"] = x["window_start"].dt.hour + x["window_start"].dt.minute / 60.0

    daily = (
        x.groupby(["date", "cluster"])
         .agg(
            windows=("cluster", "size"),
            mean_hour=("hour", "mean"),
            peak_hour=("hour", lambda s: float(s.round().mode().iloc[0])),
            total_events=("total_events", "sum"),
            mean_events_per_window=("total_events", "mean"),
            mean_unique_sensors=("n_sensors_active", "mean"),
         )
         .reset_index()
    )
    return daily

def compute_routine_scores(daily: pd.DataFrame) -> pd.DataFrame:
    """
    Computes routine stability per cluster across days.
    - frequency: fraction of days where cluster appears
    - time_consistency: std of peak_hour across active days (lower is more stable)
    - stability_score: combines both (simple and interpretable)
    """
    # total number of observed days
    n_days = daily["date"].nunique()

    per_cluster = (
        daily.groupby("cluster")
             .agg(
                active_days=("date", "nunique"),
                avg_peak_hour=("peak_hour", "mean"),
                std_peak_hour=("peak_hour", "std"),
                avg_windows_per_day=("windows", "mean"),
                avg_events_per_day=("total_events", "mean"),
                avg_unique_sensors=("mean_unique_sensors", "mean"),
             )
             .reset_index()
    )

    per_cluster["frequency"] = per_cluster["active_days"] / max(n_days, 1)
    per_cluster["std_peak_hour"] = per_cluster["std_peak_hour"].fillna(0.0)

    # simple stability score: high frequency + high time regularity
    # (normalize std: 0 -> best, >4 hours -> poor)
    per_cluster["time_consistency"] = 1.0 - np.clip(per_cluster["std_peak_hour"] / 4.0, 0, 1)
    per_cluster["stability_score"] = 0.6 * per_cluster["frequency"] + 0.4 * per_cluster["time_consistency"]

    return per_cluster.sort_values("stability_score", ascending=False)

def suggest_automations(routines: pd.DataFrame, profiles: dict[int, object]) -> pd.DataFrame:
    """
    Uses routine score + cluster profile to generate automation suggestions.
    Keeps suggestions conservative and explainable.
    """
    rows = []
    for _, r in routines.iterrows():
        cid = int(r["cluster"])
        prof = profiles.get(cid)
        top_sensor = getattr(prof, "top_sensor", "Unknown") if prof else "Unknown"
        peak = float(r["avg_peak_hour"])
        freq = float(r["frequency"])
        score = float(r["stability_score"])

        suggestion = "No suggestion"
        if score >= 0.70 and freq >= 0.50:
            if str(top_sensor).lower().startswith("kitchen"):
                suggestion = f"Recurring kitchen activity around {peak:.1f}h → suggest ventilation/heating pre-adjustment"
            elif str(top_sensor).lower().startswith("living"):
                suggestion = f"Recurring living-room presence around {peak:.1f}h → suggest comfort lighting/heating"
            elif str(top_sensor).lower().startswith("bathroom"):
                suggestion = f"Recurring bathroom routine around {peak:.1f}h → suggest bathroom heating"
            else:
                suggestion = f"Stable routine around {peak:.1f}h (top sensor: {top_sensor}) → suggest comfort adjustment"

        rows.append({
            "cluster": cid,
            "top_sensor": top_sensor,
            "avg_peak_hour": peak,
            "frequency": freq,
            "stability_score": score,
            "suggestion": suggestion
        })

    return pd.DataFrame(rows).sort_values(["stability_score", "frequency"], ascending=False)
