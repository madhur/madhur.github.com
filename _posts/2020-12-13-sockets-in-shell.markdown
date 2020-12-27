---
layout: blog-post
title: "Sockets in shell"
excerpt: "Sockets in shell"
disqus_id: /2020/12/13/sockets-in-shell/
tags:
    - Shell
---

Recently, I read an article on [Sockets in your shell](https://who23.github.io/2020/12/03/sockets-in-your-shell.html) and I thought it was amazing find for me.

Lot of times especially working with docker, I had to install tools like telnet, nc and curl to check basic connectivity.

Little did I realize that this functionality is inbuilt into shell.

For ex, let's say we have a basic http server running in local as follows:

```javascript
const http = require('http');

const requestListener = function (req, res) {
    console.log("Request recieved");
    res.writeHead(200);
    res.end('Hello, World!');
}

const server = http.createServer(requestListener);
server.listen(8080);
```

How would you send the request to this port without telnet, browser, curl and nc from terminal? Answer is:

```shell
printf "GET /\n\n" > /dev/tcp/localhost/8080
```

Its as simple as that. The only downside is that it wont be possible to know if the data was successfully submitted to port 8080 or not. However, there is a simple workaround for that:

```bash
#!/bin/bash
if exec 3>/dev/tcp/localhost/8000 ; then
	echo "server up!"
else
	echo "server down."
fi
```

Quoting from the article:

> If you’re unfamiliar, exec without any arguments is used to redirect file 
> descriptors and files. By associating fd 3 with /dev/tcp/localhost/4000, it 
> attempts to create a file there and thus a connection. We use > to open the socket > for writing, although we don’t need to write anything in this case.