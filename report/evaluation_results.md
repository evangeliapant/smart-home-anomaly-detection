# Evaluation Results

This report summarizes the per-home results generated from the project pipeline and notebooks.

The modeled outputs in this report were generated with `60`-minute windows.

## HH101

- Raw events: `1,286,244`
- Window size: `60` minutes
- Modeled windows: `8,928`
- Active windows: `7,654`
- Inactive windows: `1,274`
- Detected anomalies: `179`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2295 | 74.098 | 2.067 | 0.0 | 20.0 | LivingRoom | Kitchen |
| 1 | 1991 | 245.748 | 5.069 | 0.0 | 8.0 | LivingRoom | Bedroom |
| 2 | 478 | 619.596 | 5.119 | 0.0 | 11.0 | Bedroom | Bathroom |
| 3 | 2210 | 28.014 | 1.315 | 0.0 | 4.0 | Bedroom | LivingRoom |
| 4 | 1274 | 0.0 | 0.0 | 1.0 | 18.0 | No active sensor |  |
| 5 | 680 | 395.328 | 4.488 | 0.0 | 9.0 | Kitchen | LivingRoom |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 3 | 0.992 | 0.8 | 1.084 | 0.887 |
| 5 | 0.922 | 8.973 | 2.201 | 0.733 |
| 0 | 0.995 | 12.928 | 3.371 | 0.66 |
| 1 | 0.984 | 5.108 | 3.597 | 0.631 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Bedroom | 0.8 | 0.992 | 0.887 | AUTO | AUTO: recurring bedroom routine around 0.8h -> suggest comfort/heating adjustment |
| 5 | Kitchen | 8.973 | 0.922 | 0.733 | RECOMMEND | RECOMMEND: recurring kitchen activity around 9.0h -> suggest ventilation/heating pre-adjustment |
| 0 | LivingRoom | 12.928 | 0.995 | 0.66 | RECOMMEND | RECOMMEND: recurring living-room presence around 12.9h -> suggest comfort lighting/heating |
| 1 | LivingRoom | 5.108 | 0.984 | 0.631 | RECOMMEND | RECOMMEND: recurring living-room presence around 5.1h -> suggest comfort lighting/heating |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2012-10-24 13:00:00 | 5 | 982.0 | 6.0 | -0.113 | Unusually intense multi-room activity for this home |
| 2012-07-20 11:00:00 | 1 | 1596.0 | 6.0 | -0.085 | Unusually intense multi-room activity for this home |
| 2012-10-17 17:00:00 | 5 | 820.0 | 5.0 | -0.084 | Dense burst of repeated activity in a small set of sensors |
| 2013-05-12 10:00:00 | 2 | 972.0 | 6.0 | -0.081 | Unusually intense multi-room activity for this home |
| 2013-01-17 10:00:00 | 5 | 763.0 | 6.0 | -0.074 | Unusually intense multi-room activity for this home |

### Key Visuals

- `outputs\figures\hh101\hh101_events_per_day.png`
- `outputs\figures\hh101\hh101_top_sensors.png`
- `outputs\figures\hh101\hh101_cluster_counts.png`
- `outputs\figures\hh101\hh101_anomaly_score_timeline.png`

## HH102

- Raw events: `4,840,159`
- Window size: `60` minutes
- Modeled windows: `24,879`
- Active windows: `17,907`
- Inactive windows: `6,972`
- Detected anomalies: `498`
- Sensor features: `Bathroom, Bedroom, DiningRoom, Kitchen, LivingRoom, OutsideDoor, WorkArea`

### Cluster Summary

| cluster | n_windows | mean_total_events | mean_unique_sensors | inactive_fraction | peak_hour | top_sensor_1 | top_sensor_2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6972 | 0.0 | 0.0 | 1.0 | 1.0 | No active sensor |  |
| 1 | 1992 | 622.616 | 5.623 | 0.0 | 21.0 | Bathroom | Bedroom |
| 2 | 561 | 953.667 | 6.715 | 0.0 | 14.0 | LivingRoom | WorkArea |
| 3 | 7433 | 46.447 | 1.881 | 0.0 | 23.0 | Bedroom | Bathroom |
| 4 | 1945 | 588.77 | 5.616 | 0.0 | 18.0 | Kitchen | DiningRoom |
| 5 | 5976 | 263.167 | 5.614 | 0.0 | 15.0 | LivingRoom | Kitchen |

### Routine Stability

| cluster | frequency | avg_peak_hour | std_peak_hour | stability_score |
| --- | --- | --- | --- | --- |
| 3 | 0.998 | 1.02 | 1.924 | 0.806 |
| 5 | 0.97 | 7.862 | 2.367 | 0.745 |
| 1 | 0.867 | 10.748 | 4.178 | 0.52 |
| 4 | 0.785 | 13.888 | 3.862 | 0.485 |

### Automation Suggestions

| cluster | top_sensor | avg_peak_hour | frequency | stability_score | level | suggestion |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Bedroom | 1.02 | 0.998 | 0.806 | AUTO | AUTO: recurring bedroom routine around 1.0h -> suggest comfort/heating adjustment |
| 5 | LivingRoom | 7.862 | 0.97 | 0.745 | RECOMMEND | RECOMMEND: recurring living-room presence around 7.9h -> suggest comfort lighting/heating |
| 1 | Bathroom | 10.748 | 0.867 | 0.52 | MONITOR | No suggestion |
| 4 | Kitchen | 13.888 | 0.785 | 0.485 | MONITOR | No suggestion |

### Top Anomaly Windows

| window_start | cluster | total_events | n_sensors_active | anomaly_score | explanation |
| --- | --- | --- | --- | --- | --- |
| 2011-11-28 13:00:00 | 2 | 2864.0 | 7.0 | -0.114 | Unusually intense multi-room activity for this home |
| 2012-12-24 14:00:00 | 2 | 2239.0 | 7.0 | -0.107 | Unusually intense multi-room activity for this home |
| 2012-08-09 16:00:00 | 2 | 1907.0 | 7.0 | -0.102 | Unusually intense multi-room activity for this home |
| 2012-08-05 10:00:00 | 2 | 1961.0 | 7.0 | -0.102 | Unusually intense multi-room activity for this home |
| 2012-11-28 13:00:00 | 2 | 2022.0 | 7.0 | -0.101 | Unusually intense multi-room activity for this home |

### Key Visuals

- `outputs\figures\hh102\hh102_events_per_day.png`
- `outputs\figures\hh102\hh102_top_sensors.png`
- `outputs\figures\hh102\hh102_cluster_counts.png`
- `outputs\figures\hh102\hh102_anomaly_score_timeline.png`
