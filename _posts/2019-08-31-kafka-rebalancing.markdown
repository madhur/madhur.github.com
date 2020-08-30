---
layout: blog-post
title: "Kafka rebalancing"
excerpt: "Kafka rebalancing"
disqus_id: /2019/08/31/kafka-rebalancing/
tags:
- Kafka
---

## What is kafka rebalancing?

Every consumer in a consumer group is assigned one or more topic partitions exclusively and rebalance is re-assignment of partition ownership among consumers.

It can happen when:
* a consumer joins the group
* a consumer shuts down
* a consumer is considered dead
* new partitions are added

Starting from version 0.8.2.0, the offsets committed by the consumers aren’t saved in ZooKeeper but on a partitioned and replicated topic named `__consumer_offsets`, which is hosted on the Kafka brokers in the cluster.

## Replaying messages

Kafka (starting with version 0.10.1.0) allows you to search message offsets by timestamp. Most language implementations of Kafka API provide corresponding functions/API to perform such a search. Using this API, you can program your consumer to determine the offset of the message that appeared in its assigned partition at or immediately after a certain point of time. When configured for replaying, the consumer can thus determine the offset for a given timestamp, and simply flag it as the “committed” offset. Once this is done, the consumer will start consuming messages from that point onwards, until the the message at the latest offset is consumed. This effectively achieves the “rewind and replay” objective.