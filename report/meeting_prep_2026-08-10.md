# Meeting Preparation for August 10, 2026

This note is a compact script for explaining the project clearly in a professor meeting.

## 1. One-minute project summary

My project studies whether smart-home sensor data can be analyzed without manual labels. I use an unsupervised machine-learning pipeline that takes raw sensor events, groups them into fixed time windows, builds behavioral features, discovers recurring routines with clustering, detects unusual windows with anomaly detection, and then derives conservative automation suggestions only from stable routines. The main idea is not to classify activities such as cooking or sleeping directly, but to discover recurring behavior patterns from the data itself.

## 2. What problem the project solves

Smart-home datasets are usually large streams of sensor events, and they are difficult to interpret directly. In practice, labeled activity data is often unavailable. So the problem I address is: can we still extract useful behavioral structure from unlabeled data? My answer is to model recurring patterns, detect unusual behavior, and translate only the most stable patterns into explainable smart-home suggestions.

## 3. Pipeline step by step

1. Start with raw sensor event logs.
2. Clean the data and parse timestamps.
3. Group events into fixed time windows.
4. Build window-level features:
   - per-sensor counts,
   - total event count,
   - number of active sensors,
   - time-of-day and day-of-week,
   - inactivity indicator.
5. Run KMeans clustering to discover recurring window types.
6. Run Isolation Forest to flag unusual windows.
7. Aggregate cluster behavior across days and compute routine stability.
8. Generate automation suggestions only for stable, interpretable, non-inactivity-dominant clusters.

## 4. Why I used this method

- I used **unsupervised learning** because the dataset is unlabeled.
- I used **fixed windows** to transform event streams into comparable observations.
- I used **KMeans** because it is simple, standard, and produces interpretable groups of similar windows.
- I used **Isolation Forest** because it is a common unsupervised anomaly detector and works without labeled anomalies.
- I added a **routine stability score** because not every cluster should become an automation rule.
- I explicitly modeled **inactive windows** so quiet periods are treated as part of the data rather than ignored.

## 5. Main branch vs. `feature/1h-window-analysis`

The pipeline is the same in both branches. The main difference is the time resolution.

| Branch | Window size | Interpretation |
| --- | --- | --- |
| `main` | 5 minutes | Fine-grained, better for short bursts and short anomalies |
| `feature/1h-window-analysis` | 60 minutes | Coarser, better for broad hourly routines |

So the feature branch is a comparison setup that asks: what happens if we summarize behavior at the hour level instead of the 5-minute level?

## 6. Main results to explain

### HH101

- 1,286,244 raw events
- 8,929 hourly windows
- 179 anomalous windows
- clear interpretable clusters such as:
  - morning kitchen-centered activity,
  - midday bedroom/bathroom activity,
  - evening living-room activity,
  - one inactivity cluster.

Main takeaway: the pipeline finds broad daily routines and produces conservative recommendations such as kitchen pre-adjustment or living-room comfort settings.

### HH102

- 4,840,159 raw events
- 24,880 hourly windows
- 498 anomalous windows
- richer multi-room behavior than HH101 because the home is larger and includes `WorkArea`.

Main takeaway: the same pipeline scales to a larger and more complex home, still separating inactivity, stable routines, and unusual high-activity hours.

## 7. What the results mean

The key meaning of the results is:

- the clustering stage finds recurring behavior patterns,
- the anomaly stage finds unusual windows,
- the routine-stability stage prevents overclaiming,
- and the automation stage stays conservative.

So the project does not claim to perfectly recognize human activities. It claims that unlabeled sensor data can still support interpretable behavioral analysis.

## 8. How to explain the figures

- `events_per_day`: how overall activity changes over time.
- `top_sensors`: which rooms dominate the event stream.
- `cluster_counts`: how common each routine cluster is.
- `cluster_sensor_heatmap`: which sensors characterize each cluster.
- `anomaly_score_timeline`: when unusual windows appear.

If asked how to read a cluster figure, say: "A cluster is a recurring type of time window characterized by dominant sensors, event intensity, and typical time of day."

## 9. Likely weak point / what the professor probably meant

The materials were technically correct, but they may not have made the interpretation obvious enough:

- what exact question the project answers,
- what each stage contributes,
- how to interpret a cluster,
- what the difference is between a cluster and a real activity label,
- and what final conclusion the reader should take away.

## 10. Safe conclusion to say in the meeting

My final conclusion is that the project works as an interpretable proof of concept for unsupervised smart-home behavior analysis. It is able to extract recurring routines, identify unusual behavior windows, and propose conservative automations from unlabeled sensor streams. The main design tradeoff is temporal resolution: shorter windows capture fine detail, while hourly windows produce broader and easier-to-explain routines.

## 11. Short spoken script

"The goal of my project was to see whether unlabeled smart-home sensor data can still be used to learn useful behavioral structure. I built a pipeline that takes raw events, aggregates them into fixed windows, engineers window-level features, uses KMeans to discover recurring behavior patterns, uses Isolation Forest to detect unusual windows, and then scores the stability of those routines across days. Only the stable and interpretable routines are turned into automation suggestions. The main branch uses 5-minute windows, which are better for short events, while the `feature/1h-window-analysis` branch uses 60-minute windows, which are easier to interpret as broad daily routines. So the main contribution is an interpretable unsupervised prototype, not a fully validated production system."

## 12. Questions you may get

### Why unsupervised learning?

Because the data is unlabeled, and the project goal is to discover structure without manual annotation.

### Why KMeans?

It provides a simple and interpretable baseline for grouping similar behavioral windows.

### Why Isolation Forest?

It is suitable for unsupervised anomaly detection when there are no labeled anomalies.

### Why keep empty windows?

Because inactivity is part of real home behavior and should be modeled explicitly.

### Why compare 5-minute and 60-minute windows?

To show the tradeoff between fine detail and interpretability.

### What is the main limitation?

The clusters are behavioral patterns, not guaranteed semantic activity labels, and the system is a prototype rather than a validated deployed controller.
