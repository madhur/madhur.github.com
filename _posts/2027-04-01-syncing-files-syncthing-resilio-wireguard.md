---
title: "Syncing Files Over the Internet with Syncthing and Resilio Using WireGuard VPN"
excerpt: "How to set up Syncthing and Resilio Sync to work reliably over the internet using WireGuard VPN with wg-easy in Docker"
disqus_id: /2027/04/01/syncing-files-syncthing-resilio-wireguard/
tags:
    - Syncthing
    - Resilio
    - WireGuard
    - Docker
    - Linux
    - Homelab
    - Networking
---

Both Syncthing and Resilio Sync are excellent tools for keeping files synchronized across devices. While they work great on a local network, getting them to sync reliably over the internet can be tricky—especially when devices are behind NAT or firewalls. In this post, I'll walk through how I set up both tools to sync between my Arch Linux system and Android device using WireGuard VPN.

## The Problem

By default, both Syncthing and Resilio use relay servers when direct connections aren't possible. This works but can be slow and unreliable. If you already have a WireGuard VPN set up, you can use it to create a direct, private connection between your devices.

## My Setup

- **Server**: Arch Linux running wg-easy (WireGuard) in Docker
- **Client**: Android device with WireGuard client
- **Sync tools**: Syncthing and Resilio Sync on both devices

## Step 1: Setting Up wg-easy with Docker

I run WireGuard using the wg-easy container, which provides a nice web UI for managing clients. Here's my `docker-compose.yml`:

```yaml
volumes:
  etc_wireguard:

services:
  wg-easy:
    environment:
      - INSECURE=true
      - INIT_ENABLED=true
      - INIT_USERNAME=admin
      - INIT_PASSWORD=your-secure-password
    image: ghcr.io/wg-easy/wg-easy:15.2.1
    container_name: wg-easy
    networks:
      wg:
        ipv4_address: 10.42.42.42
        ipv6_address: fdcc:ad94:bacf:61a3::2a
    volumes:
      - etc_wireguard:/etc/wireguard
      - /lib/modules:/lib/modules:ro
    ports:
      - "51820:51820/udp"
      - "51821:51821/tcp"
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv4.conf.all.src_valid_mark=1
      - net.ipv6.conf.all.disable_ipv6=0
      - net.ipv6.conf.all.forwarding=1
      - net.ipv6.conf.default.forwarding=1

networks:
  wg:
    name: wg
    driver: bridge
    enable_ipv6: true
    ipam:
      driver: default
      config:
        - subnet: 10.42.42.0/24
        - subnet: fdcc:ad94:bacf:61a3::/64
```

After starting the container, access the web UI at `http://your-server:51821` to create a client configuration for your Android device.

## Step 2: Understanding the Network Topology

This is where I initially got stuck. The wg-easy container creates its own VPN network, typically `10.8.0.0/24`:

- **VPN Server (wg-easy)**: `10.8.0.1`
- **Android client**: `10.8.0.2` (assigned by wg-easy)

The important thing to understand is that the WireGuard interface (`wg0`) exists **inside the container**, not on the host. This means your Arch host can't directly reach VPN clients without some additional configuration.

## Step 3: The Critical Missing Piece—Routing

When I first tried to ping my Android device from my Arch host, it failed:

```bash
$ ping 10.8.0.2
PING 10.8.0.2 (10.8.0.2) 56(84) bytes of data.
--- 10.8.0.2 ping statistics ---
16 packets transmitted, 0 received, 100% packet loss
```

However, pinging from inside the container worked fine:

```bash
$ docker exec wg-easy ping 10.8.0.2
PING 10.8.0.2 (10.8.0.2): 56 data bytes
64 bytes from 10.8.0.2: seq=0 ttl=64 time=172.637 ms
```

The fix is to add a route on the host that sends VPN traffic through the container:

```bash
sudo ip route add 10.8.0.0/24 via 10.42.42.42
```

The `10.42.42.42` address is the container's IP on the Docker network (defined in the compose file).

After adding this route:

```bash
$ ping 10.8.0.2
PING 10.8.0.2 (10.8.0.2) 56(84) bytes of data.
64 bytes from 10.8.0.2: icmp_seq=1 ttl=63 time=17.8 ms
```

### Making the Route Persistent

The route disappears on reboot. To make it permanent, create a systemd service:

```bash
sudo tee /etc/systemd/system/wg-route.service << 'EOF'
[Unit]
Description=Route to WireGuard VPN subnet
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
ExecStart=/usr/sbin/ip route add 10.8.0.0/24 via 10.42.42.42
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable wg-route.service
```

## Step 4: Configuring Syncthing

With routing in place, configure Syncthing to use the VPN addresses directly.

### Find Your Listening Port

On Arch, check which port Syncthing is using:

```bash
$ ss -tlnp | grep syncthing
LISTEN 0      4096      127.0.0.1:8384       0.0.0.0:*    users:(("syncthing"...))
LISTEN 0      4096              *:22000            *:*    users:(("syncthing"...))
```

Syncthing listens on port `22000` for sync traffic (and `8384` for the web UI).

### Configure Device Addresses

**On Android Syncthing:**

1. Go to Devices → select your Arch device → Addresses
2. Change from `dynamic` to:
   ```
   tcp://10.8.0.1:22000, dynamic
   ```

**On Arch Syncthing:**

1. Go to Remote Devices → Android device → Edit → Addresses
2. Set to:
   ```
   tcp://10.8.0.2:22000, dynamic
   ```

### Check Android Run Conditions

This caught me off guard—Syncthing on Android has "Run Conditions" that can pause syncing. If your connection is refused:

1. Open Syncthing on Android
2. Go to Settings → Run Conditions
3. Make sure it's not paused due to Wi-Fi or charging requirements
4. Also check Android Settings → Apps → Syncthing → Battery → set to "Unrestricted"

## Step 5: Configuring Resilio Sync

### Find the Listening Port

Resilio often uses a non-standard port:

```bash
$ ss -tlnp | grep rslsync
LISTEN 0      10       127.0.0.1:8888       0.0.0.0:*    users:(("rslsync"...))
LISTEN 0      10         0.0.0.0:21386      0.0.0.0:*    users:(("rslsync"...))
```

In my case, Resilio is using port `21386` (not the default `55555`).

### Add Predefined Hosts

**On Android Resilio:**

1. Go to Settings → Advanced → Predefined hosts
2. Add: `10.8.0.1:21386`

**On Arch Resilio:**

If your Android has a fixed listening port, add it similarly. However, Android Resilio often defaults to port `0` (random), which makes it difficult to configure from the server side.

### Dealing with Random Ports on Android

If Android Resilio shows "Listening port: 0", try setting a fixed port:

1. Settings → Advanced → Listening port
2. Change from `0` to something like `55555`

If the setting won't stick (a known bug), don't worry—since Android has the Arch server configured as a predefined host, it can initiate the connection, and sync will work bidirectionally from there.

## Troubleshooting

### Connection Refused

If you get "connection refused" when testing ports:

```bash
$ nc -zv 10.8.0.2 22000
Connection refused
```

Check that:
1. The application is running on the target device
2. It's listening on all interfaces (not just localhost)
3. No firewall is blocking the port
4. For Android, check that run conditions aren't pausing the app

### Verify Syncthing Is Listening on All Interfaces

```bash
$ ss -tlnp | grep syncthing
```

You want to see `*:22000` or `0.0.0.0:22000`, not `127.0.0.1:22000`.

### Test Connectivity Step by Step

1. First verify VPN connectivity: `ping 10.8.0.2`
2. Then test the specific port: `nc -zv 10.8.0.2 22000`
3. Check the application logs for connection attempts

## Summary

The key insights from this setup:

1. **wg-easy runs WireGuard inside a container**, so the host needs an explicit route to reach VPN clients
2. **Add a route** on the host: `ip route add 10.8.0.0/24 via <container-ip>`
3. **Configure direct addresses** in Syncthing/Resilio using VPN IPs instead of relying on discovery
4. **Check Android run conditions**—battery optimization and run conditions can silently pause sync apps
5. **Make the route persistent** with a systemd service

Once everything is configured, your devices will sync directly over the encrypted WireGuard tunnel, bypassing slow relay servers and keeping your data private.
