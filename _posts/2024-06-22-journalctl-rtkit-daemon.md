---
layout: blog-post
title: "Rtkit Daemon flooding journalctl logs"
excerpt: "Rtkit Daemon flooding journalctl logs"
disqus_id: /2024/06/22/my-homelab-update-part1/
tags:
    - Linux
    - Journalctl
---

Recently I observed, [Rtkit daemon](https://github.com/heftig/rtkit) has been flooding the [Journalctl](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) logs

I frequently found logs such as below in the journalctl logs


```
Jun 13 22:51:50 madhur-b550mds3h rtkit-daemon[1922]: Supervising 2 threads of 1 processes of 1 users.
Jun 13 22:51:50 madhur-b550mds3h rtkit-daemon[1922]: Supervising 2 threads of 1 processes of 1 users.
Jun 13 22:51:50 madhur-b550mds3h rtkit-daemon[1922]: Supervising 2 threads of 1 processes of 1 users.
Jun 13 22:51:50 madhur-b550mds3h rtkit-daemon[1922]: Supervising 2 threads of 1 processes of 1 users.
...
Jun 12 23:48:39 madhur-b550mds3h rtkit-daemon[1942]: Failed to look up client: No such file or directory
Jun 12 23:48:42 madhur-b550mds3h rtkit-daemon[1942]: Failed to look up client: No such file or directory
Jun 12 23:48:44 madhur-b550mds3h rtkit-daemon[1942]: Failed to look up client: No such file or directory
```

Not much aware about this daemon, however, it seems to be used by audio systems such as [Pulseaudio](https://wiki.archlinux.org/title/PulseAudio) and [Pipewire](https://wiki.archlinux.org/title/PipeWire)

Fixing these logs is simple

```
systemctl edit rtkit-daemon

```

Add the following lines

```
[Service]
LogLevelMax=warning
```

And restart rtkit daemon using `systemctl restart rtkit-daemon`


