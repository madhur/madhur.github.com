---
layout: blog-post
title: "Meaning of atleast once, atmost once and exactly once delivery"
excerpt: "Meaning of atleast once, atmost once and exactly once delivery"
disqus_id: /2019/08/04/atleast-once-atmost-once-exactly-once/
tags:
- Kafka
---

Ever since I have started working with Kafka, I have came across these terms very frequently, Atleast once, Atmost once and Exactly Once. 

As an engineer, It is very important to understand these concepts.

## At-most once Configuration

As the name suggests, At-most-once means the message will be delivered atmost once. Once delivered, there is no chance of delivering again. If the consumer is unable to handle the message due to some exception, the message is lost. This is because Kafka is automatically commiting the last offset used.

* Set `enable.auto.commit` to `true`
* Set `auto.commit.interval.ms` to low value
* Since `auto.commit` is set to true, there is no need to call `consumer.commitSync()` from the consumer.

Note that it is also possible to have at-lest-once scenario with the same configuration. Let's say consumer successfully processed the message successfully into its store and in the meantime before kafka could commit the offset, consumer was restarted. In this scenario, consumer would again get the same message.

Hence, even if using at-most once or at-least once configuration, consumer should be always prepared to handle the duplicates.

## At-least once configuration

At-least once as the name suggests, message will be delivered atleast once. There is high chance that message will be delivered again as duplicate.

* Set `enable.auto.commit` to `false` OR
* Consumer should now then take control of the message offset commits to Kafka by making the `consumer.commitSync()` call.

Let's say consumer has processed the messages and committed the messages to its local store, but consumer crashes and did not get a chance to commit offset to Kafka before it has crashed. When consumer restarts, Kafka would deliver messages from the last offset, resulting in duplicates.

## Exactly-once configuraition

Exactly-once as the name suggests, there will be only one and once message delivery. It difficult to achieve in practice.

In this case offset needs to be manually managed.

* Set `enable.auto.commit` to `false`
* Do not make call to `consumer.commitSync()`
* Implement a `ConsumerRebalanceListener` and within the listener perform `consumer.seek(topicPartition,offset);` to start reading from a specific offset of that topic/partition.
* While processing the messages, get hold of the offset of each message.  Store the processed message’s offset in an atomic way along with the processed message using atomic-transaction. When data is stored in relational database atomicity is easier to implement. For non-relational data-store such as HDFS store or No-SQL store one way to achieve atomicity is as follows: Store the offset along with the message.

