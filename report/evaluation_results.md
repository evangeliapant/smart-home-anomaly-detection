# Evaluation Results

This report summarizes the per-home results generated from the project pipeline and notebooks.

The modeled outputs in this report were generated with `60`-minute windows.

## HH101

- Raw events: `1,286,244`
- Window size: `60` minutes
- Modeled windows: `8,929`
- Active windows: `7,654`
- Inactive windows: `1,275`
- Detected anomalies: `179`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2123 | 41.028 | 1.484 | 0.0 | 4.0 | LivingRoom | Bedroom |
| 1 | 698 | 396.656 | 4.501 | 0.0 | 9.0 | Kitchen | LivingRoom |
| 2 | 2016 | 48.741 | 1.589 | 0.0 | 20.0 | LivingRoom | Bedroom |
| 3 | 1275 | 0.0 | 0.0 | 1.0 | 18.0 | No active sensor |  |
| 4 | 504 | 612.524 | 5.139 | 0.0 | 11.0 | Bedroom | Bathroom |
| 5 | 2313 | 222.785 | 4.823 | 0.0 | 17.0 | LivingRoom | Bedroom |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 1 | 0.925 | 9.157 | 2.249 | 0.73 |
| 0 | 0.569 | 0.635 | 0.953 | 0.646 |
| 5 | 0.987 | 5.191 | 3.624 | 0.63 |
| 4 | 0.943 | 9.72 | 3.643 | 0.602 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Kitchen | 9.157 | 0.925 | 0.73 | RECOMMEND | RECOMMEND: recurring kitchen activity around 9.2h -> suggest ventilation/heating pre-adjustment |
| 0 | LivingRoom | 0.635 | 0.569 | 0.646 | MONITOR | No suggestion |
| 5 | LivingRoom | 5.191 | 0.987 | 0.63 | RECOMMEND | RECOMMEND: recurring living-room presence around 5.2h -> suggest comfort lighting/heating |
| 4 | Bedroom | 9.72 | 0.943 | 0.602 | RECOMMEND | RECOMMEND: recurring bedroom routine around 9.7h -> suggest comfort/heating adjustment |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2012-07-20 11:00:00 | 1 | 1596.0 | 6.0 | -0.106 | Unusually high event rate (burst of activity) |
| 2012-10-24 13:00:00 | 1 | 982.0 | 6.0 | -0.103 | Unusually high event rate (burst of activity) |
| 2012-09-06 11:00:00 | 1 | 1115.0 | 5.0 | -0.096 | Unusually high event rate (burst of activity) |
| 2013-01-17 10:00:00 | 1 | 763.0 | 6.0 | -0.09 | Unusually high event rate (burst of activity) |
| 2012-10-04 13:00:00 | 1 | 744.0 | 6.0 | -0.083 | Unusually high event rate (burst of activity) |

### Key Visuals

- `outputs\figures\hh101\hh101_events_per_day.png`
- `outputs\figures\hh101\hh101_top_sensors.png`
- `outputs\figures\hh101\hh101_cluster_counts.png`
- `outputs\figures\hh101\hh101_anomaly_score_timeline.png`

## HH102

- Raw events: `4,840,159`
- Window size: `60` minutes
- Modeled windows: `24,880`
- Active windows: `17,907`
- Inactive windows: `6,973`
- Detected anomalies: `498`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor, WorkArea`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6973 | 0.0 | 0.0 | 1.0 | 1.0 | No active sensor |  |
| 1 | 1924 | 617.729 | 5.694 | 0.0 | 18.0 | Kitchen | LivingRoom |
| 2 | 4428 | 333.697 | 6.176 | 0.0 | 8.0 | LivingRoom | Bedroom |
| 3 | 5396 | 52.71 | 1.918 | 0.0 | 23.0 | Bedroom | Bathroom |
| 4 | 1959 | 739.271 | 5.909 | 0.0 | 21.0 | Bathroom | Bedroom |
| 5 | 4200 | 104.659 | 3.142 | 0.0 | 16.0 | Kitchen | LivingRoom |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 3 | 0.988 | 1.223 | 2.366 | 0.756 |
| 5 | 0.971 | 11.082 | 2.464 | 0.736 |
| 2 | 0.965 | 8.08 | 2.723 | 0.707 |
| 4 | 0.842 | 11.656 | 4.154 | 0.505 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Bedroom | 1.223 | 0.988 | 0.756 | RECOMMEND | RECOMMEND: recurring bedroom routine around 1.2h -> suggest comfort/heating adjustment |
| 5 | Kitchen | 11.082 | 0.971 | 0.736 | RECOMMEND | RECOMMEND: recurring kitchen activity around 11.1h -> suggest ventilation/heating pre-adjustment |
| 2 | LivingRoom | 8.08 | 0.965 | 0.707 | RECOMMEND | RECOMMEND: recurring living-room presence around 8.1h -> suggest comfort lighting/heating |
| 4 | Bathroom | 11.656 | 0.842 | 0.505 | MONITOR | No suggestion |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2011-11-28 13:00:00 | 4 | 2864.0 | 7.0 | -0.145 | Unusually high event rate (burst of activity) |
| 2012-12-24 14:00:00 | 4 | 2239.0 | 7.0 | -0.138 | Unusually high event rate (burst of activity) |
| 2013-05-27 13:00:00 | 4 | 1952.0 | 6.0 | -0.129 | Unusually high event rate (burst of activity) |
| 2013-08-05 14:00:00 | 4 | 1874.0 | 7.0 | -0.126 | Unusually high event rate (burst of activity) |
| 2013-11-25 13:00:00 | 1 | 1787.0 | 7.0 | -0.126 | Unusually high event rate (burst of activity) |

### Key Visuals

- `outputs\figures\hh102\hh102_events_per_day.png`
- `outputs\figures\hh102\hh102_top_sensors.png`
- `outputs\figures\hh102\hh102_cluster_counts.png`
- `outputs\figures\hh102\hh102_anomaly_score_timeline.png`
