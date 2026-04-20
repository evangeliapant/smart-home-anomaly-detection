from __future__ import annotations

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


DEFAULT_SILHOUETTE_SAMPLE_SIZE = 10_000


def fit_kmeans(
    features: pd.DataFrame,
    n_clusters: int = 6,
    random_state: int = 42,
    silhouette_sample_size: int | None = DEFAULT_SILHOUETTE_SAMPLE_SIZE,
):
    X = features.drop(columns=["window_start"], errors="ignore")
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    labels = model.fit_predict(Xs)

    sil = None
    if silhouette_sample_size != 0 and len(set(labels)) > 1:
        if silhouette_sample_size is not None and len(Xs) > silhouette_sample_size:
            rng = np.random.default_rng(random_state)
            sample_idx = rng.choice(len(Xs), size=silhouette_sample_size, replace=False)
            sil = silhouette_score(Xs[sample_idx], labels[sample_idx])
        else:
            sil = silhouette_score(Xs, labels)

    return model, scaler, labels, sil


def save(model, scaler, path_prefix: str):
    joblib.dump(model, f"{path_prefix}_kmeans.joblib")
    joblib.dump(scaler, f"{path_prefix}_scaler.joblib")
