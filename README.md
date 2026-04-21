# Smart Home Routines and Anomaly Detection

This project investigates how smart home sensor data can be analyzed to automatically discover behavioral routines and detect anomalies using **unsupervised machine learning**.

The system focuses on learning from **unlabeled sensor streams**, avoiding the need for manual activity annotation. The objective is to explore how recurring patterns and potential automation rules can be derived directly from raw event data.

---

## 🧠 Project Objectives

- Process raw smart-home sensor event streams
- Discover recurring behavioral states via unsupervised clustering
- Detect anomalous activity and inactivity patterns
- Model routine stability across multiple days
- Derive explainable automation suggestions from learned routines

---

## 🔍 Unsupervised Learning Approach

In many real-world deployments, smart home systems do not rely on labeled activity datasets. This project therefore emphasizes:

- Pattern discovery from unlabeled sensor data
- Explicit modeling of inactivity (zero-filled time windows)
- Behavioral state identification using clustering
- Routine stability analysis based on frequency and temporal consistency
- Conservative automation inference derived from stable habits

No ground-truth labels are required.

---

## 🧩 System Components

### 1. Windowing & Feature Engineering

- Fixed-length time windows (default: 60 minutes)
- Per-sensor activation counts
- Time-of-day and day-of-week encoding
- Modeling of inactive periods

### 2. Behavioral State Discovery

- Unsupervised clustering of window-level features
- Cluster profiling (dominant sensor, peak hour, activity level)

### 3. Routine Stability Analysis

- Daily aggregation of cluster activity
- Stability scoring combining frequency and time regularity

### 4. Automation Prototype

- Tiered automation suggestions (AUTO / RECOMMEND / MONITOR)
- Fully data-driven and cluster-profile based

---

## 🧰 Tech Stack

- Python
- pandas
- numpy
- scikit-learn
- matplotlib
- CASAS dataset (unlabeled)

---

## 📂 Project Structure
```
smart-home-anomaly-detection/

├─ data/ # Raw and processed datasets
├─ src/
│ ├─ preprocessing/ # Data cleaning
│ ├─ features/ # Windowing & feature engineering
│ ├─ models/ # Clustering & anomaly detection
│ └─ automation/ # Cluster profiling & routine inference
├─ scripts/ # Pipeline & demo runners
├─ notebooks/ # Exploratory analysis
├─ outputs/ # Saved models & figures
└─ report/ # Documentation
```

---

## 🚀 Running the Project

1. Clone the repo:

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

5. View cluster summaries, anomalies, and automation suggestions:

```bash
python -m scripts.run_demo
```
