# Notebook Evaluation Results

These results are derived from the analyses in:

- `notebooks/01_exploration.ipynb`
- `notebooks/02_routine_discovery.ipynb`
- `notebooks/03_anomaly_analysis.ipynb`

The current repository data is the bundled sample dataset at `data/sample/sample_home.csv` and the modeled output at `data/processed/features_with_models.csv`.

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

Interpretation: the sample data is balanced across two days and includes repeated activity in kitchen, bedroom, bathroom, dining-room, and door sensors, which is enough to demonstrate the pipeline behavior end to end.

## 2. Routine Discovery

The modeled feature table contains `484` five-minute windows:

- Active windows: `21`
- Inactive windows: `463`
- KMeans clusters: `6`

Cluster summary:

| cluster | windows | peak hour | top sensor | mean total events | inactive fraction |
|---|---:|---:|---|---:|---:|
| 0 | 178 | 20.0 | Kitchen | 0.01 | 0.99 |
| 1 | 101 | 2.0 | Bathroom | 0.08 | 0.96 |
| 2 | 4 | 8.0 | OutsideDoor | 2.50 | 0.00 |
| 3 | 7 | 7.0 | Kitchen | 2.86 | 0.00 |
| 4 | 4 | 6.0 | Bedroom | 2.00 | 0.00 |
| 5 | 190 | 10.0 | DiningRoom | 0.01 | 0.99 |

Routine stability scores:

| cluster | active days | average peak hour | frequency | stability score |
|---|---:|---:|---:|---:|
| 1 | 2 | 6.0 | 1.00 | 1.00 |
| 2 | 2 | 8.0 | 1.00 | 1.00 |
| 4 | 2 | 6.0 | 1.00 | 1.00 |
| 3 | 2 | 6.5 | 1.00 | 0.93 |
| 0 | 1 | 18.0 | 0.50 | 0.70 |
| 5 | 1 | 12.0 | 0.50 | 0.70 |

Interpretation:

- Clusters `2`, `3`, and `4` capture compact active routines with strong time consistency.
- Clusters `0` and `5` are inactivity-dominant and should not be treated as automatable routines.
- Cluster `1` is frequent but still mostly inactive, so it is better treated as a monitor-only pattern.

Automation recommendation levels:

| cluster | top sensor | frequency | stability score | level |
|---|---|---:|---:|---|
| 1 | Bathroom | 1.00 | 1.00 | MONITOR |
| 2 | OutsideDoor | 1.00 | 1.00 | AUTO |
| 4 | Bedroom | 1.00 | 1.00 | AUTO |
| 3 | Kitchen | 1.00 | 0.93 | AUTO |
| 0 | Kitchen | 0.50 | 0.70 | MONITOR |
| 5 | DiningRoom | 0.50 | 0.70 | MONITOR |

## 3. Anomaly Analysis

- Total anomalies flagged by Isolation Forest: `10`
- Active anomalies after excluding empty windows: `10`

Top anomaly windows:

| window start | cluster | total events | active sensors | anomaly score |
|---|---:|---:|---:|---:|
| 2024-01-01 06:35:00 | 3 | 4.0 | 2.0 | -0.0596 |
| 2024-01-02 12:05:00 | 3 | 4.0 | 2.0 | -0.0574 |
| 2024-01-02 18:15:00 | 2 | 3.0 | 2.0 | -0.0431 |
| 2024-01-01 18:10:00 | 3 | 3.0 | 2.0 | -0.0416 |
| 2024-01-01 18:05:00 | 2 | 3.0 | 2.0 | -0.0411 |

Longest inactivity runs:

| start | end | windows | duration (hours) |
|---|---|---:|---:|
| 2024-01-01 22:30:00 | 2024-01-02 06:15:00 | 94 | 7.83 |
| 2024-01-02 12:10:00 | 2024-01-02 18:10:00 | 73 | 6.08 |
| 2024-01-01 12:20:00 | 2024-01-01 18:00:00 | 69 | 5.75 |

Interpretation: the anomaly detector is mainly surfacing short windows with denser-than-usual multi-sensor activity, while the inactivity-run view helps identify long quiet periods that may be operationally relevant.

## 4. Overall Evaluation

For the bundled sample data, the repository is functioning correctly as a reproducible demonstration system:

- preprocessing and feature generation run successfully
- regression tests pass
- clustering separates compact active routines from inactivity-heavy background windows
- anomaly detection surfaces a small set of unusual active windows
- the automation layer appropriately downgrades inactivity-dominant clusters to `MONITOR`

For a thesis or class report, the strongest claim is that the system works as an interpretable unsupervised prototype, not that it is already validated on a large real-world dataset. The sample data is useful for demonstrating pipeline correctness, routine extraction, anomaly scoring, and explainable automation suggestions.
