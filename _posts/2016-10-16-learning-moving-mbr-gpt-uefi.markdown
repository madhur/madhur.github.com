---
layout: blog-post
title: "Learnings from moving from MBR to GPT, triple booting and random stuff"
excerpt: "Learnings from moving from MBR to GPT, triple booting and random stuff"
disqus_id: /2016/09/05/learning-moving-mbr-gpt-uefi/
tags:
- Linux
- OS
- UEFI
- MBR
- GPT
---

This weekend, I converted all my 3 disks (2 HDD and 1 SSD) from a [MBR](https://en.wikipedia.org/wiki/Master_boot_record) based partition table to the newer one [GPT](https://en.wikipedia.org/wiki/GUID_Partition_Table). This was some work as I had to ensure that all my existing OSes ( [Debian 8](https://www.debian.org/), [Kali](https://www.kali.org/) and [Windows 10](https://www.microsoft.com/en-in/software-download/windows10ISO) ) run smoothlessly. 

I am sharing some of the lessons and solutions to problem I faced:

* Make sure you backup all importand data and have bootable ISO's (USB or CDs) of Operating Systems you want up and running. I cannot stress this enough. While working with disk partition tables, things go wrong very easily and you will have an unbootable system very soon. This will be especially true if you are a tinkerer and like going deep into things. Having bootable USB drives will save you a lot of time. Use tools like [unetbootin](https://unetbootin.github.io/) or familiarize your self with [dd command](https://en.wikipedia.org/wiki/Dd_(Unix)) to create this yourself.

* Read about UEFI. This is a very new standard with confusing information all over the internet. In a nutshell, it is nothing more than a partition with code `ef00`, but it is also a standard and a firmware.

* Some of these readings would help:  
[https://en.wikipedia.org/wiki/EFI_system_partition](https://en.wikipedia.org/wiki/EFI_system_partition)  
[https://wiki.archlinux.org/index.php/EFI_System_Partition](https://wiki.archlinux.org/index.php/EFI_System_Partition)  
[https://msdn.microsoft.com/en-us/windows/hardware/commercialize/manufacture/desktop/configure-uefigpt-based-hard-drive-partitions](https://msdn.microsoft.com/en-us/windows/hardware/commercialize/manufacture/desktop/configure-uefigpt-based-hard-drive-partitions)  
[http://superuser.com/questions/520068/efi-partition-vs-boot-partition](http://superuser.com/questions/520068/efi-partition-vs-boot-partition)  
[https://wiki.debian.org/UEFI](https://wiki.debian.org/UEFI)


* First make sure your [BIOS]() supports [UEFI](). Most of the new BIOS do it but there are some quirks and each BIOS manufacturer is different. For example, in my case HDD boot order does not work for UEFI boot. I had to switch the SATA cables in my HDD to make sure [GRUB]() is my primary bootloader. Also, when you enable UEFI in BIOS, you will get double entries for eash UEFI Boot enabled disk. (one for UEFI boot and other for normal boot). Don't be alarmed by it, its normal.

* You will need to do actual conversion of partition tables first. For this, best utility is combination of [gdisk]() and [gparted]() works best. Make sure you spend some time going through their commands. I created [gparted live CD](http://gparted.org/livecd.php) Do not do this conversion in Windows. [How can I change/convert a Ubuntu MBR drive to a GPT, and make Ubuntu boot from EFI?](http://askubuntu.com/questions/84501/how-can-i-change-convert-a-ubuntu-mbr-drive-to-a-gpt-and-make-ubuntu-boot-from)

* If you are using Windows, familiarize with [bcdedit](https://technet.microsoft.com/en-us/library/cc709667(v=ws.10).aspx) . It is a command line tool to work with Windows boot entries. I would not advise using tools like [EasyBCD](http://neosmart.net/EasyBCD/c) etc as they are too buggy.
For linux, make sure you know [mount](http://man7.org/linux/man-pages/man8/mount.8.html) and [chroot](https://en.wikipedia.org/wiki/Chroot) very well, these commands are very handy and it saves a lot of time if you them in advance than looking up internet everytime.

* It is also good to determine when your OS is booted up in UEFI mode vs legacy mode. For linux, this command works: ` cat /sys/firmware/efi ` , If this folder exists, the system is booted in UEFI mode. [How can I tell if my system was booted as EFI/UEFI or BIOS?](http://askubuntu.com/questions/162564/how-can-i-tell-if-my-system-was-booted-as-efi-uefi-or-bios)


* For linux GRUB, you will need to install `grub-efi-amd64` or `grub-efi`. Also remember to run `update-grub` after conversion. You might be also required to install the bootloader again using `grub install /dev/sdX` depending upon the situation. [How to reinstall GRUB2 EFI?](http://superuser.com/questions/376470/how-to-reinstall-grub2-efi)

* If you are running debian based system, this article is gold [Switch Debian 7 wheezy from legacy to UEFI boot mode](http://www.getreu.net/public/downloads/doc/legacy2UEFIboot/Transform-Debian_7_wheezy-from_legacy_to_UEFI_boot_mode.html#_boot_a_live_system)


More references:  
[What's a GPT?](http://www.rodsbooks.com/gdisk/whatsgpt.html)  
[Booting from GPT](http://www.rodsbooks.com/gdisk/booting.html)  
[Partitioning Advice](http://www.rodsbooks.com/gdisk/advice.html)  
[Windows 8 removes Grub as default boot manager](http://askubuntu.com/questions/235567/windows-8-removes-grub-as-default-boot-manager)  
[A gdisk Walkthrough](http://www.rodsbooks.com/gdisk/walkthrough.html)  
 

