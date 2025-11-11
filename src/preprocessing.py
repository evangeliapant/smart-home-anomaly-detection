# src/preprocessing.py

from pathlib import Path
import pandas as pd


def load_raw_casas_csv(path: str | Path) -> pd.DataFrame:
    """
    Load a CASAS-style log file (e.g. hh101, hh102) and return a DataFrame
    with datetime index, sensor, and value columns.
    """

    # Try to read the file (CASAS logs usually space-separated, no header)
    df = pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=["Date", "Time", "Sensor", "Value"],
        engine="python"
    )

    # Combine Date and Time into one datetime column
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors="coerce")

    # Drop rows where parsing failed
    df = df.dropna(subset=["datetime"])

    # Set datetime as index and sort
    df = df.sort_values("datetime").set_index("datetime")

    # Optional: keep only the useful columns
    return df[["Sensor", "Value"]]


def add_active_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add an 'active' numeric column based on the textual 'Value' column.
    Maps ON/OPEN/ACTIVE/PRESENT -> 1, otherwise 0.
    """
    if "Value" not in df.columns:
        raise ValueError("Expected column 'Value' in dataframe.")

    df = df.copy()
    df["active"] = df["Value"].astype(str).str.upper().map(
        lambda x: 1 if x in ["ON", "OPEN", "ACTIVE", "PRESENT"] else 0
    )
    return df


def window_features(
    df: pd.DataFrame,
    window: str = "10T",
) -> pd.DataFrame:
    """
    Aggregate sensor activity into fixed time windows.

    Parameters
    ----------
    df : DataFrame
        Must have index = datetime, columns at least: ['Sensor', 'active'].
    window : str
        Pandas offset alias, e.g. '10T' (10 minutes), '15T', '1H'.

    Returns
    -------
    features : DataFrame
        Index = time windows
        Columns = one per sensor
        Values = sum of 'active' events per sensor per window.
    """
    if "Sensor" not in df.columns:
        raise ValueError("Expected column 'Sensor' in dataframe.")
    if "active" not in df.columns:
        raise ValueError("Expected column 'active'. Call add_active_column first.")

    # group by time window and sensor
    counts = (
        df.groupby([pd.Grouper(freq=window), "Sensor"])["active"]
        .sum()
        .unstack(fill_value=0)
    )

    # ensure sorted index
    counts = counts.sort_index()

    return counts


def save_features(features: pd.DataFrame, out_path: str | Path) -> None:
    """
    Save processed feature matrix to CSV, creating parent folder if needed.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(out_path)
