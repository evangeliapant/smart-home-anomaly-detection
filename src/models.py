# src/models.py

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def fit_kmeans(
    features: pd.DataFrame,
    n_clusters: int = 6,
    random_state: int = 42,
) -> tuple[KMeans, pd.Series]:
    """
    Fit a KMeans clustering model on the given feature matrix.

    Returns
    -------
    model : KMeans
    labels : pd.Series with index = features.index and cluster label per row
    """
    X = features.values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    labels = model.fit_predict(X_scaled)

    labels = pd.Series(labels, index=features.index, name="cluster")
    return model, labels


def fit_isolation_forest(
    features: pd.DataFrame,
    contamination: float = 0.01,
    random_state: int = 42,
) -> tuple[IsolationForest, pd.Series]:
    """
    Fit IsolationForest for unsupervised anomaly detection.

    Returns
    -------
    model : IsolationForest
    anomalies : pd.Series (True for anomalous windows)
    """
    X = features.values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
    )
    preds = model.fit_predict(X_scaled)  # -1 = anomaly, 1 = normal
    anomalies = pd.Series(preds == -1, index=features.index, name="anomaly")
    return model, anomalies
