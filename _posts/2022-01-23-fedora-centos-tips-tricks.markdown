---
layout: blog-post
title: "Fedora / CentOS Tips & Tricks"
excerpt: "Fedora / CentOS Tips & Tricks"
disqus_id: /2022/01/23/fedora-centos-trips-tricks/
tags:
    - Fedora
    - CentOS
---

Have been using Fedora as my desktop OS for quite some time now. Here are some of the thigns that has helped:

*  If you are using Wifi on these OS, there are some services which do not start until Wifi has come up. There will be a warning during startup

>A start job is running for wait for network to be configured

In that case, to disable the wait-online service to prevent the system from waiting on a network connection, and use 

```
systemctl disable systemd-networkd-wait-online.service
```

* Use Snap and Flatpak

My preferred way of installing applications is through [Snap](https://snapcraft.io/docs/installing-snap-on-centos) and [Flatpak](https://flatpak.org/) first and if they are not available in these channels, then only I revert to [rpm](https://rpm.org/)

* Use Zsh

[Bash](https://www.gnu.org/software/bash/) is the default shell in these OSes. If youo are using for daily use, [zsh](https://www.zsh.org/) helps a lot


* Install better fonts

The font rendering in linux is far behind from Mac / Windows. Use these fonts in terminal / code editors to have better experience. Its still lags behind Mac / Windows though.

[Source Code Pro](https://github.com/adobe-fonts/source-code-pro)   
[JetBrains Mono](https://www.jetbrains.com/lp/mono/)   
[Consolas](https://docs.microsoft.com/en-us/typography/font-list/consolas)   
[Fira Code](https://github.com/tonsky/FiraCode)

* Install latest kernel

The default kernel is usually older. If you are using latest hardware, installing the latest kernel version really helpsp if you are facing some non-detected hardware issue such as Wifi. Installing latest kernel is as easy as following these steps:

```
sudo dnf update -y
sudo dnf -y install https://www.elrepo.org/elrepo-release-8.el8.elrepo.noarch.rpm
# Install mainline kernels
sudo dnf --enablerepo=elrepo-kernel install kernel-ml
sudo dnf --enablerepo=elrepo-kernel install kernel-ml-{devel,headers}
sudo reboot
```

Verify latest kernel
```
uname -r
```

