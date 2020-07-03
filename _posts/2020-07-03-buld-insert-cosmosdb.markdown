---
layout: blog-post
title: "Bulk insertion of Rows in CosmosDB"
excerpt: "Bulk insertion of Rows in CosmosDB"
disqus_id: /2020/07/03/bulk-insert-cosmosdb/
tags:
    - Java
    - CosmosDB
---

Recently, I have been involved in an effort which required migrating a database with millions of rows from [MySQL](https://www.mysql.com/) to [Azure CosmosDB](https://azure.microsoft.com/en-us/services/cosmos-db/). Those who are new to CosmosDB, it is a Microsoft's globally distributed, multi-model database service. The good thing about CosmosDB is that it provides data access using the familiar API's in form of SQL, MongoDB, Cassandra etc.

We used the MongoDB driver for our use-case, so essentially it was a RDBMS to NOSQL migration.

In this post, we are going to look at the best ways to insert the data in Azure CosmosDB in bulk in fastest amount of time.

We primarily used Spring data MongoDB. For ex, we have a simple entity as follows:


```java
@Data
public class Event {
    private String _id;
    private Integer schemaVersion = 0;
    private String eventId;
    private Date createdAt;
}
```    

The simplest way to insert batch of these entities into MongoDb is by using  [Bulk APIs]()

```java
public void writeRecords(List<Event> eventsList) {
    BulkOperations bulkOps = mongoTemplate.bulkOps(BulkOperations.BulkMode.UNORDERED, Event.class);
    eventsList.forEach(record -> {
        bulkOps.insert(record);
    });
    BulkWriteResult result = bulkOps.execute();
}
```

The line `bulkOps.execute()` will be a blocking call and will return only after all the rows has been inserted. One point to note here is that parameter `BulkOperations.BulkMode.UNORDERED` will allow the processing to continue even in case of errors (such as `DuplicateKeyException`),. Use the `BulkOperations.BulkMode.ORDERED` if you want the processing to stop.

I wouldn't recommend using `BulkMode.UNORDERED` especially if you are dealing with transactional data.

Even with `BulkMode.ORDERED`, there can be other failures duing this batch insertion for ex, network blips, server crashes etc. Thus, this approach is fine if we are bulk inserting thousands of rows (which would probably take a second or two). However, for inserting millions of records, it is best idea to batch this process using [Spring Batch](https://spring.io/projects/spring-batch) or a custom batching logic. The idea is that you want to be able to resume the insertion in an event of the failure. How the failure is handled totally depends on the type of failure occurred.

One might note that, [Spring Data](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#reference) provides the `saveAll()` method, so why not use that and do an insertion like this:

```java
public void writeRecords(List<Event> eventsList)  {
    List<List<Event>> partitionedList = Lists.partition(eventsList, DEFAULT_BATCH_SIZE);
    for (List<Event> events : partitionedList) {
        eventRepository.saveAll(events);
    }
}
```

That was an interesting question and I had to dig into the source code of [spring-data-mongodb](https://github.com/spring-projects/spring-data-mongodb) to get this answer.  

Turns out, as of spring-data-mongodb 3.0, Spring will automatically use the MongoDB's bulk insertion API's to perform the persistence of records using `saveAll()`.  

However, there is one catch. The `_id` field of these entities must be null, i.e. you'll have to let the MongoDB generate the `_id` field for you.  

In cases, such as migration, wherein we might want to provide our own value of `_id`, Spring wil resort to one by one insertion and that will be very slow compared to Bulk API's.


