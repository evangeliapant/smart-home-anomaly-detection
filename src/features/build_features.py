from __future__ import annotations
import numpy as np
import pandas as pd

def build_window_features(
    events_with_windows: pd.DataFrame,
    window_index: pd.DataFrame | None = None
) -> pd.DataFrame:
    """
    Input must have columns: timestamp, sensor, value, window_start
    Optional:
      window_index: DataFrame with a column 'window_start' containing the full timeline of windows.

    Output:
      one row per window_start with engineered features, including empty windows if window_index provided.
    """
    df = events_with_windows.copy()

    # Basic counts per sensor (only for windows that have events)
    counts = (
        df.groupby(["window_start", "sensor"])
          .size()
          .unstack(fill_value=0)
          .reset_index()
    )

    # Total events + unique sensors (only for windows that have events)
    total_events = df.groupby("window_start").size().rename("total_events").reset_index()
    n_sensors = df.groupby("window_start")["sensor"].nunique().rename("n_sensors_active").reset_index()

    # Merge into one feature table (event-present windows only)
    out = counts.merge(total_events, on="window_start", how="left")
    out = out.merge(n_sensors, on="window_start", how="left")

    # If full window timeline provided, left-join to include empty windows
    if window_index is not None:
        if "window_start" not in window_index.columns:
            raise ValueError("window_index must contain a 'window_start' column")

        out = window_index.merge(out, on="window_start", how="left")

        # Fill missing sensor counts + totals with 0
        for c in out.columns:
            if c != "window_start":
                out[c] = out[c].fillna(0)

    # Ensure types are numeric for feature columns
    for c in out.columns:
        if c != "window_start":
            out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)

    # Time-of-day features
    dt = pd.to_datetime(out["window_start"])
    hour = dt.dt.hour + dt.dt.minute / 60.0
    out["tod_sin"] = np.sin(2 * np.pi * hour / 24.0)
    out["tod_cos"] = np.cos(2 * np.pi * hour / 24.0)

    # Day-of-week (0=Mon)
    out["dow"] = dt.dt.dayofweek
    out["is_inactive"] = (out["total_events"] == 0).astype(int)

    return out
