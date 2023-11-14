---
layout: blog-post
title: "Transfer files from k8s or docker shell to other host"
excerpt: "Transfer files from k8s or docker shell to other host"
disqus_id: /2023/11/14/transfer-files-from-shell-k8s/
tags:
    - Kubernetes
    - Shell
---


If you are anytime stuck in a shell where you want to transfer files out of it, and do not have full access such as `kubectl` or `docker exec`. Here is the nifty hack:

### Method 1 (Using ngrok):

Run a ngrok tunnel on the target computer 

```
ngrok http 5000
```

Run a simple node program to capture request body
```javascript
const express = require('express')
const app = express()
const port = 80
var bodyParser = require('body-parser')

app.post('/', (req, res)=> {
    console.log(req.body);
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

```
The disadvantage of this method is that post body size will be limited by terms dictated by [ngrok](https://ngrok.com/)

Another disadvantage is that you cannot use this to transfer sensitive info.


### Method 2 (using Netcat)

Run the [netcat](https://en.wikipedia.org/wiki/Netcat) server on the target computer

```shell
nc -l -p 5000  > file.txt < /dev/null 
```

Stream the file to the port from the source shell

```shell
cat anyfile.txt | netcat server.ip.here 5000
```

Here the target computer needs to be on internet. It can done via ngrok tcp tunnel or a small EC2 instance.





