---
layout: blog-post
title: "A nifty Apache Benchmark alternative - hey"
excerpt: "A nifty Apache Benchmark alternative - hey"
disqus_id: /2023/02/23/apache-benchmark-alternative-hey/
tags:
    - ab
    - hey
---


If you have been reading my posts, I am a big fan of [Apache Benchmark](https://httpd.apache.org/docs/2.4/programs/ab.html)


Apache benchmark allows you to quickly run a small load test on a single machine.

You can specify various options like number of request and the concurrency of those requests.

For example, I can send 10 million requests with a concurrency of 1000 as follows:

```
ab -n 10000000 -c 1000 "http://localhost:8080"  
```


Once the ab is finished benchmarking:


```text
Server Software:        
Server Hostname:        localhost
Server Port:            8080

Document Path:          /
Document Length:        53 bytes

Concurrency Level:      1000
Time taken for tests:   332.363 seconds
Complete requests:      10000000
Failed requests:        4301677
   (Connect: 0, Receive: 0, Length: 4301677, Exceptions: 0)
Total transferred:      1621642574 bytes
HTML transferred:       571642574 bytes
Requests per second:    30087.60 [#/sec] (mean)
Time per request:       33.236 [ms] (mean)
Time per request:       0.033 [ms] (mean, across all concurrent requests)
Transfer rate:          4764.78 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   15  21.8     14    1047
Processing:     0   18   3.9     17      53
Waiting:        0   13   3.2     12      41
Total:          1   33  22.2     32    1076

Percentage of the requests served within a certain time (ms)
  50%     32
  66%     34
  75%     35
  80%     36
  90%     39
  95%     42
  98%     46
  99%     49
 100%   1076 (longest request)
```

One of the things missing in ab is the ability to send requests at a specified requests/seconds

The ability to specify requests/seconds is very useful when testing for things such as cache evictions etc

That is when I stumbled upon [hey](https://github.com/rakyll/hey)

[hey](https://github.com/rakyll/hey) is a dropin replacement for [ab](https://httpd.apache.org/docs/2.4/programs/ab.html) with the ability to specify requests/seconds

For example, If I want to run the load for one minute at 100 requests/seconds, I can sepcify

```
hey -z 1m -q 2 "http://localhost:8080/"
```

Here the `q` parameter specifies the requests per second per worker. The default number of workers are 50 (can be overriden via -c parameter)

I also like the way the results are presented


```
Summary:
  Total:	60.0033 secs
  Slowest:	0.3025 secs
  Fastest:	0.0001 secs
  Average:	0.0033 secs
  Requests/sec:	99.9945
  

Response time histogram:
  0.000 [1]	|
  0.030 [5949]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.061 [0]	|
  0.091 [0]	|
  0.121 [0]	|
  0.151 [0]	|
  0.182 [0]	|
  0.212 [0]	|
  0.242 [0]	|
  0.272 [0]	|
  0.303 [50]	|


Latency distribution:
  10% in 0.0005 secs
  25% in 0.0006 secs
  50% in 0.0008 secs
  75% in 0.0010 secs
  90% in 0.0012 secs
  95% in 0.0013 secs
  99% in 0.0016 secs

Details (average, fastest, slowest):
  DNS+dialup:	0.0000 secs, 0.0001 secs, 0.3025 secs
  DNS-lookup:	0.0000 secs, 0.0000 secs, 0.0013 secs
  req write:	0.0000 secs, 0.0000 secs, 0.0008 secs
  resp wait:	0.0032 secs, 0.0001 secs, 0.3013 secs
  resp read:	0.0000 secs, 0.0000 secs, 0.0011 secs

Status code distribution:
  [202]	6000 responses
```