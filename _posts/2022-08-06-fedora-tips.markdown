---
layout: blog-post
title: "Fedora Tips & Tricks"
excerpt: "Fedora Tips & Tricks"
disqus_id: /2022/07/10/fedora-tips-tricks/
tags:    
    - Fedora
---


This is a followup post to [ealier post on Fedora]({% post_url 2022-01-23-fedora-centos-tips-tricks %})

* Mount folders without requiring passwords

Usually, mount folder permission is only available to `root` user. In order to allow this for normal user, we need to add a policy rule for
[polkit](https://en.wikipedia.org/wiki/Polkit)

```
sudo vi /etc/polkit-1/localauthority/50-local.d/10-mount-without-password.pkla

```


```ini
[storage group mount override] 
Identity=unix-user:madhur 
Action=org.freedesktop.udisks2.filesystem-mount;org.freedesktop.udisks2.filesystem-mount-system 
ResultAny=yes 
ResultInactive=yes 
ResultActive=yes
```

* Similarly, if you want to allow normal user to manage `systemd` units

```
/etc/polkit-1/localauthority/50-local.d/service-auth.pkla
```

```ini
[Allow yourname to start/stop/restart services]
Identity=unix-user:madhur 
Action=org.freedesktop.systemd1.manage-units 
ResultActive=yes
```


* Set a default font in Fedora Linux

```xml
<?xml version="1.0" encoding="UTF-8"?>
<match target="pattern">
   <test name="family" qual="any">
      <string>monospace</string>
   </test>
   <edit binding="strong" mode="prepend" name="family">
      <string>JetBrains Mono</string>
   </edit>
</match>
```


* Change the [CPU governor policy](https://wiki.archlinux.org/title/CPU_frequency_scaling) for maximum performance

```
echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

* Auto login user through [LightDM](https://wiki.archlinux.org/title/LightDM#Greeter)

```
/etc/lightdm/lightdm.conf.d/12-autologin.conf
```

```ini
[SeatDefaults] 
autologin-user=madhur
```