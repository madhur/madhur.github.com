---
layout: blog-post
title: "CentOS is dead"
excerpt: "CentOS is dead"
disqus_id: /2022/02/05/centos-is-dead/
tags:    
    - CentOS
---

[Red Hat](https://www.redhat.com/en) has finally pulled the plug on the [CentOS](https://www.centos.org/)


[Announcement: CentOS Linux 8 is EOL of December 31st 2021](https://www.centos.org/news-and-events/1322-october-centos-dojo-videos/)

CentOS which has been backbone of all the major servers, there are alternatives now out there such as [Rocky Linux](https://rockylinux.org/) and [Alma Linux](https://almalinux.org/) which claim 1:1 binary compatibility with [RHEL](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux)

If you are a desktop user such as me, its better to migrate to [Fedora](https://getfedora.org/)

Also, if you are getting error such as 

```
Failed to download metadata for repo 'appstream'
```

CentOS team has moved all their packages from mirrorlist.centos.org to vault.centos.org

Running below commands should solve the problem

```
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
```