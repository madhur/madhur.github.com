---
layout: blog-post
title: "id generation strategies"
excerpt: "id generation strategies"
disqus_id: /2019/08/10/id-generation-strategies/
tags:
- Design
---

In any distributed system, one of the primary probem statement every engineer faces is the id generation for an entity. In this post, we are going to look at the id generation strategies at a very high level. I wanted to have a quick reference or a cheat sheet to lookup for a problem like this:

Design considerations
* Shold the ids be sortable?
* The system should introduce as few new ‘moving parts’ as possible 
* Should the id be generated at server or database?

* Let your database handle it
  This is usually the best strategy. Because your database engine will handle any collisions etc. For MySQL, it can be autoincrement number. The con of an autoincrement number is it is susceptible to attacks. You do not want your autoincrement ids to be exposed to public in the form of Order number etc. They also don't work with sharded databases.

In case you are using, Java with Hibernate JPA, it can be configured as follows:

## Identity

The GenerationType.IDENTITY is the easiest to use but not the best one from a performance point of view. It relies on an auto-incremented database column and lets the database generate a new value with each insert operation. From a database point of view, this is very efficient because the auto-increment columns are highly optimized, and it doesn’t require any additional statements.

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
@Column(name = "id", updatable = false, nullable = false)
private Long id;
```

## Sequence
The GenerationType.SEQUENCE is my preferred way to generate primary key values and uses a database sequence to generate unique values.

It requires additional select statements to get the next value from a database sequence. But this has no performance impact for most applications. 

* Note that custom sequences are not supported by MySQL.

```java
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE)
@Column(name = "id", updatable = false, nullable = false)
private Long id;
```
## Table

The GenerationType.TABLE gets only rarely used nowadays. It simulates a sequence by storing and updating its current value in a database table which requires the use of pessimistic locks which put all transactions into a sequential order. This slows down your application, and you should, therefore, prefer the GenerationType.SEQUENCE, if your database supports sequences, which most popular databases do.


```java
@Id
@GeneratedValue(strategy = GenerationType.TABLE)
@Column(name = "id", updatable = false, nullable = false)
private Long id;
```

## UUID

UUIDs are 128-bit hexadecimal numbers that are globally unique. The chances of the same UUID getting generated twice is negligible.

The problem with UUIDs is that they are very big in size and don’t index well. When your dataset increases, the index size increases as well and the query performance takes a hit.

* If you use a timestamp as the first component of the ID, the IDs remain time-sortable

## Another component like twitter snowflake

[Twitter snowflake](https://github.com/twitter-archive/snowflake/tree/snowflake-2010) is a dedicated component just for generating ids. I am not sure if its good to have this a new component in your infrastructure.


## Conclusion
* MySQL does not support custom sequences. So if you are using mysql and want to avoid auto-increment ids, your only bet is server side.
* UUID has performance impact on indexing
* Auto-increment keys are not possible in sharded databases


### References
[Sharding & IDs at Instagram](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)