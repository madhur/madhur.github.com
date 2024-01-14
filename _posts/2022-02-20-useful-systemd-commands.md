---
layout: blog-post
title: "Useful Systemd commands"
excerpt: "Useful Systemd commands"
disqus_id: /2022/02/20/useful-systemd-commands/
tags:    
    - Systemd
---

### Find the time taking services during system boot

```
systemd-analyze blame

7.239s libvirtd.service
4.528s systemd-udev-settle.service
2.829s dracut-initqueue.service
2.043s plymouth-quit-wait.service
1.541s vboxdrv.service
1.435s udisks2.service
1.149s sssd.service
1.066s gssproxy.service
1.065s zookeeper.service
632ms lvm2-monitor.service
411ms lightdm.service
410ms systemd-logind.service
238ms initrd-switch-root.service
172ms accounts-daemon.service
137ms polkit.service
121ms sysroot.mount
106ms gpd.service
99ms systemd-fsck@dev-disk-by\x2duuid-BE47\x2d662D.service
92ms systemd-tmpfiles-clean.service
82ms upower.service
81ms rtkit-daemon.service
79ms chronyd.service
79ms lm_sensors.service
```


### Find total time to boot

```
systemd-analyze

Startup finished in 8.359s (firmware) + 5.486s (loader) + 2.499s (kernel) + 3.289s (initrd) + 14.384s (userspace) = 34.018s
graphical.target reached after 14.380s in userspace
```

### Find the dependencies of service

```
systemctl list-dependencies --reverse plymouth-quit-wait.service

plymouth-quit-wait.service
● └─multi-user.target
●   └─graphical.target
```

### Find the reverse dependencies of service

```
systemctl list-dependencies  docker.service 

docker.service
● ├─containerd.service
● ├─docker.socket
● ├─system.slice
● ├─network-online.target
● └─sysinit.target
●   ├─dev-hugepages.mount
●   ├─dev-mqueue.mount
●   ├─dracut-shutdown.service
●   ├─import-state.service
●   ├─iscsi-onboot.service
●   ├─kmod-static-nodes.service
●   ├─ldconfig.service
●   ├─loadmodules.service
●   ├─lvm2-lvmpolld.socket
●   ├─lvm2-monitor.service
●   ├─multipathd.service
●   ├─nis-domainname.service
●   ├─plymouth-read-write.service
●   ├─plymouth-start.service
●   ├─proc-sys-fs-binfmt_misc.automount
●   ├─selinux-autorelabel-mark.service
●   ├─sys-fs-fuse-connections.mount
●   ├─sys-kernel-config.mount
●   ├─sys-kernel-debug.mount
●   ├─systemd-ask-password-console.path
●   ├─systemd-binfmt.service
●   ├─systemd-firstboot.service
●   ├─systemd-hwdb-update.service
●   ├─systemd-journal-catalog-update.service
●   ├─systemd-journal-flush.service
●   ├─systemd-journald.service
●   ├─systemd-machine-id-commit.service
●   ├─systemd-modules-load.service
●   ├─systemd-random-seed.service
●   ├─systemd-sysctl.service
●   ├─systemd-sysusers.service
●   ├─systemd-tmpfiles-setup-dev.service
●   ├─systemd-tmpfiles-setup.service
●   ├─systemd-udev-trigger.service
●   ├─systemd-udevd.service
●   ├─systemd-update-done.service
●   ├─systemd-update-utmp.service
●   ├─cryptsetup.target
●   ├─local-fs.target
●   │ ├─-.mount
●   │ ├─boot-efi.mount
●   │ ├─boot.mount
●   │ ├─ostree-remount.service
●   │ └─systemd-remount-fs.service
●   └─swap.target
```


### Find Active Services

```
systemctl list-units --type=service --state=active
```


### Find Running Services

```
systemctl list-units --type=service --state=running

```

### Find Enabled Units
```
systemctl list-unit-files --state=enabled
```


### Find Loaded Services
```
systemctl list-units --type=service --state=loaded
```

### View last boot log
```
journalctl -b
```

### View errors in services
```
journalctl -xe
```

### View kernel logs
```
journalctl -k