# Smart Home Routines and Anomaly Detection

This project explores how smart home sensor data can be analyzed to recognize user routines and detect anomalies, such as inactivity or unusual patterns. It uses unsupervised machine learning to derive insights from unlabeled data.

## 🧠 Goals
- Analyze smart-home sensor data
- Identify routine behavior
- Detect anomalies using unsupervised learning
- Demonstrate simple automation based on detected patterns

## 🔍 Unsupervised Focus
The project prioritizes learning from **unlabeled** smart-home data to avoid manual
annotation, which is costly and impractical for most real-world deployments. The
pipeline therefore emphasizes:
- Pattern discovery from routine behavior without ground-truth labels
- Anomaly detection as deviations from learned routines
- Optional automation triggers derived from recurring patterns

## 🧰 Tech Stack
- Python (pandas, numpy, scikit-learn, TensorFlow)
- CASAS & custom datasets
- Visualization: matplotlib / plotly
- Optional integration: Home Assistant

## 📂 Structure
- `data/` — Raw and processed datasets  
- `notebooks/` — Jupyter notebooks for analysis and modeling  
- `src/` — Core Python scripts  
- `reports/` — Progress and final documentation  

## 🚀 Getting Started
1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/smart-home-anomaly-detection.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```