from __future__ import annotations
import pandas as pd


def add_fixed_windows(events: pd.DataFrame, window_minutes: int) -> pd.DataFrame:
    """
    Adds a 'window_start' column (floored to fixed time windows) for each event.
    """
    if "timestamp" not in events.columns:
        raise ValueError("events must contain 'timestamp'")

    df = events.copy()
    df["window_start"] = df["timestamp"].dt.floor(f"{window_minutes}min")
    return df


def build_window_index(events: pd.DataFrame, window_minutes: int) -> pd.DataFrame:
    """
    Build a full timeline of windows from min to max timestamp.
    Returns DataFrame with a single column: window_start.
    """
    if "timestamp" not in events.columns:
        raise ValueError("events must contain 'timestamp'")

    t0 = events["timestamp"].min().floor(f"{window_minutes}min")
    t1 = events["timestamp"].max().ceil(f"{window_minutes}min")

    # full range of windows
    window_start = pd.date_range(start=t0, end=t1, freq=f"{window_minutes}min")
    return pd.DataFrame({"window_start": window_start})


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