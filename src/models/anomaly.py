from __future__ import annotations
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib

def fit_isolation_forest(features: pd.DataFrame, contamination: float = 0.02, random_state: int = 42):
    X = features.drop(columns=["window_start"], errors="ignore")
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    model = IsolationForest(contamination=contamination, random_state=random_state)
    pred = model.fit_predict(Xs)          # -1 anomaly, 1 normal
    score = model.decision_function(Xs)   # higher = more normal

    return model, scaler, pred, score

def save(model, scaler, path_prefix: str):
    joblib.dump(model, f"{path_prefix}_iforest.joblib")
    joblib.dump(scaler, f"{path_prefix}_scaler.joblib")