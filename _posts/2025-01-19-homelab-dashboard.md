---
layout: blog-post
title: "Homelab Dashboard"
excerpt: "Homelab Dashboard"
disqus_id: /2025/01/19/homelab-dashboard/
tags:
    - Homelab
---

Quick update on my personal homelab server.

I set up a dashboard using [homepage](https://github.com/gethomepage/homepage) to monitor and manage all my services in one place. Though it was a bit tedious to set up, it turned out well.


<a href="/images/homepage.png" data-fancybox>
<img src='/images/homepage.png' height=800px />
</a>


I also setup a [Debian VM](https://cdimage.debian.org/images/cloud/bookworm/20250115-1993/) on my [proxmox](https://www.proxmox.com/en/) to host some of the applications on docker.

The applications I am hosting through docker are:

* [FreshRSS](https://freshrss.org/index.html) - RSS Aggregator
* [Memos](https://github.com/usememos/memos) - Self-hosted note-taking application for capturing and organizing thoughts
* [Wallos](https://github.com/ellite/Wallos) - Open Source tool for tracking and managing personal subscriptions
* [Mailcow](https://github.com/mailcow/mailcow-dockerized) - Full-featured email server solution with SMTP capabilities


Setting up Mailcow has been rewarding. As now, I am able to deliver some of the notifications from my applications directly to email.

Example of some of the notifications are:

### Torrent download complete notification through qbittorrent.

<a href="/images/email1.png" data-fancybox>
<img src='/images/email1.png' height=500px  />
</a>

### Disk usage of some of my applications

Find the [disk monitoring script here](https://gist.github.com/madhur/436481bf712866ed57af7007552912f9)

<a href="/images/email2.png" data-fancybox>
<img src='/images/email2.png' height=500px  />
</a>

### CPU Utilizations of my servers in homelab through [AlertManager](https://prometheus.io/docs/alerting/latest/alertmanager/)

Prometheus configuraiton for same

```yaml
groups:
  - name: cpu_alerts
    rules:
    - alert: HighCPUUsage
      expr: |
        (1 - avg by(instance) (
          rate(node_cpu_seconds_total{mode="idle"}[1m])
        )) * 100 > 50
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: High CPU usage detected on {{ $labels.instance }}
        description: |
          CPU usage has exceeded 50%
          Current value: {{ $value }}%
          Instance: {{ $labels.instance }}
          
    - alert: HighCPUUsageCritical
      expr: |
        (1 - avg by(instance) (
          rate(node_cpu_seconds_total{mode="idle"}[1m])
        )) * 100 > 80
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: Critical CPU usage detected on {{ $labels.instance }}
        description: |
          CPU usage has exceeded 80%
          Current value: {{ $value }}%
          Instance: {{ $labels.instance }}
```

<a href="/images/email3.png" data-fancybox>
<img src='/images/email3.png' height=500px />
</a>




### Availability notifications through [Uptime Kuma](https://github.com/louislam/uptime-kuma)


<a href="/images/email4.png" data-fancybox>
<img src='/images/email4.png' height=500px  />
</a>