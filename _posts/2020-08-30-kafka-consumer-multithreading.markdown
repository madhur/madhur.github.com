---
layout: blog-post
title: "Kafka Consumer Multithreading"
excerpt: "Kafka Consumer Multithreading"
disqus_id: /2020/08/30/kafka-consumer-multithreading/
tags:
    - Kafka
    - Concurrency
    - Multithreading
---

Multithreading / Concurrency have always been the favourite topic of mine. It gives me a pure joy to extract most out of a machine by loading the CPU with work just like a master exploiting its slaves :)

Unfortunately, these days due to distributed nature of computing, most of the time in a machine is spent waiting on I/O (either from database, API's etc) and our CPU just sits idle most of the time.

[Kafka]() allows you to scale your distributed system through partitions where a compute can be attached to consuming from particular parition, which is an ordered subset of messages in a topic.

Recently, I have seen a trend where developers instead of making sure a compute is able to efficeintly process the data from the single partition, prefer the easy way out of increasing the partitions/vm's to reach the desired
throughput. It's like throwing money at the problem.

In this post, we will look at ways to increase concurrency of Kafka consumer so that we are able to achieve more from a single consumer instead of increasing the partitions. There are pros/cons of each approach and we'll go
over these.

