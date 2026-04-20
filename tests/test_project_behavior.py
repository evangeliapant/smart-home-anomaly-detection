from __future__ import annotations

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import pandas as pd

from scripts.run_pipeline import resolve_raw_path
from src.automation.routines import compute_cluster_daily_stats, compute_routine_scores, suggest_automations
from src.automation.simulator import INACTIVE_SENSOR_LABEL, build_cluster_profiles
from src.features.build_features import build_window_features
from src.models.clustering import fit_kmeans
from src.pipeline_paths import DEFAULT_SAMPLE_RAW


class FeatureEngineeringTests(unittest.TestCase):
    def test_build_window_features_marks_inactive_windows(self) -> None:
        events = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(["2024-01-01 06:00:00", "2024-01-01 06:00:30"]),
                "sensor": ["Kitchen", "Kitchen"],
                "value": ["ON", "OFF"],
                "window_start": pd.to_datetime(["2024-01-01 06:00:00", "2024-01-01 06:00:00"]),
            }
        )
        window_index = pd.DataFrame(
            {
                "window_start": pd.to_datetime(
                    ["2024-01-01 06:00:00", "2024-01-01 06:05:00", "2024-01-01 06:10:00"]
                )
            }
        )

        features = build_window_features(events, window_index=window_index)

        self.assertEqual(features["is_inactive"].tolist(), [0, 1, 1])
        self.assertEqual(features["total_events"].tolist(), [2.0, 0.0, 0.0])


class RoutineScoringTests(unittest.TestCase):
    def test_daily_stats_exclude_inactive_windows_by_default(self) -> None:
        df = pd.DataFrame(
            {
                "window_start": pd.to_datetime(
                    [
                        "2024-01-01 06:00:00",
                        "2024-01-01 06:05:00",
                        "2024-01-02 06:00:00",
                        "2024-01-02 06:05:00",
                    ]
                ),
                "cluster": [0, 0, 0, 1],
                "total_events": [0.0, 3.0, 0.0, 4.0],
                "n_sensors_active": [0.0, 2.0, 0.0, 2.0],
            }
        )

        daily = compute_cluster_daily_stats(df)

        self.assertEqual(len(daily), 2)
        self.assertEqual(sorted(daily["cluster"].tolist()), [0, 1])
        self.assertTrue((daily["total_events"] > 0).all())

    def test_inactivity_clusters_are_not_promoted_to_automation(self) -> None:
        df = pd.DataFrame(
            {
                "window_start": pd.to_datetime(
                    [
                        "2024-01-01 06:00:00",
                        "2024-01-01 06:05:00",
                        "2024-01-01 06:10:00",
                        "2024-01-01 18:00:00",
                    ]
                ),
                "cluster": [0, 0, 0, 1],
                "Kitchen": [0, 0, 1, 3],
                "LivingRoom": [0, 0, 0, 1],
                "total_events": [0.0, 0.0, 1.0, 4.0],
                "n_sensors_active": [0.0, 0.0, 1.0, 2.0],
                "is_inactive": [1, 1, 0, 0],
            }
        )

        profiles = build_cluster_profiles(df, sensor_cols=["Kitchen", "LivingRoom"])
        daily = compute_cluster_daily_stats(df, active_only=True)
        routines = compute_routine_scores(daily)
        suggestions = suggest_automations(routines, profiles)

        inactive_row = suggestions.loc[suggestions["cluster"] == 0].iloc[0]
        self.assertTrue(bool(inactive_row["is_inactivity_cluster"]))
        self.assertEqual(inactive_row["level"], "MONITOR")

    def test_inactivity_cluster_profiles_use_no_active_sensor_label(self) -> None:
        df = pd.DataFrame(
            {
                "window_start": pd.to_datetime(
                    [
                        "2024-01-01 01:00:00",
                        "2024-01-01 01:05:00",
                        "2024-01-01 10:00:00",
                    ]
                ),
                "cluster": [0, 0, 1],
                "Kitchen": [0, 0, 2],
                "LivingRoom": [0, 0, 1],
                "total_events": [0.0, 0.0, 3.0],
                "n_sensors_active": [0.0, 0.0, 2.0],
            }
        )

        profiles = build_cluster_profiles(df, sensor_cols=["Kitchen", "LivingRoom"])

        self.assertEqual(profiles[0].top_sensor, INACTIVE_SENSOR_LABEL)
        self.assertEqual(profiles[1].top_sensor, "Kitchen")


class PipelineDefaultTests(unittest.TestCase):
    def test_pipeline_defaults_to_bundled_sample_data(self) -> None:
        args = SimpleNamespace(raw=None, house=None)
        self.assertEqual(resolve_raw_path(args), DEFAULT_SAMPLE_RAW)
        self.assertTrue(Path(DEFAULT_SAMPLE_RAW).exists())


class ClusteringTests(unittest.TestCase):
    def test_fit_kmeans_samples_large_silhouette_inputs(self) -> None:
        features = pd.DataFrame(
            {
                "window_start": pd.date_range("2024-01-01", periods=120, freq="5min"),
                "f1": np.r_[np.zeros(60), np.ones(60)],
                "f2": np.r_[np.zeros(60), np.ones(60)],
            }
        )

        with patch("src.models.clustering.silhouette_score", return_value=0.42) as mock_silhouette:
            _model, _scaler, labels, sil = fit_kmeans(
                features,
                n_clusters=2,
                random_state=42,
                silhouette_sample_size=25,
            )

        self.assertEqual(len(labels), len(features))
        self.assertEqual(sil, 0.42)
        silhouette_X, silhouette_labels = mock_silhouette.call_args.args
        self.assertEqual(len(silhouette_X), 25)
        self.assertEqual(len(silhouette_labels), 25)


if __name__ == "__main__":
    unittest.main()
