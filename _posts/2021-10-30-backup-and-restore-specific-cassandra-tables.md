---
layout: blog-post
title: "Backup and Restore specific cassandra tables"
excerpt: "Backup and Restore specific cassandra tables"
disqus_id: /2021/10/30/backup-and-restore-specific-cassandra-tables/
tags:
    - Cassandra
---

Recently, we had to make alterations directly to production cassandra tables due to an urgent bug fix and required to backup and restore specific cassandra tables so that we could roll back incase something gone wrong.

Backup and restoring tables is seamless using [nodetool](https://cassandra.apache.org/doc/latest/cassandra/tools/nodetool/nodetool.html) and [sstableloader](https://cassandra.apache.org/doc/latest/cassandra/tools/sstable/sstableloader.html)

## Cassandra table backup steps

 
* Login to Casandra Box  
* Execute the following commands from the cassandra bin directory


```
   ./nodetool snapshot -cf <tablename> <keyspace>
```
   
* Repeat the same for any other table to be backed up


* This will create snapshots in the data directory at following locations:

```
  cassandra/data/data/<keyspace>/<table>-<UID>/snapshots/<epoch>
```


## Cassandra table restore steps


* Login to cassandra box  
* Navigate to following folder

```
  cassandra/data/data/f<keyspace>/<table>-<UID>
```
Execute following command

```
  cp snapshots/<epoch>/*.* .
```

* Repeat the same for any other table to be restored

* Once all the snapshots have been copied to data directory, run following commands in sequence:

```
  ./nodetool refresh <keyspace> <table>;
```