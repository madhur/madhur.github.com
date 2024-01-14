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

The details of memory can be seen through:

```
$ cat /proc meminfo                                                                                                                                                                                                                                                                                                  
MemTotal:       32291324 kB
MemFree:        18888628 kB
MemAvailable:   24967520 kB
Buffers:               0 kB
Cached:          6619108 kB
SwapCached:            0 kB
Active:          2897464 kB
Inactive:        9542004 kB
Active(anon):      48104 kB
Inactive(anon):  6022228 kB
Active(file):    2849360 kB
Inactive(file):  3519776 kB
Unevictable:          48 kB
Mlocked:              48 kB
SwapTotal:      16850940 kB
SwapFree:       16850940 kB
Dirty:               876 kB
Writeback:             0 kB
AnonPages:       5616548 kB
Mapped:          1052904 kB
Shmem:            252404 kB
KReclaimable:     146152 kB
Slab:             339892 kB
SReclaimable:     146152 kB
SUnreclaim:       193740 kB
KernelStack:       22464 kB
PageTables:        96620 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    32996600 kB
Committed_AS:   22143820 kB
VmallocTotal:   34359738367 kB
VmallocUsed:      103880 kB
VmallocChunk:          0 kB
Percpu:            34176 kB
HardwareCorrupted:     0 kB
AnonHugePages:   1886208 kB
ShmemHugePages:        0 kB
ShmemPmdMapped:        0 kB
FileHugePages:         0 kB
FilePmdMapped:         0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
Hugetlb:               0 kB
DirectMap4k:      948848 kB
DirectMap2M:    18917376 kB
DirectMap1G:    13631488 kB
```

Here the `SRreclaimable` is the memory which can be reclaimed by clearing the buffer memory area.


The buffer memory can be clared by givng the command

```
echo 3 | sudo tee /proc/sys/vm/drop_caches
```



References:

* [https://www.linuxatemyram.com/](https://www.linuxatemyram.com/)
* [https://serverfault.com/questions/561350/unusually-high-dentry-cache-usage](https://serverfault.com/questions/561350/unusually-high-dentry-cache-usage)
