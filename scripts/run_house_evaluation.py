from __future__ import annotations

import json
import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    "01_exploration.ipynb",
    "02_routine_discovery.ipynb",
    "03_anomaly_analysis.ipynb",
]


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Run the pipeline and execute all notebooks for one or more smart-home datasets."
    )
    parser.add_argument(
        "--houses",
        nargs="+",
        default=["hh101", "hh102"],
        help="Dataset names under data/raw without the .csv suffix.",
    )
    parser.add_argument(
        "--skip-pipeline",
        action="store_true",
        help="Skip pipeline runs and only execute reports/notebooks.",
    )
    parser.add_argument(
        "--skip-notebooks",
        action="store_true",
        help="Skip notebook execution.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="How many rows the textual report scripts should show.",
    )
    return parser.parse_args()


def run_command(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    print("Running:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout)
        if completed.stderr:
            print(completed.stderr)
        raise subprocess.CalledProcessError(
            completed.returncode,
            command,
            output=completed.stdout,
            stderr=completed.stderr,
        )
    return completed


def write_text_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_text_reports(house: str, top_n: int) -> None:
    report_dir = ROOT / "outputs" / "reports" / house
    report_dir.mkdir(parents=True, exist_ok=True)

    demo = run_command(
        [sys.executable, "-m", "scripts.run_demo", "--house", house, "--top-n", str(top_n)]
    )
    write_text_output(report_dir / f"{house}_demo.txt", demo.stdout)

    profile = run_command([sys.executable, "-m", "scripts.cluster_profile", "--house", house])
    write_text_output(report_dir / f"{house}_cluster_profile.txt", profile.stdout)


def execute_notebooks(house: str) -> None:
    notebook_output_dir = ROOT / "outputs" / "notebooks" / house
    notebook_output_dir.mkdir(parents=True, exist_ok=True)

    os.environ["SMART_HOME_HOUSE"] = house
    os.environ.setdefault("MPLBACKEND", "Agg")
    for notebook_name in NOTEBOOKS:
        source_path = ROOT / "notebooks" / notebook_name
        notebook = json.loads(source_path.read_text(encoding="utf-8"))
        namespace: dict[str, object] = {"__name__": "__main__", "__file__": str(source_path)}
        executed_cells = 0

        print(f"Executing notebook cells from {source_path.name} for {house}")
        for index, cell in enumerate(notebook.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            if not source.strip():
                continue
            try:
                exec(compile(source, f"{source_path.name}#cell{index}", "exec"), namespace)
                executed_cells += 1
            except Exception as exc:
                raise RuntimeError(
                    f"Notebook execution failed in {source_path.name} cell {index} for house {house}"
                ) from exc

        log_path = notebook_output_dir / f"{source_path.stem}_{house}_execution.txt"
        write_text_output(
            log_path,
            f"Executed {executed_cells} code cells from {source_path.name} for house {house}.\n",
        )


def main() -> None:
    args = parse_args()

    for house in args.houses:
        raw_path = ROOT / "data" / "raw" / f"{house}.csv"
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw dataset not found: {raw_path}")

        if not args.skip_pipeline:
            run_command([sys.executable, "-m", "scripts.run_pipeline", "--house", house])

        run_text_reports(house, args.top_n)

        if not args.skip_notebooks:
            execute_notebooks(house)

    print("Completed evaluation runs for:", ", ".join(args.houses))


if __name__ == "__main__":
    main()
