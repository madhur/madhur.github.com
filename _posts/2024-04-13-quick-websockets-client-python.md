---
layout: blog-post
title: "Quick Websockets client in Python"
excerpt: "Quick Websockets client in Python"
disqus_id: /2024/04/13/quick-websockets-client-python/
tags:
    - Websockets
---

When interacting with lot of websockets server, you need a nifty client to test out the behaviour of websocket server.

Till now, I have been using [wscat](https://github.com/websockets/wscat) as the command line utility to interact with websockets server.

However, this command line utility has several disadvantages:
* It doesn't allow you to send custom ping messages
* It doesn't support authentication

Due to these limitations, I wrote a simple python script below which can send a custom ping payload.

This little script helps to quickly test out websocket servers.


```python
import websocket
import json

session_id="12345"

ready_message = {"type":"setup","sid":session_id,"time":1712393684026, "src": "79677227"} 
ping_payload={"type":"heartbeatreq","time":1712393714042,"src":"79677227"}

def on_message(wsapp, message):
    print("Received: ", message)

def on_ping(wsapp, message):
    print("Got a ping! A pong reply has already been automatically sent.")

def on_pong(wsapp, message):
    wsapp.send(message)

def on_open(wsapp):
    print("sending ready")
    ready_msg = json.dumps(ready_message) + "\n"
    wsapp.send(ready_msg)

def on_error(wsapp, message):
    print(message)

def on_close(wsapp, close_status_code, close_reason):
    print("closed", close_reason, close_status_code)

wsapp = websocket.WebSocketApp("ws://localhost:8080",
on_message=on_message, on_ping=on_ping, on_pong=on_pong, on_open=on_open, on_error=on_error, on_close=on_close)
wsapp.run_forever(ping_interval=2, ping_timeout=1, ping_payload=json.dumps(ping_payload)+ "\n")  

```