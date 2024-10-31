---
layout: blog-post
title: "Reisze disk in Proxmox VM"
excerpt: "Reisze disk in Proxmox VM"
disqus_id: /2024/11/01/resize-disks-proxmox/
tags:
    - Proxmox
---

I was looking to quickly resize the disk of my Proxmox VM.

The Debian 12 bookworm VM created through [Proxmox VE Helper Scripts](https://tteck.github.io/Proxmox/#debian-12-vm) comes with default size of 2 GB even if opted for advanced installation.

There is no way to select the disk size during installation.

### Pre-Requisites
Install the following tools `parted` , `fdisk`

```
apt install parted fdisk
```

* Resize the disk through Proxmox GUI.

* Now login into the VM and run the command `fdisk -l`. You should get a warning such as below

> GPT PMBR size mismatch (167772159 != 314572799) will be corrected by write.
> The backup GPT table is not on the end of the device. This problem will be corrected by write.

* Next step is to use `parted`

```
parted /dev/sda

print
```

You should again get warning such as below

> Warning: Not all of the space available to /dev/sda appears to be used, you can fix the GPT to use all of the space (anextra 146800640 blocks) or continue with the current setting?

```
Fix/Ignore? F
```

Next run resizepart

```
(parted) resizepart 1
Warning: Partition /dev/sda1 is being used. Are you sure you want to continue?
Yes/No? y
End? [85.9GB]? 100%
quit
```

After following the above steps, we have to run `resize2fs` to take effect

```
resize2fs /dev/sda1
```

Note that this method works only for ext4 non-LLVM filesystems 


