---
layout: blog-post
title: "Different HTTP Timeouts in HTTP Client"
excerpt: "Different HTTP Timeouts in HTTP Client"
disqus_id: /2020/05/16/http-timeouts/
date: 2020-05-16 00:00:00
tags:
    - Java
    - HTTP
---

In a well designed backend application, which makes calls to other HTTP services, it is very important to configure appropriate timeout values. In event of a service failure, a large timeout value can cause threads on the application to keep waiting for service to respond and may ultimately run out of threads which could have been used for doing other work. Otherwise, low timeout value can cause genuine requests to be aborted which would have been responded.

First of all, it is very important which are the different types of timeouts which can be configured from the aspect of a HTTP client.

### Connection Timeout

A connect timeout is the period between which the connection between a client and a server must be established. It includes the time for DNS resolution, and setup a TCP connection including the handshake. This is a client setting because it's the client which will initiate the connection.

`http.connection.timeout` - the default value is zero, which means infinite.

### Request Timeout

This is the time, during which a request must be completed after the connection has been made. It includes the time for the client to send the request, and also the server to respond. If the client doesn't send the request, the request can time out.

Note that this is a server side setting. This is because, server wouldn't want to keep the connection (and ultimately a thread) waiting indefinitely for the client to request.

One must think that this should be a client setting as well, what if the server takes too much time to respond. Correct. There is a similar setting on client as well, which is usually called, Socket Timeout, but it is not exactly same as Request TimeOut

### Socket Timeout

This is a maximum time between two data packets to arrive. This is a client side setting. Some people confuse this with RequestTimeout on the client side. It is only a timeout between two packets. If we set this value to 5 seconds, it can still take the entire request to take lets say 15 seconds given that the time period between two consecutive packets was always < 5 seconds.

`http.socket.timeout` - The default value is zero, which means infinite.

### Connection Request TimeOut

This is applicable if you are using connection pooling on the client. This Timeout setting defines the maximum time during which a connection must be obtained from the pool.

The below code snippet shows how to set the various client timeout settings on the Apache HTTP Client.

```java
    public HttpClient retryHttpClient() {

        RequestConfig requestConfig = RequestConfig.custom()
                .setConnectTimeout(CONN_TIMEOUT_MS)
                .setConnectionRequestTimeout(CONN_REQUEST_TIMEOUT_MS)
                .setSocketTimeout(CONN_SOCKET_TIMEOUT_MS).build();

        return HttpClientBuilder.create()
                .setConnectionManager(connectionManager)
                .setDefaultRequestConfig(requestConfig)
                .build();
    }
```
