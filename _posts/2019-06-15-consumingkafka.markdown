---
layout: blog-post
title: "Consuming from Kafka"
excerpt: "Consuming from Kafka"
disqus_id: /2019/06/15/consuming-kafka/
tags:
- Kafka
- Java
---

I have been exploring on the best ways to consume from Kafka topic in Java. There are several ways:

1 The simplest way is using `KafkaListener`

{% highlight java %}
@Slf4j
@Component
public class ExampleConsumer {

    @KafkaListener(id = "fooGroup", topics = "Topic2")
    public void listen(String in) {
        log.info("Received: " + in);
        if (in.startsWith("foo")) {
            throw new RuntimeException("failed");
        }
    }
}
{% endhighlight %}

2 The second way is to use [Apache Camel](https://camel.apache.org/) . Using Apache camel is useful if you have lot of filtering logic to be applied on incoming messages and also output the processed messages onto another topic or stream.

{% highlight java %}
@Component
public class CamelListener extends RouteBuilder {

    @Autowired
    private KafkaConsumerProperties kafkaConsumerProperties;

    @Override
    public void configure() throws Exception {
        from(kafkaConsumerProperties.kafkaUri()).process(exchange -> {

            String payload = exchange.getIn().getBody(String.class);
            System.out.println("Camel consumer: " + payload);
        }).end();
    }
}
{% endhighlight %}

3 The final and my preferred way is to use [Kafka Streams](https://kafka.apache.org/documentation/streams/)

{% highlight java %}
@Service
@Slf4j
public class KafkaStreamConsumer {

    @Autowired
    private KafkaConsumerProperties kafkaConsumerProperties;

    @Autowired
    private KafkaOrderFeedProcessor kafkaOrderFeedProcessor;

    private String topic;

    @PostConstruct
    public void processKafkaConsumer() {
        Properties properties = kafkaConsumerProperties.getConsumerProperties();
        KafkaStreams kafkaStreams = null;
        try {
            StreamsBuilder builder = new StreamsBuilder();
            KStream<String, String> kStream = builder.stream(topic);
            kStream.process(kafkaOrderFeedProcessor, new String[0]);
            kafkaStreams = new KafkaStreams(builder.build(), properties);
            kafkaStreams.start();
            log.info("op={}, status=OK, desc={}", "KafkaConsumer", "kafka consumer stream  started successfully");
        } catch (Exception var9) {
            log.error("op={}, status=KO, desc={} and exception={}", new Object[]{"KafkaConsumer", "exception while starting kafka consumer stream", var9.getMessage()});
            if (kafkaStreams != null) {
                kafkaStreams.close();
            }
        }

    }
}
{% endhighlight %}

There are various advantages of using Kafka's Streams API.

Kafka's Streams API (https://kafka.apache.org/documentation/streams/) is built on top of Kafka's producer and consumer clients. It's significantly more powerful and also more expressive than the Kafka consumer client. Here are some of the features of the Kafka Streams API:

* supports exactly-once processing semantics (Kafka versions 0.11+)
* supports fault-tolerant stateful processing including streaming joins, aggregations, and windowing
* supports event-time processing as well as processing based on processing-time and ingestion-time
has first-class support for both streams and tables, which is where stream processing meets databases; in practice, most stream processing applications need both streams AND tables for implementing their respective use cases, so if a stream processing technology lacks either of the two abstractions (say, no support for tables) you are either stuck or must manually implement this functionality yourself (good luck with that...)
* supports interactive queries to expose the latest processing results to other applications and services)
* more expressive: it ships with (1) a functional programming style DSL with operations such as map, filter, reduce as well as (2) an imperative style Processor API for e.g. doing complex event processing (CEP), and (3) you can even combine the DSL and the Processor API.