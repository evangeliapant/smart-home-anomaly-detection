from __future__ import annotations

import numpy as np
import pandas as pd


def compute_cluster_daily_stats(
    df: pd.DataFrame,
    active_only: bool = True,
    min_total_events: float = 1.0,
) -> pd.DataFrame:
    """
    Input: features_with_models.csv-like DF with at least:
      window_start, cluster, total_events, n_sensors_active

    Output: per (date, cluster) stats.
    By default, only windows with actual activity are used so inactivity-heavy
    clusters do not dominate routine scoring.
    """
    x = df.copy()
    x["window_start"] = pd.to_datetime(x["window_start"], errors="coerce")
    x = x.dropna(subset=["window_start"])

    if active_only:
        x = x[x["total_events"] >= min_total_events].copy()

    if x.empty:
        return pd.DataFrame(
            columns=[
                "date",
                "cluster",
                "windows",
                "mean_hour",
                "peak_hour",
                "total_events",
                "mean_events_per_window",
                "mean_unique_sensors",
            ]
        )

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
    - frequency: fraction of active days where cluster appears
    - std_peak_hour: standard deviation of peak_hour across active days
    - time_consistency: normalized [0..1] version of std_peak_hour
    - stability_score: combined score
    """
    if daily.empty:
        return pd.DataFrame(
            columns=[
                "cluster",
                "active_days",
                "avg_peak_hour",
                "std_peak_hour",
                "avg_windows_per_day",
                "avg_events_per_day",
                "avg_unique_sensors",
                "frequency",
                "time_consistency",
                "stability_score",
            ]
        )

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
    per_cluster["time_consistency"] = 1.0 - np.clip(per_cluster["std_peak_hour"] / 4.0, 0, 1)
    per_cluster["stability_score"] = 0.6 * per_cluster["frequency"] + 0.4 * per_cluster["time_consistency"]

    return per_cluster.sort_values("stability_score", ascending=False)


def suggest_automations(
    routines: pd.DataFrame,
    profiles: dict[int, object],
    allow_inactivity_clusters: bool = False,
) -> pd.DataFrame:
    """
    Uses routine score + cluster profile to generate automation suggestions.
    Inactivity-dominant clusters are downgraded to MONITOR by default.
    """
    rows = []

    for _, r in routines.iterrows():
        cid = int(r["cluster"])
        prof = profiles.get(cid)

        top_sensor = getattr(prof, "top_sensor", "Unknown") if prof else "Unknown"
        peak = float(r["avg_peak_hour"])
        freq = float(r["frequency"])
        score = float(r["stability_score"])
        inactivity_fraction = float(getattr(prof, "inactive_window_fraction", 0.0)) if prof else 0.0
        is_inactivity_cluster = bool(getattr(prof, "is_inactivity_cluster", False)) if prof else False

        if is_inactivity_cluster and not allow_inactivity_clusters:
            level = "MONITOR"
        elif score >= 0.80 and freq >= 0.80:
            level = "AUTO"
        elif score >= 0.60 and freq >= 0.60:
            level = "RECOMMEND"
        else:
            level = "MONITOR"

        suggestion = "No suggestion"
        if is_inactivity_cluster and not allow_inactivity_clusters:
            suggestion = "MONITOR: inactivity-dominant cluster excluded from automation suggestions"
        elif level != "MONITOR":
            ts = str(top_sensor).lower()

            if ts.startswith("kitchen"):
                suggestion = (
                    f"{level}: recurring kitchen activity around {peak:.1f}h -> "
                    "suggest ventilation/heating pre-adjustment"
                )
            elif ts.startswith("living"):
                suggestion = (
                    f"{level}: recurring living-room presence around {peak:.1f}h -> "
                    "suggest comfort lighting/heating"
                )
            elif ts.startswith("bathroom"):
                suggestion = (
                    f"{level}: recurring bathroom routine around {peak:.1f}h -> "
                    "suggest bathroom heating"
                )
            elif ts.startswith("bedroom"):
                suggestion = (
                    f"{level}: recurring bedroom routine around {peak:.1f}h -> "
                    "suggest comfort/heating adjustment"
                )
            else:
                suggestion = (
                    f"{level}: stable routine around {peak:.1f}h (top sensor: {top_sensor}) -> "
                    "suggest comfort adjustment"
                )

        rows.append(
            {
                "cluster": cid,
                "top_sensor": top_sensor,
                "avg_peak_hour": peak,
                "frequency": freq,
                "stability_score": score,
                "inactive_window_fraction": inactivity_fraction,
                "is_inactivity_cluster": is_inactivity_cluster,
                "level": level,
                "suggestion": suggestion,
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "cluster",
                "top_sensor",
                "avg_peak_hour",
                "frequency",
                "stability_score",
                "inactive_window_fraction",
                "is_inactivity_cluster",
                "level",
                "suggestion",
            ]
        )

    return pd.DataFrame(rows).sort_values(["stability_score", "frequency"], ascending=False)
