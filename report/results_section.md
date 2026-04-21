# Results

This section summarizes the results produced by the smart-home anomaly detection pipeline on the two CASAS-style homes available locally in `data/raw/`: `hh101` and `hh102`. In this branch, the pipeline uses **60-minute windows** by default, so the results emphasize broader hourly routines instead of short five-minute activity bursts.

## Overview

| Home | Raw events | Modeled windows | Active windows | Inactive windows | Anomalies |
| --- | --- | --- | --- | --- | --- |
| hh101 | 1,286,244 | 8,929 | 7,654 | 1,275 | 179 |
| hh102 | 4,840,159 | 24,880 | 17,907 | 6,973 | 498 |

Compared with the earlier five-minute setup, hourly windowing greatly reduces the number of modeled observations and produces coarser but more interpretable routine groups. The tradeoff is that short-lived anomalies are smoothed into larger hourly behavior blocks.

## Results for HH101

For `hh101`, the system processed more than 1.28 million raw events and aggregated them into `8,929` hourly windows. Of these, `7,654` windows contained activity and `1,275` were inactive. The anomaly detector flagged `179` windows as anomalous.

With hourly aggregation, the cluster structure in `hh101` becomes easier to interpret at a daily-routine level. Instead of many short states, the model separates the home into broad patterns such as morning kitchen-centered activity, midday bedroom and bathroom activity, evening living-room and bedroom presence, and one clearly inactivity-dominant background cluster.

### Cluster Summary

| Cluster | Windows | Mean events | Mean active sensors | Inactive fraction | Peak hour | Main interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2,123 | 41.03 | 1.48 | 0.00 | 4.0 | Night living-room and bedroom routine |
| 1 | 698 | 396.66 | 4.50 | 0.00 | 9.0 | Morning kitchen-centered multi-room routine |
| 2 | 2,016 | 48.74 | 1.59 | 0.00 | 20.0 | Evening living-room and bedroom routine |
| 3 | 1,275 | 0.00 | 0.00 | 1.00 | 18.0 | Inactivity/background pattern |
| 4 | 504 | 612.52 | 5.14 | 0.00 | 11.0 | Midday bedroom and bathroom routine |
| 5 | 2,313 | 222.78 | 4.82 | 0.00 | 17.0 | Late-day multi-room activity |

The strongest routines in `hh101` are cluster `1` (morning kitchen activity), cluster `5` (late-day living-room centered multi-room activity), and cluster `4` (midday bedroom routine). Cluster `0` is stable in time but appears on fewer active days, so it remains below the promotion threshold for an action-oriented suggestion.

### Automation Interpretation

The automation layer produced `RECOMMEND`-level suggestions for the most stable active routines:

- Kitchen-related ventilation or heating pre-adjustment for cluster `1`
- Living-room comfort lighting or heating for cluster `5`
- Bedroom-related comfort or heating adjustment for cluster `4`

This is useful because the hourly setup still produces explainable routine-to-action mappings, but now those mappings correspond to broader phases of the day rather than short five-minute episodes.

### Anomaly Interpretation

The most extreme anomalies in `hh101` are hourly windows with unusually high total event counts, often involving five or six active sensors. Under hourly windowing, the anomaly model is no longer isolating very short bursts; instead, it surfaces unusually intense **hours** of household activity.

Useful visual outputs for `hh101`:

- `outputs/figures/hh101/hh101_events_per_day.png`
- `outputs/figures/hh101/hh101_top_sensors.png`
- `outputs/figures/hh101/hh101_cluster_counts.png`
- `outputs/figures/hh101/hh101_anomaly_score_timeline.png`

## Results for HH102

For `hh102`, the system processed 4.84 million raw events and generated `24,880` hourly windows. Out of these, `17,907` windows were active and `6,973` were inactive. The anomaly detector identified `498` anomalous windows.

Compared with `hh101`, `hh102` remains larger and behaviorally richer even after hourly aggregation. The additional `WorkArea` sensor and the higher overall activity level lead to broader multi-room clusters that combine living-room, kitchen, bedroom, bathroom, and work-area behavior within the same hour.

### Cluster Summary

| Cluster | Windows | Mean events | Mean active sensors | Inactive fraction | Peak hour | Main interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 6,973 | 0.00 | 0.00 | 1.00 | 1.0 | Inactivity/background pattern |
| 1 | 1,924 | 617.73 | 5.69 | 0.00 | 18.0 | High-intensity evening kitchen/living routine |
| 2 | 4,428 | 333.70 | 6.18 | 0.00 | 8.0 | Morning living-room and bedroom multi-room routine |
| 3 | 5,396 | 52.71 | 1.92 | 0.00 | 23.0 | Late-night bedroom and bathroom routine |
| 4 | 1,959 | 739.27 | 5.91 | 0.00 | 21.0 | Late-evening bathroom/bedroom/work-area routine |
| 5 | 4,200 | 104.66 | 3.14 | 0.00 | 16.0 | Midday kitchen and living-room routine |

The most stable routines in `hh102` are cluster `3` (late-night bedroom behavior), cluster `5` (midday kitchen-centered activity), and cluster `2` (morning living-room presence). Cluster `4` is intense but more variable in timing, so it stays in `MONITOR` mode.

### Automation Interpretation

For `hh102`, the automation stage produced three `RECOMMEND`-level suggestions:

- Bedroom-related comfort or heating adjustment for cluster `3`
- Kitchen-related ventilation or heating pre-adjustment for cluster `5`
- Living-room comfort lighting or heating for cluster `2`

This is a reasonable outcome because the system remains conservative: even with broad hourly windows, only clusters that are both interpretable and temporally stable are promoted into suggestion-level routines.

### Anomaly Interpretation

The strongest anomalies in `hh102` are extreme hourly windows with very large event volumes, sometimes above `2,000` events and up to `7` active sensors in the same hour. These are no longer minute-scale spikes; they represent unusually dense periods of behavior at the level of a full hour.

Useful visual outputs for `hh102`:

- `outputs/figures/hh102/hh102_events_per_day.png`
- `outputs/figures/hh102/hh102_top_sensors.png`
- `outputs/figures/hh102/hh102_cluster_counts.png`
- `outputs/figures/hh102/hh102_anomaly_score_timeline.png`

## Cross-Home Comparison

Across both homes, the system still shows consistent behavior with hourly aggregation:

- It separates inactivity-heavy background windows from active routine clusters.
- It discovers interpretable room-centered or multi-room hourly patterns.
- It flags unusually intense hours as anomalies.
- It remains conservative when generating automation suggestions.

The main difference between the two homes is still scale and complexity. `hh102` contains more raw events, more modeled hourly windows, and a richer feature space due to the additional `WorkArea` sensor. As a result, it produces more anomalies and broader multi-room clusters. `hh101` is simpler, but still demonstrates the same end-to-end pipeline behavior and supports interpretable hourly routine recommendations.

## Result Summary

Overall, the project works as intended with hourly windowing. The preprocessing, modeling, and notebook-based analysis all complete successfully, and the resulting outputs remain suitable for inclusion in a course report or thesis chapter. With this branch configuration, the strongest claim is that the system is a functioning and interpretable unsupervised smart-home analysis prototype that can:

- detect recurring hourly behavioral states
- distinguish activity from inactivity
- identify anomalous high-activity hours
- derive conservative, explainable smart-home suggestions from stable routines

For a final submission, the most useful supporting files are:

- `report/evaluation_results.md`
- `outputs/reports/hh101/hh101_demo.txt`
- `outputs/reports/hh102/hh102_demo.txt`
- the figures under `outputs/figures/hh101/` and `outputs/figures/hh102/`
