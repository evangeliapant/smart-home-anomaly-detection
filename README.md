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

Run the full evaluation flow for one or more local homes, including notebook-driven figures/tables:

```bash
python -m scripts.run_house_evaluation --houses hh101 hh102
```

## Notebook Workflow

The Jupyter notebooks are part of the evaluation workflow, with one important detail:

- the notebooks are used to generate per-home results, figures, and tables
- the batch script does not currently save fully executed `.ipynb` files with visible cell outputs
- instead, it executes the notebook code cells directly and writes artifacts to disk

Generated notebook artifacts are written here:

- `outputs/figures/hh101/` and `outputs/figures/hh102/`
- `outputs/tables/hh101/` and `outputs/tables/hh102/`
- `outputs/notebooks/hh101/` and `outputs/notebooks/hh102/` for execution logs

This means the notebooks currently act as analysis templates rather than saved executed notebooks.

If you want to open and run the notebooks manually in VS Code or Jupyter for a specific home, set the house in the terminal first and then launch Jupyter.

For `hh101`:

```powershell
$env:SMART_HOME_HOUSE='hh101'
python -m jupyter notebook
```

For `hh102`:

```powershell
$env:SMART_HOME_HOUSE='hh102'
python -m jupyter notebook
```

Then run the notebooks in this order:

1. `notebooks/01_exploration.ipynb`
2. `notebooks/02_routine_discovery.ipynb`
3. `notebooks/03_anomaly_analysis.ipynb`

Running them interactively will show the plots and still save the generated figures and tables into the per-home `outputs/` folders.

In short:

- yes, the notebooks are already being used
- yes, they produce the visuals and summary tables
- no, the automated flow does not currently save output-filled `.ipynb` notebook files

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
- KMeans silhouette scoring is sampled on large datasets by default so larger homes remain practical to run

## Tests

Run the lightweight regression checks with:

```bash
python -m unittest discover -s tests
```
