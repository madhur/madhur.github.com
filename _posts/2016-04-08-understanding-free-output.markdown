---
layout: blog-post
title: "Understanding free output in Linux"
excerpt: "Understanding free output in Linux"
disqus_id: /2016/04/08/understanding-free-output-linux/
location: Bangalore, India
time: 9:00 PM
tags:
- Linux
---

If you are managing Linux machines daily like me, its important to understnad the output of `free` command, which shows the free system memory.


{% highlight text %}
[root@localhost vagrant]# free
              total        used        free      shared  buff/cache   available
Mem:        5824332     2292284     1155732      132980     2376316     3087844
Swap:        839676       18172      821504
[root@localhost vagrant]#
{% endhighlight %}

`free -g` is much more helpful instead

{% highlight text %}
[root@localhost vagrant]# free -g
              total        used        free      shared  buff/cache   available
Mem:              5           2           1           0           2           2
Swap:             0           0           0
[root@localhost vagrant]#
{% endhighlight %}

Some flavours of linux might output in this format:


{% highlight text %}
             total       used       free     shared    buffers     cached
Mem:            62         46         16          0          0         10
-/+ buffers/cache:         35         27
Swap:            0          0          0
-----------------------------
{% endhighlight %}


* total - Your total, physical (assuming no virtualization) memory
* used - How much of that is currently used (by anything)
* free - How much of that is completely free (not used at all)
* shared - (never anything there, ignore that column)
* buffers - Memory used by kernel buffers
* cached - Memory used for cache

Essentially, the figures which we should be focussing on is `-/+ buffers/cache` which excludes the used buffer.

