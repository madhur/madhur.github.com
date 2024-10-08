---
layout: blog-post
title: "s3cmd Fast way to copy s3 data"
excerpt: "s3cmd Fast way to copy s3 data"
disqus_id: /2024/10/05/s5cmd-fastest-way-to-copy-s3-data/
tags:
    - s5cmd
    - S3
---

If you are looking to copy huge amount of data to/from [AWS S3](https://aws.amazon.com/s3/)


Look no further than [s5cmd](https://github.com/peak/s5cmd)


Download the entire s3 bucket to local

```
s5cmd cp  s3://bucket/ .
```


I was able to download almost 10 GB folder in couple of minutes, which is around 83MBps ~ 10 MB/s

Whereas `aws s3 cp --recursive  s3://bucket/ .` was giving me around 500 KB/s




