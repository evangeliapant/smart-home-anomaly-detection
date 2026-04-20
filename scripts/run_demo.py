from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

import pandas as pd

from src.automation.routines import (
    compute_cluster_daily_stats,
    compute_routine_scores,
    suggest_automations,
)
from src.automation.simulator import (
    build_cluster_profiles,
    explain_anomaly,
    infer_sensor_columns,
)
from src.pipeline_paths import DEFAULT_FEATURES_MODELS_OUT, modeled_output_path_for_house


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Inspect modeled smart-home features and print anomaly/routine summaries."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="CSV file produced by scripts.run_pipeline.",
    )
    parser.add_argument(
        "--house",
        help="Use data/processed/<house>_features_with_models.csv.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of rows to show in anomaly and routine summaries.",
    )
    return parser.parse_args()


def resolve_input_path(args: Namespace) -> Path:
    if args.input is not None:
        return args.input
    if args.house:
        return modeled_output_path_for_house(args.house)
    return DEFAULT_FEATURES_MODELS_OUT


def _coerce_bool(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    return series.astype(str).str.lower().isin({"true", "1", "yes"})


def main() -> None:
    args = parse_args()
    input_path = resolve_input_path(args)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Modeled features not found: {input_path}. Run scripts.run_pipeline first or pass --input."
        )

    df = pd.read_csv(input_path)
    df["is_anomaly"] = _coerce_bool(df["is_anomaly"])

    inactive_windows = int((df["total_events"] == 0).sum())
    print(
        f"Loaded {len(df)} windows from {input_path} "
        f"({inactive_windows} inactive windows, {len(df) - inactive_windows} active windows)."
    )

    anomalies = df[df["is_anomaly"] & (df["total_events"] > 0)].copy()
    anomalies = anomalies.sort_values("anomaly_score").head(args.top_n)

    print(f"\nTop {args.top_n} anomalies:")
    for _, r in anomalies.iterrows():
        print(r["window_start"], "-", explain_anomaly(r))

    sensor_cols = infer_sensor_columns(df)
    profiles = build_cluster_profiles(df, sensor_cols=sensor_cols)

    print("\nCluster profiles (summary):")
    for cid, p in profiles.items():
        print(
            f"cluster={cid} peak_hour={p.peak_hour} top_sensor={p.top_sensor} "
            f"mean_events={p.mean_total_events:.2f} inactive_fraction={p.inactive_window_fraction:.2f}"
        )

    daily = compute_cluster_daily_stats(df, active_only=True)
    routines = compute_routine_scores(daily)
    suggestions = suggest_automations(routines, profiles)

    print("\nTop routine clusters (activity-only scoring):")
    if routines.empty:
        print("No active routine windows found.")
    else:
        print(
            routines.head(args.top_n)[
                ["cluster", "frequency", "avg_peak_hour", "std_peak_hour", "stability_score"]
            ]
        )

    print("\nAutomation suggestions from stable routines:")
    if suggestions.empty:
        print("No automation suggestions available.")
    else:
        print(
            suggestions.head(args.top_n)[
                [
                    "cluster",
                    "top_sensor",
                    "avg_peak_hour",
                    "frequency",
                    "stability_score",
                    "inactive_window_fraction",
                    "level",
                    "suggestion",
                ]
            ]
        )

        suggestion_map = {
            int(r["cluster"]): (r["level"], r["suggestion"]) for _, r in suggestions.iterrows()
        }

        print("\nSample routine-based automations (one example per cluster):")
        sample = df[df["total_events"] > 0].sort_values("window_start").groupby("cluster", as_index=False).head(1)

        for _, r in sample.sort_values("cluster").iterrows():
            cid = int(r["cluster"])
            level, action = suggestion_map.get(cid, ("MONITOR", "No suggestion"))
            routine_peak = routines.loc[routines["cluster"] == cid, "avg_peak_hour"]
            peak_text = f"{float(routine_peak.iloc[0]):.1f}h" if not routine_peak.empty else "n/a"

            print(
                r["window_start"],
                "-",
                f"[{level}]",
                action,
                f"(cluster={cid}, routine_peak~{peak_text})",
            )


if __name__ == "__main__":
    main()
