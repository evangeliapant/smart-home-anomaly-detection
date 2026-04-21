# Notebook Evaluation Results

These results are derived from the analyses in:

- `notebooks/01_exploration.ipynb`
- `notebooks/02_routine_discovery.ipynb`
- `notebooks/03_anomaly_analysis.ipynb`

The current repository data is the bundled sample dataset at `data/sample/sample_home.csv` and the modeled output at `data/processed/features_with_models.csv`. In this branch, the sample is processed with the new **60-minute default windowing**.

## 1. Data Exploration

- Raw events: `48`
- Observation days: `2` (`2024-01-01` to `2024-01-02`)
- Distinct sensors: `6`
- Events per day: `24` on each day

Most frequent sensors:

| sensor | count |
|---|---:|
| Kitchen | 12 |
| Bedroom | 8 |
| Bathroom | 8 |
| DiningRoom | 8 |
| OutsideDoor | 8 |
| LivingRoom | 4 |

Interpretation: the sample data is still balanced across two days, but with hourly windows the emphasis shifts from short episodes to broader daily phases such as morning, midday, evening, and overnight inactivity.

## 2. Routine Discovery

The modeled feature table now contains `42` hourly windows:

- Active windows: `10`
- Inactive windows: `32`
- KMeans clusters: `6`

Cluster summary:

| cluster | windows | peak hour | top sensor | mean total events | inactive fraction |
|---|---:|---:|---|---:|---:|
| 0 | 10 | 22.0 | Bathroom | 4.0 | 0.80 |
| 1 | 4 | 6.0 | DiningRoom | 6.0 | 0.00 |
| 2 | 10 | 9.0 | No active sensor | 0.0 | 1.00 |
| 3 | 2 | 7.0 | OutsideDoor | 2.0 | 0.00 |
| 4 | 2 | 18.0 | Kitchen | 6.0 | 0.00 |
| 5 | 14 | 13.0 | No active sensor | 0.0 | 1.00 |

Routine stability scores:

| cluster | active days | average peak hour | frequency | stability score |
|---|---:|---:|---:|---:|
| 0 | 2 | 22.0 | 1.00 | 1.00 |
| 1 | 2 | 6.0 | 1.00 | 1.00 |
| 4 | 2 | 18.0 | 1.00 | 1.00 |
| 3 | 2 | 7.5 | 1.00 | 0.93 |

Interpretation:

- Cluster `1` captures a repeatable early-day dining-room routine.
- Cluster `4` captures a repeatable evening kitchen routine.
- Cluster `3` captures a compact door-related transition routine.
- Clusters `2` and `5` are fully inactivity-dominant and should not be treated as automatable routines.
- Cluster `0` includes some bathroom activity, but because `80%` of its windows are inactive it is still downgraded to monitor-only.

Automation recommendation levels:

| cluster | top sensor | frequency | stability score | level |
|---|---|---:|---:|---|
| 0 | Bathroom | 1.00 | 1.00 | MONITOR |
| 1 | DiningRoom | 1.00 | 1.00 | AUTO |
| 4 | Kitchen | 1.00 | 1.00 | AUTO |
| 3 | OutsideDoor | 1.00 | 0.93 | AUTO |

## 3. Anomaly Analysis

- Total anomalies flagged by Isolation Forest: `1`
- Active anomalies after excluding empty windows: `1`

Top anomaly windows:

| window start | cluster | total events | active sensors | anomaly score |
|---|---:|---:|---:|---:|
| 2024-01-02 06:00:00 | 1 | 8.0 | 4.0 | -0.0017 |

Longest inactivity runs:

| start | end | windows | duration (hours) |
|---|---|---:|---:|
| 2024-01-01 23:00:00 | 2024-01-02 05:00:00 | 7 | 7.0 |
| 2024-01-01 13:00:00 | 2024-01-01 17:00:00 | 5 | 5.0 |
| 2024-01-02 13:00:00 | 2024-01-02 17:00:00 | 5 | 5.0 |

Interpretation: with hourly aggregation, the anomaly detector becomes much more conservative. Instead of highlighting several short dense windows, it surfaces only one unusually active hour in the sample.

## 4. Overall Evaluation

For the bundled sample data, the repository is functioning correctly as a reproducible demonstration system under the hourly-window configuration:

- preprocessing and hourly feature generation run successfully
- regression tests pass
- clustering separates broad active routines from inactivity-heavy background windows
- anomaly detection surfaces unusually dense hours rather than short bursts
- the automation layer appropriately downgrades inactivity-dominant clusters to `MONITOR`

For a thesis or class report, the strongest claim is now that the system works as an interpretable unsupervised prototype for **hour-level** smart-home routine discovery. The hourly setup is better for broad daily behavior summaries, while the earlier five-minute setup remains better if the goal is fine-grained anomaly detection or very short routine segments.
