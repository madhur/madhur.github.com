---
layout: blog-post
title: "Parallelism and ordering"
excerpt: "Parallelism and ordering"
disqus_id: /2019/07/04/parallelism-ordering/
tags:
- Parallel
---

One of the disadvantages of microservice event based architectures is that there is lot of parallel processing of a single entity across multiple modules.
There are many cases we want the parallelism but at the same time, want the messages to be processed in ordered manner.

There are several design pattern to solve this problem:

* Kafka solves this through [partitions](http://kafka.apache.org/090/documentation.html). A topic can be split into partitions. Messages are guaranteed to be in order within a single partition. You can have multiple consumers consuming from each partition separately providing for scalability and ordering. This design assumes that each consumer is single threaded and processing the messages one after other. In practical, scenarios this is usually not the case.

* One of the solution is to use SEDA queue. [Camel](https://camel.apache.org/) has a dedicated page on [Parallelism and ordering](https://camel.apache.org/parallel-processing-and-ordering.html)

* There is whitepaper titles [A Scalable Architecture for Ordered Parallelism](https://people.csail.mit.edu/sanchez/papers/2015.swarm.micro.pdf)
  I haven't gone through it yet.

  Are there other methods to handle the ordering while processing the messages in parallel?