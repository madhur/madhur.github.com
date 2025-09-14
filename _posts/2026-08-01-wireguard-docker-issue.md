---
layout: post
title: "WireGuard Docker Configuration Drift"
excerpt: "SWireGuard Docker Configuration Drift"
disqus_id: /2026/08/01/wireguard-docker-issue/
tags:
    - Wireguard
    - Docker
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.


# WireGuard Docker Configuration Drift: A Debugging Journey

Recently, I encountered a frustrating networking issue with my containerized WireGuard VPN setup. My Android client could connect to the WireGuard server running in Docker, but couldn't access the internet or any services. What started as a simple connectivity problem turned into a lesson about configuration drift and the importance of understanding how different network layers interact.

## The Setup

I was running [WG-Easy](https://github.com/wg-easy/wg-easy) in Docker Compose with a custom network configuration:

```yaml
services:
  wg-easy:
    image: ghcr.io/wg-easy/wg-easy:15
    container_name: wg-easy
    networks:
      wg:
        ipv4_address: 10.42.42.42  # Static IP in custom network
    volumes:
      - etc_wireguard:/etc/wireguard
    ports:
      - "51820:51820/udp"
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    # ... other config

networks:
  wg:
    driver: bridge
    ipam:
      config:
        - subnet: 10.42.42.0/24
```

The container was running fine, WireGuard clients could connect, but they couldn't reach the internet.

## The Investigation

### Network Traffic Analysis

Using `tcpdump`, I captured the network traffic and noticed something interesting:

```
07:59:26.193202 IP RT-AC68U-4740.local.35734 > zk.docker.dev.https: Flags [P.]
08:05:27.821764 IP6 fdcc:ad94:bacf:61a4::cafe:2.39226 > whatsapp-chatd-edge6-shv-02-iad3.facebook.com.https
08:05:28.076785 IP 10.42.42.2.38844 > whatsapp-chatd-edge-shv-02-mia3.facebook.com.https
```

The traffic showed:
- Container was at `10.42.42.42` (Docker network IP)
- Android client was assigned `10.42.42.2` (VPN client IP)
- WireGuard handshakes were successful

Everything looked normal from a network perspective, so I dug deeper.

### Configuration Inspection

Inside the WireGuard container, I found the first clue:

```bash
$ docker exec -it wg-easy wg show
interface: wg0
  public key: gi/bShTv06aiw1x8NT48x93oS5gx9drWdUEUtJMUpQ0=
  listening port: 51820
  peer: zEEv0Ig9h5zjHGYZMai06DSNnCsqgz7tD4oJK7JL0y0=
    allowed ips: 10.42.42.2/32
    latest handshake: 1 minute, 48 seconds ago
    transfer: 469.18 KiB received, 4.66 KiB sent
```

But then I checked the actual WireGuard interface:

```bash
$ docker exec -it wg-easy ip addr show wg0
4: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN
    inet 10.8.0.1/24 scope global wg0  # ← This was the problem!
```

### The Root Cause

Here's what was happening:

| Component | Expected IP | Actual IP | Status |
|-----------|-------------|-----------|---------|
| Docker Container | 10.42.42.42 | 10.42.42.42 | ✅ Correct |
| WireGuard Server | 10.42.42.1 | **10.8.0.1** | ❌ Wrong |
| WireGuard Client | 10.42.42.2 | **10.8.0.2** | ❌ Wrong |
| NAT Rules | 10.42.42.0/24 | **10.8.0.0/24** | ❌ Wrong |

The WireGuard configuration file showed one thing, but the running interface used completely different IP ranges!

```bash
$ docker exec -it wg-easy cat /etc/wireguard/wg0.conf
[Interface]
Address = 10.42.42.1/24  # Config file said this
# But actual interface was 10.8.0.1/24
```

### Why This Happened

**WG-Easy's Auto-Configuration Behavior:**
1. WG-Easy automatically generates WireGuard configs on first startup
2. It uses its own default VPN subnet (`10.8.0.0/24`) regardless of Docker network settings
3. The Docker network (`10.42.42.0/24`) is for container-to-container communication
4. The WireGuard network (`10.8.0.0/24`) is for VPN clients connecting to the server
5. These networks are intentionally separate in WG-Easy's design

**Configuration Drift:**
The config file (`/etc/wireguard/wg0.conf`) contained stale or template data that didn't match the actual running configuration. This can happen when:
- Container versions change behavior between updates
- Manual configuration edits conflict with auto-generated settings
- Persistent volumes retain old configs when you expect them to refresh

### The Debugging Process

1. **IP Forwarding**: ✅ Enabled (`/proc/sys/net/ipv4/ip_forward` = 1)
2. **Container Internet Access**: ✅ Working (`ping 8.8.8.8` succeeded)
3. **WireGuard Interface**: ❌ Wrong IP range
4. **NAT Rules**: ❌ Only masquerading `10.8.0.0/24`, not `10.42.42.0/24`

```bash
$ docker exec -it wg-easy iptables -t nat -L POSTROUTING -n
Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
MASQUERADE  all  --  10.8.0.0/24          0.0.0.0/0  # Only 10.8.x traffic!
```

## The Solution

Rather than trying to manually fix the configuration drift, I chose to just re-create the wg-easy container

```bash
# Complete teardown
docker-compose down -v

# Remove the persistent volume (destroys all WireGuard configs)
docker volume rm $(docker volume ls -q | grep etc_wireguard)

# Recreate everything
docker-compose up -d
```


## Key Learnings

### 1. **Understand Network Layer Separation**
Docker networks and VPN tunnels serve different purposes:
- **Docker network**: Container-to-container communication
- **VPN network**: Client-to-server tunnel communication

Don't assume they should use the same IP ranges.

---

*Have you encountered similar Docker networking issues? Share your debugging stories in the comments below!*