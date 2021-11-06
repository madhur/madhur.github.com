---
layout: blog-post
title: "Querying AWS ALB Logs using Athena"
excerpt: "Querying AWS ALB Logs using Athena"
disqus_id: /2021/11/06/querying-alb-logs-aws-athena/
tags:
    - AWS
    - Athena
---

Recently, I had a requirement of querying [AWS Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html#:~:text=Elastic%20Load%20Balancing%20automatically%20distributes,only%20to%20the%20healthy%20targets.) Logs to get some data around request/ sec and p95 latencies.

The Application load balancer logs are stored in [AWS S3](https://aws.amazon.com/s3/) by default and follows a consistent format which is [documented here](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html)

[AWS Athena](https://aws.amazon.com/athena/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc) is the best tool to query such logs.


## Best practices using AWS Athena

* Make sure you specify the time period when querying Athena, else the data scanned will be very huge and you will end up paying lot more.

* To find out the relevant time period to query, have a look at the [AWS Cloudwatch](https://aws.amazon.com/cloudwatch/) metrics and find intreseting patterns such as spikes in request count, response time etc 

* If your ALB has comples routing logic, make sure to specify the [Target group](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html) in the query


### Find url and times it was called within the specified time period 

```sql
SELECT request_url, count(*) as count FROM "alb_logs"."<alb_name>" where year='2021' and month='10' and day='24' and 
request_creation_time > '2021-10-24T13:37:00.000000Z' and request_creation_time < '2021-10-24T13:38:00.000000Z' group by request_url order by count desc limit 50 
```

### Find p95 Latency by url

```sql
SELECT request_url, approx_percentile(target_processing_time, 0.95)  as p95  FROM "alb_logs"."<alb_name>" where year='2021' and month='10' and day='24' and request_creation_time > '2021-10-24T13:43:00.000000Z' and request_creation_time < '2021-10-24T13:44:00.000000Z'  group by request_url order by p95 desc limit 50 
```