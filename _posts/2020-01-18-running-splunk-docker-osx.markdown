---
layout: blog-post
title: "Running splunk on docker on OSX"
excerpt: "Running splunk on docker on OSX"
disqus_id: /2020/01/18/running-splunk-docker-osx/
tags:
- Splunk
---

Recently, I tried to try out the [Splunk](https://www.splunk.com/) for log aggregation instead of [ELK stack](https://www.elastic.co/what-is/elk-stack). I wanted to see what are the advantages of it over ELK. Well, that's reserved for another post.

However, I faced an issue as soon as I start the splunk container.

```bash
homePath='/opt/splunk/var/lib/splunk/audit/db' of index=_audit on unusable filesystem. Validating databases (splunkd validatedb) failed with code '1'
```

The problem is that splunk relies on the filesystem with the locking mechanism while the OSX does not have that functionality.

The solution is to use the option `OPTIMISTIC_ABOUT_FILE_LOCKING=1` in the splunk configuration file `splunk-launch.conf`. For this, I mounted both the configuration (`/opt/splunk/etc`) and the data directory (`/opt/splunk/var`) of the splunk through the host machines. This also helps preserves configuration and data in case of docker container exits.

The following `docker-compose.yaml` works perfectly fine for testing out splunk through docker.

```yaml
version: "3.7"
services:
  splunk:
    image: splunk/splunk:7.2.6
    environment:
    - SPLUNK_START_ARGS=--accept-license
    - SPLUNK_PASSWORD=******
    volumes:
    - /log:/log    
    - ./opt-splunk-etc:/opt/splunk/etc
    - ./opt-splunk-var:/opt/splunk/var
    ports:
    - 8000:8000


  forwarder:
    image: splunk/universalforwarder:7.2.6
    environment:
    - SPLUNK_START_ARGS=--accept-license
    - SPLUNK_PASSWORD==******
    volumes:
    - /log:/log    
    ports:
    - 9997:9997
```