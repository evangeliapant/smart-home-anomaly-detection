from __future__ import annotations
from argparse import ArgumentParser, Namespace
from pathlib import Path

from src.preprocessing.clean import load_events_csv
from src.features.windowing import add_fixed_windows, build_window_index
from src.features.build_features import build_window_features
from src.models.clustering import fit_kmeans
from src.models.anomaly import fit_isolation_forest

DEFAULT_HOUSE = "hh101"
DEFAULT_WINDOW_MINUTES = 5
DEFAULT_N_CLUSTERS = 6
DEFAULT_CONTAMINATION = 0.02
DEFAULT_RANDOM_STATE = 42


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Run the smart-home preprocessing, clustering, and anomaly-detection pipeline."
    )
    parser.add_argument(
        "--house",
        default=DEFAULT_HOUSE,
        help="Dataset name under data/raw without the .csv suffix. Ignored if --raw is provided.",
    )
    parser.add_argument(
        "--raw",
        type=Path,
        help="Explicit path to a raw events CSV file.",
    )
    parser.add_argument(
        "--window-minutes",
        type=int,
        default=DEFAULT_WINDOW_MINUTES,
        help="Window size in minutes for feature aggregation.",
    )
    parser.add_argument(
        "--n-clusters",
        type=int,
        default=DEFAULT_N_CLUSTERS,
        help="Number of KMeans clusters to fit.",
    )
    parser.add_argument(
        "--contamination",
        type=float,
        default=DEFAULT_CONTAMINATION,
        help="Expected anomaly fraction for IsolationForest (0 < value <= 0.5).",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=DEFAULT_RANDOM_STATE,
        help="Random seed shared by the clustering and anomaly models.",
    )
    parser.add_argument(
        "--features-out",
        type=Path,
        help="CSV path for engineered features before model predictions are added.",
    )
    parser.add_argument(
        "--features-models-out",
        type=Path,
        help="CSV path for engineered features plus cluster/anomaly outputs.",
    )
    return parser.parse_args()


def validate_args(args: Namespace) -> None:
    if args.window_minutes <= 0:
        raise ValueError("--window-minutes must be greater than 0")
    if args.n_clusters < 2:
        raise ValueError("--n-clusters must be at least 2")
    if not 0 < args.contamination <= 0.5:
        raise ValueError("--contamination must be between 0 and 0.5")


def resolve_raw_path(args: Namespace) -> Path:
    if args.raw is not None:
        return args.raw
    return Path("data") / "raw" / f"{args.house}.csv"


def default_output_path(raw_path: Path, suffix: str) -> Path:
    processed_dir = Path("data") / "processed"
    if raw_path == Path("data") / "raw" / f"{DEFAULT_HOUSE}.csv":
        filename = "features.csv" if suffix == "features" else "features_with_models.csv"
    else:
        filename = f"{raw_path.stem}_{suffix}.csv"
    return processed_dir / filename


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()
    validate_args(args)

    raw_path = resolve_raw_path(args)
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {raw_path}")

    features_out = args.features_out or default_output_path(raw_path, "features")
    features_models_out = args.features_models_out or default_output_path(raw_path, "features_with_models")

    print(
        "Running pipeline with "
        f"raw={raw_path}, window_minutes={args.window_minutes}, "
        f"n_clusters={args.n_clusters}, contamination={args.contamination}"
    )

    events = load_events_csv(str(raw_path))

    # Choose window length for baseline experiment
    events_w = add_fixed_windows(events, window_minutes=args.window_minutes)
    win_index = build_window_index(events, window_minutes=args.window_minutes)
    feats = build_window_features(events_w, window_index=win_index)

    ensure_parent_dir(features_out)
    feats.to_csv(features_out, index=False)

    # Clustering
    _kmeans, _scaler_c, labels, sil = fit_kmeans(
        feats,
        n_clusters=args.n_clusters,
        random_state=args.random_state,
    )
    feats["cluster"] = labels
    print(f"KMeans silhouette: {sil}")

    # Anomaly
    _iforest, _scaler_a, pred, score = fit_isolation_forest(
        feats,
        contamination=args.contamination,
        random_state=args.random_state,
    )
    feats["is_anomaly"] = (pred == -1)
    feats["anomaly_score"] = score

    ensure_parent_dir(features_models_out)
    feats.to_csv(features_models_out, index=False)

    print(f"Saved features: {features_out}")
    print(f"Saved modeled features: {features_models_out}")

if __name__ == "__main__":
    main()
