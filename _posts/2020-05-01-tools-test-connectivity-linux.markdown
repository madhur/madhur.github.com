---
layout: blog-post
title: "Tools to test remote connectivity in Linux"
excerpt: "Tools to test remote connectivity in Linux"
disqus_id: /2020/05/01/tools-test-connectivity-linux/
tags:
- Linux
---

In this post, we will look at tools to test remote connectivity in Linux. With increasing usage of firewalls, server hardening due to cyber attacks, it becomes important to determine appropriate connectivity between two hots. Note that, we are looking for connectivity tests w.r.t. server systems such as databases, application servers etc.

Organizations having multiple datacenters, systems running in private / public clouds, accessing vendor partner systems, its important to have a know how to determine if the a system is able to connect to a remote system or not. 

Note that our focus will be on covering out of the box tools in Linux and not any custom built tools by 3rd party.

So, let's get down to it.

* [ping](#ping)
* [telnet](#telnet)
* [netcat](#netcat)
* [curl](#curl)
* [netstat](#netstat)
* [nmap](#nmap)

<a name="ping"></a>

# ping
[ping](https://en.wikipedia.org/wiki/Ping_(networking_utility)) is one of the oldest Linux utilities to test connectivity between two hosts. It works on [ICMP](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)

```console
$ ping -c 5 www.example.com
PING www.example.com (93.184.216.34): 56 data bytes
64 bytes from 93.184.216.34: icmp_seq=0 ttl=56 time=11.632 ms
64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=11.726 ms
64 bytes from 93.184.216.34: icmp_seq=2 ttl=56 time=10.683 ms
64 bytes from 93.184.216.34: icmp_seq=3 ttl=56 time=9.674 ms
64 bytes from 93.184.216.34: icmp_seq=4 ttl=56 time=11.127 ms

--- www.example.com ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 9.674/10.968/11.726/0.748 ms
```

- The issue with ping is that it does not test TCP connectivity to a particular port. It was designed in mind when there used to be no firwalls or restriction between 2 hosts. But in modern world, ICMP traffic is usually restricted. So its possible that there exists a valid connectvity between two hosts at a particular port while ping command shows unreachable.

<a name="telnet"></a>

# telnet
[Telnet](https://en.wikipedia.org/wiki/Telnet) is another utility which has been widely used in history to test connectivity between hosts at a specific port. For ex,

if we want to test the connectivty at IP 172.217.163.46 at port 443, we can simply do

```console
$ ~ telnet 172.217.163.46 443
Trying 172.217.163.46...
Connected to maa05s01-in-f14.1e100.net.
Escape character is '^]'.
```

- The issue with telnet is that it transfer everything in plaintext. So if you type a password in it, it will be transferred without encryption. Due to this reason, many popular flavors of Linux such as Fedora, CentOS and RHEL do not include this utility anymore in standard Linux distribution. It can be installed manually through `yum install telnet` though.

<a name="nc"></a>

# netcat (nc)
[Netcat or nc](https://en.wikipedia.org/wiki/Netcat) is by far the most currently popular tool right now. It is very powerful as it allows you to even setup your own server and is generally referred to as swiss army knife.

Taking the same above example,

```console
$ ~ nc -v  172.217.163.46 443
found 0 associations
found 1 connections:
     1:	flags=82<CONNECTED,PREFERRED>
	outif en0
	src 192.168.1.96 port 55004
	dst 172.217.163.46 port 443
	rank info not available
	TCP aux info available
```
+ It can do port scanning

+ It can test out UDP ports too

<a name="curl"></a>

# curl
[curl](https://curl.haxx.se/docs/manpage.html#-k) is the best tool if you are dealing with HTTP / HTTPS traffic.

```console
$ ~ curl -k https://172.217.163.46
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
```
-k option is used to skip SSL check.

Using verbose option (-vvv) can give you much more information about HTTP version, headers and TLS version. 

```console
$ ~ curl -vvv -k https://172.217.163.46
* Rebuilt URL to: https://172.217.163.46/
*   Trying 172.217.163.46...
* TCP_NODELAY set
* Connected to 172.217.163.46 (172.217.163.46) port 443 (#0)
* ALPN, offering h2
* ALPN, offering http/1.1
* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
* successfully set certificate verify locations:
*   CAfile: /etc/ssl/cert.pem
  CApath: none
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS change cipher, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-RSA-CHACHA20-POLY1305
* ALPN, server accepted to use h2
* Server certificate:
*  subject: C=US; ST=California; L=Mountain View; O=Google LLC; CN=*.google.com
*  start date: Apr  7 09:27:14 2020 GMT
*  expire date: Jun 30 09:27:14 2020 GMT
*  issuer: C=US; O=Google Trust Services; CN=GTS CA 1O1
*  SSL certificate verify ok.
* Using HTTP2, server supports multi-use
* Connection state changed (HTTP/2 confirmed)
* Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0
* Using Stream ID: 1 (easy handle 0x7fb685003c00)
> GET / HTTP/2
> Host: 172.217.163.46
> User-Agent: curl/7.54.0
> Accept: */*
>
* Connection state changed (MAX_CONCURRENT_STREAMS updated)!
< HTTP/2 301
< location: http://www.google.com/
< content-type: text/html; charset=UTF-8
< date: Fri, 01 May 2020 14:27:00 GMT
< expires: Sun, 31 May 2020 14:27:00 GMT
< cache-control: public, max-age=2592000
< server: gws
< content-length: 219
< x-xss-protection: 0
< x-frame-options: SAMEORIGIN
< alt-svc: h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"
<
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
* Connection #0 to host 172.217.163.46 left intact
```

<a name="netstat"></a>

# netstat
[netstat](https://linux.die.net/man/8/netstat) is another one of mine favourite tools. Though, it doesn't allow you to test the connectivity with the new host, its the best tool if you want to view the list of already 
connected hosts.

```console
# ~ netstat -tun
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 10.33.128.63:36352      10.12.24.223:9092       ESTABLISHED
tcp        0      0 10.33.128.63:22         172.29.124.150:63515    ESTABLISHED
tcp        0      0 10.33.128.63:55638      10.12.38.199:9997       TIME_WAIT
tcp        0      0 10.33.128.63:45938      10.36.66.150:5000       ESTABLISHED
tcp        0      0 10.33.128.63:37738      10.12.38.187:9997       TIME_WAIT
tcp        0      0 10.33.128.63:44620      10.12.38.206:9997       ESTABLISHED
tcp        0      0 10.33.128.63:33676      10.33.128.63:22         TIME_WAIT
tcp        0      0 10.33.128.63:41616      10.12.24.222:9092       ESTABLISHED
tcp        0     52 10.33.128.63:22         172.28.96.245:58173     ESTABLISHED
```

It also gives the state of TCP port as well (ESTABLISHED, TIME_WAIT, LISTENING)

<a name="nmap"></a>

# nmap
[nmap](https://nmap.org/) is one of the most advanced tools out of these. It might not be installed out of the box in every Linux distribution.
It is considered a very advanced security tool for OS fingerprinting, port scanning.

