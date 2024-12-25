---
layout: blog-post
title: "Qtile crash on Arch Linux"
excerpt: "Qtile crash on Arch Linux"
disqus_id: /2024/12/25/qtile-crash-arch-linux/
tags:
    - Qtile
---

I was playing around with [Qtile](https://qtile.org/) when it suddenly stopped working.

I tried everything to troubleshoot but wasn't getting any clues.

There was nothing in `~/.local/share/qtile/qtile.log`

I found this entry in systemd journal through `journalctl | grep qtile`
Here's what the logs showed:


```
Dec 24 09:14:45 madhur-b550mds3h systemd-coredump[26096]: Process 26057 (qtile) of user 1000 terminated abnormally with signal 11/SEGV, processing...
Dec 24 09:14:45 madhur-b550mds3h systemd-coredump[26097]: Process 26057 (qtile) of user 1000 dumped core.
Dec 24 09:19:53 madhur-b550mds3h kernel: qtile[3456]: segfault at 7ffc3f44dff8 ip 0000760e6dcbc2d5 sp 00007ffc3f44e000 error 6 in libc.so.6[ad2d5,760e6dc33000+171000] likely on CPU 4 (core 4, socket 0)
```

Then I came across this [Reddit thread](https://www.reddit.com/r/archlinux/comments/1gtgx9e/some_applications_dump_core_after_update/)


According to this thread, installing [nwg-look](https://github.com/nwg-piotr/nwg-look) had modified the file `~/.icons/default/index.theme` and this was causing the issue. I vaguely remembered installing this program a few days back.

I immediately ran `pacman -R nwg-look` to remove it since I didn't need it anyway.

And voila! It solved the problem of loading Qtile. That's one of the weirdest tech issues I have ever come across. If you're experiencing similar crashes with Qtile on Arch Linux, it might be worth checking if you have nwg-look installed.
