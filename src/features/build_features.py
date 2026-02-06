from __future__ import annotations
import numpy as np
import pandas as pd

def build_window_features(events_with_windows: pd.DataFrame) -> pd.DataFrame:
    """
    Input must have columns: timestamp, sensor, value, window_start
    Output: one row per window_start with engineered features.
    """
    df = events_with_windows.copy()

    # Basic counts per sensor
    counts = (
        df.groupby(["window_start", "sensor"])
          .size()
          .unstack(fill_value=0)
    )

    # Total events + unique sensors
    total_events = df.groupby("window_start").size().rename("total_events")
    n_sensors = df.groupby("window_start")["sensor"].nunique().rename("n_sensors_active")

    out = pd.concat([counts, total_events, n_sensors], axis=1).fillna(0)

    # Time-of-day features
    dt = pd.to_datetime(out.index)
    hour = dt.hour + dt.minute / 60.0
    out["tod_sin"] = np.sin(2 * np.pi * hour / 24.0)
    out["tod_cos"] = np.cos(2 * np.pi * hour / 24.0)

    # Day-of-week (0=Mon)
    out["dow"] = dt.dayofweek

    # Density
    # (window length unknown here; you can keep per-window total or add window_minutes in pipeline)
    return out.reset_index().rename(columns={"window_start": "window_start"})