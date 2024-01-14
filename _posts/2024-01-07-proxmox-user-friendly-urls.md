---
layout: blog-post
title: "Proxmox - Setting up user friendly urls"
excerpt: "Proxmox - Setting up user friendly urls"
disqus_id: /2024/01/07/proxmos-user-friendly-urls/
tags:
    - Proxmox
    - LXC
---

I have been recently tinkering up with idea of setting up a [homelab](https://en.wikipedia.org/wiki/Home_server) and [self hosting](https://en.wikipedia.org/wiki/Self-hosting_(web_services)) few services
such as [DNS Server](https://en.wikipedia.org/wiki/Name_server), [Media server](https://en.wikipedia.org/wiki/Media_server), [RSS Aggregator](https://en.wikipedia.org/wiki/News_aggregator) etc along with some standard monitoring tools.

I evaluated two products, [Proxmox](https://www.proxmox.com/en/) and [Unraid](https://unraid.net/)

After evaluating both, I choose Proxmox primarily because it seemed to fit my needs more than Unraid. Unraid is primarily useful if you have lot of data which needs to be made available to multiple services.

Whereas, Proxmox seems more suitable to run independent services altogether, either in [Docker](https://en.wikipedia.org/wiki/Docker_(software), [VMs](https://en.wikipedia.org/wiki/Virtual_machine) or [Linux Containers](https://en.wikipedia.org/wiki/LXC)

For me, the size of the data was not going to be very much, atleast initially and I found the idea of running an open source software (Proxmox) more appealing than one I had to purchase (Unraid).

I had a spare 12 CORE / 32 GB machine on which I quickly setup Proxmox and I must say, I really like the way I was quickly able to run the following services in a day:

* [Jellyfin](https://jellyfin.org/) - Media server
* [Commafeed](https://github.com/Athou/commafeed) - Open source RSS aggregator written in Java
* [PiHole](https://pi-hole.net/) - DNS Server with Ad Blocking
* [qbittorrent](https://www.qbittorrent.org/) - Torrent client
* [Nginx Proxy Manager](https://nginxproxymanager.com/) - A simple reverse proxy
* [Prometheus](https://prometheus.io/) - Well known time series database
* [Grafana](https://grafana.com/) - Well known visualization platform


The cool thing about [Proxmox](https://www.proxmox.com/en/) is that it uses a [Type 1 Hypervisor](https://www.ibm.com/topics/hypervisors) called [Kernel-based Virtual Machine (KVM)](https://ubuntu.com/blog/kvm-hyphervisor) to run all the above mentioned services in [Linux Containers running on Debian Linux OS](https://wiki.debian.org/LXC)

What that essentially means is that all these services get their own unique IP Addresses on my LAN network as opposed to all running on a single IP Addresses and exposing on different ports. Type 1 Hypervisor means that they are able to directly access machine hardware and do not have the any additional layer or overhead of resource hungry VM's.

Each LXC takes around 200 - 300 MB of disk space and around 512 MB of RAM , making them all fit in a single commodity machine.

One caveat of this approach is that now I have tons of IP addresses and ports for me to memorize to access these services when I require. Though I can bookmark them, I do not find it appealing.

Hence, I decided to setup a reverse proxy in nginx for each of them in order for me to reach them through a very user friendly url. Here is the screenshot of the setup:

<img src='/images/nginx.png' height='600px' />

The above setup requires some manual setup of setting up a [`/etc/hosts`](https://en.wikipedia.org/wiki/Hosts_(file)) file with appropriate entries as follows

```
# Hosts for nginx proxy manager
192.168.1.133 nginx
192.168.1.133 plexui
192.168.1.133 tui
192.168.1.133 jellyfinui
192.168.1.133 grafanaui
192.168.1.133 promui
192.168.1.133 zkui
192.168.1.133 piholeui
192.168.1.133 rssui

```

Here `192.168.1.133` is the IP Address of [Nginx Proxy Manager](https://github.com/NginxProxyManager/nginx-proxy-manager)

With the above setup I can reach my services in friendly urls such as:

http://plexui, http://tui, http://jellyfinui, http://grafanaui etc.

### Using Pihole for DNS Records instead of static host file

One might argue that these hosts entries need to be done in each individiaul client that needs to access Proxmox containers and is not a scaleable approach.

That is correct, the reason I went with hosts file approach is that right now, I only have a single client - my desktop PC and I do not foresee running PiHole 24x7.

Incase, I choose PiHole as my permanent DNS resolver and AdBlocker, the scaleable way would be to add these entries in PiHole itself so that it becomes available to any client within my network.

