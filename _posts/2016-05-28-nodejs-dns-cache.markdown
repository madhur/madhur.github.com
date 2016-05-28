---
layout: blog-post
title: "Speeding up Node.js HTTP requests with DNS caching"
excerpt: "Speeding up Node.js HTTP requests with DNS caching"
disqus_id: /2016/05/28/nodejs-dns-cache/
tags:
- NodeJs
---


I recently discovered in one of my projects that results of DNS are not cached by [NodeJs](https://nodejs.org/en/). Caching the results of DNS queries is one of the important things and can dramatically improve the speed and scalability of your application. In our application, we saw the number of HTTP requests jump from 35 to 2500 per seconds which is an almost 100x factor.

##How to cache results of DNS queries

One way could be to use a caching DNS library for Node such as [DnsCache](https://www.npmjs.com/package/dnscache). Once this module is installed via `npm install dnscache` , every call to a dns method is first looked into the local cache, in case of cache hit the value from cache is returned, in case of cache miss the original dns call is made and the return value is cached in the local cache.

It is very similar to GOF Proxy design pattern providing a Cache Proxy.

The goal of this module is to cache the most used/most recent dns calls, to avoid the network delay and improve the performance.

{% highlight javascript %}
var dns = require('dns'),
    dnscache = require('dnscache')({
        "enable" : true,
        "ttl" : 300,
        "cachesize" : 1000
    });
    
    //to use the cached dns either of dnscache or dns can be called. 
    //all the methods of dns are wrapped, this one just shows lookup on an example 
    
    //will call the wrapped dns 
    dnscache.lookup('www.yahoo.com', function(err, result) {
        //do something with result 
    });
    
    //will call the wrapped dns 
    dns.lookup('www.google.com', function(err, result) {
        //do something with result 
    });
{% endhighlight %}


Second way is to cache the results of queries at OS level. This is my preferred way as your application does not have to worry about caching as it is done automatically by OS for you. There are many DNS caching resolvers available such as: [Bind](https://www.isc.org/downloads/bind/), [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) and [unbound](http://unbound.net/)

##How to check if DNS cache is working

If you are using the DNS caching resolver such as dnsmasq or unbound, the result of DNS query should be very fast i.e. in order of 1 msec or even 0 msec.

For example executing `dig facebook.com` gives me following output:

{% highlight text %}
dig facebook.com

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.37.rc1.el6_7.7 <<>> facebook.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 6468
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;facebook.com.          IN  A

;; ANSWER SECTION:
facebook.com.       300 IN  A   69.171.230.68

;; Query time: 375 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Sat May 28 10:03:26 2016
;; MSG SIZE  rcvd: 46
{% endhighlight %}

Here the query time of `375 msec` is what we are interested in. That's way too high. If your DNS caching resolver is working fine, next time you execute this command, its time should be <=1msec. 

{% highlight text %}
dig facebook.com

; <<>> DiG 9.8.2rc1-RedHat-9.8.2-0.37.rc1.el6_7.7 <<>> facebook.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7997
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;facebook.com.          IN  A

;; ANSWER SECTION:
facebook.com.       184 IN  A   69.171.230.68

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Sat May 28 10:05:22 2016
;; MSG SIZE  rcvd: 46
{% endhighlight %}

In the first case, where in you are using application level caching, DNS request should not be sent at all, i.e. we would have to monitor the DNS traffic and confirm its absence. 

We can simply use [TCPDump](http://www.tcpdump.org/) for this purpose.

`tcpdump -s 0 -l -n port 53` will give the all DNS traffic. For example in my 
executing `dig facebook.com` gives the following traffic:

{% highlight text %}
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
10:03:26.061650 IP 205.147.100.85.53967 > 192.54.112.30.domain: 30692% [1au] A? facebook.com. (41)
10:03:26.206708 IP 192.54.112.30.domain > 205.147.100.85.53967: 30692- 0/6/5 (649)
10:03:26.207148 IP 205.147.100.85.53067 > 69.171.255.12.domain: 10866% [1au] A? facebook.com. (41)
10:03:26.207348 IP 205.147.100.85.35076 > 192.31.80.30.domain: 62038% [1au] NS? facebook.com. (41)
10:03:26.290949 IP 69.171.255.12.domain > 205.147.100.85.53067: 10866*- 1/2/4 A 69.171.230.68 (169)
10:03:26.291306 IP 205.147.100.85.35719 > 192.54.112.30.domain: 13554% [1au] DS? facebook.com. (41)
10:03:26.423309 IP 192.31.80.30.domain > 205.147.100.85.35076: 62038- 0/6/5 (649)
10:03:26.423732 IP 205.147.100.85.13121 > 69.171.255.12.domain: 14660% [1au] NS? facebook.com. (41)
10:03:26.424027 IP 205.147.100.85.28055 > 69.171.239.12.domain: 58880% [1au] AAAA? a.ns.facebook.com. (46)
10:03:26.424211 IP 205.147.100.85.15049 > 69.171.255.12.domain: 29662% [1au] A? b.ns.facebook.com. (46)
10:03:26.424305 IP 205.147.100.85.33030 > 69.171.255.12.domain: 45018% [1au] AAAA? b.ns.facebook.com. (46)
10:03:26.424402 IP 205.147.100.85.42614 > 69.171.255.12.domain: 51358% [1au] A? a.ns.facebook.com. (46)
10:03:26.435590 IP 192.54.112.30.domain > 205.147.100.85.35719: 13554*- 0/6/1 (762)
10:03:26.512147 IP 69.171.255.12.domain > 205.147.100.85.13121: 14660*- 2/0/4 NS a.ns.facebook.com., NS b.ns.facebook.com. (153)
10:03:26.513377 IP 69.171.255.12.domain > 205.147.100.85.33030: 45018*- 1/2/3 AAAA 2a03:2880:ffff:c:face:b00c:0:35 (153)
10:03:26.513398 IP 69.171.255.12.domain > 205.147.100.85.15049: 29662*- 1/2/3 A 69.171.255.12 (153)
10:03:26.520676 IP 69.171.239.12.domain > 205.147.100.85.28055: 58880*- 1/2/3 AAAA 2a03:2880:fffe:c:face:b00c:0:35 (153)
10:03:26.525315 IP 69.171.255.12.domain > 205.147.100.85.42614: 51358*- 1/2/3 A 69.171.239.12 (153)
{% endhighlight %}

In case of successful caching, no traffic should be observed from the application.
