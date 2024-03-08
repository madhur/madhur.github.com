---
layout: blog-post
title: "Building RediSearch module in Amazon Linux 2"
excerpt: "Building RediSearch module in Amazon Linux 2"
disqus_id: /2024/03/08/building-rediSearch-module/
tags:
    - Redisearch
---

RediSearch is a [Redis](https://redis.io/) module that provides querying, secondary indexing, and full-text search for Redis. To use RediSearch, you first declare indexes on your Redis data. You can then use the RediSearch query language to query that data.

There is a very good [RediSearch getting started](https://github.com/RediSearch/redisearch-getting-started) tutorial on github.

There are several steps in bulding RediSearch module. The following steps worked on Amazon Linux 2 machine for us:

```shell
yum install git perl perl-DateTime perl-JSON perl-Capture-Tiny
git clone https://github.com/RediSearch/RediSearch.git
wget https://github.com/linux-test-project/lcov/releases/download/v2.0/lcov-2.0-1.noarch.rpm
rpm -ivh /root/lcov-2.0-1.noarch.rpm
cd RediSearch
make setup
make build

```

At this point, the module should be built at the following location 
```shell
./RediSearch/bin/linux-x64-release/search/redisearch.so
```

Copy it to `/etc/redis`

```shell
cp /root/RediSearch/bin/linux-x64-release/search/redisearch.so  /etc/redis/

```

The module can be activated in redis conf as follows:


```
loadmodule /etc/redis/redisearch.so
```