---
layout: blog-post
title: "Increase Grub2 Resolution in CentOS / Fedora"
excerpt: "Increase Grub2 Resolution in CentOS / Fedora"
disqus_id: /2022/01/31/increase-grub2-resolution-centos/
tags:
    - Fedora
    - CentOS
---


Quick tip to increase your boot loader resolution in Grub2.

The key is to set `GRUB_TERMINAL_OUTPUT` to `gfxterm` and provide some resolution modes appropriate for your monitor in `GRUB_GFXMODE` parameter.

```bash
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="gfxterm"
GRUB_CMDLINE_LINUX="crashkernel=512m selinux=0"
GRUB_DISABLE_RECOVERY="true"
GRUB_ENABLE_BLSCFG=true
GRUB_GFXMODE=3840x2160,2560x1440,1920x1080x16
```


Optionally, you can also provide a custom font using 

```bash
GRUB_FONT=/boot/grub2/unicode.pf2
```

There are other solutions on the internet suggesting to use `vbeinfo` or `videoinfo`.

These solutions do not seem to work for newer systems which boot using [EFI](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface)