---
layout: blog-post
title: "Block Storage vs Object Storage"
excerpt: "Block Storage vs Object Storage"
disqus_id: /2026/04/01/block-storage-vs-object-storage/
tags:
    - Design
---

In this article, we will look at [Block Storage](https://aws.amazon.com/what-is/block-storage/) and [Object Storage](https://aws.amazon.com/what-is/object-storage/) and differences between them.

### Block Storage

Block storage consists of Block servers whose responsibility is to take a file, split it into blocks, then optionally compress and encrypt it and then finally store it into actual storage.

One of the advantage Block servers provide is Delta sync. When a file is modified, only modified blocks are synced instead of the whole file using a sync algorithm.

Block servers process filed passed from clients by splitting a file into blocks, compressing each block, and encrypting them. 

Question-> How do they determine which blocks are modified?

> Frequent modification
> Block storage supports frequent data writes without affecting performance. Instead of rewriting > the entire file, the system identifies the particular block that needs to be amended. Then, it rewrites the selected block with the new data. This makes block storage very efficient for managing large files that require frequent updates.

Example of block storage is [Amazon EBS](https://aws.amazon.com/ebs/)

Block storage gives the flexibility of storing frequent data on SSD while non-frequent data on HDD.

### How does it work?

Block servers process files passed from clients by splitting a file into blocks, compress each block and encrypting them. Instead of uploading the whole file to the storage system, only modified blocks are transferred.


The advantage of it is that in version history, you need not store the entire file. Only modified blocks.

Block storage offers high performance, low latency, and quick data transfer rates. As it operates on a block level, you can directly access data and achieve a high I/O performance. You use block storage for applications that need fast access to data you have stored, like a virtual machine or database. 


### Object Storage

Object storage is different from Block storage

Object storage systems prioritize storage quantity over availability. As highly scalable systems, you can store large volume of unstructured data in an object storage system. However, there’s more latency when you access these files. Object storage also has a lower throughput compared to block storage and cloud storage. 



Example of object storage is [Amazon s3](https://aws.amazon.com/s3/)

### Block Storage vs Object Storage

Block storage is mainly useful for structured data with high volumes of read and write loads.

Th key here is that in these files, mostly you don't need the entire file in its entirety, but only the part of it. For example few rows of database, few files inside the VM mount etc.

Block Storage is like having a filing cabinet with lots of small, numbered drawers. Perfect when you neet to quickly grab a specific drawer.

Object storage is best used for large amouts of unstructured data.

In object storage, you typically need the whole file to operate. for example Images, Videos, PDF, backups etc.

Object Storage is like having a warehouse with labeled boxes. Perfect when you need to retrieve entire boxes (complete files)


References:
https://aws.amazon.com/compare/the-difference-between-block-file-object-storage/
