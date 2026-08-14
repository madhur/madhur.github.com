---
title: Useful tcpdump usages
date: '2017-02-18'
description: Useful tcpdump usages
tags:
  - tcpdump
draft: false
params:
  disqus_id: /2017/02/18/useful-tcpdump-usages/
---

[Tcpdump](http://www.tcpdump.org/tcpdump_man.html) and [Netcat](http://nc110.sourceforge.net/) are one of the most useful utilities for Linux network debugging.

Some of the examples where I have found `tcpdump`  to be extremely useful are given below. In the next post, I will cover netcat.

### Look for traffic based on IP address

```text
tcpdump host 1.2.3.4
```

### Capture based on protocol

```text
tcpdump udp
```


### Capture based on interface

```text
tcpdump -i eth1
```

### Capture filter based on certain port

```text
tcpdump port 80
```

### Capture filter based on source port or destination port

```text
tcpdump src port 80
tcpdump dst port 80
```

### Capture based on port range

```text
tcpdump portrange 80-90
```

### Capture display in ASCII

```text
tcpdump -A -i eth0
```


### Capture to a file

```text
tcpdump -w 08232010.pcap -i eth0
```
