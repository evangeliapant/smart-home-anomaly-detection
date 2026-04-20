from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

import pandas as pd

from src.automation.simulator import build_cluster_profiles, infer_sensor_columns
from src.pipeline_paths import DEFAULT_FEATURES_MODELS_OUT, modeled_output_path_for_house


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Print dynamic cluster profiles from modeled feature data.")
    parser.add_argument(
        "--input",
        type=Path,
        help="CSV file produced by scripts.run_pipeline.",
    )
    parser.add_argument(
        "--house",
        help="Use data/processed/<house>_features_with_models.csv.",
    )
    return parser.parse_args()


def resolve_input_path(args: Namespace) -> Path:
    if args.input is not None:
        return args.input
    if args.house:
        return modeled_output_path_for_house(args.house)
    return DEFAULT_FEATURES_MODELS_OUT


def main() -> None:
    args = parse_args()
    input_path = resolve_input_path(args)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Modeled features not found: {input_path}. Run scripts.run_pipeline first or pass --input."
        )

    df = pd.read_csv(input_path)
    sensor_cols = infer_sensor_columns(df)
    profiles = build_cluster_profiles(df, sensor_cols=sensor_cols)

    print("\n==== CLUSTER PROFILES ====\n")
    for cluster_id in sorted(profiles):
        profile = profiles[cluster_id]
        print(f"\nCLUSTER {cluster_id}")
        print(f"active_window_count = {profile.active_window_count}")
        print(f"total_window_count = {profile.total_window_count}")
        print(f"inactive_window_fraction = {profile.inactive_window_fraction:.2f}")
        print(f"is_inactivity_cluster = {profile.is_inactivity_cluster}")
        print(f"mean_hour = {profile.mean_hour:.2f}")
        print(f"peak_hour = {profile.peak_hour:.2f}")
        print(f"top_sensor = {profile.top_sensor}")
        print(f"mean_total_events = {profile.mean_total_events:.2f}")
        print(f"mean_unique_sensors = {profile.mean_unique_sensors:.2f}")
        print("-" * 40)


if __name__ == "__main__":
    main()
