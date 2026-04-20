from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

import pandas as pd

from src.automation.routines import compute_cluster_daily_stats, compute_routine_scores, suggest_automations
from src.automation.simulator import build_cluster_profiles, explain_anomaly, infer_sensor_columns


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Create a markdown results summary from per-house outputs.")
    parser.add_argument(
        "--houses",
        nargs="+",
        default=["hh101", "hh102"],
        help="Dataset names under data/raw without the .csv suffix.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("report/evaluation_results.md"),
        help="Markdown file to write.",
    )
    return parser.parse_args()


def format_dataframe(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows available._"
    text_df = df.fillna("").copy()
    columns = [str(col) for col in text_df.columns]
    rows = [[str(value) for value in row] for row in text_df.astype(object).values.tolist()]

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def build_house_section(house: str) -> str:
    raw_path = ROOT / "data" / "raw" / f"{house}.csv"
    modeled_path = ROOT / "data" / "processed" / f"{house}_features_with_models.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {raw_path}")
    if not modeled_path.exists():
        raise FileNotFoundError(f"Modeled dataset not found: {modeled_path}")

    raw_lines = sum(1 for _ in raw_path.open("r", encoding="utf-8", errors="ignore"))
    df = pd.read_csv(modeled_path)
    df["window_start"] = pd.to_datetime(df["window_start"], errors="coerce")
    df = df.dropna(subset=["window_start"]).copy()
    df["is_anomaly"] = df["is_anomaly"].astype(str).str.lower().isin({"true", "1", "yes"})

    sensor_cols = infer_sensor_columns(df)
    profiles = build_cluster_profiles(df, sensor_cols=sensor_cols)
    daily = compute_cluster_daily_stats(df, active_only=True)
    routines = compute_routine_scores(daily)
    suggestions = suggest_automations(routines, profiles)

    active_windows = int((df["total_events"] > 0).sum())
    inactive_windows = int((df["total_events"] == 0).sum())
    anomaly_count = int(df["is_anomaly"].sum())
    anomaly_examples = (
        df[df["is_anomaly"] & (df["total_events"] > 0)]
        .sort_values("anomaly_score")
        .head(5)
        .copy()
    )
    if not anomaly_examples.empty:
        anomaly_examples["explanation"] = anomaly_examples.apply(explain_anomaly, axis=1)
        anomaly_examples = anomaly_examples[
            ["window_start", "cluster", "total_events", "n_sensors_active", "anomaly_score", "explanation"]
        ]

    cluster_summary = pd.read_csv(ROOT / "outputs" / "tables" / house / f"{house}_cluster_summary.csv")
    cluster_summary = cluster_summary[
        [
            "cluster",
            "n_windows",
            "mean_total_events",
            "mean_unique_sensors",
            "inactive_fraction",
            "peak_hour",
            "top_sensor_1",
            "top_sensor_2",
        ]
    ]

    routine_summary = routines.head(4)[
        ["cluster", "frequency", "avg_peak_hour", "std_peak_hour", "stability_score"]
    ].round(3)
    suggestion_summary = suggestions.head(4)[
        ["cluster", "top_sensor", "avg_peak_hour", "frequency", "stability_score", "level", "suggestion"]
    ].round(3)

    figure_dir = ROOT / "outputs" / "figures" / house
    figure_list = [
        figure_dir / f"{house}_events_per_day.png",
        figure_dir / f"{house}_top_sensors.png",
        figure_dir / f"{house}_cluster_counts.png",
        figure_dir / f"{house}_anomaly_score_timeline.png",
    ]

    lines = [
        f"## {house.upper()}",
        "",
        f"- Raw events: `{raw_lines:,}`",
        f"- Modeled windows: `{len(df):,}`",
        f"- Active windows: `{active_windows:,}`",
        f"- Inactive windows: `{inactive_windows:,}`",
        f"- Detected anomalies: `{anomaly_count:,}`",
        f"- Sensor features: `{', '.join(sensor_cols)}`",
        "",
        "### Cluster Summary",
        "",
        format_dataframe(cluster_summary.round(3)),
        "",
        "### Routine Stability",
        "",
        format_dataframe(routine_summary),
        "",
        "### Automation Suggestions",
        "",
        format_dataframe(suggestion_summary),
        "",
        "### Top Anomaly Windows",
        "",
        format_dataframe(anomaly_examples.round(3)),
        "",
        "### Key Visuals",
        "",
    ]

    for figure in figure_list:
        if figure.exists():
            lines.append(f"- `{figure.relative_to(ROOT)}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    sections = [
        "# Evaluation Results",
        "",
        "This report summarizes the per-home results generated from the project pipeline and notebooks.",
        "",
    ]
    for house in args.houses:
        sections.append(build_house_section(house))

    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(sections).strip() + "\n", encoding="utf-8")
    print(f"Wrote results report to {output_path}")


if __name__ == "__main__":
    main()
