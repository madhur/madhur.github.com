---
layout: blog-post
title: "Designing Change Data Capture"
excerpt: "Designing Change Data Capture"
disqus_id: /2021/08/20/design-change-data-capture/
tags:
    - Design
---

Change Data Capture (CDC) is a very important topic for any backend developer to understand. Lot of systems backbone is based on Change data capture.

When I started my career as a backend developer, I did not have any understand of CDC. It is only after talking to some of the industry experts, I realized how important this topic is.

In this post, we will try to understand what is CDC and its practical usages:

> Change Data Capture is a software process that identifies and tracks changes to data in a source database. The source database can be relational or any database for that matter. CDC provides real time or near real time movement of data by moving and processing data continuously as new database events occur.

One of the example of CDC is Microsoft's Cosmos DB Change Feed

* [Change feed in Azure Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed)

* [Debezium](https://debezium.io/) is another solution which provides CDC for the databases such as MySQL


## Change data capture Methods

### Audit Columns

By using columns such as LAST_UPDATED, DATE_MODIFIED columns. The application can query the rows which have modified that changed since data was last extracted and publish into the stream.

### Trigger Based CDC

Defining database triggers that fire after INSERT, UPDATE OR DELETE commands are another method use to create a change log. Some databases have native support for triggers.

### Log based CDC

Databases support transaction logs that store all database events. With log based CDC, new database transactions are read from source database native transaction logs.

> The changes are captured without making application level changes and without having to > scan operational tables, both of which add additional workload and reduce source > systems’ performance.

## Using CDC to implement the Outbox Pattern

Content taken from https://debezium.io/blog/2020/02/10/event-sourcing-vs-cdc/

> The primary goal of the Outbox Pattern is to ensure that updates to the application  state (stored in tables) and publishing of the respective domain event is done within a  single transaction. This involves creating an Outbox table in the database to collect  those domain events as part of a transaction. Having transactional guarantees around the  domain events and their propagation via the Outbox is important for data consistency  across a system.

> After the transaction completes, the domain events are then picked up by a CDC  connector and forwarded to interested consumers using a reliable message broker (see  Figure 5). Those consumers may then use the domain events to materialize their own  aggregates (see above per Event Sourcing)

<img src='/images/Blog/cdc.png'  />