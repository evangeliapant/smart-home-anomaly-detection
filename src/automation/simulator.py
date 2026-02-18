from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd


# --------- Anomaly explanation (still simple but useful) ---------

def explain_anomaly(row: pd.Series) -> str:
    """
    Human-readable explanation of why a window might be anomalous.
    This is intentionally conservative (no medical claims).
    """
    total = float(row.get("total_events", 0))
    uniq = float(row.get("n_sensors_active", 0))

    if total == 0:
        return "No activity in this window (normal if short)"
    if total > 150:
        return "Unusually high event rate (burst of activity)"
    if uniq >= 6:
        return "Many sensors active in a short period (multi-room activity)"
    return "Unusual pattern (model-based)"


# --------- Cluster profiling (data-driven, no hardcoded cluster IDs) ---------

@dataclass(frozen=True)
class ClusterProfile:
    cluster_id: int
    mean_hour: float
    peak_hour: float
    mean_total_events: float
    mean_unique_sensors: float
    top_sensor: str


def _ensure_datetime(df: pd.DataFrame, time_col: str = "window_start") -> pd.DataFrame:
    out = df.copy()
    out[time_col] = pd.to_datetime(out[time_col], errors="coerce")
    out = out.dropna(subset=[time_col])
    return out


def infer_sensor_columns(df: pd.DataFrame) -> List[str]:
    """
    Try to infer which columns correspond to per-sensor feature counts.
    This helps make the system resilient when the set of sensors changes.
    """
    ignore = {
        "window_start",
        "date",
        "timestamp",
        "time",
        "total_events",
        "n_sensors_active",
        "tod_sin",
        "tod_cos",
        "dow",
        "cluster",
        "is_anomaly",
        "anomaly_score",
        "hour",
    }
    # heuristic: numeric columns that are not in ignore
    sensor_cols = []
    for c in df.columns:
        if c in ignore:
            continue
        if pd.api.types.is_numeric_dtype(df[c]):
            sensor_cols.append(c)
    return sensor_cols


def build_cluster_profiles(df: pd.DataFrame, sensor_cols: Optional[List[str]] = None) -> Dict[int, ClusterProfile]:
    """
    Builds a summary profile per cluster.
    Returns: dict cluster_id -> ClusterProfile
    """
    df = _ensure_datetime(df, "window_start")

    if "cluster" not in df.columns:
        raise ValueError("DataFrame must contain a 'cluster' column")

    if sensor_cols is None:
        sensor_cols = infer_sensor_columns(df)

    if not sensor_cols:
        raise ValueError(
            "No sensor columns found/inferred. Pass sensor_cols explicitly "
            "or ensure your feature table contains per-sensor numeric columns."
        )

    # compute hour-of-day float (ensure datetime for runtime safety)
    df = df.copy()
    df["window_start"] = pd.to_datetime(df["window_start"], errors="coerce")
    df = df.dropna(subset=["window_start"])
    df["hour"] = df["window_start"].dt.hour + df["window_start"].dt.minute / 60.0


    profiles: Dict[int, ClusterProfile] = {}

    for k in sorted(df["cluster"].unique()):
        sub = df[df["cluster"] == k]

        # Robust peak hour
        peak_hour = float(sub["hour"].round().mode().iloc[0]) if len(sub) else float("nan")

        # Top sensor by mean count
        sensor_means = sub[sensor_cols].mean(numeric_only=True)
        top_sensor = str(sensor_means.sort_values(ascending=False).index[0])

        profiles[int(k)] = ClusterProfile(
            cluster_id=int(k),
            mean_hour=float(sub["hour"].mean()),
            peak_hour=peak_hour,
            mean_total_events=float(sub.get("total_events", pd.Series([0])).mean()),
            mean_unique_sensors=float(sub.get("n_sensors_active", pd.Series([0])).mean()),
            top_sensor=top_sensor,
        )

    return profiles


# --------- Dynamic automation rule derivation ---------

def derive_automation_rule(profile: ClusterProfile) -> str:
    """
    Assign automation based on behavioral characteristics.
    These rules are general and depend on the cluster profile, not the cluster ID.
    """

    hour = profile.peak_hour
    top = profile.top_sensor
    activity = profile.mean_total_events
    uniq = profile.mean_unique_sensors

    # Very quiet night-like pattern
    if 0 <= hour <= 5 and activity < 5:
        return "Night mode: reduce heating, enable security"

    # Cooking / kitchen-intensive
    if top.lower().startswith("kitchen") and activity > 25:
        return "Cooking mode: activate ventilation"

    # Morning-ish routine
    if 6 <= hour <= 10 and (top.lower().startswith("kitchen") or top.lower().startswith("bathroom")):
        return "Morning routine: increase heating, kitchen/bathroom lights"

    # Evening living area routine
    if 17 <= hour <= 23 and top.lower().startswith("living"):
        return "Evening routine: dim lights, lower heating"

    # High multi-room activity (general)
    if activity > 80 or uniq >= 5:
        return "High activity detected: ensure ventilation active"

    return "No profile-based rule (use routine suggestions or monitor)"


def automation_from_cluster(cluster_id: int, profiles: Dict[int, ClusterProfile]) -> str:
    """
    Given a cluster id and precomputed profiles, return the derived automation action.
    """
    profile = profiles.get(int(cluster_id))
    if profile is None:
        return "Unknown cluster"
    return derive_automation_rule(profile)
