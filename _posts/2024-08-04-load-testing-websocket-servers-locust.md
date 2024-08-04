---
layout: blog-post
title: "Load testing Websocket servers using Locust"
excerpt: "Load testing Websocket servers using Locust"
disqus_id: /2024/08/04/load-testing-websocket-servers-locust/
tags:
    - Java
    - Locust
    - Websocket
---

The entire code of this article is present on this [github repository](https://github.com/madhur/load-test-websocket-locust)

Load testing WebSocket servers is crucial for ensuring their performance and scalability. 

This article will guide you through using Locust, a popular open-source load testing tool, to test your Java WebSocket server.

We will use Jetty WebSocket in Java to run our websocket server. Jetty WebSocket is a Java library and part of the larger Jetty project, which is a popular open-source web server and servlet container.

The only message we will be handling is heartbeat requests for simplicity.

```java
 private boolean start(String host, int port) {
    try {
        ServerConnector socketConnector = new ServerConnector(server);
        socketConnector.setPort(port);
        socketConnector.setHost(host);
        server.setConnectors(new Connector[] { socketConnector });
        disableServerVersionHeader();
        WebSocketHandler webSocketHandler = new WebSocketHandler() {
            @Override
            public void configure(WebSocketServletFactory webSocketServletFactory) {
                webSocketServletFactory.register(WebSocketChannelHandler.class);
                webSocketServletFactory.getExtensionFactory().unregister("permessage-deflate");
            }
        };
        server.setHandler(webSocketHandler);
        server.start();
        isRunning = server.isStarted();
        logger.info("Websocket Jetty server started @- {}/{}", host, port);

    } catch (Exception e) {
        logger.error("Unable to start the server on {}/{}", host, port, e);
        isRunning = false;
    }
    return isRunning;
}
```

Here is a simple handler which handles heartbeat requests

```java
@OnWebSocketMessage
public void onMessage(Session session, String message) {
    try {
        logger.info("WS message received : {}", message);
        processMessage(session, message);
    } catch (Exception e) {
        logger.error("Exception in onMessage for session {} message {} due to {}", session, message,
                e);
    }
}

private void processMessage(Session session, String message) {
    JSONObject json = new JSONObject(message);
    String messageType = json.optString("type").toLowerCase();
    processEventsBasedOnMessageType(session, messageType, json);
}

private void processEventsBasedOnMessageType(Session session, String messageType, JSONObject json) {
    switch (messageType) {
        case "heartbeatreq":
            SystemFactory.getInstance().getWebSocketMessageHandler().handleHeartBeatMessages(session);
            break;
        default:
            logger.info("Unknown message type received : {}", messageType);
    }
}
```

For the load testing part, we will use the popular [Locust](https://locust.io/) load testing framework.

We use [websocket-client](https://github.com/websocket-client/websocket-client/) to manage websockets inside python. It is a very elegant library which allows to handle both short lived and long lived websocket connections. 

Whenever we send the heartbeat request to server, we send a timestamp from the client side in the field `publishTimestamp`. The server then responds with the `heartbeatresp` and also includes the original timestamp `publishTimestamp` which was sent in the request in the response. The server also includes the `serverDelay` which represents the delay of server in processing the heartbeat response.

Our contract looks like this:
```json
{
    "type": "heartbeatreq",
    "userId": 1,
    "publishTimestamp": 1722758706760
}


{
    "type": "heartbeatresp",
    "userId": 1,
    "serverDelay": 1,
    "clientPublishTimestamp": 1722758706760
}
```

We can subtract the current time (the time we received the message in locust) and the `clientPublishTimestamp` in the `heartbeatresp` to calculate the end to end time of processing the heartbeat request message.

When running the load test with Locust, it's important to ensure that Locust itself is not experiencing high CPU usage. Otherwise, the high latency could be attributed to the lag in receiving the messages in the locust itself, rather than the processing time of the server.


We run the load with 10K connected users with ramp up rate of 500. I choose this number because I am running this on my local desktop computer.

This means we will be connecting 500 websockets / s until we reach total 10K connected sockets on the server.

<a href="/images/Blog/locust_start.png" data-fancybox>
<img src='/images/Blog/locust_start.png'  width="1000px"  />
</a>


Locust will take some time to spawn all the 10K users. At this point, we can see that rate of `ws_connect` is 500 per second.


<a href="/images/Blog/locust_spawn.png" data-fancybox>
<img src='/images/Blog/locust_spawn.png'  width="1000px"  />
</a>

Once the spawn state is finished, all the websockets are connected. At this point, all the connected websockets will be sending heartbeat requests at every 2 seconds, which comes out to ~ 5000 heartbeat requests per second as shown below.


<a href="/images/Blog/locust_running.png" data-fancybox>
<img src='/images/Blog/locust_running.png'  width="1000px"  />
</a>

### Conclusion

In this article, we saw how to load test WebSocket servers using locust. The benefit of using locust is to have fine grained control over number of sockets to connect, when to trigger messages as well as calculate end to end latency.

The entire code of this article is present on this [github repository](https://github.com/madhur/load-test-websocket-locust)

Feel free to use this code or if you have any comments, add comment using the comment box below.


