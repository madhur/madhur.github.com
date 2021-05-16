---
layout: blog-post
title: "Handling Distributed transactions rollback"
excerpt: "Handling Distributed transactions rollback"
disqus_id: /2021/05/016/handling-distributed-transactions-rollback/
tags:
    - Transactions
---

Distributed transactions rollback are a tough beast. There are many patterns to solve this such as:
* [Two-phase commit](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)
* [Saga pattern](https://microservices.io/patterns/data/saga.html)

In this post, we will look at one of the example of a problem and how to solve it using the Saga pattern.

Let's say, we are an e-commerce platform and building a backend service for taking and submitting orders.

A typical flow would like this:

<img src='/images/Blog/orderflow1.png'  />

Now, Just assume, what would happen if an intermittent database failure is to happen during operation no. 8, i.e. while updating the order details to database. We have already captured the payment from user's card. If the user retries the failed operation, we will end up double charging the user. Even if the user doesn't retries, we have charged the user and because of unsuccessful DB operation, the order most probably won't be fulfilled because the details are not captured itself.

This can be handled as follows:


<img src='/images/Blog/orderflow2.png'  />

In the modified flow above, what we are doing is after detecting the database failure, we are calling the payment service and canelling the charge, whatever was made before the failure. This way, even though, the overall operation failed, we havn't charged the user extra money.

Things become interesting, when you see what would happen if operation no. 10 also fails. We are in same problem again. We have failed to return the money to user card probably because payment gateway was down, or there was a service timeout etc. 

In this case, there are two approaches to solve it:

* Try to record this failed update status in DB and let a job scheduler pickup these kinds of records and do a refund to user. The FE error should indicate to the user that `There was an error while submitting order. If you are charged, you will be refunded in few minutes.`

The problem with this approach is that since the database was unavailable intermittently, this database status update also is going to result in a failure in most probability.

* The order solution is to drop a message after operation 10 into a kafka queue, where this message would be picked up by a consumer and would try to retry operation 10 after some delay. If the operation succeeds, the asynchronous notification to be sent to the user that the money has been refunded.  


<img src='/images/Blog/orderflow3.png'  />

* One of the other solution is to make the operation 10. itself asynchronous. i.e. instead of the waiting for the response, the request will be queued by PaymentService and executed later. However, in this case, the user will always needs to be shown the message `There was an error while submitting order. If you are charged, you will be refunded in few minutes.`  


<img src='/images/Blog/orderflow4.png'  />

