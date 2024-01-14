---
layout: blog-post
title: "Estimate no. of kafka partitions handled by a single thread on compute"
excerpt: "Estimate no. of kafka partitions handled by a single thread on compute"
disqus_id: /2020/09/06/estimate-partitions-single-thread-compute/
tags:
    - Kafka
    - Concurrency
    - Multithreading
---

In a complex multi data center Kafka deployments, it is also important to
estimate no. of partition each thread will be handling per compute. It is very
important parameter to tune. For example, if you are seeing high lag and less
CPU usage, it could be because a single thread is handling too much partitions
and it might be advisable to increase the no. of threads per compute.

Let me take a hypothetical example of ours.

We have an active-active kafka setup with a topic having 210 partitions.

There is concurrency of 2 per compute i.e. a single VM will be spawning 2
threads to connect to Kafka broker.

There is imbalance in no. of computes. There are 8 computes in DC 1 and
16 computes in DC2.

Thus in DC1, 8*2=16 threads consume 120 partitions. 120/16 = 7.5, which means
Kafka should be allocating 7-8 partitions per thread. When I look at my
distribution, here is what I discover:

```
C1 - 8+8 = 16 partitions (8/thread)
C2 - 8+8 = 16
C3 - 8+7 = 15
C4 - 8+8 = 16
C5 - 7+7 = 14
C6 - 7+7 = 14
c7 - 8+7 = 15
C8 - 7+7 = 14
```

Similarly, in DC2, 16*2=32 threads consume 120 partitions. 120/32 = 3.5, means
Kafka allocates 3-4 partitions per thread on each compute.

Thus, computes in DC1 are doing a lot more work assuming equal distribution
across both DC's.

It is very important to tune the Kafka settings for both the DC's separately
since both are doing unequal amount of work.