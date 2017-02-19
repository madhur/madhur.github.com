---
layout: blog-post
title: "Useful tcpdump usages"
excerpt: "Useful tcpdump usages"
disqus_id: /2017/02/18/useful-tcpdump-usages/
tags:
- tcpdump
---

[Tcpdump](http://www.tcpdump.org/tcpdump_man.html) and [Netcat](http://nc110.sourceforge.net/) are one of the most useful utilities for Linux network debugging.

Some of the examples where I have found `tcpdump`  to be extremely useful are given below. In the next post, I will cover netcat.

###Look for traffic based on IP address

{% highlight text %}
tcpdump host 1.2.3.4
{% endhighlight %}

###Capture based on protocol

{% highlight text %}
tcpdump udp
{% endhighlight %}


###Capture based on interface

{% highlight text %}
tcpdump -i eth1
{% endhighlight %}

###Capture filter based on certain port

{% highlight text %}
tcpdump port 80
{% endhighlight %}

###Capture filter based on source port or destination port

{% highlight text %}
tcpdump src port 80
tcpdump dst port 80
{% endhighlight %}

###Capture based on port range

{% highlight text %}
tcpdump portrange 80-90
{% endhighlight %}

###Capture display in ASCII

{% highlight text %}
tcpdump -A -i eth0
{% endhighlight %}


###Capture to a file

{% highlight text %}
tcpdump -w 08232010.pcap -i eth0
{% endhighlight %}
