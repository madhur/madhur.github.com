---
layout: blog-post
title: "Tuning Linux servers for scalability"
excerpt: "Tuning Linux servers for scalability"
disqus_id: /2017/01/30/tuning-linux-servers-scalability/
tags:
- Linux
- Scalability
- TCP/IP
---

Focus on performance and scalablity is one of my primary personal and professional goal when working with tech products.

The server can be any Linux based server such as [CentOS](https://www.centos.org/) or [Debian](https://www.debian.org/) derivative such as [Ubuntu](https://www.ubuntu.com/).

In this post, I will outline my learnings on scaling the Linux server. Scaling here implies many things such as 

* Being able to open many files at once. Here files can be generally applied to concept such as open ports, threads etc and not necessary physical files

* Being able to handle many concurrent network connections

Knowing Linux OS and related concepts such as [Iptables](https://en.wikipedia.org/wiki/Iptables) is a pre-requisite.


  
##Open files

We need to keep our file limit high for any linux production server. Check the current value using `ulimit -a`

We can configure this limit using `/etc/security/limits.conf`

{% highlight text %}
* hard nofile 300000
* soft nofile 300000

tomcat hard nofile 300000
tomcat soft nofile 300000
{% endhighlight %}

Note that we can also specify per user limit as shown above (special limits for tomcat user)

The file descriptor limit for a running process can be seen in the following file under Max open files.

{% highlight text %}
$ cat /proc/<pid>/limits

Max open files            30000
{% endhighlight %}

  
##Ephemeral Ports
Increase the number of ephemeal ports availabl to your application. The default value is `32768 - 61000`. 

  
##TIME_WAIT state

TCP connections go through lot of states, last of them is `TIME_WAIT` state.
The default `TIME_WAIT` timeout is for 2 minutes, Which means you’ll run out of available ports if you receive more than about 400 requests a second, or if we look back to how nginx does proxies, this actually translates to 200 requests per second.

These parameters can be tuned using these settings in `/etc/sysctl.conf`

{% highlight text %}
net.ipv4.ip_local_port_range = 18000    65535
net.ipv4.netfilter.ip_conntrack_tcp_timeout_time_wait = 1
{% endhighlight %}

  
##Connection Tracking

The next parameter we looked at was Connection Tracking. This is a side effect of using `iptables`. Since `iptables` needs to allow two-way communication between established HTTP and ssh connections, it needs to keep track of which connections are established, and it puts these into a connection tracking table. This table grows. And grows. And grows.

You can see the current size of this table using `sysctl net.netfilter.nf_conntrack_count` and its limit using `sysctl net.nf_conntrack_max`. If count crosses max, your linux system will stop accepting new TCP connections and you’ll never know about this. The only indication that this has happened is a single line hidden somewhere in `/var/log/syslog` saying that you’re out of connection tracking entries. One line, once, when it first happens.

A better indication is if count is always very close to max. You might think, “Hey, we’ve set max exactly right.”, but you’d be wrong.

What you need to do (or at least that’s what you first think) is to increase max.

Keep in mind though, that the larger this value, the more RAM the kernel will use to keep track of these entries. RAM that could be used by your application.

We started down this path, increasing net.nf_conntrack_max, but soon we were just pushing it up every day. Connections that were getting in there were never getting out.

  
##Maximum number of pending connections on a socket

During some of our initial load testing, we ran into a strange problem where we were unable to open more than approximately 128 concurrent connections at once.

After some investigation, we learned about the following kernel parameter.

{% highlight text %}
net.core.somaxconn
{% endhighlight %}

This kernel parameter is the size of the backlog of TCP connections waiting to be accepted by the application. If a connection indication arrives when the queue is full, the connection is refused. The default value for this parameters is 128 on most modern operating systems.

Bumping up this limit in `/etc/sysctl.conf` helped us get rid of the “connection refused” issues on our Linux machines.

  
##JVM thread count

A few hours after we allowed a significant percentage of production traffic to hit our server for the first time, we were alerted to the fact that the load balancer was unable to connect to a few of our machines. On further investigation, we saw the following all over our server logs.

{% highlight text %}
java.lang.OutOfMemoryError: unable to create new native thread
{% endhighlight %}

If you hit the JVM thread limit, chances are that there is a thread leak in your code that needs to be fixed. However, if you find that all your threads are actually doing useful work, is there a way to tweak the system to let you create more threads and accept more connections?

The answer, as always, is fun. It’s interesting to discuss how available memory limits the number of threads that can be created on a JVM. The stack size of a thread determines the memory available for static memory allocation. Thus, the absolute theoretical maximum number of threads is a process’s user address space divided by the thread stack size. However, the reality is that the JVM also uses memory for dynamic allocation on the heap. With a few quick tests with a small Java process, we could verify that as more memory is allocated for the heap, less is available for the stack. Thus, the limit on the number of threads decreases with increasing heap size.

To summarize, you can increase the thread count limit by decreasing the stack size per thread `(-Xss)` or by decreasing the memory allocated to the heap `(-Xms, -Xmx).`


