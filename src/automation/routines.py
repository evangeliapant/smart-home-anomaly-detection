from __future__ import annotations

import numpy as np
import pandas as pd


def compute_cluster_daily_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: features_with_models.csv-like DF with at least:
      window_start, cluster, total_events, n_sensors_active

    Output: per (date, cluster) stats.
    """
    x = df.copy()
    x["window_start"] = pd.to_datetime(x["window_start"], errors="coerce")
    x = x.dropna(subset=["window_start"])

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

    Metrics:
    - frequency: fraction of days where cluster appears
    - std_peak_hour: standard deviation of peak_hour across active days (lower is more stable)
    - time_consistency: normalized [0..1] version of std_peak_hour (higher is better)
    - stability_score: combined score (interpretable, tunable)

    Returns:
      DataFrame with one row per cluster, sorted by stability_score descending.
    """
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

    # Normalize std: 0 hours -> best, >=4 hours -> poor (clipped)
    per_cluster["time_consistency"] = 1.0 - np.clip(per_cluster["std_peak_hour"] / 4.0, 0, 1)

    # Combined stability score (tunable weights)
    per_cluster["stability_score"] = 0.6 * per_cluster["frequency"] + 0.4 * per_cluster["time_consistency"]

    return per_cluster.sort_values("stability_score", ascending=False)


def suggest_automations(routines: pd.DataFrame, profiles: dict[int, object]) -> pd.DataFrame:
    """
    Uses routine score + cluster profile to generate automation suggestions.

    Semi-industrial tiering:
      - AUTO: very stable and frequent -> can be applied automatically
      - RECOMMEND: reasonably stable -> recommend/confirm with user
      - MONITOR: too uncertain -> don't act, only monitor

    Returns:
      DataFrame with one row per cluster, including tier (level) and suggestion text.
    """
    rows = []

    for _, r in routines.iterrows():
        cid = int(r["cluster"])
        prof = profiles.get(cid)

        top_sensor = getattr(prof, "top_sensor", "Unknown") if prof else "Unknown"
        peak = float(r["avg_peak_hour"])
        freq = float(r["frequency"])
        score = float(r["stability_score"])

        # Tier decision (tunable)
        if score >= 0.80 and freq >= 0.80:
            level = "AUTO"
        elif score >= 0.60 and freq >= 0.60:
            level = "RECOMMEND"
        else:
            level = "MONITOR"

        suggestion = "No suggestion"
        if level != "MONITOR":
            ts = str(top_sensor).lower()

            if ts.startswith("kitchen"):
                suggestion = (
                    f"{level}: recurring kitchen activity around {peak:.1f}h → "
                    "suggest ventilation/heating pre-adjustment"
                )
            elif ts.startswith("living"):
                suggestion = (
                    f"{level}: recurring living-room presence around {peak:.1f}h → "
                    "suggest comfort lighting/heating"
                )
            elif ts.startswith("bathroom"):
                suggestion = (
                    f"{level}: recurring bathroom routine around {peak:.1f}h → "
                    "suggest bathroom heating"
                )
            elif ts.startswith("bedroom"):
                suggestion = (
                    f"{level}: recurring bedroom routine around {peak:.1f}h → "
                    "suggest comfort/heating adjustment"
                )
            else:
                suggestion = (
                    f"{level}: stable routine around {peak:.1f}h (top sensor: {top_sensor}) → "
                    "suggest comfort adjustment"
                )

        rows.append(
            {
                "cluster": cid,
                "top_sensor": top_sensor,
                "avg_peak_hour": peak,
                "frequency": freq,
                "stability_score": score,
                "level": level,
                "suggestion": suggestion,
            }
        )

    return pd.DataFrame(rows).sort_values(["stability_score", "frequency"], ascending=False)