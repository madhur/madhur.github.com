---
layout: blog-post
title: "Redis Node moving out of cluster repeatedly"
excerpt: "Redis Node moving out of cluster repeatedly"
disqus_id: /2022/05/15/redis-node-moving-out-cluster-repeatedly/
tags:    
    - Redis
---

Recently, we noticed a production issue where some of the redis slave nodes were repeatedly being kicked out of the cluster. This was interesting since that redis cluster had been running without any issues for almost 3  years.

The logs were repeatedly filled with slave trying to get full sync from master nodes again and again.

```
# Connection with master lost.
* Caching the disconnected master state.
* Connecting to MASTER x.x.x.x:6379
* MASTER <-> SLAVE sync started
* Non blocking connect for SYNC fired the event.
* Master replied to PING, replication can continue...
* Trying a partial resynchronization (request 7cbefe20e13fffe4deddc4191479e95a2e9c39e5:2723884887862).
* Full resync from master: 7cbefe20e13fffe4deddc4191479e95a2e9c39e5:2724002738232
* Discarding previously cached master state.
* MASTER <-> SLAVE sync: receiving 1438631551 bytes from master
# I/O error trying to sync with MASTER: connection lost
* Connecting to MASTER x.x.x.x:6379
* MASTER <-> SLAVE sync started
* Non blocking connect for SYNC fired the event.
* Master replied to PING, replication can continue...
* Partial resynchronization not possible (no cached master)
* Full resync from master: 7cbefe20e13fffe4deddc4191479e95a2e9c39e5:2724138480914
* MASTER <-> SLAVE sync: receiving 1439249094 bytes from master
# I/O error trying to sync with MASTER: connection lost
* Connecting to MASTER x.x.x.x:6379
* MASTER <-> SLAVE sync started
* Non blocking connect for SYNC fired the event.
* Master replied to PING, replication can continue...
* FAIL message received from 485f5d069279fe4690faa4e92a121d85c894050e about 680a7c6ae885094d806206522ce639e3527e9dbf
# Cluster state changed: fail
* Partial resynchronization not possible (no cached master)
* Full resync from master: 7cbefe20e13fffe4deddc4191479e95a2e9c39e5:2724269765637
# Cluster state changed: ok
* Clear FAIL state for node 680a7c6ae885094d806206522ce639e3527e9dbf: master without slots is reachable again.
* MASTER <-> SLAVE sync: receiving 1440022343 bytes from master
# I/O error trying to sync with MASTER: connection lost
* Connecting to MASTER x.x.x.x:6379
* MASTER <-> SLAVE sync started
* Non blocking connect for SYNC fired the event.
* Master replied to PING, replication can continue...
* Partial resynchronization not possible (no cached master)
* Full resync from master: 7cbefe20e13fffe4deddc4191479e95a2e9c39e5:2724405468825
* MASTER <-> SLAVE sync: receiving 1440902610 bytes from master
# I/O error trying to sync with MASTER: connection lost
```


The offending nodes had lower `client-output-buffer-limit` value (256mb) which caused the replication process to go into infinite loop. The reason for this is documented in 
[Redis blog: The Endless Redis Replication Loop: What, Why and How to Solve It](https://redis.com/blog/the-endless-redis-replication-loop-what-why-and-how-to-solve-it/)


We bumped up the value to recommended 512mb value and problem went away.

The question is, why did the slave disconnect from the master in the first place?

Well, that will be covered in the next post.