from __future__ import annotations
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

def fit_kmeans(features: pd.DataFrame, n_clusters: int = 6, random_state: int = 42):
    X = features.drop(columns=["window_start"], errors="ignore")
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    labels = model.fit_predict(Xs)

    sil = None
    if len(set(labels)) > 1:
        sil = silhouette_score(Xs, labels)

    return model, scaler, labels, sil

def save(model, scaler, path_prefix: str):
    joblib.dump(model, f"{path_prefix}_kmeans.joblib")
    joblib.dump(scaler, f"{path_prefix}_scaler.joblib")