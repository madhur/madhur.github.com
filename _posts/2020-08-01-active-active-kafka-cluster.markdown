---
layout: blog-post
title: "Overview of Active-Active Kafka Cluster using MirrorMaker 2.0"
excerpt: "Overview of Active-Active Kafka Cluster using MirrorMaker 2.0"
disqus_id: /2020/08/01/active-active-kafka-cluster/
tags:
    - Kafka
---

In order to make our application, highly available and fault tolerant, I have been researching a lot on best disaster recovery strategy for Kafka.

In earlier relational systems, such as MySQL or Oracle, it was standard to have an active-passive cluster where in the application does
reads and writes to a primary cluster. This primary cluster is asynchronously replicated to a secondary cluster. The application falls back to the secondary cluster incase the primary cluster fails.

The fall back can be automatic or manual. Database vendors such as [Postgres](https://www.postgresql.org/docs/9.6/warm-standby-failover.html), [Oracle](https://docs.oracle.com/cd/B28359_01/server.111/b28295/sofo.htm#:~:text=An%20Oracle%20database%20operates%20in,two%20roles%3A%20primary%20or%20standby.&text=A%20failover%20is%20done%20when,take%20over%20the%20primary%20role.) and [MariaDB](https://mariadb.com/kb/en/mariadb-maxscale-22-automatic-failover-with-mariadb-monitor/) have built products to automate the failover.

Newer distributed applications, such as NoSQL databases like Cassandra prefer an active-active approach. This because these databases might not require very high consistency.

Recently, Kafka has also adopted this approach using [MirrorMaker](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=27846330)

## What is Mirror Maker

In simple terms, Mirror Maker allows you to mirror a Kafka cluster to another cluster. All topics, partitions and messages are replicated. Any changes in source, like addition / deletion of topics, messages will be mirrored to destination. Mirror Makes allows Kafka users to setup an active-passive cluster where in an active cluster is continuously mirroring the data to secondary cluster.

## What is the problem ?

All is good uptil now, until we realize that huge amount of infrastructure and network bandwidth is being wasted to maintain this active-passive cluster, wherein the passive cluster will come in use only when active goes down.
Not to mention that large Kafka deployments process millions of messages per sec and all that data needs to be replicated to destination cluster.

### Solution - Mirror Maker 2.0

Kafka team has recently launched a new version of Mirror Maker 2.0, which allows you to setup a bi-directional mirror between two clusters. This solves the problem of wasted network infrastructure of secondary cluster which would have come in use only if primary cluster had gone down.

So, how does this work? In simple terms, Mirror Maker 2.0 does bi-directional mirroring, i.e. data from primary cluster will be mirrored to secondary cluster and data from secondary cluster will be mirrored to primary cluster.

If you logically think of this approach, this can result in an infinite loop, where in a message can be continuously mirrored between two clusters.

To solves, this problem, Mirror Maker allows topic renaming to eliminate the above problem. Let me illustrate how:


Let's say, We have two DC's DC1 and DC2, with topics T1 and T2.

Producer in DC1 produces message M1 in topic T1 and M2 in topic T2

Producer in DC2 produces message M3 in topic T1 and M4 in topic T2

Note that these two are completely different clusters with zookeepers of their own and hence topics T1 and T2 are local to their clusters.

What Mirror maker will do is, it will create topic T1.DC2 and T2.DC2 in DC1, which will contain the replicated data from topics T1 and T2 of DC2

Similarly, in DC2, topics T1.DC1 and T2.DC1 will be created which will contain the replicated data from topics T1 and T2 of DC1



                                                                                                                                                                                
           DC1                                                                                                                                                                                                    
                                                                                          DC2                                                                                                                     
                                                                                                                                                                                                                  
    +-------------------+                                                                                                                                                                                         
    |                   |                                                           +-------------------+                                                                                                         
    |                   |                                                           |                   |                                                                                                         
    |    PRODUCER       |                                                           |    PRODUCER       |                                                                                                         
    |                   |                                                           |                   |                                                                                                         
    +-------------------+                                                           +-------------------+                                                                                                         
                                                                                                                                                                                                                  
    PRODUCES M1 IN TOPIC T1 AND M2 IN TOPIC T2                                      PRODUCES M3 IN TOPIC T1 AND M4 IN TOPIC T2                                                                                    
                                                                                                                                                                                                                  
    +-------------------------------------+                                         +----------------------------------+                                                                                          
    |  Topic T1         M1                |---------------------------------------> | Topic T1.DC1      M1             |                                                                                          
    +-------------------------------------+                                         +----------------------------------+                                                                                          
                                                                                                                                                                                                                  
    +-------------------------------------+                                         +----------------------------------+                                                                                          
    |  Topic T1.DC2      M3               | <-------------------------------------- | Topic T1         M3              |                                                                                          
    +-------------------------------------+                                         +----------------------------------+                                                                                          
                                                          MIRROR MAKER                                                                                                                                            
    +-------------------------------------+                                         +----------------------------------+                                                                                          
    | Topic T2          M2                |---------------------------------------> | Topic T2.DC1     M2              |                                                                                          
    +-------------------------------------+                                         +----------------------------------+                                                                                          
                                                                                                                                                                                                                  
    +-------------------------------------+                                         +----------------------------------+                                                                                          
    | Topic T2.DC2       M4               | <---------------------------------------  Topic T2          M4             |                                                                                          
    +-------------------------------------+                                         +----------------------------------+                                                                                          
                                                                                                                                                                                                                  



In this case, the full network cluster bandwidth is utilized. The producers can load balance their traffic to two clusters either using round robin or local affinity.

The consumer in DC1 will have to subscribe to the data from both T1 and T1.DC2. This can be done easily using wild card subscription which is supported in most frameworks such as Spring as shown below:

```java
@KafkaListener(id = "xxx", topicPattern = "kbgh.*")
public void listen(String in) {
    System.out.println(in);
}
```


Even if one DC goes down, the entire data is available in other cluster.