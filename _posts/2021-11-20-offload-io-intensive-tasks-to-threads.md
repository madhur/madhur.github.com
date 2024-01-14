---
layout: blog-post
title: "Offload IO Intensive tasks to worker threads"
excerpt: "Offload IO Intensive tasks to worker thread"
disqus_id: /2021/11/20/offload-io-intensive-tasks-to-threads/
tags:
    - Java
    - Spring
---

In most of the modern web REST implementations, much of the task is spent waiting on IO, for example waiting for data to be fetched from database or through remote REST service.

When the application receives high traffic on a thread based application server, such as Tomcat, much of its threads are just waiting for data to come from database or remote REST service.

This is inefficient because, you cannot increase the number of threads vertically in a single compute. Theoretically you can, but its just pure inefficient because most of those threads will be just blocked.

Thus, in order to scale such applications, the better model is to offload this waiting to pool of worker threads. This will free up the Tomcat http worker threads("http-nio-n") to recieve more incoming requests.

This can be easily achieved using [`DeferredResult`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/context/request/async/DeferredResult.html)

A typical implementation in Java / Spring looks like this:

```java
@GetMapping("/deferred")
public DeferredResult<ResponseEntity<String>> getDeferredResult() {
        CompletableFuture<String> completableFuture = deferredResultService.getDelayedResult();
        DeferredResult<ResponseEntity<String>> deferredResult = new DeferredResult<>();
        completableFuture.thenAccept(result -> {
            if (deferredResult.hasResult()) {
                return;
            }
            deferredResult.setResult(new ResponseEntity<>(result, HttpStatus.OK));
        });
        completableFuture.exceptionally(e -> {
            return null;
        });
        return deferredResult;
}
```

`DeferredResultService` instead of returning the actual result, just returns the future, whose actual implementation happens in a worker thread

If we run benchmark this API using [ab](https://httpd.apache.org/docs/2.4/programs/ab.html) by firing 100 requests concurrently, we see that it consumers only ~30 http-nio-n threads.

```
PS D:\apache\Apache24\bin> ./ab -n 100 -c 100 http://localhost:8080/deferred
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient).....done


Server Software:
Server Hostname:        localhost
Server Port:            8080

Document Path:          /deferred
Document Length:        8 bytes

Concurrency Level:      100
Time taken for tests:   20.030 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      14000 bytes
HTML transferred:       800 bytes
Requests per second:    4.99 [#/sec] (mean)
Time per request:       20029.525 [ms] (mean)
Time per request:       200.295 [ms] (mean, across all concurrent requests)
Transfer rate:          0.68 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0       1
Processing: 10008 10014   3.9  10015   10022
Waiting:    10004 10014   4.0  10015   10022
Total:      10008 10014   3.9  10015   10022

Percentage of the requests served within a certain time (ms)
  50%  10015
  66%  10016
  75%  10017
  80%  10017
  90%  10020
  95%  10021
  98%  10022
  99%  10022
 100%  10022 (longest request)
 ```

<img src='/images/threads.png'  />

Check out the demo project in my [github repository](https://github.com/madhur/deferred-result)

