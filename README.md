# Smart Home Routines and Anomaly Detection

This project explores how smart-home sensor streams can be used to discover recurring routines and flag unusual behavior with unsupervised learning.

The pipeline works on CASAS-style event logs and is organized into four stages:

- preprocessing raw events
- aggregating fixed time-window features
- clustering behavioral states and scoring anomalies
- summarizing stable routines and generating automation suggestions

## Project Goals

- process raw smart-home sensor event streams
- discover recurring behavioral states via unsupervised clustering
- detect anomalous activity patterns
- model routine stability across multiple days
- derive explainable automation suggestions from learned routines

## Repository Layout

```text
smart-home-anomaly-detection/
|-- data/
|   |-- sample/      # Bundled synthetic smoke-test dataset
|   |-- raw/         # External datasets placed locally, not committed
|   |-- processed/   # Generated feature/model outputs
|-- src/
|   |-- preprocessing/
|   |-- features/
|   |-- models/
|   `-- automation/
|-- scripts/
|-- notebooks/
|-- outputs/
`-- report/
```

More detail on the data folders is in `data/README.md`.

## Setup

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If you want to run the notebooks as well, install the notebook extras:

```bash
pip install -r requirements-notebooks.txt
```

The repository includes a small synthetic dataset at `data/sample/sample_home.csv`, so a fresh clone can run a smoke test without downloading the full CASAS data first.

## Running the Project

Run the pipeline on the bundled sample dataset:

```bash
python -m scripts.run_pipeline
python -m scripts.run_demo
```

Run on a local CASAS file placed in `data/raw/`:

```bash
python -m scripts.run_pipeline --house hh101
python -m scripts.run_demo --house hh101
python -m scripts.cluster_profile --house hh101
```

Run on an explicit CSV path with custom settings:

```bash
python -m scripts.run_pipeline --raw data/raw/hh102.csv --window-minutes 10 --n-clusters 8 --contamination 0.03
python -m scripts.run_demo --input data/processed/hh102_features_with_models.csv
```

## External Data

The full CASAS datasets are not committed to the repository. To use them:

1. download or copy the desired CSV locally
2. place it in `data/raw/` with a name like `hh101.csv` or `hh102.csv`
3. run the pipeline with `--house <name>` or `--raw <path>`

If a requested raw file is missing, the scripts now fail with a direct message telling you where the data should go.

## Modeling Notes

- window features include inactive windows explicitly via `is_inactive`
- routine scoring now uses active windows by default so inactivity-heavy clusters do not dominate "habit" discovery
- automation suggestions are downgraded to `MONITOR` for inactivity-dominant clusters
- cluster profiling is data-driven and no longer depends on a hardcoded sensor schema

## Tests

Run the lightweight regression checks with:

```bash
python -m unittest discover -s tests
```
