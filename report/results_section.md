# Results

This section summarizes the results produced by the smart-home anomaly detection pipeline on the two CASAS-style homes available locally in `data/raw/`: `hh101` and `hh102`. For both homes, the same workflow was used: raw event parsing, fixed-window feature generation, KMeans clustering for routine discovery, Isolation Forest for anomaly detection, and notebook-based visualization.

## Overview

| Home | Raw events | Modeled windows | Active windows | Inactive windows | Anomalies |
| --- | --- | --- | --- | --- | --- |
| hh101 | 1,286,244 | 107,127 | 45,673 | 61,454 | 2,143 |
| hh102 | 4,840,159 | 298,543 | 107,369 | 191,174 | 5,971 |

The results show that both datasets contain a large amount of inactivity, which is expected in real homes because sensor logs include long quiet periods. The pipeline handled this explicitly by marking inactive windows and preventing inactivity-dominant clusters from being overinterpreted as meaningful routines.

## Results for HH101

For `hh101`, the system processed more than 1.28 million raw events and converted them into 107,127 five-minute windows. Of these, 45,673 windows contained activity and 61,454 were inactive. The anomaly detector flagged 2,143 windows as anomalous.

The cluster structure in `hh101` separates background inactivity from several active behavioral states. Two clusters are clearly inactivity-dominant and are now labeled with `No active sensor`, while the active clusters are associated with interpretable spaces such as the living room, bedroom, and kitchen.

### Cluster Summary

| Cluster | Windows | Mean events | Mean active sensors | Inactive fraction | Peak hour | Main interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 27,669 | 0.00 | 0.00 | 1.00 | 18.0 | Inactivity pattern |
| 1 | 3,378 | 57.83 | 3.35 | 0.00 | 14.0 | Living-room centered activity |
| 2 | 4,835 | 85.65 | 2.23 | 0.00 | 12.0 | Bedroom and bathroom routine |
| 3 | 3,664 | 90.07 | 3.09 | 0.00 | 10.0 | Kitchen-centered routine |
| 4 | 33,785 | 0.00 | 0.00 | 1.00 | 2.0 | Inactivity pattern |
| 5 | 33,796 | 10.26 | 1.12 | 0.00 | 10.0 | Low-intensity living-room activity |

The most stable routines in `hh101` are clusters `2`, `3`, and `5`. Cluster `2` is associated with bedroom-centered behavior, cluster `3` with kitchen activity, and cluster `5` with lower-intensity living-room presence. These clusters were frequent enough across days to be surfaced by the routine scoring stage, although the stability scores indicate moderate rather than perfect regularity.

### Automation Interpretation

The automation layer produced `RECOMMEND`-level suggestions for the strongest active routines:

- Bedroom-related comfort or heating adjustment for cluster `2`
- Kitchen-related ventilation or heating pre-adjustment for cluster `3`
- Living-room comfort lighting or heating for cluster `5`

This is a useful result because it shows that the pipeline does not only cluster behavior, but also maps stable recurring patterns into explainable smart-home actions.

### Anomaly Interpretation

The most extreme anomalies in `hh101` were high-density windows with unusually large event bursts, often involving many sensors at once. This suggests that the anomaly detector is primarily identifying short periods of atypically intense activity rather than only rare room usage.

Useful visual outputs for `hh101`:

- `outputs/figures/hh101/hh101_events_per_day.png`
- `outputs/figures/hh101/hh101_top_sensors.png`
- `outputs/figures/hh101/hh101_cluster_counts.png`
- `outputs/figures/hh101/hh101_anomaly_score_timeline.png`

## Results for HH102

For `hh102`, the system processed 4.84 million raw events and generated 298,543 five-minute windows. Out of these, 107,369 windows were active and 191,174 were inactive. The anomaly detector identified 5,971 anomalous windows.

Compared with `hh101`, `hh102` is both larger and behaviorally richer. It includes an additional `WorkArea` sensor feature, and the resulting active clusters show a stronger spread across living-room, kitchen, bathroom, bedroom, and work-area activity.

### Cluster Summary

| Cluster | Windows | Mean events | Mean active sensors | Inactive fraction | Peak hour | Main interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 72,506 | 0.00 | 0.00 | 1.00 | 16.0 | Inactivity pattern |
| 1 | 59,262 | 13.94 | 1.56 | 0.00 | 20.0 | Lower-intensity living-room activity |
| 2 | 11,823 | 90.93 | 4.50 | 0.00 | 20.0 | High multi-room living/work activity |
| 3 | 118,668 | 0.00 | 0.00 | 1.00 | 4.0 | Inactivity pattern |
| 4 | 16,084 | 84.22 | 3.18 | 0.00 | 19.0 | Kitchen and dining routine |
| 5 | 20,200 | 78.33 | 2.55 | 0.00 | 21.0 | Bathroom and bedroom routine |

The active structure in `hh102` is stronger than in `hh101`. Cluster `2` captures a high-activity pattern involving both living-room and work-area sensors, cluster `4` captures a kitchen and dining pattern, and cluster `5` captures bathroom and bedroom behavior. Two very large clusters again represent inactivity and should be interpreted as background state rather than meaningful routines.

### Automation Interpretation

For `hh102`, the automation stage produced one `RECOMMEND`-level suggestion for recurring living-room activity. The remaining top clusters were left in `MONITOR` mode. This is a reasonable outcome because the system is designed to be conservative: only clusters with sufficient routine stability and interpretable profile characteristics are promoted into action-oriented suggestions.

### Anomaly Interpretation

The strongest anomalies in `hh102` are even more extreme than in `hh101`, with some windows containing well above 300 events and up to 7 simultaneously active sensors. These results indicate that the anomaly model is correctly surfacing unusually dense periods of behavior in a much larger and more complex home environment.

Useful visual outputs for `hh102`:

- `outputs/figures/hh102/hh102_events_per_day.png`
- `outputs/figures/hh102/hh102_top_sensors.png`
- `outputs/figures/hh102/hh102_cluster_counts.png`
- `outputs/figures/hh102/hh102_anomaly_score_timeline.png`

## Cross-Home Comparison

Across both homes, the system shows consistent behavior:

- It separates inactivity-heavy background windows from active routine clusters.
- It discovers interpretable room-centered or multi-room patterns.
- It flags short bursts of unusually intense activity as anomalies.
- It remains conservative when generating automation suggestions.

The main difference between the two homes is scale and complexity. `hh102` contains more raw events, more modeled windows, and a richer feature space due to the additional `WorkArea` sensor. As a result, it produces more anomalies and a wider range of active routine clusters. `hh101` is somewhat simpler, but still demonstrates the same end-to-end pipeline behavior and supports interpretable automation recommendations.

## Result Summary

Overall, the project works as intended on both uploaded homes. The preprocessing, modeling, and notebook-based analysis all complete successfully, and the resulting outputs are suitable for inclusion in a course report or thesis chapter. The strongest claim supported by these results is that the system is a functioning and interpretable unsupervised smart-home analysis prototype that can:

- detect recurring behavioral states
- distinguish activity from inactivity
- identify anomalous windows
- derive conservative, explainable smart-home suggestions from stable routines

For a final submission, the most useful supporting files are:

- `report/evaluation_results.md`
- `outputs/reports/hh101/hh101_demo.txt`
- `outputs/reports/hh102/hh102_demo.txt`
- the figures under `outputs/figures/hh101/` and `outputs/figures/hh102/`
