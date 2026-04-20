# Evaluation Results

This report summarizes the per-home results generated from the project pipeline and notebooks.

## HH101

- Raw events: `1,286,244`
- Modeled windows: `107,127`
- Active windows: `45,673`
- Inactive windows: `61,454`
- Detected anomalies: `2,143`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 27669 | 0.0 | 0.0 | 1.0 | 18.0 | No active sensor |  |
| 1 | 3378 | 57.835 | 3.346 | 0.0 | 14.0 | LivingRoom | OutsideDoor |
| 2 | 4835 | 85.651 | 2.233 | 0.0 | 12.0 | Bedroom | Bathroom |
| 3 | 3664 | 90.07 | 3.089 | 0.0 | 10.0 | Kitchen | LivingRoom |
| 4 | 33785 | 0.0 | 0.0 | 1.0 | 2.0 | No active sensor |  |
| 5 | 33796 | 10.26 | 1.122 | 0.0 | 10.0 | LivingRoom | Bedroom |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 2 | 0.984 | 10.951 | 3.025 | 0.688 |
| 3 | 0.984 | 10.71 | 3.639 | 0.626 |
| 5 | 1.0 | 13.666 | 5.434 | 0.6 |
| 1 | 0.987 | 12.262 | 4.455 | 0.592 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | Bedroom | 10.951 | 0.984 | 0.688 | RECOMMEND | RECOMMEND: recurring bedroom routine around 11.0h -> suggest comfort/heating adjustment |
| 3 | Kitchen | 10.71 | 0.984 | 0.626 | RECOMMEND | RECOMMEND: recurring kitchen activity around 10.7h -> suggest ventilation/heating pre-adjustment |
| 5 | LivingRoom | 13.666 | 1.0 | 0.6 | RECOMMEND | RECOMMEND: recurring living-room presence around 13.7h -> suggest comfort lighting/heating |
| 1 | LivingRoom | 12.262 | 0.987 | 0.592 | MONITOR | No suggestion |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2012-07-20 11:35:00 | 1 | 228.0 | 6.0 | -0.107 | Unusually high event rate (burst of activity) |
| 2012-10-07 06:55:00 | 1 | 155.0 | 6.0 | -0.105 | Unusually high event rate (burst of activity) |
| 2013-03-28 10:00:00 | 1 | 204.0 | 5.0 | -0.104 | Unusually high event rate (burst of activity) |
| 2012-09-01 00:05:00 | 1 | 170.0 | 6.0 | -0.103 | Unusually high event rate (burst of activity) |
| 2013-01-27 00:35:00 | 1 | 167.0 | 6.0 | -0.102 | Unusually high event rate (burst of activity) |

### Key Visuals

- `outputs\figures\hh101\hh101_events_per_day.png`
- `outputs\figures\hh101\hh101_top_sensors.png`
- `outputs\figures\hh101\hh101_cluster_counts.png`
- `outputs\figures\hh101\hh101_anomaly_score_timeline.png`

## HH102

- Raw events: `4,840,159`
- Modeled windows: `298,543`
- Active windows: `107,369`
- Inactive windows: `191,174`
- Detected anomalies: `5,971`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor, WorkArea`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 72506 | 0.0 | 0.0 | 1.0 | 16.0 | No active sensor |  |
| 1 | 59262 | 13.944 | 1.561 | 0.0 | 20.0 | LivingRoom | Bedroom |
| 2 | 11823 | 90.934 | 4.505 | 0.0 | 20.0 | LivingRoom | WorkArea |
| 3 | 118668 | 0.0 | 0.0 | 1.0 | 4.0 | No active sensor |  |
| 4 | 16084 | 84.22 | 3.175 | 0.0 | 19.0 | Kitchen | DiningRoom |
| 5 | 20200 | 78.33 | 2.555 | 0.0 | 21.0 | Bathroom | Bedroom |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 1 | 1.0 | 12.763 | 4.609 | 0.6 |
| 4 | 0.971 | 15.727 | 3.86 | 0.597 |
| 5 | 0.973 | 14.17 | 5.044 | 0.584 |
| 2 | 0.958 | 14.598 | 4.48 | 0.575 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | LivingRoom | 12.763 | 1.0 | 0.6 | RECOMMEND | RECOMMEND: recurring living-room presence around 12.8h -> suggest comfort lighting/heating |
| 4 | Kitchen | 15.727 | 0.971 | 0.597 | MONITOR | No suggestion |
| 5 | Bathroom | 14.17 | 0.973 | 0.584 | MONITOR | No suggestion |
| 2 | LivingRoom | 14.598 | 0.958 | 0.575 | MONITOR | No suggestion |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2013-08-05 14:30:00 | 2 | 377.0 | 7.0 | -0.164 | Unusually high event rate (burst of activity) |
| 2012-08-13 21:15:00 | 2 | 360.0 | 7.0 | -0.139 | Unusually high event rate (burst of activity) |
| 2012-06-11 13:05:00 | 2 | 299.0 | 7.0 | -0.137 | Unusually high event rate (burst of activity) |
| 2013-07-26 14:50:00 | 2 | 404.0 | 6.0 | -0.134 | Unusually high event rate (burst of activity) |
| 2013-12-09 14:30:00 | 2 | 308.0 | 7.0 | -0.134 | Unusually high event rate (burst of activity) |

### Key Visuals

- `outputs\figures\hh102\hh102_events_per_day.png`
- `outputs\figures\hh102\hh102_top_sensors.png`
- `outputs\figures\hh102\hh102_cluster_counts.png`
- `outputs\figures\hh102\hh102_anomaly_score_timeline.png`
