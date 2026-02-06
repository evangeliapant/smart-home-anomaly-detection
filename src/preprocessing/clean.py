from __future__ import annotations
import pandas as pd

def load_events_csv(path: str) -> pd.DataFrame:
    """
    Loads CASAS-like smart-home event logs in either format:

    Format A (4 columns):
      date,time,sensor,value
      2012-07-18,12:54:45.196564,OutsideDoor,OPEN

    Format B (single column per row):
      2012-07-18 12:54:45.196564 OutsideDoor OPEN

    Returns:
      DataFrame with columns: timestamp, sensor, value
    """
    # Read raw lines as strings (don't let pandas guess separators)
    raw = pd.read_csv(path, header=None, dtype=str, engine="python")

    # Case B: one text column containing entire line
    if raw.shape[1] == 1:
        s = raw.iloc[:, 0].astype(str).str.strip()

        # Split into 4 parts: date, time, sensor, value (value may contain spaces rarely -> keep rest)
        parts = s.str.split(r"\s+", n=3, expand=True)
        if parts.shape[1] < 4:
            raise ValueError(
                "Could not split lines into 4 fields (date time sensor value). "
                "Check for empty lines or unexpected formatting."
            )

        parts.columns = ["date", "time", "sensor", "value"]
        df = parts

    # Case A: already multiple columns
    elif raw.shape[1] >= 4:
        df = raw.iloc[:, :4].copy()
        df.columns = ["date", "time", "sensor", "value"]

    else:
        raise ValueError(f"Unsupported format. Column count: {raw.shape[1]}")

    # Parse timestamp
    df["timestamp"] = pd.to_datetime(
        df["date"].astype(str).str.strip() + " " + df["time"].astype(str).str.strip(),
        errors="coerce",
    )
    df = df.dropna(subset=["timestamp"]).copy()

    # Clean sensor/value
    df["sensor"] = df["sensor"].astype(str).str.strip()
    df["value"] = df["value"].astype(str).str.strip()

    # Keep canonical output
    out = df[["date","timestamp", "sensor", "value"]].sort_values("timestamp")
    out = out.drop_duplicates()

    return out