# src/utils.py

from pathlib import Path


def get_project_root() -> Path:
    """
    Return the root folder of the project (where README.md lives).
    Assumes this file is in src/ under the root.
    """
    return Path(__file__).resolve().parents[1]


def data_paths():
    """
    Convenience function returning paths for raw and processed data.
    """
    root = get_project_root()
    data_raw = root / "data" / "raw"
    data_processed = root / "data" / "processed"
    return data_raw, data_processed
