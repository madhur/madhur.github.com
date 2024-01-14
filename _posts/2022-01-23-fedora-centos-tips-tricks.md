---
layout: blog-post
title: "Fedora / CentOS Tips & Tricks - running it as Desktop OS"
excerpt: "Fedora / CentOS Tips & Tricks - running it as Desktop OS"
disqus_id: /2022/01/23/fedora-centos-trips-tricks/
tags:
    - Fedora
    - CentOS
---


Have been using Fedora as my desktop OS for quite some time now. Here are some of the thigns that has helped:

### Use Snap and Flatpak

My preferred way of installing applications is through [Snap](https://snapcraft.io/docs/installing-snap-on-centos), [Flatpak](https://flatpak.org/), [Homebrew](https://brew.sh/) first and if they are not available in these channels, then only I revert to [rpm](https://rpm.org/)

### Use Zsh

[Bash](https://www.gnu.org/software/bash/) is the default shell in these OS. If youo are using for daily use, [zsh](https://www.zsh.org/) helps a lot


### Install better fonts

The font rendering in linux is far behind from Mac / Windows. Use these fonts in terminal / code editors to have better experience. Its still lags behind Mac / Windows though.

[Source Code Pro](https://github.com/adobe-fonts/source-code-pro)   
[JetBrains Mono](https://www.jetbrains.com/lp/mono/)   
[Consolas](https://docs.microsoft.com/en-us/typography/font-list/consolas)   
[Fira Code](https://github.com/tonsky/FiraCode)

### Install latest kernel

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

### Configure display scaling and text scaling

If you are using a high resolution 4k monitor, chance are that you will find text and icons too small for daily use. This is not just true for Linux, its true for Windows as well.
Its just that Windows will act smart and automatically enable scaling to make display look sharp. In Linux, you will have to do it manually. There are two options: Display scaling and text scaling. It is important to understand the difference between two.

Display scaling scales all the screen elements including the windows, icons and text by a fraction, whereas text scaling only scales the text.

In my case, display scaling was resulting in icons looking blurry. Text scaling preserved the icon scaling but scaled only the text resuling in overall great display.

I would leave upto you to determine what works best for you.

Additional resources:  
[The perils of running Windows 10 on a 4K monitor](https://blogs.windows.com/windows-insider/2017/01/09/announcing-windows-10-insider-preview-build-15002-pc/#B4p617eIRYORoHM1.97)  
[Display scaling introduced in Cinnamon](https://www.linuxmint.com/rel_ulyana_cinnamon_whatsnew.php)  

### Disable SELinux

SELinux is not really required for desktop linux. Its best to disable it.

```
vi /etc/sysconfig/selinux
SELINUX=disabled
```

### Disable Firewalld

For pure desktop usage, firewall is not at all required. Though it depends upon the type of network you are using. For public wifi networks, it is definitely required.
For home networks, it can be disabled.

```
systemctl disable firewalld
```

### Install Conky for System monitoring

The default system monitor linux app is not at all comprehensive and is not the kind of app you would want to look at again and again.
For system monitoring, I recommend [Conky](https://github.com/brndnmtthws/conky)

It needs bit of configuration and tweaks depending upon the hardware installed. But once configured, it works beatifully.
You can have a look at my [configuration here](https://github.com/madhur/awesome-conky)

### Install imwheel for Mouse wheel scroll customization

Linux apart from all the advancements, lacks basic feature of customizing mouse wheel scroll length / sensitivity.

Though [KDE](https://kde.org/) has recently introduced this feature, other desktop still lack it.

You can use [imwheel](https://github.com/app/imwheel) for this. Its not perfect, but it gets the job done with some minor quirks.

I use the following configuration in `~/.imwheelrc`

```
".*"
None,       Up,     Up,     9
None,       Down,   Down,   9
```


### Install Development Tools and Multimedia codecs

This is something basic. If you want to become even an intermediate user in Linux, it will require knowledge of compiling and building source code.
For that you will need dev tools such as [GCC](https://gcc.gnu.org/), [Meson](https://mesonbuild.com/) and [Ninja](https://ninja-build.org/)


### Wifi Issues  

If you are using Wifi on these OS, there are some services which do not start until Wifi has come up. There will be a warning during startup

>A start job is running for wait for network to be configured

In that case, to disable the wait-online service to prevent the system from waiting on a network connection, and use 

```
systemctl disable NetworkManager-wait-online
```