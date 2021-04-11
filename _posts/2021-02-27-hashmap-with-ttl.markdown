---
layout: blog-post
title: "HashMap with TTL"
excerpt: "HashMap with TTL"
disqus_id: /2021/02/27/hashmap-with-ttl/
tags:
    - Java
---

We were working on a proof of concept and for that I quickly needed a HashMap with a Time to Live (TTL). Basically, I wanted the keys to expire automatically after a certain time period.

Fortunatly, [Google Guava](https://github.com/google/guava) provides this out of the box in form of [LoadingCache](https://guava.dev/releases/19.0/api/docs/com/google/common/cache/LoadingCache.html)

Here is how you would initialize it,

```java
private LoadingCache<String, String> cache = CacheBuilder.newBuilder()
            .maximumSize(Integer.MAX_VALUE)
            .expireAfterWrite(5, TimeUnit.MINUTES)
            .build(new CacheLoader<String, String>() {
                @Override
                public String load(final String response) throws Exception {
                    return response;
                }
            });
```

You can specify the maximum size of cache, after which the entries will be automatically evicted according to Least Recently Used (LRU) algorithm.

The TTL can be specified using [`expireAfterWrite`](https://guava.dev/releases/19.0/api/docs/com/google/common/cache/CacheBuilder.html#expireAfterWrite(long,%20java.util.concurrent.TimeUnit)) method.

Note that when using this implementation, do not rely on the `size()` property of the map since that might contain the expired entries as well. However, they will not be retrievable using the `get` method.

The expired entires are removed after a certain time duration using a routine maintainence job.

