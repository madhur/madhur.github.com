---
layout: blog-post
title: "Dual Booting Windows and Linux on different HDD / SDD"
excerpt: "Dual Booting Windows and Linux on different HDD / SDD"
disqus_id: /2020/11/01/dual-boot-windows-kali-different-hdd/
tags:
    - Windows
    - Kali
    - Dual Boot
---

Recently, I setup dual boot of Windows 10 and [Kali Linux](https://www.kali.org/) on different SDD. 

Technically,  its not a dual boot when you install two different OS on different hard disks
altogether. However, with dropping prices of SSD's many people want to install
these OS on different hard disks altogether rather than cramming up them in
single hard disk with single partition.


In my case, UEFI rather than legacy boot. Here is the quick guide to setup
Windows and Linux in two different SDD.

1. Disable legacy boot in BIOS. Make sure your boot mode is set to [UEFI](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface)
   
2. Disable [secure boot](https://docs.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-secure-boot) / fast boot
   
3. Install Windows on HDD/ SDD 1 (`/dev/sda`). Windows will setup EFI partition on the same
   hard disk as well. You should be able to boot the Windows without any issues
   using UEFI boot.

4. Coming to Linux installation, here you need to choose custom partitioning. We
   will partition the second hard drive (`/dev/sdb`) for setting up Linux.

5. Create 1st partition `/EFI` on `/dev/sdc` of around 650 MB. Make sure to set it
   as Use as: [EFI](https://en.wikipedia.org/wiki/EFI_system_partition) and its at beginning of space.

6. Create 2nd partition `/` root partition of 80% of your space. Again it should
   be primary partition. However its type will be ext4 and mount point as "/".

7. Create 3rd partition as [swap partition](https://wiki.archlinux.org/index.php/swap). You can give remaining space to this
   partition. Make sure to use it as `swap`.

8. That should be enough for partitions. You can setup optional `/home` partition
   incase you need it.

9.  Bootloader device - Installer will ask where you want to install bootloader.
   Do no install it on Master Boot record. Install it on first EFI partition on
   `/dev/sdb1`.
   
11. Finish installation and reboot. You should see that the GRUB bootloader
    automatically adds the option of Windows 10 in its boot menu.

<img src='/images/Blog/kali-linux.jpg'  width='700px' />


Incase you want to change the default option. You can boot into linux and
    edit the `/etc/grub/default` files and run `sudo update-grub` to update the
    GRUB configuration.