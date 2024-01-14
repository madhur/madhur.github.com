---
layout: blog-post
title: "Create a couchbase bucket during build of the container"
excerpt: "Create a couchbase bucket during build of the container"
disqus_id: /2016/07/07/create-couchbase-bucket-docker/
tags:
- Couchbase
- Docker
---

We are using docker to automate the develop environments through [docker compose](https://docs.docker.com/compose/). We use couchbase heavily in our applications. One problem we faced is that if you boot up the [docker image of couchbase](https://hub.docker.com/r/couchbase/server/), you will have to manually perform the setup process, create buckets and so on.  Performing all of these steps manually and everytime is time consuming and not at all ideal.

I will show you how we solved this problem and automated these steps through [Dockerfile](https://docs.docker.com/engine/reference/builder/)

The key thing here is that Couchbase exposes a set of [services](http://docs.couchbase.com/admin/admin/rest-intro.html) to perform each of the operation which can be invoked just after the server start.

We are using `docker-compose` and hence our `docker-compose.yml` is as follows:


{% highlight yaml %}
version: '2'
services:
  couchbase:
    build: couchbase/
    ports:
     - 8091:8091
     - 8092:8092 
     - 8093:8093 
     - 11210:11210
{% endhighlight %}

Through `build: couchbase/`, I am pointing to a couchbase directory which contains our `Dockerfile` and a script `configure-node.sh` which invokes the REST API endpoints of couchbase.

Here is the very simplistic `Dockerfile`

{% highlight text %}
FROM couchbase:community-3.1.3

COPY configure-node.sh /opt/couchbase

CMD ["/opt/couchbase/configure-node.sh"]
{% endhighlight %}


We use the following script to configure the node.

All the files are given in this [github repo](https://github.com/madhur/couchbase-docker)

{% highlight shell %}
set -m

/entrypoint.sh couchbase-server &

sleep 60

# Setup index and memory quota
curl -v -X POST http://127.0.0.1:8091/pools/default -d memoryQuota=300 -d indexMemoryQuota=300

# Setup services
curl -v http://127.0.0.1:8091/node/controller/setupServices -d services=kv%2Cn1ql%2Cindex

# Setup credentials
curl -v http://127.0.0.1:8091/settings/web -d port=8091 -d username=Administrator -d password=password

# Load travel-sample bucket
#curl -v -u Administrator:password -X POST http://127.0.0.1:8091/sampleBuckets/install -d '["travel-sample"]'
curl -X POST -u Administrator:password -d name=default -d ramQuotaMB=100 -d authType=none -d replicaNumber=2 -d proxyPort=11215 http://127.0.0.1:8091/pools/default/buckets


curl -X POST -u Administrator:password -d name=feed -d ramQuotaMB=100 -d authType=none -d replicaNumber=2 -d proxyPort=11215 http://127.0.0.1:8091/pools/default/buckets


# Setup Memory Optimized Indexes
curl -i -u Administrator:password -X POST http://127.0.0.1:8091/settings/indexes -d 'storageMode=memory_optimized'

echo "Type: $TYPE, Master: $COUCHBASE_MASTER"

if [ "$TYPE" = "worker" ]; then
  sleep 15
  set IP=`hostname -I`
  couchbase-cli server-add --cluster=$COUCHBASE_MASTER:8091 --user Administrator --password password --server-add=$IP
  # TODO: Hack with the cuts, use jq may be better.
  #KNOWN_NODES=`curl -X POST -u Administrator:password http://$COUCHBASE_MASTER:8091/controller/addNode \
  #  -d hostname=$IP -d user=Administrator -d password=password -d services=kv,n1ql,index | cut -d: -f2 | cut -d\" -f 2 | sed -e   's/@/%40/g'`

  if [ "$AUTO_REBALANCE" = "true" ]; then
    echo "Auto Rebalance: $AUTO_REBALANCE"
    sleep 10
    couchbase-cli rebalance -c $COUCHBASE_MASTER:8091 -u Administrator -p password --server-add=$IP
    #curl -v -X POST -u Administrator:password http://$COUCHBASE_MASTER:8091/controller/rebalance --data "knownNodes=$KNOWN_NODES&ejectedNodes="
  fi;
fi;

fg 1
{% endhighlight %}


    

 