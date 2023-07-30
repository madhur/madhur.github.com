---
layout: blog-post
title: "Creating vagrant basebox"
excerpt: "Creating vagrant basebox"
disqus_id: /2023/07/30/creating-vagrant-base-box/
tags:
    - Vagrant
---

For me, [Vagrant](https://www.vagrantup.com/) is the ultimate tool to simulate production like envrionments in the development machine.

Some people prefer [Docker](https://www.docker.com/) as an alternative to Vagrant, because of being lightweight and quick to provision.

However, I feel Docker and Vagrant have their own places and their responsibilities do not overlap. Let me explain why.

* Docker is good for running application services. Ultimately, now a days, since production code is deployed in containers itself, docker provides good testing ground for testing out [Dockerfile](https://docs.docker.com/engine/reference/builder/) and [images](https://docs.docker.com/engine/reference/commandline/images/)

* Though application services are deployed on containers, the stateful sets have not really reached that maturity stage where the persistent stores are deployed in containers.

Organizations still prefer to run the [Cassandra](https://cassandra.apache.org/_/index.html), [Redis](https://redis.io/), [MongoDB](https://www.mongodb.com/), [MySQL](https://www.mysql.com/) in the cloud VM's  if those are self hosted, instead of the containers.

This is where Vagrant becomes a crucial tool for sysadmins.

Any sysadmin, who manages such infrastructure would find Vagrant an incredibly useful tool to replicate the entire setup on development environment and test out any changes in its development environment before proceeding to higher environments.

For example, someone testing out the Cassandra DB cluster upgrade, can test it out in Vagrant environment before doing it in staging / production environment. This can help save cost.

There are [Vagrant boxes](https://app.vagrantup.com/boxes/search) available for each and every popular Operating systems such as [CentOS 7])(https://app.vagrantup.com/centos/boxes/7), [CentOS 8](https://app.vagrantup.com/generic/boxes/centos8) and [Debian](https://app.vagrantup.com/debian/boxes/jessie64)


[Github](https://github.com/search?q=vagrant+mysql&type=repositories) is full of open source scripts to provision any type of server with Vagrant.

Sometimes, it is helpful to create your own [Vagrant base box](https://developer.hashicorp.com/vagrant/docs/boxes/base) in order to avoid downloading big dependencies from package repositories such as [apt](https://wiki.debian.org/apt-get#:~:text=apt%2Dget%20is%20a%20tool,part%20of%20the%20DebianPackageManagement%20system.) or [dnf](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html-single/managing_software_with_the_dnf_tool/index)

The dependencies can be packaged inside Vagrant basebox itself so that when the box is provisioned, there is no need to download these cut shorting the time to provision.

Recently, I had such a scenario and found some important tips when creating own vagrant boxes.

* The official guidelines for creating base box for [Virtualbox](https://www.virtualbox.org/)  [https://developer.hashicorp.com/vagrant/docs/providers/virtualbox/boxes](https://developer.hashicorp.com/vagrant/docs/providers/virtualbox/boxes) recommends installing [Virtual Box guest additions](https://www.virtualbox.org/manual/ch04.html) in the basebox. Infact, it has been listed as a must.

> VirtualBox Guest Additions must be installed so that things such as shared folders can function. Installing guest additions also usually improves performance since the guest OS can make some optimizations by knowing it is > running within VirtualBox.

This is one of the most illogical and idiotic advice according to me. Because, VirtualBox Guest additions package is tied to specific version of VirtualBox. Once you install VirtualBox Guest additions package and later upgrade or downgrade VirtualBox version, it is of no use. This creates a tight coupling between the consumer (developer) and the Vagrant Base box. According to me, installing Virtual Box Guest Additions package is best avoided unless you really need fancy two way synchronizations between host and guest folders, which I believe no serious sysadmin should care about.


* When you provision a Vagrant box, the folder in which `Vagrantfile` resides is mounted inside the guest machine as `/vagrant`. Before executing `vagrant package --base basebox`, which triggers the creation of basebox, make sure to delete the `/vagrant` folder else it will be packaged as a regular folder inside the basebox which in most cases you don't want.

* It is very important to keep the size of basebox as small as possible to make sure it does not occupy huge disk space when boxes are provisioned from the base box. Vagrant does the compression of the basebox, however it does the compression based on the binary analysis of the disk. If there has been lot of files in and out of the box, even after deleting those files, the space won't be reclaimed by vagrant compression. Hence its best to zero out the empty space before initiating creation of box using

```bash
# Zero free space to aid VM compression
printf "STEP: Zero free space to aid VM compression\n"
dd if=/dev/zero of=/EMPTY bs=1M
rm -f /EMPTY
```
The above step should take care of filling the empty space with zeroes which vagrant would be able to compress out signifcantly.

* If you care about the space optimzation very deeply, there are certain files such as [man pages](https://www.kernel.org/doc/man-pages/) and [log files](https://en.wikipedia.org/wiki/Logging_(computing)) which can be removed from Linux OS. Have a look at this [gist](https://gist.github.com/carlessanagustin/2fb92e88f2068300a2ed) for such tweaks to optimize. I am recopying the gist below incase gist is later unavailable:

```bash

#!/bin/sh
 
# Credits to:
#  - http://vstone.eu/reducing-vagrant-box-size/
#  - https://github.com/mitchellh/vagrant/issues/343
#  - https://gist.github.com/adrienbrault/3775253

## for vagrant related tasks, uncomment vagrant comments
 
# vagrant: Unmount project
#printf "STEP: vagrant: Unmount project\n"
#umount /vagrant
 
# Remove APT cache
printf "STEP: Remove APT cache\n"
apt-get clean -y
apt-get autoclean -y
 
# Zero free space to aid VM compression
printf "STEP: Zero free space to aid VM compression\n"
dd if=/dev/zero of=/EMPTY bs=1M
rm -f /EMPTY
 
# Remove APT files
printf "STEP: Zero free space to aid VM compression\n"
find /var/lib/apt -type f | xargs rm -f
 
# Remove documentation files
printf "STEP: Remove documentation files\n"
find /var/lib/doc -type f | xargs rm -f
 
# vagrant: Remove Virtualbox specific files
#printf "STEP: vagrant: Remove Virtualbox specific files\n"
#rm -rf /usr/src/vboxguest* /usr/src/virtualbox-ose-guest*
 
# Remove Linux headers
printf "STEP: Remove Linux headers\n"
rm -rf /usr/src/linux-headers*
 
# Remove Unused locales (edit for your needs, this keeps only en* and pt_BR)
printf "STEP: Remove Unused locales (edit for your needs, this keeps only en* and pt_BR)
find\n" 
find /usr/share/locale/{af,am,ar,as,ast,az,bal,be,bg,bn,bn_IN,br,bs,byn,ca,cr,cs,csb,cy,da,de,de_AT,dz,el,en_AU,en_CA,eo,es,et,et_EE,eu,fa,fi,fo,fr,fur,ga,gez,gl,gu,haw,he,hi,hr,hu,hy,id,is,it,ja,ka,kk,km,kn,ko,kok,ku,ky,lg,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,nb,ne,nl,nn,no,nso,oc,or,pa,pl,ps,qu,ro,ru,rw,si,sk,sl,so,sq,sr,sr*latin,sv,sw,ta,te,th,ti,tig,tk,tl,tr,tt,ur,urd,ve,vi,wa,wal,wo,xh,zh,zh_HK,zh_CN,zh_TW,zu} -type d -delete
 
# Remove bash history
printf "STEP: Remove bash history\n"
unset HISTFILE
rm -f /root/.bash_history

# vagrant: Remove bash history
#printf "STEP: vagrant: Remove bash history\n"
#rm -f /home/vagrant/.bash_history
 
# Cleanup log files
printf "STEP: Cleanup log files\n"
find /var/log -type f | while read f; do echo -ne '' > $f; done;
 
# Whiteout root
printf "STEP: Whiteout root\n"
count=`df --sync -kP / | tail -n1  | awk -F ' ' '{print $4}'`;
count=$((count -= 1))
dd if=/dev/zero of=/tmp/whitespace bs=1024 count=$count;
rm /tmp/whitespace;
 
# Whiteout /boot
printf "STEP: Whiteout /boot\n"
count=`df --sync -kP /boot | tail -n1 | awk -F ' ' '{print $4}'`;
count=$((count -= 1))
dd if=/dev/zero of=/boot/whitespace bs=1024 count=$count;
rm /boot/whitespace;
 
# Whiteout swap 
printf "STEP: Whiteout swap\n"
swappart=`cat /proc/swaps | tail -n1 | awk -F ' ' '{print $1}'`
swapoff $swappart;
dd if=/dev/zero of=$swappart;
mkswap $swappart;
swapon $swappart;

```