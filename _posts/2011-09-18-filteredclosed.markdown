---
layout: blog-post
title: "Difference between Filtered vs Closed Ports"
excerpt: "Difference between Filtered vs Closed Ports"
disqus_id: /2011/09/18/filteredclosed/
location: Delhi, India
time: 11:00 AM
tags:
- Hacking
- Nmap
---

Often during Nmap scanning techniques, you will find the port state as either **open** or **filtered**
{% highlight text %}
PORT      STATE    SERVICE
22/tcp    open     ssh
443/tcp   open     https
1024/tcp  filtered kdm
1084/tcp  filtered ansoft-lm-2
1863/tcp  filtered msnp
3128/tcp  open     squid-http
3333/tcp  filtered dec-notes
4900/tcp  filtered hfcs
9943/tcp  filtered unknown
30000/tcp open     unknown
38292/tcp filtered landesk-cba
40911/tcp filtered unknown
52673/tcp filtered unknown
{% endhighlight %} 

What exactly is the difference between two ?

* **Closed Port**: If you send a SYN to a closed port, it will respond back with a RST.
* **Filtered Port**: Presumably, the host is behind some sort of firewall.  Here, the packet is simply dropped and you receive no response (not even a RST).
* **Open Port**: If you send a SYN to an open port, you would expect to receive SYN/ACK.

