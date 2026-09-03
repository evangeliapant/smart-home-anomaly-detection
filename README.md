# Smart Home Routines and Anomaly Detection

This project investigates whether smart-home sensor data can be used to discover recurring routines and unusual behavior without manual labels. It implements an unsupervised analysis pipeline that turns raw event streams into interpretable behavioral patterns, anomaly flags, and conservative automation suggestions.

## Problem the Project Solves

Smart-home logs contain long streams of sensor events, but those events are hard to interpret directly. In many realistic settings there is no labeled dataset saying which windows correspond to cooking, sleeping, or leaving home.

This project addresses that problem by asking:

- can we discover recurring behavior patterns directly from raw sensor events,
- can we identify unusual periods without labeled anomalies,
- and can we derive careful smart-home suggestions from stable routines?

The project is therefore best understood as an **unsupervised smart-home behavior modeling prototype**.

## Project Objectives

- Process raw smart-home sensor event streams
- Discover recurring behavioral states via unsupervised clustering
- Detect anomalous activity and inactivity patterns
- Model routine stability across multiple days
- Derive explainable automation suggestions from learned routines

## Why Unsupervised Learning

This repository intentionally avoids relying on ground-truth activity labels. Instead, it emphasizes:

- pattern discovery from unlabeled sensor data,
- explicit modeling of inactivity through zero-filled windows,
- behavioral state identification using clustering,
- routine stability analysis based on frequency and temporal consistency,
- and conservative automation inference from stable habits.

This makes the project suitable for settings where labeled activity data is unavailable or expensive to produce.

## System Components

### 1. Windowing and Feature Engineering

- Fixed-length time windows
- Default in this branch: **60-minute windows**
- Per-sensor activation counts
- Total events and number of active sensors per window
- Time-of-day and day-of-week features
- Explicit inactivity modeling

### 2. Behavioral State Discovery

- Unsupervised clustering of window-level features using KMeans
- Cluster profiling with top sensor, peak hour, and activity intensity

### 3. Anomaly Detection

- Isolation Forest on the engineered window-level features
- Flags windows whose activity pattern differs from typical behavior

### 4. Significant-Deviation Alerts

- Builds a separate historical baseline for every sensor and hour of day
- Creates an alert only when a sensor exceeds or falls below its own usual range by a material amount
- Prevents high-frequency sensors from being treated as anomalous merely because they are often active
- Saves a tabular alert report with the sensor name, observed activity, and expected activity

### 5. Routine Stability Analysis

- Daily aggregation of cluster activity
- Stability score combining frequency and temporal consistency

### 6. Automation Prototype

- Tiered outputs: `AUTO`, `RECOMMEND`, `MONITOR`
- Suggestions generated only for stable and interpretable routines
- Inactivity-dominant clusters are intentionally downgraded

## End-to-End Pipeline

The pipeline works as follows:

1. Read raw sensor event logs.
2. Clean timestamps and standardize the event table.
3. Group events into fixed windows.
4. Build window-level features:
   - per-sensor counts,
   - total event count,
   - number of active sensors,
   - time-of-day encoding,
   - day-of-week,
   - inactivity flag.
5. Run KMeans to discover recurring behavioral window types.
6. Run Isolation Forest to detect unusual windows.
7. Create significant-deviation alerts relative to each sensor's hourly history.
8. Score cluster stability across days.
9. Generate conservative automation suggestions from the most stable clusters.
10. Save outputs as processed tables, figures, and report files.

## How to Read the Results

The project outputs are meant to be interpreted in layers:

- **Cluster summary**
  - each cluster is a recurring type of window,
  - not a guaranteed human activity label,
  - interpretation comes from dominant sensors, event intensity, and time of day.

- **Routine stability**
  - high frequency means the cluster appears on many days,
  - low variation in peak hour means the timing is consistent,
  - higher stability means the pattern is more trustworthy as a routine.

- **Automation suggestions**
  - `AUTO` means very stable and frequent,
  - `RECOMMEND` means plausible but still conservative,
  - `MONITOR` means do not automate yet.

- **Anomalies**
  - anomalies are windows that differ from normal behavior,
  - in this branch they represent unusual **hours**,
  - in the main branch they represent unusual short **bursts**.

- **Significant-deviation alerts**
  - are intended for alerting rather than exploratory model output,
  - compare a sensor to its own historical activity at the same hour, including both unusually high and unusually low activity,
  - are exported in a table with sensor names and observed, expected, and excess event counts.

## Main Takeaway

The strongest supported claim is:

> Unlabeled smart-home sensor data can be transformed into interpretable routine clusters, anomaly signals, and conservative automation suggestions.

This repository should therefore be presented as an **interpretable proof of concept**, not as a fully validated production smart-home controller.

## Branch Comparison

The two most important branches use the same overall pipeline but different temporal resolutions:

| Branch | Default window size | Main purpose | Strength | Tradeoff |
| --- | --- | --- | --- | --- |
| `main` | 5 minutes | Fine-grained analysis | Better for short activity bursts and short anomalies | Harder to interpret as broad daily routines |
| `feature/1h-window-analysis` | 60 minutes | Broad routine analysis | Easier to explain as morning / midday / evening patterns | Short events are smoothed into hourly blocks |

So the feature branch is not a different algorithm. It is the **same pipeline at a coarser time scale**.

## Tech Stack

- Python
- pandas
- numpy
- scikit-learn
- matplotlib
- CASAS dataset format

## Project Structure

```text
smart-home-anomaly-detection/
├─ data/                   # Raw and processed datasets
├─ src/
│  ├─ preprocessing/       # Data cleaning
│  ├─ features/            # Windowing and feature engineering
│  ├─ models/              # Clustering and anomaly detection
│  └─ automation/          # Cluster profiling and routine inference
├─ scripts/                # Pipeline and reporting runners
├─ notebooks/              # Exploratory and explanatory analysis
├─ outputs/                # Figures, tables, and text reports
└─ report/                 # Narrative writeups and evaluation summaries
```

## Running the Project

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/smart-home-anomaly-detection.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the full processing pipeline with the default hourly windowing:

```bash
python -m scripts.run_pipeline
```

4. Optionally override the window size for experiments:

```bash
python -m scripts.run_pipeline --window-minutes 15
```

The run also writes `outputs/tables/<dataset>/<dataset>_significant_deviations.csv`.
Use `--deviations-out <path>` to select another location.

5. View cluster summaries, anomalies, and routine suggestions:

```bash
python -m scripts.run_demo
```

## Best Files to Read First

For the fastest orientation, start with:

- `report/evaluation_results.md`
- `report/results_section.md`
- `outputs/reports/hh101/hh101_demo.txt`
- `outputs/reports/hh102/hh102_demo.txt`
- `outputs/figures/hh101/`
- `outputs/figures/hh102/`
