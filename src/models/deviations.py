"""History-relative sensor deviations used for explainable alerts.

The Isolation Forest output is retained as a broad exploratory signal.  This
module answers the operational question separately: did an individual sensor
fire substantially more or less often than is usual for that sensor at this
hour?
"""

from __future__ import annotations

import numpy as np
import pandas as pd


MAD_SCALE = 1.4826


def build_significant_deviation_table(
    features: pd.DataFrame,
    sensor_cols: list[str],
    *,
    z_threshold: float = 3.5,
    min_history_windows: int = 7,
    min_difference_events: float = 3.0,
    tail_quantile: float = 0.995,
) -> pd.DataFrame:
    """Return one row for every significant sensor deviation.

    Baselines are calculated separately for every sensor and hour of day with
    a median/MAD statistic.  Consequently, a sensor which is normally very
    active at (for example) 08:00 does not alert just because it has a large
    raw event count. A material excess (high deviation) or shortfall (low
    deviation) outside its own historical range is retained. In addition to
    the robust-score rule, the event count must be in the most extreme 0.5%
    of that sensor/hour's observed history. This prevents routine variation
    from producing excessive alerts. The report keeps the original sensor name
    so the result remains easy to interpret for the current datasets.
    """
    required = {"window_start", *sensor_cols}
    missing = required.difference(features.columns)
    if missing:
        raise ValueError(f"Features are missing required columns: {sorted(missing)}")
    if not sensor_cols:
        raise ValueError("At least one sensor column is required")
    if not 0.5 < tail_quantile < 1.0:
        raise ValueError("tail_quantile must be between 0.5 and 1.0")

    wide = features[["window_start", *sensor_cols]].copy()
    wide["window_start"] = pd.to_datetime(wide["window_start"], errors="coerce")
    wide = wide.dropna(subset=["window_start"])
    wide["hour"] = wide["window_start"].dt.hour
    long = wide.melt(
        id_vars=["window_start", "hour"],
        value_vars=sensor_cols,
        var_name="sensor_name",
        value_name="observed_events",
    )
    long["observed_events"] = pd.to_numeric(long["observed_events"], errors="coerce").fillna(0.0)

    grouped = long.groupby(["sensor_name", "hour"])["observed_events"]
    baseline = grouped.agg(history_windows="size", expected_events="median").reset_index()
    mad = grouped.apply(lambda values: float(np.median(np.abs(values - np.median(values))))).rename("mad")
    baseline = baseline.merge(mad.reset_index(), on=["sensor_name", "hour"], how="left")
    empirical_high = grouped.quantile(tail_quantile).rename("empirical_high_threshold")
    empirical_low = grouped.quantile(1.0 - tail_quantile).rename("empirical_low_threshold")
    baseline = baseline.merge(empirical_high.reset_index(), on=["sensor_name", "hour"], how="left")
    baseline = baseline.merge(empirical_low.reset_index(), on=["sensor_name", "hour"], how="left")

    # A zero MAD is common for sparse event counts.  The Poisson-like fallback
    # keeps the threshold meaningful without treating routine zero/one counts
    # as alerts.
    baseline["robust_scale"] = baseline["mad"] * MAD_SCALE
    fallback_scale = np.sqrt(np.maximum(baseline["expected_events"], 1.0))
    baseline["robust_scale"] = baseline["robust_scale"].where(
        baseline["robust_scale"] > 0, fallback_scale
    )
    baseline["high_alert_threshold"] = np.maximum(
        baseline["expected_events"] + z_threshold * baseline["robust_scale"],
        baseline["empirical_high_threshold"],
    )
    baseline["low_alert_threshold"] = np.minimum(
        np.maximum(baseline["expected_events"] - z_threshold * baseline["robust_scale"], 0.0),
        baseline["empirical_low_threshold"],
    )

    table = long.merge(baseline, on=["sensor_name", "hour"], how="left")
    table["signed_difference_events"] = table["observed_events"] - table["expected_events"]
    table["deviation_score"] = table["signed_difference_events"] / table["robust_scale"]
    table["deviation_events"] = table["signed_difference_events"].abs()
    has_enough_history = table["history_windows"] >= min_history_windows
    high_deviation = (
        has_enough_history
        & (table["signed_difference_events"] >= min_difference_events)
        & (table["deviation_score"] >= z_threshold)
        & (table["observed_events"] >= table["high_alert_threshold"])
    )
    low_deviation = (
        has_enough_history
        & (table["signed_difference_events"] <= -min_difference_events)
        & (table["deviation_score"] <= -z_threshold)
        & (table["observed_events"] <= table["low_alert_threshold"])
    )
    significant = table[high_deviation | low_deviation].copy()
    significant["alert"] = np.where(
        significant["deviation_score"] > 0,
        "HIGH_DEVIATION",
        "LOW_DEVIATION",
    )
    significant = significant[
        [
            "window_start",
            "sensor_name",
            "observed_events",
            "expected_events",
            "low_alert_threshold",
            "high_alert_threshold",
            "deviation_events",
            "deviation_score",
            "history_windows",
            "alert",
        ]
    ].sort_values(["deviation_events", "window_start"], ascending=[False, True])
    return significant.reset_index(drop=True).round(3)
