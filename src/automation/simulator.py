from __future__ import annotations
import pandas as pd

def explain_anomaly(row: pd.Series) -> str:
    # Simple interpretable reasons (extend later)
    if row.get("total_events", 0) == 0:
        return "Inactivity window (no events)"
    if row.get("n_sensors_active", 0) >= 8:
        return "Unusually many sensors active"
    return "Unusual pattern (model-based)"

def automation_from_cluster(cluster_id: int) -> str:
    # Placeholder mapping (you will fill after interpreting clusters)
    mapping = {
        0: "Morning routine: adjust heating, open blinds",
        1: "High activity mode: ensure ventilation active",
        2: "Evening routine: dim lights, lower heating",
        3: "Cooking mode: increase kitchen ventilation",
        4: "Personal care routine: adjust bathroom heating",
        5: "Afternoon routine: moderate lighting",
    }
    return mapping.get(cluster_id, "No automation rule defined")