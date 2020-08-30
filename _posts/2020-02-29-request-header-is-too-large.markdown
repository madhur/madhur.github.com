---
layout: blog-post
title: "Solving: Request header is too large"
excerpt: "Solving: Request header is too large"
disqus_id: /2020/02/29/request-header-is-too-large/
tags:
- Tomcat
- Java
---

Recently, I faced a production issue where some of our requests were failing with the following exception


```java
org.apache.coyote.http11.Http11Processor.service Error parsing HTTP request header
 Note: further occurrences of HTTP header parsing errors will be logged at DEBUG level.
 java.lang.IllegalArgumentException: Request header is too large
    at org.apache.coyote.http11.Http11InputBuffer.parseHeaders(Http11InputBuffer.java:583)
    at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:703)
    at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:66)
    at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:790)
    at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1468)
    at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
    at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
    at java.lang.Thread.run(Thread.java:745)
```

Interestingly, the occurrence of these errors in the logs were very few but I was seeing lot of failures in our availability dashboards. That's where I observed this note in the exception:

` Note: further occurrences of HTTP header parsing errors will be logged at DEBUG level.`

The way tomcat works is that for certain type of errors such as above, it will only log the error once with the `INFO` level, and then further occurrences are logged only at the `DEBUG` level. 

This change in log level is an in memory change and hence is retained until the tomcat is restarted.

You can see that in the source code here on line 1144:  
[https://github.com/apache/tomcat/blob/7.0.x/java/org/apache/coyote/http11/AbstractHttp11Processor.java](https://github.com/apache/tomcat/blob/7.0.x/java/org/apache/coyote/http11/AbstractHttp11Processor.java)

To get this error log emitted for each event, `DEBUG` log needs to be enabled. For this add
`org.apache.coyote.level = FINE`  in `tomcat/conf/logging.properties`

## Why is this problem caused?


HTTP specification does not enforce any size limit on the size of headers. However, modern browsers and application servers such as Tomcat enforce this limit. By default 4 KB is the limit on Tomcat, which is more than enough. However, if you are adding lot of headers or using cookies extensively, this limit can be breached.

To solve this, I needed to add `maxHttpHeaderSize` in `$TOMCAT_HOME/conf/server.xml`

```xml
<Connector port="8080" maxHttpHeaderSize="65536" protocol="HTTP/1.1" ... />
```

In case, you are using Spring Boot, add the following in `application.properties`

```properties
server.max-http-header-size=65536 
```