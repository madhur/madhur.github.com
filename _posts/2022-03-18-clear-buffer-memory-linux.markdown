---
layout: blog-post
title: "Clear buffer memory on Linux"
excerpt: "Clear buffer memory on Linux"
disqus_id: /2022/03/18/clear-buffer-memory-linux/
tags:    
    - Linux
    - Memory
---

Recently, few of our production server running Redis was exhibiting high memory usage. Strangely, redis was consuming very low memory, but the overall system usage was pretty high (> 70 %).

One of the things which was common having this issue was that uptime of those systems was relatively higher than others. They were running without reboot for over 3 years.

That's when someone indicated that its the buffer memeory which might be full.

What actually happens is that linux borrows memory for disk caching. Once the buffer which is kept in memory is actually written to disk, the buffer memory is not released immediately and instead kept for reuse. Overtime, what can happen is that lot of memory can be occupied in buffer memory.

This is not a cause of concern and once the applications demand the memory actually will be given from othe buffer memory pool, however this can be a concern if you have the alerts setup for memory usage. The buffer memory usage is not excluded from OS memory usage calculations and will cause the alarms to trigger.

The buffer memory can be clared by givng the command

```
echo 3 | sudo tee /proc/sys/vm/drop_caches
```



References:

* https://www.linuxatemyram.com/
* https://serverfault.com/questions/561350/unusually-high-dentry-cache-usage
