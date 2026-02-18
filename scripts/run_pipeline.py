from __future__ import annotations
import os
import pandas as pd

from src.preprocessing.clean import load_events_csv
from src.features.windowing import add_fixed_windows, build_window_index
from src.features.build_features import build_window_features
from src.models.clustering import fit_kmeans
from src.models.anomaly import fit_isolation_forest

RAW = "data/raw/hh101.csv"
OUT = "data/processed/features.csv"

def main():
    events = load_events_csv(RAW)

    # Choose window length for baseline experiment
    events_w = add_fixed_windows(events, window_minutes=5)
    win_index = build_window_index(events, window_minutes=5)
    feats = build_window_features(events_w, window_index=win_index)

    os.makedirs("data/processed", exist_ok=True)
    feats.to_csv(OUT, index=False)

    # Clustering
    kmeans, scaler_c, labels, sil = fit_kmeans(feats, n_clusters=6)
    feats["cluster"] = labels
    print(f"KMeans silhouette: {sil}")

    # Anomaly
    iforest, scaler_a, pred, score = fit_isolation_forest(feats, contamination=0.02)
    feats["is_anomaly"] = (pred == -1)
    feats["anomaly_score"] = score

    feats.to_csv("data/processed/features_with_models.csv", index=False)
    print("Saved: data/processed/features_with_models.csv")

if __name__ == "__main__":
    main()
