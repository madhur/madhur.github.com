---
layout: blog-post
title: "Row level locking in database"
excerpt: "Row level locking in database"
disqus_id: /2025/07/09/row-level-locking-database/
tags:
    - Database
---


Quick refereshers on how locks are implemented in databases.

* Exclusive Locks - The row is locked for read and update. Until the exclusive lock is released, no reads and writes are allowed. Only one transaction can acquire an exclusive lock.

* Shared Lock - The row is locked for update. However, readers are allowed to read. Multiple transactions are allowed to acquire shared locks.

Major points
* If the transaction has shared lock on resource, other transaction cannot acquire exclusive lock on it.

* A process cannot acquire a shared lock on a resource that is locked by an exclusive lock.


### Optimistic vs Pessimistic Locking

* Optimistic - Let multiple transactions be allowed to update the row concurrently. One one will succeed and others will fail.

* Pessimistic - Only one transaction is allowed to update the row. Others are put to wait.

### Transaction Isolation

What happens when a transaction tries to read a row updated by another transaction?

Problems when transaction isolation is not done

* Dirty Read — Let’s take a situation where one transaction updates a row or a table but does not commit the changes. If the database lets another transaction read those changes (before it’s committed) then it’s called a dirty read. Why? Let’s say the first transaction rolls back its changes. The other transaction which read the row/table has stale data.


* Non-repeatable read — Another side effect of concurrent execution of transactions is that consecutive reads can retrieve different results if you allow another transaction to do updates in between

* Phantom read — In a similar situation as above, if one transaction does two reads of the same query, but another transaction inserts or deletes new rows leading to a change in the number of rows retrieved by the first transaction in its second read, it’s called a Phantom read.


### Levels of Isolation

* Read uncomitted - This level of isolation lets other transactions read data that was not committed to the database by other transactions.

* Read committed — This, as the name suggests, lets other transactions only read data that is committed to the database. While this looks like an ideal level of isolation, it only solves the dirty read problem mentioned above. If a transaction is updating a row, and another transaction tries to access it, it won’t be able to. But this can still cause non-repeatable and phantom reads because this applies only to updates and not read queries.

* Repeatable read - To counter the transactions from getting inconsistent data, we need a higher level of isolation and that is offered by repeatable read. In this, the resource is locked throughout the transaction. So, if the transaction contains two select queries and in between, if another transaction tries to update the same rows, it would be blocked from doing so. This isolation level is not immune to phantom reads though it helps against non-repeatable reads. This is the default level of isolation in many databases.

* Serializable — This is the highest level of isolation. In this, all concurrent transactions “appear” to be executed serially. Pay attention to how I said it appears to be. That’s because it’s not truly serially or sequentially executed. This level works against phantom reads as well.

### References
https://medium.com/inspiredbrilliance/what-are-database-locks-1aff9117c290

