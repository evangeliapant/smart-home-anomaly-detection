from __future__ import annotations
import pandas as pd

def add_fixed_windows(events: pd.DataFrame, window_minutes: int) -> pd.DataFrame:
    """
    Adds a 'window_start' column (floored to fixed time windows).
    """
    if "timestamp" not in events.columns:
        raise ValueError("events must contain 'timestamp'")

    df = events.copy()
    df["window_start"] = df["timestamp"].dt.floor(f"{window_minutes}min")
    return df

def sessionize_by_gap(events: pd.DataFrame, gap_minutes: int = 15) -> pd.DataFrame:
    """
    Sessionize events: a new session starts if time gap between events exceeds gap_minutes.
    Adds 'session_id' column.
    """
    df = events.sort_values("timestamp").copy()
    gaps = df["timestamp"].diff().dt.total_seconds().fillna(0) / 60.0
    new_session = (gaps > gap_minutes).astype(int)
    df["session_id"] = new_session.cumsum()
    return df