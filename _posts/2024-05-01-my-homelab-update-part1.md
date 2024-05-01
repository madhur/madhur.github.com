---
layout: blog-post
title: "My Homelab Update - Part I"
excerpt: "My Homelab Update - Part I"
disqus_id: /2025/05/01/my-homelab-update-part1/
tags:
    - Homelab
---

[Continuing my Homelab journey using Proxmox]({% post_url 2024-01-07-proxmox-user-friendly-urls %}), I have setup a full fledged home network with multiple services running.

Here is the quick diagram below for reference:

![](/images/Blog/homenetwork.png)

Some of the services I am running on my homenetwork as of now are 

* [Jellyfin](https://github.com/jellyfin/jellyfin)
* [Commmafeed](https://github.com/Athou/commafeed)
* [Prometheus](https://github.com/prometheus/prometheus)
* [Grafana](https://github.com/grafana/grafana)
* [Nginx Proxy Manager](https://github.com/NginxProxyManager/nginx-proxy-manager)
* [Snapdrop](https://snapdrop.net/)
* [Uptime Kuma](https://github.com/louislam/uptime-kuma)
* [Change Detection](https://github.com/dgtlmoon/changedetection.io)
* [qBittorrent](https://github.com/qbittorrent/qBittorrent)
* [Olivetin](https://github.com/OliveTin/OliveTin)
* [Vaultwarden](https://github.com/dani-garcia/vaultwarden)
* [ntfy](https://github.com/binwiederhier/ntfy)

Some of the things I am trying to solve:

* Easily able to VPN from outside to access my password manager, RSS feeds, media etc
* Get rid of [PfSense](https://www.pfsense.org/), PfSense is good but I feel its overkill for my needs.
* Evaluate [Tailscale](https://tailscale.com/), [Wireguard](https://www.wireguard.com/) and [OpenVPN](https://openvpn.net/)

And finally,
* Having less power bill while powering my Proxmox server 24x7 :)

Stay tuned for further updates if you are interested.