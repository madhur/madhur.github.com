---
layout: blog-post
title: "API Response Group Pattern - Improving latencies using GraphQL"
excerpt: "API Response Group Pattern - Improving latencies using GraphQL"
disqus_id: /2021/06/13/api-response-group-pattern/
tags:
    - Design
    - GraphQL
---

In a complex multiple microservices architecture, especially where in one microservice ends up calling a chain of other microservices, the API latency can become a concern.

This is because there is network hop at each microservice layer, which adds to the latency in addition to the actual logic executed by the microservice itself.

For example, in an e-commerce application, an Add to Cart API request might end up calling multiple downstream microservices such as Pricing Service, Availability Service etc.

In a complex architecture, where multiple clients are involved such as Mobile Apps and web browsers, the data needed by clients can differ depending upon the situation.

For example, if the user is adding an item to cart from the homepage, the client might not need pricing details as it might have that data already cached.

In other scenario, if the user is just increasing the quantity of the item, there might not be need to call the availability service as the front end might have called it when user initially called it 
and front end could cache the availability data of the item for some time (lets say 15 minutes).

To achieve the best API performance, it is important to recognize these patterns and incorporate into the API design. 

So instead of creating a separate API for each of these use cases, its better incorporate this by using
the *Response Group Pattern*

For example, in our hypothetical case, we might come up with following response groups:

| Response Group | Pricing Service | Seller Service | Asset Service |
|----------------|-----------------|----------------|---------------|
| full           | ✓               | ✓              | ✓             |
| basic          | ✓               | x              | x             |
| summary        | x               | ✓              | x             |


<br/>
As shown above, we don't want to call Seller and Asset service when addToCart is invoked with response group basic, for example

```text
/addToCart?responseGroup=basic

/addToCart?responseGroup=full

/addToCart?responseGroup=summary
```

The next problem to solve is, who will send this response group.

In ideal situation, the client should not be worried about the response group, hardcoding these response group at the client side is maintainence nightmare and possible bugs. As the feature evolve, the client would have to worry about the appropriate response group to call all the time.

That's where [GraphQL](https://graphql.org/) comes into the picture. The client should just pass the fields it requires to a GraphQL service, call the appropriate [mutation](https://graphql.org/learn/queries/) and graphQL layer should have logic to determine the response and pass it to backend service.

In nutshell, that's how our architecture looks like:  


<a href="/images/Blog/responsegroup.png"><img src='/images/Blog/responsegroup.png' width="825px" height="428px"/></a>