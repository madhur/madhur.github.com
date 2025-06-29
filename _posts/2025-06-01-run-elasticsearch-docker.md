---
layout: blog-post
title: "Run elasticsearch in docker"
excerpt: "Run elasticsearch in docker"
disqus_id: /2025/06/01/run-elasticsearch-docker/
tags:
    - Elasticsearch
---

If you're running Elasticsearch in Docker locally, you might encounter a frustrating issue where your cluster suddenly goes into a red (unhealthy) state, even though everything seems fine. This often happens when your local disk usage exceeds 90%.


I tend to mount the elasticsearch data directory into my host file system to preserve data.

```yaml
version: "3.9"
services:
  elasticsearch:
    image: elasticsearch:9.0.2
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
      - xpack.security.enabled=false
    volumes:
      - ./es_data:/usr/share/elasticsearch/data
    ports:
      - target: 9200
        published: 9200
    networks:
      - elastic

  kibana:
    image: kibana:9.0.2
    ports:
      - target: 5601
        published: 5601
    depends_on:
      - elasticsearch
    networks:
      - elastic      

volumes:
  es_data:
    driver: local

networks:
  elastic:
    name: elastic
    driver: bridge
```

### The Problem: Disk Space Watermarks

When your local filesystem usage exceeds 90%, Elasticsearch triggers its high watermark threshold, causing the cluster to enter a red state. This is particularly common on development machines where disk space is often limited.

### Solution: Adjusting Watermark Thresholds

If you are facing the same issue, to resolve this, run this curl command which adjusts the disk space percentage at which elasticsearch goes into unhealthy state.

```shell
curl -X PUT "localhost:9200/_cluster/settings" \
  -H 'Content-Type: application/json' \
  -d '{
    "persistent": {
      "cluster.routing.allocation.disk.watermark.low": "95%",
      "cluster.routing.allocation.disk.watermark.high": "97%",
      "cluster.routing.allocation.disk.watermark.flood_stage": "98%"
    }
  }'

```

Check your cluster health:

```shell
curl "localhost:9200/_cluster/health?pretty"
```