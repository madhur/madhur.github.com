---
layout: blog-post
title: "Quickly Compare two MySQL databases"
excerpt: "Quickly Compare two MySQL databases"
disqus_id: /2022/01/16/quickly-compare-two-mysql-databases/
tags:
    - MySQL
---

A very nifty and quick way to compare two mysql databases is to use `mysqldump` command. This also works well if you just want to compare DDL

```
mysqldump -d --skip-comments --skip-extended-insert -u root -p -h mysql.host db1  > db1.sql   
mysqldump -d --skip-comments --skip-extended-insert -u root -p -h mysql.host db2 > db2.sql   
diff db1.sql db2.sql
```