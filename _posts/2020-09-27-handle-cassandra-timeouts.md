---
layout: blog-post
title: "Handle timeouts while connecting to cassandra"
excerpt: "Handle timeouts while connecting to cassandra"
disqus_id: /2020/09/27/handle-cassandra-timeouts/
tags:
    - Cassandra
---

I have been recently playing with [Cassandra](https://cassandra.apache.org/) a lot using [Python cassandra client](https://github.com/datastax/python-driver).

One issue I saw a lot while timeouts connecting cassandra. The default timeout set in the client library is 5 seconds and it isn't very intuitive how to increase it.

```python
from cassandra.cluster import Cluster
from cassandra.cluster import ExecutionProfile
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import EXEC_PROFILE_DEFAULT

auth_provider = PlainTextAuthProvider(username='username', password='password')
profile = ExecutionProfile(request_timeout=60)
cluster = Cluster(
    ['hostnanme'],
    auth_provider=auth_provider,
    execution_profiles={EXEC_PROFILE_DEFAULT: profile},
    connect_timeout=120,
)
session = cluster.connect("database")
```

The above coode snippet increases the connect timeout and request timeout to 120 and seconds respectively.

