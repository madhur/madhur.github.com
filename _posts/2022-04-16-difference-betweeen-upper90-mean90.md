---
layout: blog-post
title: "Difference between upper90 and mean90"
excerpt: "Difference between upper90 and mean90"
disqus_id: /2022/04/16/difference-between-upper90-mean90/
tags:    
    - StatsD
---

[StatsD](https://github.com/statsd/statsd) which is an excellent metrics aggregator, which can send aggregate and send metrics to variety of backends such as [Graphite](https://graphiteapp.org/)

One of the aggregations which StatsD is generate an upper_99 and mean_99 for series of metrics. It is important to understand the differences between two. This is because if you are just measuring mean_99 , you might be missing on certain outliers which are important to understand the overall picture in the system.


For example, if the latencies reported by system are

```
0 
5 
10 
15 
20 
25 
30 
35 
40 
45 
50 
55 
60 
65 
70 
75 
80 
85 
90 
95
---


mean_90 = 42.5 (mean of 0 - 85)
upper_90 = 85
```

If you are plotting `mean_90` , in the dashboard to monitor the latencies, it would give a very wrong picture, as the 90th percentile of dataset is actually 85.5. Looking at `mean_90`, completely distorts the picture.

Hence, always opt for looking at `upper_99` metrics while at important system metrics such as latencies.