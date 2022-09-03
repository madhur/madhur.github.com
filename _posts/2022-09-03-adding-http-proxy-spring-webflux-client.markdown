---
layout: blog-post
title: "Adding HTTP Proxy to Spring WebFlux Client"
excerpt: "Adding HTTP Proxy to Spring WebFlux Client"
disqus_id: /2022/09/03/adding-http-proxy-spring-webflux-client/
tags:    
    - Spring
    - HTTP
---

What's the normal way to add http proxy in JVM?


```bash
JAVA_FLAGS=-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=8888
```

Similarly, for https

```bash
JAVA_FLAGS=-Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=8888
```

However, these properties do not work if you are using Spring Webflux Client

There is a bug logged for the same

[https://github.com/reactor/reactor-netty/issues/887#issuecomment-549439355](https://github.com/reactor/reactor-netty/issues/887#issuecomment-549439355)

The proxy support in Spring Webflux client code can only be added through code. 

Here is the snippet:


```java

protected WebClient webClient;

public void init() {
   webClient = WebClient.builder().filter(errorHandlingFilter())
                .clientConnector(new ReactorClientHttpConnector(build())).build();
}

private HttpClient build() {
        HttpClient httpClient = HttpClient.create()
                .tcpConfiguration(tcpClient ->
                        tcpClient.proxy(proxy -> proxy.type(ProxyProvider.Proxy.HTTP).host("127.0.0.1").port(8888)));
        return httpClient;
}
```


 
