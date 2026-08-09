# Evaluation Results

This report summarizes the per-home results generated from the project pipeline and notebooks.

## HH101

- Raw events: `1,286,244`
- Modeled windows: `107,126`
- Active windows: `45,673`
- Inactive windows: `61,453`
- Detected anomalies: `2,143`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 27668 | 0.0 | 0.0 | 1.0 | 18.0 | No active sensor |  |
| 1 | 3378 | 57.835 | 3.346 | 0.0 | 14.0 | LivingRoom | OutsideDoor |
| 2 | 4835 | 85.651 | 2.233 | 0.0 | 12.0 | Bedroom | Bathroom |
| 3 | 3664 | 90.07 | 3.089 | 0.0 | 10.0 | Kitchen | LivingRoom |
| 4 | 33785 | 0.0 | 0.0 | 1.0 | 2.0 | No active sensor |  |
| 5 | 33796 | 10.26 | 1.122 | 0.0 | 10.0 | LivingRoom | Bedroom |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 3 | 0.984 | 10.04 | 3.844 | 0.606 |
| 5 | 1.0 | 12.232 | 5.769 | 0.6 |
| 1 | 0.987 | 13.135 | 4.606 | 0.592 |
| 2 | 0.984 | 11.098 | 4.023 | 0.59 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Kitchen | 10.04 | 0.984 | 0.606 | RECOMMEND | RECOMMEND: recurring kitchen activity around 10.0h -> suggest ventilation/heating pre-adjustment |
| 5 | LivingRoom | 12.232 | 1.0 | 0.6 | RECOMMEND | RECOMMEND: recurring living-room presence around 12.2h -> suggest comfort lighting/heating |
| 1 | LivingRoom | 13.135 | 0.987 | 0.592 | MONITOR | No suggestion |
| 2 | Bedroom | 11.098 | 0.984 | 0.59 | MONITOR | No suggestion |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2012-07-20 11:35:00 | 1 | 228.0 | 6.0 | -0.107 | Unusually intense multi-room activity for this home |
| 2012-10-07 06:55:00 | 1 | 155.0 | 6.0 | -0.105 | Unusually intense multi-room activity for this home |
| 2013-03-28 10:00:00 | 1 | 204.0 | 5.0 | -0.104 | Unusually intense multi-room activity for this home |
| 2012-09-01 00:05:00 | 1 | 170.0 | 6.0 | -0.103 | Unusually intense multi-room activity for this home |
| 2013-01-27 00:35:00 | 1 | 167.0 | 6.0 | -0.102 | Unusually intense multi-room activity for this home |

### Key Visuals

- `outputs\figures\hh101\hh101_events_per_day.png`
- `outputs\figures\hh101\hh101_top_sensors.png`
- `outputs\figures\hh101\hh101_cluster_counts.png`
- `outputs\figures\hh101\hh101_anomaly_score_timeline.png`

## HH102

- Raw events: `4,840,159`
- Modeled windows: `298,542`
- Active windows: `107,369`
- Inactive windows: `191,173`
- Detected anomalies: `5,971`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor, WorkArea`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 71176 | 0.293 | 0.048 | 0.955 | 4.0 | Bedroom | WorkArea |
| 1 | 19241 | 76.57 | 3.156 | 0.0 | 19.0 | Kitchen | DiningRoom |
| 2 | 13274 | 85.476 | 4.387 | 0.0 | 14.0 | LivingRoom | WorkArea |
| 3 | 22997 | 73.358 | 2.54 | 0.0 | 21.0 | Bathroom | Bedroom |
| 4 | 98882 | 5.05 | 0.646 | 0.541 | 16.0 | LivingRoom | Bedroom |
| 5 | 72972 | 0.319 | 0.051 | 0.954 | 2.0 | Bedroom | WorkArea |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 1 | 0.974 | 16.377 | 3.855 | 0.599 |
| 4 | 0.997 | 12.415 | 4.137 | 0.598 |
| 3 | 0.977 | 12.762 | 5.128 | 0.586 |
| 2 | 0.962 | 14.957 | 4.341 | 0.577 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Kitchen | 16.377 | 0.974 | 0.599 | MONITOR | No suggestion |
| 4 | LivingRoom | 12.415 | 0.997 | 0.598 | MONITOR | MONITOR: inactivity-dominant cluster excluded from automation suggestions |
| 3 | Bathroom | 12.762 | 0.977 | 0.586 | MONITOR | No suggestion |
| 2 | LivingRoom | 14.957 | 0.962 | 0.577 | MONITOR | No suggestion |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2013-08-05 14:30:00 | 2 | 377.0 | 7.0 | -0.172 | Unusually intense multi-room activity for this home |
| 2012-08-13 21:15:00 | 2 | 360.0 | 7.0 | -0.152 | Unusually intense multi-room activity for this home |
| 2013-07-26 14:50:00 | 2 | 404.0 | 6.0 | -0.15 | Unusually intense multi-room activity for this home |
| 2012-06-11 13:05:00 | 2 | 299.0 | 7.0 | -0.147 | Unusually intense multi-room activity for this home |
| 2012-12-24 14:20:00 | 2 | 315.0 | 7.0 | -0.147 | Unusually intense multi-room activity for this home |

### Key Visuals

- `outputs\figures\hh102\hh102_events_per_day.png`
- `outputs\figures\hh102\hh102_top_sensors.png`
- `outputs\figures\hh102\hh102_cluster_counts.png`
- `outputs\figures\hh102\hh102_anomaly_score_timeline.png`
