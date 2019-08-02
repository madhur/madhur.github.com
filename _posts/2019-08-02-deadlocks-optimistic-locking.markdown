---
layout: blog-post
title: "Deadlocks in Optimistic locking"
excerpt: "Deadlocks in Optimistic locking"
disqus_id: /2019/08/02/deadlocks-optimistic-locking/
tags:
- Deadlocks
- Oracle
---

Recently, our application has been generating lot of deadlocks in Oracle database. The application uses [Optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)

`Error: ORA-00060: deadlock detected while waiting for resource`

In an optimistic concurrency control, transactions use data resources without acquiring locks on the resources. Before committing, each transaction verifies that no other transaction has modified the data it has read. If the check reveals conflicting modifications, the committing transaction rolls back and can be restarted.

Which begs the questions, why should there be a deadlock at all in optimistic concurrency control?

The keypoint to understand here first is that Optimistic locking is not a feature provided by DBMS engine. Databases just provide mechanism to initiate transactions, rollbacks, versioning and locks. Ultiamtely, it is upto the application to implement eithe optimisitc locking or pessimistic locking.

An example of implementing optimistic locking is as follows:

```sql
SELECT address_line1, city, state, zip, version
  FROM addressTable
 WHERE address_id = `<<some key>>`
 ```

 When you are about to do the update, you use the version in your update and throw an error if the row changed:

```sql
 UPDATE addressTable
   SET address_line1 = `<<new address line 1>>`,
       city = `<<new city>>`,
       state = `<<new state>>`,
       zip = `<<new zip>>`,
       version = version + 1
 WHERE address_id = `<<some key>>`
   AND version = `<<version you read initially>>`

IF( SQL%ROWCOUNT = 0 )
THEN
  RAISE_APPLICATION_ERROR( -20001, 'Oops, the row has changed since you read it.' );
END IF;
```

However, it is possible for a deadlock to occur in oracle, because of the way transactions are implemented in database engines. 

```sql
BEGIN;    -- in one connection
UPDATE thing_1;
UPDATE thing_2;
COMMIT;

BEGIN;    -- in another connection, at the "exact same time"
UPDATE thing_2;
UPDATE thing_1;
COMMIT;
```

This is the classic example of a deadlock 

After a few seconds, Oracle will detect the deadlock and pick one of the sessions and ‘rollback’ the statement. This is where we see our first misunderstanding about deadlocks.

* Oracle does not kill the session.
* Oracle does not kill the transaction.
* Oracle only kills the statement.
* Oracle does rollback the failing statement, but Oracle does not rollback the entire transaction that the failing statement is part of. (Correction by Mark Bobak.)
PMON (Process Monitor) does not clear out the locks.

It is the responsibility of the session that detects the “ORA-00060 deadlock detected while waiting for resource” error to trap and handle the error by issuing a rollback (or a commit) command. Only once this has been done will the other session be able to continue.