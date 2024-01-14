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

Multithreading / Concurrency have always been the favorite topic of mine. It gives me a pure joy to extract most out of a machine by loading the CPU with work just like a master exploiting its slaves :)

Unfortunately, these days due to distributed nature of computing, most of the time in a machine is spent waiting on I/O (either from database, API's etc.) and our CPU just sits idle most of the time.

[Kafka](https://kafka.apache.org/) allows you to scale your distributed system through partitions where a compute can be attached to consuming from particular partition, which is an ordered subset of messages in a topic.

Recently, I have seen a trend where developers instead of making sure a compute is able to efficiently process the data from the single partition, prefer the easy way out of increasing the partitions/vm's to reach the desired
throughput. It's like throwing money at the problem.

In this post, we will look at ways to increase concurrency of Kafka consumer so
that we are able to achieve more from a single consumer instead of increasing
the partitions. There are two types of multithreading which can be achieved with
Kafka - 

* Thread per consumer model
* Multi-threaded consumer model

In the thread per consumer model, each thread is instantiated and connects to
Kafka broker. The kafka broker assigns the partitions whose messages will be
delivered to these threads.

In the multi-threaded consumer mode, a single thread connects to Kafka and may
get data from multiple / single partition(s). Once the data has been delivered
that thread, the thread may deliver the messages to multiple pool of threads to
allow them to process in parallel. In this approach, consumer thread can decide
which type of messages will be handled by which child thread. However, offset
management becomes very tricky in this case.

There are pros/cons of each approach and we'll go over these.

## Thread per consumer model

This is a simplest approach, which can be easily
achieved using Spring Kafka as shown below.

It's very easy to configure spring to spawn multiple threads to connect to
Kafka. Let's see how the behavior differs. We have a single topic `test-topic`
with 10 partitions and a single VM running spring application with single
concurrency.

Just to be clear, the following configuration specifies the concurrency in
spring kafka listener

```java
/**
* Consumer configuration for email topics
*
* @return
*/
@Bean
public ConsumerFactory<String, String> consumerFactory()
{
    Map<String, Object> props = new HashMap<>();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ConsumerConfig.GROUP_ID_CONFIG, EMAIL_STATUS_CONSUMER_GROUP);
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
            StringDeserializer.class);
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
            StringDeserializer.class);
    return new DefaultKafkaConsumerFactory<>(props);
}

/**
* Sets Concurrency for kafka listener
*
* @return
*/
@Bean
public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory()
{
    ConcurrentKafkaListenerContainerFactory<String, String> factory = new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(consumerFactory());
    factory.setConcurrency(1);
    return factory;
}
```

We are using consumer group `spring-group` to listen to this partition.
Following is the behavior with single concurrency:

```
GROUP           TOPIC           PARTITION  CONSUMER-ID                                     HOST            CLIENT-ID
spring-group    test-topic      8          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      2          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      1          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      4          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      5          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      6          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      3          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      7          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      9          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
spring-group    test-topic      0          consumer-1-01a5779b-940b-44cf-b8c6-2e414aa38eb1 /172.22.0.1     consumer-1
```

If you closely observe the above output, the consumer ID of the application is
same for all the 10 partitions, indicating that its the single thread which is
connected to all the partitions.

Now, let's see the output, when concurrency is increased to 2,

```
GROUP           TOPIC           PARTITION  CONSUMER-ID                                     HOST            CLIENT-ID
spring-group    test-topic      8          consumer-2-8ab0213d-683c-4f92-b3c8-767701905994 /172.22.0.1     consumer-2
spring-group    test-topic      5          consumer-2-8ab0213d-683c-4f92-b3c8-767701905994 /172.22.0.1     consumer-2
spring-group    test-topic      6          consumer-2-8ab0213d-683c-4f92-b3c8-767701905994 /172.22.0.1     consumer-2
spring-group    test-topic      7          consumer-2-8ab0213d-683c-4f92-b3c8-767701905994 /172.22.0.1     consumer-2
spring-group    test-topic      9          consumer-2-8ab0213d-683c-4f92-b3c8-767701905994 /172.22.0.1     consumer-2
spring-group    test-topic      4          consumer-1-886f1a6e-f316-4e17-90d2-599a582682e4 /172.22.0.1     consumer-1
spring-group    test-topic      2          consumer-1-886f1a6e-f316-4e17-90d2-599a582682e4 /172.22.0.1     consumer-1
spring-group    test-topic      3          consumer-1-886f1a6e-f316-4e17-90d2-599a582682e4 /172.22.0.1     consumer-1
spring-group    test-topic      1          consumer-1-886f1a6e-f316-4e17-90d2-599a582682e4 /172.22.0.1     consumer-1
spring-group    test-topic      0          consumer-1-886f1a6e-f316-4e17-90d2-599a582682e4 /172.22.0.1     consumer-1
```

If you notice above, now there are 2 threads which have been equally given 5
partitions each.

This is very straightforward to understand, Kafka will try to distribute the
partitions equally among the threads belonging to same consumer group. If we
spawn, 10 concurrency, we will have a dedicated thread for each partition.

It's interesting to study this behavior when there are multiple topics to
consumer from. So now, let's create two more topics, `test-topic2` and
`test-topic3` with 10 partitions each.


This has an interesting behaviour the way consumers are written within spring.

For example, if we are consuming from all three topics like this:

```java
@KafkaListener(containerFactory = "kafkaListenerContainerFactory", topics = {"test-topic", "test-topic2", "test-topic3"})
public void consume(String message) {
    logger.info(String.format("$$ -> Consumed Message -> %s",message));
}
```

We get a single thread listening from all the 30 partitions of 3 topics combined

```
GROUP           TOPIC           PARTITION  CONSUMER-ID                                     HOST            CLIENT-ID
spring-group    test-topic3     7          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     0          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      2          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     3          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     1          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     6          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      8          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     5          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     9          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      4          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      5          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      6          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      3          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     2          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     6          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     8          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     4          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     0          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     3          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     7          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      1          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     2          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      7          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      9          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic      0          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     1          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     8          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic2     4          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     5          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
spring-group    test-topic3     9          consumer-1-51ce4005-ce57-472f-bfe4-4419e1fb8d43 /172.22.0.1     consumer-1
```


On the other hand, if we split the consumption within different methods,

```java
@KafkaListener(containerFactory = "kafkaListenerContainerFactory", topics = "test-topic")
public void consume(String message) {
    logger.info(String.format("$$ -> Consumed Message -> %s",message));
}

@KafkaListener(containerFactory = "kafkaListenerContainerFactory", topics = "test-topic2")
public void consume2(String message) {
    logger.info(String.format("$$ -> Consumed Message -> %s",message));
}

@KafkaListener(containerFactory = "kafkaListenerContainerFactory", topics = "test-topic3")
public void consume3(String message) {
    logger.info(String.format("$$ -> Consumed Message -> %s",message));
}
```

Spring will automatically spawn a thread for each listener even though we have
provided the concurrency as one

```
GROUP           TOPIC           PARTITION  CONSUMER-ID                                     HOST            CLIENT-ID
spring-group    test-topic3     6          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     7          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     0          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     3          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     1          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     2          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     8          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     4          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     5          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic3     9          consumer-1-edd9ef42-6a06-4289-925b-f97cb489e8c7 /172.22.0.1     consumer-1
spring-group    test-topic2     5          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     9          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     2          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     6          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     0          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     3          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     7          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     1          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     8          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic2     4          consumer-3-b5304419-cde4-4355-b194-ee7bb8b40894 /172.22.0.1     consumer-3
spring-group    test-topic      8          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      2          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      1          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      4          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      5          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      6          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      3          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      7          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      9          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
spring-group    test-topic      0          consumer-2-18796186-831a-468a-b3c4-b39d43f750f0 /172.22.0.1     consumer-2
```

This is a very important distinct to be aware of in order to properly scale your
applications to consume the heavy traffic from the topics without any lag.

So what we understand is that the method
[`setConcurrency`](https://docs.spring.io/spring-kafka/api/org/springframework/kafka/listener/ConcurrentMessageListenerContainer.html#setConcurrency-int-)
is per instance of
[`KafkaListener`](https://docs.spring.io/spring-kafka/api/org/springframework/kafka/config/KafkaListenerContainerFactory.html)

It is also important to understand that there is no point creating more threads
than there are number of partitions as those will be left idle.

The above sample application source can be found in my [Github repository](https://github.com/madhur/kafka-consumer-concurrency)

In the next post, we will look at Multi-threaded consumer model.