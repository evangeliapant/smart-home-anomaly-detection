from __future__ import annotations
import pandas as pd
from src.automation.simulator import explain_anomaly, automation_from_cluster

def main():
    df = pd.read_csv("data/processed/features_with_models.csv")
    anomalies = df[df["is_anomaly"] == True].copy()
    anomalies = anomalies.sort_values("anomaly_score").head(10)

    print("\nTop 10 anomalies:")
    for _, r in anomalies.iterrows():
        print(r["window_start"], "-", explain_anomaly(r))

    # Example automation printout
    print("\nSample automations (first 10 rows):")
    for _, r in df.head(10).iterrows():
        print(r["window_start"], "-", automation_from_cluster(int(r["cluster"])))

if __name__ == "__main__":
    main()
