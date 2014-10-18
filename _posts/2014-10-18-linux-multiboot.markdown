---
layout: blog-post
title: "Multiboot: Booting linux from ISO placed in HDD via GRUB"
excerpt: "Multiboot: Booting linux from ISO placed in HDD via GRUB"
disqus_id: /2014/10/18/linux-multiboot/
location: New Delhi, India
time: 9:00 PM
tags:
- Linux
---

I am a big fan of Linux and want to frequently try out various distributions such as [Mint](http://www.linuxmint.com/), [Ubuntu](http://www.ubuntu.com/), [Kali](http://www.kali.org/) and [ArchLinux](https://www.archlinux.org/).

Though my main system is Linux 16, I use ISO placed in my HDD to boot and try these various distributions whenever I like.
What are the advatages:
* No messing up with partitions on HDD
* No installation required
* Most major flavours support live booting

Disadvantages:
* Changes are not persisted
* Can take some time to initially setup

I will describe how it can be done with very minimnal conifuration and hassle.

We are going to setup the multiboot configuration of following OS. They will be booted entirely from ISO placed in HDD 
* Gparted Live CD (ISO)
* Kali Linux (ISO)
* Linux Mint 17 (ISO)

I assume you are running any Linux distribution with [GRUB](http://www.gnu.org/software/grub/) as the bootloader.

First download the ISO's for the distributions you want to boot. For this article, I downloaded the above 3 from:
* [http://gparted.org/download.php](http://gparted.org/download.php)
* [http://www.kali.org/downloads/](http://www.kali.org/downloads/)
* [http://www.linuxmint.com/download.php](http://www.linuxmint.com/download.php)

Place it in any directory in your root partition. In my case I dropped them in  `~/isos/` as `kali.iso`, `mint17.iso` and `gparted-live.iso`

Now, edit your grub configuration to add the custom entries. The file we are looking to edit is `/etc/grub.d/40_custom`

Here is my configuration:

```text
menuentry "Gparted live" {
	insmod ntfs
	insmod iso9660

      set isofile="/home/madhur/isos/gparted-live.iso"
      loopback loop (hd0,msdos2)$isofile
      linux (loop)/live/vmlinuz boot=live config union=aufs noswap noprompt vga=788 ip=frommedia toram=filesystem.squashfs findiso=$isofile nomodeset
      initrd (loop)/live/initrd.img
    }


menuentry "Mint 17" {
	insmod ntfs
	insmod iso9660

      set isofile="/home/madhur/isos/mint17.iso"
      loopback loop (hd0,msdos2)$isofile
      linux (loop)/casper/vmlinuz file=/cdrom/preseed/linuxmint.seed iso-scan/filename=$isofile boot=casper debug --verbose nomodeset
      initrd (loop)/casper/initrd.lz
    }



menuentry "Kali" {
	insmod ntfs
	insmod iso9660

      set isofile="/home/madhur/isos/kali.iso"
      loopback loop (hd0,msdos2)$isofile
      linux (loop)/live/vmlinuz boot=live noconfig=sudo username=root hostname=kali findiso=$isofile debug --verbose nomodeset
      initrd (loop)/live/initrd.img
    }
```

Some of the parameters deserve explanation:

* `insmod ntfs` and `insmod iso9660` load the ntfs and iso kernel modules if they are not loaded
* `debug --verbose` will disable the splash screen and show the textual boot screen while loading. This can be helpful to see if something goes wrong.
* `nomodeset` will defer loading the Video drivers and will force fallback to BIOS for display. You might not need it. However, it was required in my case as my 
   graphics card (Nvidia GeForce 750 Ti) was not detected.
*  `(hd0, msdos2)` this needs to be changed to reflect the disk# and partition# of partition where ISO's are located. Here `hd0` means the first hard disk and `msdos2` means second partition. Note that in grub disk numbering  starts from zero while partition numbering starts from 1. Weird.


Once done with all the changes, fire `sudo update-grub` to update your `grub.cfg` with these changes.

###Troubleshooting
* Note that you might not just get this right in first go. Things can go wrong and be prepared for it.
* Take special care of `(hd0, msdos2)` to determine your correct configuration. It is not easy as /dev/sda1=(hd0, 1) and /dev/sdb1 = (hd1, 1). In my case /dev/sdc referred to hd0. Had hard time figuring out.
* While booting from grub, you can press `e` to edit the command line on the fly and try out various options wuch as commenting out `nomodeset` and different combinations for `(hd#, msdos#)`. Once you have figured out the correct option, update the `40_custom` and execute `update-grub` again.
* You can also press `c` on the grub screen to fall into grub terminal and execute command such as `ls (hd0, msdos2) /` to see if that works.
* Different distros have their specific command line options. Peek into the ISO file to look at `grub.cfg` or `entries.cfg` to determine the corrent command line boot options.





