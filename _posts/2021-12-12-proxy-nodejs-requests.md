---
layout: blog-post
title: "Proxy nodejs requests through Proxy Server"
excerpt: "Proxy nodejs requests through Proxy Server"
disqus_id: /2021/12/12/proxy-nodejs-requests/
tags:
    - NodeJs
---

If you want to proxy all Nodejs HTTP requests through a  proxy server, just like JVM's 

```
-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=8888
```

Here is the quickest solution, without modifying the application source code

```bash
npm i global-agent
export GLOBAL_AGENT_HTTP_PROXY=http://127.0.0.1:8888
node -r 'global-agent/bootstrap' app.js
```


This will enable you to proxy all requests through proxy server running at 127.0.0.1 on port 8888, which could be [Charles](https://www.charlesproxy.com/) or [Burp](https://portswigger.net/burp/communitydownload)