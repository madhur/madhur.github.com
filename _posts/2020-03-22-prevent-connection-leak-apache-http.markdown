---
layout: blog-post
title: "Lessons learnt using Apache HTTP Connection Pooling Library"
excerpt: "Lessons learnt using Apache HTTP Connection Pooling Library"
disqus_id: /2020/03/22/prevent-connection-leak-apache-http/
tags:
- HTTP
- Java
---

Recently, I was facing an issue in production where our backend service used to get stuck while making a HTTP client request through Apache HTTP

After some debugging, I got this stack trace from the logs

```log
org.apache.http.conn.ConnectionPoolTimeoutException: Timeout waiting for connection from pool
	at org.apache.http.impl.conn.PoolingHttpClientConnectionManager.leaseConnection(PoolingHttpClientConnectionManager.java:316)
	at org.apache.http.impl.conn.PoolingHttpClientConnectionManager$1.get(PoolingHttpClientConnectionManager.java:282)
	at org.apache.http.impl.execchain.MainClientExec.execute(MainClientExec.java:190)
	at org.apache.http.impl.execchain.ProtocolExec.execute(ProtocolExec.java:186)
	at org.apache.http.impl.execchain.RetryExec.execute(RetryExec.java:89)
	at org.apache.http.impl.execchain.ServiceUnavailableRetryExec.execute(ServiceUnavailableRetryExec.java:85)
	at org.apache.http.impl.execchain.RedirectExec.execute(RedirectExec.java:110)
	at org.apache.http.impl.client.InternalHttpClient.doExecute(InternalHttpClient.java:185)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:83)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:108)
	at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:56)
```

The peculiar thing was that it was happening for only single endpoint and not any other endpoint.

We were using Apache HTTP connection pooling library and my focus shifted to that. According to [PoolingHttpClientConnectionManager](https://hc.apache.org/httpcomponents-client-ga/httpclient/apidocs/org/apache/http/impl/conn/PoolingHttpClientConnectionManager.html) documentation, it maintains a maximum limit of connection on a per route basis and in total.

We were using a simple bean configured as follows

```java
@Bean
public HttpClient httpClient()
{
    final int CONN_TIMEOUT_MS = 1000;
    final int CONN_REQUEST_TIMEOUT_MS = 60000;
    final int CONN_SOCKET_TIMEOUT_MS = 60000;
    final int CONN_POOL_DEFAULT_MAX = 40;
    final int CONN_POOL_DEFAULT_MAX_PER_ROUTE = 20;

    connectionManager
            .setDefaultMaxPerRoute(CONN_POOL_DEFAULT_MAX_PER_ROUTE);

    connectionManager.setMaxTotal(CONN_POOL_DEFAULT_MAX);

    RequestConfig requestConfig =
            RequestConfig.custom().setConnectTimeout(CONN_TIMEOUT_MS)
                    .setConnectionRequestTimeout(CONN_REQUEST_TIMEOUT_MS)
                    .setSocketTimeout(CONN_SOCKET_TIMEOUT_MS).build();
    return HttpClientBuilder.create()
            .setConnectionManager(connectionManager)
            .setDefaultRequestConfig(requestConfig).build();
}
```

After going through our code, I observed that in some cases, where response case was != 200, we weren't consuming the response
using `EntityUtils.toString(response.getEntity())` and that seemed to be the problem. This is because, we weren't interested in the response if the status code indicated a failure. However, according to Apache HTTP documentation, the response must be consumed using `EntityUtils.toString(response.getEntity())`  or `EntityUtils.consumeQuietly(response.getEntity())`. The latter can be used when the client is not interested in the response, which can be the case for failure scenarios.

## Pool Statistics

There is a way to get more interesting information about using [PoolStats](https://hc.apache.org/httpcomponents-core-ga/httpcore/apidocs/org/apache/http/pool/PoolStats.html)

As per this [stackoverflow thread](https://stackoverflow.com/questions/19112121/check-available-connections-in-poolingclientconnectionmanager), the stats of the `PoolingHttpClientConnectionManager` can be obtained through following method:

```java
private static String createHttpInfo(PoolingHttpClientConnectionManager connectionManager) {
    StringBuilder sb = new StringBuilder();
    sb.append("=========================").append("\n");
    sb.append("General Info:").append("\n");
    sb.append("-------------------------").append("\n");
    sb.append("MaxTotal: ").append(connectionManager.getMaxTotal()).append("\n");
    sb.append("DefaultMaxPerRoute: ").append(connectionManager.getDefaultMaxPerRoute()).append("\n");
    sb.append("ValidateAfterInactivity: ").append(connectionManager.getValidateAfterInactivity()).append("\n");
    sb.append("=========================").append("\n");

    PoolStats totalStats = connectionManager.getTotalStats();
    sb.append(createPoolStatsInfo("Total Stats", totalStats));

    Set<HttpRoute> routes = connectionManager.getRoutes();

    if (routes != null) {
        for (HttpRoute route : routes) {
            sb.append(createRouteInfo(connectionManager, route));
        }
    }

    return sb.toString();
}
```

I have setup a [github repository](https://github.com/madhur/apache-http-connection-pool-test), which contains the above code and some sample test cases which indicate the failure / success scenarios of Apache HTTP connection pool. Check it out at [https://github.com/madhur/apache-http-connection-pool-test](https://github.com/madhur/apache-http-connection-pool-test)