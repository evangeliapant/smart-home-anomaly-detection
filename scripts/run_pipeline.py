from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

from src.features.build_features import build_window_features
from src.features.windowing import add_fixed_windows, build_window_index
from src.models.anomaly import fit_isolation_forest
from src.models.clustering import DEFAULT_SILHOUETTE_SAMPLE_SIZE, fit_kmeans
from src.pipeline_paths import (
    DEFAULT_SAMPLE_RAW,
    default_output_path,
    ensure_parent_dir,
    raw_path_for_house,
)
from src.preprocessing.clean import load_events_csv

DEFAULT_WINDOW_MINUTES = 5
DEFAULT_N_CLUSTERS = 6
DEFAULT_CONTAMINATION = 0.02
DEFAULT_RANDOM_STATE = 42
DEFAULT_SILHOUETTE_SAMPLE = DEFAULT_SILHOUETTE_SAMPLE_SIZE


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Run the smart-home preprocessing, clustering, and anomaly-detection pipeline."
    )
    parser.add_argument(
        "--house",
        help="Dataset name under data/raw without the .csv suffix.",
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
        "--silhouette-sample-size",
        type=int,
        default=DEFAULT_SILHOUETTE_SAMPLE,
        help="Maximum number of windows used to estimate the KMeans silhouette score; 0 skips it.",
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
    if args.silhouette_sample_size < 0:
        raise ValueError("--silhouette-sample-size must be greater than or equal to 0")


def resolve_raw_path(args: Namespace) -> Path:
    if args.raw is not None:
        return args.raw
    if args.house:
        return raw_path_for_house(args.house)
    return DEFAULT_SAMPLE_RAW


def missing_data_message(raw_path: Path) -> str:
    if raw_path == DEFAULT_SAMPLE_RAW:
        return (
            f"Bundled sample dataset not found: {raw_path}. "
            "The repository should include this file for a fresh-clone smoke test."
        )

    return (
        f"Raw dataset not found: {raw_path}. "
        "Place the CASAS CSV in data/raw/ or pass --raw with an explicit file path."
    )


def main() -> None:
    args = parse_args()
    validate_args(args)

    raw_path = resolve_raw_path(args)
    if not raw_path.exists():
        raise FileNotFoundError(missing_data_message(raw_path))

    features_out = args.features_out or default_output_path(raw_path, "features")
    features_models_out = args.features_models_out or default_output_path(raw_path, "features_with_models")

    print(
        "Running pipeline with "
        f"raw={raw_path}, window_minutes={args.window_minutes}, "
        f"n_clusters={args.n_clusters}, contamination={args.contamination}"
    )

    events = load_events_csv(str(raw_path))
    events_w = add_fixed_windows(events, window_minutes=args.window_minutes)
    win_index = build_window_index(events, window_minutes=args.window_minutes)
    feats = build_window_features(events_w, window_index=win_index)

    ensure_parent_dir(features_out)
    feats.to_csv(features_out, index=False)

    _kmeans, _scaler_c, labels, sil = fit_kmeans(
        feats,
        n_clusters=args.n_clusters,
        random_state=args.random_state,
        silhouette_sample_size=args.silhouette_sample_size,
    )
    feats["cluster"] = labels
    if args.silhouette_sample_size == 0:
        print("KMeans silhouette: skipped")
    elif args.silhouette_sample_size and len(feats) > args.silhouette_sample_size:
        print(f"KMeans silhouette (sampled {args.silhouette_sample_size} windows): {sil}")
    else:
        print(f"KMeans silhouette: {sil}")

    _iforest, _scaler_a, pred, score = fit_isolation_forest(
        feats,
        contamination=args.contamination,
        random_state=args.random_state,
    )
    feats["is_anomaly"] = pred == -1
    feats["anomaly_score"] = score

    ensure_parent_dir(features_models_out)
    feats.to_csv(features_models_out, index=False)

    print(f"Saved features: {features_out}")
    print(f"Saved modeled features: {features_models_out}")


if __name__ == "__main__":
    main()
