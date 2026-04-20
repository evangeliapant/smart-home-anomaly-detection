from __future__ import annotations

from pathlib import Path


DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
SAMPLE_DIR = DATA_DIR / "sample"
PROCESSED_DIR = DATA_DIR / "processed"

DEFAULT_SAMPLE_NAME = "sample_home"
DEFAULT_SAMPLE_RAW = SAMPLE_DIR / f"{DEFAULT_SAMPLE_NAME}.csv"
DEFAULT_FEATURES_OUT = PROCESSED_DIR / "features.csv"
DEFAULT_FEATURES_MODELS_OUT = PROCESSED_DIR / "features_with_models.csv"


def raw_path_for_house(house: str) -> Path:
    return RAW_DIR / f"{house}.csv"


def features_output_path_for_house(house: str) -> Path:
    return PROCESSED_DIR / f"{house}_features.csv"


def modeled_output_path_for_house(house: str) -> Path:
    return PROCESSED_DIR / f"{house}_features_with_models.csv"


def default_output_path(raw_path: Path, suffix: str) -> Path:
    if raw_path == DEFAULT_SAMPLE_RAW:
        return DEFAULT_FEATURES_OUT if suffix == "features" else DEFAULT_FEATURES_MODELS_OUT

    if suffix == "features":
        return features_output_path_for_house(raw_path.stem)
    return modeled_output_path_for_house(raw_path.stem)


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
