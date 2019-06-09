---
layout: blog-post
title: "Using SEDA"
excerpt: "Using SEDA"
disqus_id: /2019/06/09/staged-events/
tags:
- SEDA
- Java
---

The [staged event-driven architecture (SEDA)](https://en.wikipedia.org/wiki/Staged_event-driven_architecture) refers to an approach to software architecture that decomposes a complex, event-driven application into a set of stages connected by queues. It avoids the high overhead associated with thread-based concurrency models (i.e. locking, unlocking, and polling for locks), and decouples event and thread scheduling from application logic. 

For Java platform, [Apache Camel](http://camel.apache.org/) provides support for [SEDA component](https://camel.apache.org/seda.html)

These are some of the important properties of SEDA:

* `size`: Size of the queue. By default, its unbounded

* `concurrentconsumers`: By default only one thread will be consuming from the queue

* `blockWhenFull` : If the queue is full, the thread can be blocked. By default, an exception is thrown. In most scenario, you would want the thread to block.

Now, onto some code:

Below is an example of simple producer component:

{% highlight java %}
@SpringBootApplication
@RestController
@Slf4j
@ComponentScan()
public class SedaApplication {

    public static void main(String[] args) {
        SpringApplication.run(SedaApplication.class, args);
    }

    @Autowired
    private ProducerTemplate producerTemplate;

    @Autowired
    private CamelContext camelContext;

    @RequestMapping("/send/{message}")
    public String sendMessage(@PathVariable String message) throws Exception {
        producerTemplate.sendBody("seda:start?size=10&blockWhenFull=false", message);
        System.out.println("Producing message: " + message);
        SedaEndpoint sedaEndpoint = (SedaEndpoint) camelContext.getEndpoint("seda:start");
        System.out.println("Remaining capacity : " + sedaEndpoint.getQueue().remainingCapacity());
        return "";
    }
}
{% endhighlight %}

And the consumer:

{% highlight java %}
@Component
@Slf4j
public class TestRouter extends RouteBuilder {

    @Override
    public void configure() throws Exception {
        from("seda:start?size=10").process(exchange -> {
            System.out.println("Consumed message: " + exchange.getIn().getBody());
        }).end();
    }
}
{% endhighlight %}

Here is the link to complete [github repository](https://github.com/madhur/camel-example)