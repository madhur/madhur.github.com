---
layout: blog-post
title: "Considerations for high throughput kafka producer"
excerpt: "Considerations for high throughput kafka producer"
disqus_id: /2019/06/17/considerations-high-throughput-kafka-producer/
tags:
- Java
- Kafka
---

I have been recently working on lot of high throughput kafka producers. Our application publishes close to 3 million kafka publishes per day. (which is still low compared to what kafka can handle)

There are some of the learnings along the way in maintaining such kafka producers:

* Choose the number of partitions wisely: The number of partitions determine how much consumers can scale. Number of partitions is degree of parallelism in kafka. Kafka gives a single partition's data to single thread.

Our general thumb rule is to have partitions equal to number of consumer servers. For example, if we have cluster of 20 servers consuming from kafka topic, each server will be consuming from single partition so 20 partitions.

There are many other factors to be considered [as explained here](https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster)

* Decide a consistent key while publishing - Messages published with the same key will be published to a single partition. A partition is logic unit of ordering of messages. So if ordering of messages is important to you, you should choose a consistent key for those messages. 


* Use power of asynchronous - Kafka producer is by default asynchronous unless you use a blocking call explicitly. That means that kafka publish can fail and your code would have moved past the publish method already. Kafka producer provides a callback once the server has executed the publish instruction. In this callback, the user can check for failure and retry the option or send to a dead letter queue etc. Kafka producer itself retries for 3 times but I believe that is too less and not enough for data critical applications.

Below is the sample snippet of such producer

```java
@Autowired
@Qualifier("createKafkaSslProducerOrder")
Producer kafkaSslProducer;

public void publish(String messageKey, String payload, String topic) {

    try {

        ProducerRecord record = new ProducerRecord<>(topic, messageKey, payload);

        kafkaSslProducer.send(record, (metadata, exception) -> {

            if (Optional.ofNullable(exception).isPresent()) {
                log.error("op={}, status=KO, desc={} and exception={}",
                        new Object[] { "KafkaProducer",
                                "Error posting message to kafka topic: " + topic,
                                exception.getMessage() });
                // Send for re-processing
            }

        });

    } catch (Exception ex) {
        log.error("op={}, status=KO, desc=Error posting message to SSL kafka: {}, stackTrace={} ", LOG_OP_INFO, ex.getMessage(), ex);
        // Re-throw the exception so that status can be recorded in the database.
    }
}
```


* In case of kafka messages, it is useful to provide a complete publish timestamp and original modify timestamp of the message (such as db record). Using these timestamps, client can determine if the incoming message is stale or a new update.

* Initially, during development, it is very useful to store the partition and offset of the consumed messages. This can be stored in the consumer data store or application logs. Using this information, the message can be directly looked up in kafka to see the original message. 