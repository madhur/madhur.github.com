---
layout: blog-post
title: "Resize disk in Proxmox VM"
excerpt: "Resize disk in Proxmox VM"
disqus_id: /2024/11/01/resize-disks-proxmox/
tags:
    - Proxmox
---

I needed to resize a disk in my Proxmox VM. Specifically, I was working with a Debian 12 (Bookworm) VM created through [Proxmox VE Helper Scripts](https://tteck.github.io/Proxmox/#debian-12-vm). These VMs come with a default size of 2 GB, even when using the advanced installation option. Unfortunately, there's no way to select the disk size during the initial installation process.


### Pre-Requisites
First, install the required tools:

```bash
apt install parted fdisk
```

### Steps to Resize the disk
* Resize the disk through Proxmox GUI.

* Login to the VM and run `fdisk -l` . You should see warnings similar to:

> GPT PMBR size mismatch (167772159 != 314572799) will be corrected by write.
> The backup GPT table is not on the end of the device. This problem will be corrected by write.

* Use parted to fix the partition table:

```bash
parted /dev/sda

print
```

You'll see a warning:


> Warning: Not all of the space available to /dev/sda appears to be used, you can fix the GPT to use all of the space (an extra 146800640 blocks) or continue with the current setting?

* Fix the partition table

```
Fix/Ignore? F
```

* Resize the partition:

```
(parted) resizepart 1
Warning: Partition /dev/sda1 is being used. Are you sure you want to continue?
Yes/No? y
End? [85.9GB]? 100%
quit
```

* Apply the changes to the filesystem:

```
resize2fs /dev/sda1
```

Note: This method works only for ext4 non-LVM filesystems.


