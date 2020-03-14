---
layout: blog-post
title: "Tailing log files on multiple remote machines"
excerpt: "Tailing log files on multiple remote machines"
disqus_id: /2020/03/14/tailing-multiple-log-files/
tags:
- SSH
---

Recently, our ELK infrastructure went down which aggregates log from our multiple servers. I wanted to investigate a production issue which involved looking up logs of multiple servers simultaneously.

I tried different methods such as [tmux](https://github.com/tmux/tmux/wiki), [multitail](https://www.vanheusden.com/multitail/) and ssh command such as 

```shell
ssh HOST_1 "tail -f /path/to/file" | tee -a /path/to/merged/contents
```

```shell
ssh HOST_2 "tail -f /path/to/file" | tee -a /path/to/merged/contents
```

```
tail -f /path/to/merged/contents
```

All these are nice solutions, but none of them is elegant. It involves setting up multiple terminal sessions just to start the monitoring.

There is also this [open source project](https://github.com/dbiservices/DBITail) which tries to solves this problem but don't think does a good job at it.

However, the best solution comes in the form of using [Fabric](http://www.fabfile.org/)

>  Fabric is a high level Python (2.7, 3.4+) library designed to execute shell commands remotely over SSH, yielding useful Python objects in return.
It builds on top of Invoke (subprocess command execution and command-line features) and Paramiko (SSH protocol implementation), extending their APIs to complement one another and provide additional functionality.

Once, Fab is installed using `pip install fabric` , the multiple logs can be tailed as follows:

```
fab -P -u username  --linewise -H x.x.x.x,y.y.y.y  -- tail -f /path/file.log
```

Also, what I like to do is instead of typing this log command, just alias it into my `~/.zshrc`

```shell
alias catalinadev='fab -P -u username  --linewise -H x.x.x.x,y.y.y.y  -- tail -f /path/file.log'
```

Thus, I can just type `catalinadev` anytime and start tailing my Tomcata catalina log files from dev envrionment.

Here is the output in action, notice how the IP address on the left handside tells us the machine from which the log line was fetched:

[Open in fullscren](/images/Blog/output.gif)

<img src='/images/Blog/output.gif' height='897px' width='1417px' />
