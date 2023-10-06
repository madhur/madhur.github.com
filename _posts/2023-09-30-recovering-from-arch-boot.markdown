---
layout: blog-post
title: "Recovering from Arch Boot failure"
excerpt: "Recovering from Arch Boot failure"
disqus_id: /2023/09/30/recoving-from-arch-boot/
tags:
    - Arch
    - Linux
---

Recently I faced boot failure after upgrading my [Arch Linux](https://archlinux.org/) system.

The error was 

```shell
ERROR: device 'UUID=1dd743ed-e0a5-4b0c-80ee-186e89eea401' not found. Skipping fsck.
mount: /new_root: can't find UUID=1dd743ed-e0a5-4b0c-80ee-186e89eea401.
ERROR: failed to mount '1dd743ed-e0a5-4b0c-80ee-186e89eea401' on real root
You are now being dropped into an emergency shell.
sh: can't access tty; job control turned off
[rootfs ~]# _

```

This could happen while building errorneous [initramfs](https://en.wikipedia.org/wiki/Initial_ramdisk) image

It was evident from `/var/log/pacman.log` logs

```
[2023-10-04T20:36:26+0530] [ALPM] running '90-mkinitcpio-install.hook'...
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET] ==> Building image from preset: /etc/mkinitcpio.d/linux.preset: 'default'
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET] ==> Using configuration file: '/etc/mkinitcpio.conf'
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET]   -> -k /boot/vmlinuz-linux -c /etc/mkinitcpio.conf -g /boot/initramfs-linux.img
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET] ==> Starting build: '6.5.2-arch1-1'
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET]   -> Running build hook: [base]
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET]   -> Running build hook: [udev]
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET]   -> Running build hook: [autodetect]
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET] sort: cannot read: '/sys/devices/pci0000:00/0000:00:08.1/0000:08:00.3/usb3/3-1/3-1.2/3-1.2:1.2/ep_04/uevent': No such file or directory
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET] modprobe: ERROR: missing parameters. See -h.
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET]   -> Running build hook: [modconf]
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET]   -> Running build hook: [block]
[2023-10-04T20:36:27+0530] [ALPM-SCRIPTLET]   -> Running build hook: [keyboard]
[2023-10-04T20:36:27+0530] [ALPM-SCRIPTLET]   -> Running build hook: [keymap]
[2023-10-04T20:36:27+0530] [ALPM-SCRIPTLET]   -> Running build hook: [consolefont]
[2023-10-04T20:36:27+0530] [ALPM-SCRIPTLET] ==> WARNING: consolefont: no font found in configuration
[2023-10-04T20:36:27+0530] [ALPM-SCRIPTLET]   -> Running build hook: [filesystems]
[2023-10-04T20:36:27+0530] [ALPM-SCRIPTLET]   -> Running build hook: [fsck]
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET] ==> Generating module dependencies
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET] ==> Creating zstd-compressed initcpio image: '/boot/initramfs-linux.img'
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET] ==> Image generation successful
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET] ==> Building image from preset: /etc/mkinitcpio.d/linux.preset: 'fallback'
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET] ==> Using configuration file: '/etc/mkinitcpio.conf'
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET]   -> -k /boot/vmlinuz-linux -c /etc/mkinitcpio.conf -g /boot/initramfs-linux-fallback.img -S autodetect
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET] ==> Starting build: '6.5.2-arch1-1'
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET]   -> Running build hook: [base]
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET]   -> Running build hook: [udev]
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET]   -> Running build hook: [modconf]
[2023-10-04T20:36:28+0530] [ALPM-SCRIPTLET]   -> Running build hook: [block]
[2023-10-04T20:36:29+0530] [ALPM-SCRIPTLET] ==> WARNING: Possibly missing firmware for module: 'qed'
[2023-10-04T20:36:29+0530] [ALPM-SCRIPTLET] ==> WARNING: Possibly missing firmware for module: 'bfa'
[2023-10-04T20:36:29+0530] [ALPM-SCRIPTLET] ==> WARNING: Possibly missing firmware for module: 'qla2xxx'
[2023-10-04T20:36:29+0530] [ALPM-SCRIPTLET] ==> WARNING: Possibly missing firmware for module: 'aic94xx'
[2023-10-04T20:36:29+0530] [ALPM-SCRIPTLET] ==> WARNING: Possibly missing firmware for module: 'wd719x'
[2023-10-04T20:36:29+0530] [ALPM-SCRIPTLET] ==> WARNING: Possibly missing firmware for module: 'qla1280'
[2023-10-04T20:36:30+0530] [ALPM-SCRIPTLET] ==> WARNING: Possibly missing firmware for module: 'xhci_pci'
[2023-10-04T20:36:31+0530] [ALPM-SCRIPTLET]   -> Running build hook: [keyboard]
[2023-10-04T20:36:32+0530] [ALPM-SCRIPTLET]   -> Running build hook: [keymap]
[2023-10-04T20:36:32+0530] [ALPM-SCRIPTLET]   -> Running build hook: [consolefont]
[2023-10-04T20:36:32+0530] [ALPM-SCRIPTLET] ==> WARNING: consolefont: no font found in configuration
[2023-10-04T20:36:32+0530] [ALPM-SCRIPTLET]   -> Running build hook: [filesystems]
[2023-10-04T20:36:33+0530] [ALPM-SCRIPTLET]   -> Running build hook: [fsck]
[2023-10-04T20:36:34+0530] [ALPM-SCRIPTLET] ==> Generating module dependencies
[2023-10-04T20:36:34+0530] [ALPM-SCRIPTLET] ==> Creating zstd-compressed initcpio image: '/boot/initramfs-linux-fallback.img'
[2023-10-04T20:36:35+0530] [ALPM-SCRIPTLET] ==> Image generation successful

```

The line which caused the issue during image generation:

```
[2023-10-04T20:36:26+0530] [ALPM-SCRIPTLET] sort: cannot read: '/sys/devices/pci0000:00/0000:00:08.1/0000:08:00.3/usb3/3-1/3-1.2/3-1.2:1.2/ep_04/uevent': No such file or directory
```

The solution to recover was to boot to another OS. I run CentOS Steam 8 as a dual boot. And then mount the root file system of arch on path `/run/media/madhur/arch`

Run the following commands

```shell
mount -t proc /proc proc/
mount -t sysfs /sys sys/
mount --rbind /dev dev/
mount --rbind /sys/firmware/efi/efivars sys/firmware/efi/efivars/
chroot /run/media/madhur/arch
mikinitcpio -p linux

```

The final command will generate the new initramfs image

More information about this issue can be found in this [thread](https://bbs.archlinux.org/viewtopic.php?id=289336)