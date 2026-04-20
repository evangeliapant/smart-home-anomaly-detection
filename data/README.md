# Data Layout

`data/sample/sample_home.csv`

- Bundled synthetic smart-home event log for a fresh-clone smoke test.
- Safe to use with `python -m scripts.run_pipeline` when you just want to verify the project runs.

`data/raw/`

- Place external CASAS-style CSV files here when you want to run the project on real datasets.
- Example names used by the scripts: `hh101.csv`, `hh102.csv`
- This folder is gitignored on purpose, so large or restricted datasets stay local.

`data/processed/`

- Generated feature tables and model outputs created by the pipeline scripts.
