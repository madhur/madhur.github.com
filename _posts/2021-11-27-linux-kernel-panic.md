---
layout: blog-post
title: "Kernel Panic with AMD Ryzen 5600x on CentOS 7"
excerpt: "Kernel Panic with AMD Ryzen 5600x on CentOS 7"
disqus_id: /2021/11/27/linux-kernel-panic/
tags:
    - Linux
---

Recently, I upgraded my personal computer CPU from [Intel Core i7 2600K (SandyBridge)](https://ark.intel.com/content/www/us/en/ark/products/52214/intel-core-i72600k-processor-8m-cache-up-to-3-80-ghz.html) to [AMD Ryzen 5600x](https://www.amd.com/en/products/cpu/amd-ryzen-5-5600x)

The older processor was a decade old and the accompanying board didn't support new age SSDs such as [Nvme PCI 4 SSD](https://www.samsung.com/us/computing/memory-storage/solid-state-drives/980-pro-pcie-4-0-nvme-ssd-1tb-mz-v8p1t0b-am/)

However, post upgradation, as soon as I booted my existing system running CentOS 7, I recieved a dreaded [kernel panic](https://en.wikipedia.org/wiki/Kernel_panic) very similar to [BSOD in Windows](https://en.wikipedia.org/wiki/Blue_screen_of_death)

<img src='/images/kernel-panic.jpg' height="600px"  />

Turns out that latest AMD processors are not supported on Kernel 3.x which comes with CentOS 7. I had to upgrade it to Cent OS 8 which comes with Kernel 4.x

