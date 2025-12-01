---
layout: blog-post
title: "Secure Your Homelab: Exposing Services Selectively with WireGuard VPN and Traefik"
excerpt: "Secure Your Homelab: Exposing Services Selectively with WireGuard VPN and Traefik"
disqus_id: /2026/06/01/secure-homelab-wireguard-docker-traefik/
tags:
    - Traefik
    - VPN
    - WireGuard
    - Homelab
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.


Running a homelab is exciting, but security should never be an afterthought. In this guide, I'll show you how to create a sophisticated setup where:

- **Public services** remain accessible to everyone (like your blog or portfolio)
- **Private services** require VPN access (like admin panels, monitoring tools, or personal apps)
- **Home network access** works seamlessly when you're at home
- **VPN access** is required when traveling

We'll use **WireGuard** for VPN connectivity and **Traefik** as our reverse proxy to intelligently route traffic based on your location.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Setting Up WireGuard with wg-easy](#setting-up-wireguard-with-wg-easy)
- [Configuring Traefik for Selective Access](#configuring-traefik-for-selective-access)
- [Example Service Configurations](#example-service-configurations)
- [Testing Your Setup](#testing-your-setup)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

Our setup creates three distinct access patterns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Internet      │    │   Home Network   │    │   VPN Clients   │
│   (Public)      │    │   (Trusted)      │    │   (Secure)      │
└─────────┬───────┘    └────────┬─────────┘    └─────────┬───────┘
          │                     │                        │
          │                     │                        │
    ┌─────▼─────────────────────▼────────────────────────▼─────┐
    │                    Traefik                               │
    │            (Reverse Proxy + SSL Termination)            │
    └─────┬─────────────────────┬────────────────────────┬─────┘
          │                     │                        │
    ┌─────▼─────┐         ┌─────▼─────┐            ┌─────▼─────┐
    │  Public   │         │   Mixed   │            │  Private  │
    │ Services  │         │ Services  │            │ Services  │
    │ (Blog,    │         │(Admin +   │            │(Database, │
    │  API)     │         │ Public)   │            │ Monitoring│
    └───────────┘         └───────────┘            └───────────┘
```

## Prerequisites

Before we start, ensure you have:

- A server with Docker and Docker Compose installed
- A domain name with DNS pointing to your server
- Basic familiarity with Docker Compose
- Traefik already running (or follow the basic setup below)

### Basic Traefik Setup

If you don't have Traefik running yet, here's a minimal configuration:

```yaml
# traefik/docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedByDefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=your-email@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "./letsencrypt:/letsencrypt"
    networks:
      - proxy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.rule=Host(`traefik.yourdomain.com`)"
      - "traefik.http.routers.traefik.entrypoints=websecure"
      - "traefik.http.routers.traefik.tls.certresolver=letsencrypt"

networks:
  proxy-network:
    external: true
```

Create the network: `docker network create proxy-network`

## Setting Up WireGuard with wg-easy

WireGuard Easy (wg-easy) v15 is a complete rewrite that simplifies VPN management significantly. Unlike previous versions, it uses a web-based setup wizard instead of environment variables.

### WireGuard Configuration

```yaml
# wireguard/docker-compose.yml
version: '3.8'

volumes:
  etc_wireguard:

services:
  wg-easy:
    image: ghcr.io/wg-easy/wg-easy:15
    container_name: wg-easy
    environment:
      # v15 requires minimal environment variables
      - INSECURE=false  # Set to true if accessing via HTTP instead of HTTPS
    networks:
      proxy-network: {}  # For Traefik access to web UI
      wg:  # VPN network with static IPs
        ipv4_address: 10.42.42.42
        ipv6_address: fdcc:ad94:bacf:61a3::2a
    volumes:
      - etc_wireguard:/etc/wireguard
      - /lib/modules:/lib/modules:ro
    ports:
      - "51820:51820/udp"  # WireGuard VPN port (must be directly exposed)
      # Port 51821 is handled internally by Traefik
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
    labels:
      # Traefik labels for HTTPS access to web management UI
      - "traefik.enable=true"
      - "traefik.http.routers.wg-easy.rule=Host(`wg.yourdomain.com`)"
      - "traefik.http.routers.wg-easy.entrypoints=websecure"
      - "traefik.http.routers.wg-easy.tls.certresolver=letsencrypt"
      - "traefik.http.services.wg-easy.loadbalancer.server.port=51821"
      - "traefik.docker.network=proxy-network"

networks:
  wg:
    name: wg  # Force exact network name
    driver: bridge
    enable_ipv6: true
    ipam:
      driver: default
      config:
        - subnet: 10.42.42.0/24
        - subnet: fdcc:ad94:bacf:61a3::/64

  proxy-network:
    external: true
```

### Initial Setup

1. **Deploy WireGuard:**
   ```bash
   cd wireguard
   docker-compose up -d
   ```

2. **Access the setup wizard:**
   - Visit `https://wg.yourdomain.com`
   - Complete the setup wizard:
     - Server IP: Your server's public IP
     - Admin password: Choose a strong password
     - VPN subnet: `10.42.42.0/24`
     - DNS servers: `1.1.1.1, 8.8.8.8`

3. **Create your first VPN client:**
   - Click "Add Client" in the web UI
   - Download the configuration or scan the QR code
   - Test the connection

## Configuring Traefik for Selective Access

Now comes the magic! We'll create different access patterns using Traefik's IP whitelisting middleware.

### Access Pattern 1: Public Services

These services are accessible from anywhere on the internet:

```yaml
# examples/public-service.yml
services:
  blog:
    image: nginx:alpine
    container_name: blog
    volumes:
      - ./blog-content:/usr/share/nginx/html
    networks:
      - proxy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.blog.rule=Host(`blog.yourdomain.com`)"
      - "traefik.http.routers.blog.entrypoints=websecure"
      - "traefik.http.routers.blog.tls.certresolver=letsencrypt"
      - "traefik.http.services.blog.loadbalancer.server.port=80"
      # No IP restrictions - publicly accessible

networks:
  proxy-network:
    external: true
```

### Access Pattern 2: VPN + Home Network Only

These services require either VPN access OR being on your home network:

```yaml
# examples/mixed-access-service.yml
services:
  admin-panel:
    image: your-admin-app:latest
    container_name: admin-panel
    networks:
      - proxy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.admin.rule=Host(`admin.yourdomain.com`)"
      - "traefik.http.routers.admin.entrypoints=websecure"
      - "traefik.http.routers.admin.tls.certresolver=letsencrypt"
      - "traefik.http.services.admin.loadbalancer.server.port=3000"
      # IP whitelist: VPN clients + home network + localhost
      - "traefik.http.routers.admin.middlewares=home-and-vpn"
      - "traefik.http.middlewares.home-and-vpn.ipwhitelist.sourcerange=10.42.42.0/24,192.168.1.0/24,127.0.0.1/32"

networks:
  proxy-network:
    external: true
```

### Access Pattern 3: VPN-Only Services

These services are only accessible through the VPN:

```yaml
# examples/vpn-only-service.yml
services:
  monitoring:
    image: grafana/grafana:latest
    container_name: monitoring
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secure-password
    networks:
      - proxy-network
    volumes:
      - grafana_data:/var/lib/grafana
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.monitoring.rule=Host(`monitoring.yourdomain.com`)"
      - "traefik.http.routers.monitoring.entrypoints=websecure"
      - "traefik.http.routers.monitoring.tls.certresolver=letsencrypt"
      - "traefik.http.services.monitoring.loadbalancer.server.port=3000"
      # Strict VPN-only access
      - "traefik.http.routers.monitoring.middlewares=vpn-only"
      - "traefik.http.middlewares.vpn-only.ipwhitelist.sourcerange=10.42.42.0/24"

volumes:
  grafana_data:

networks:
  proxy-network:
    external: true
```

### Access Pattern 4: Network Isolation

For maximum security, some services can be completely isolated from the internet:

```yaml
# examples/isolated-service.yml
services:
  database:
    image: postgres:13
    container_name: database
    environment:
      - POSTGRES_DB=homelab
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secure-password
    networks:
      - wg  # Only connected to VPN network
    volumes:
      - postgres_data:/var/lib/postgresql/data
    # No Traefik labels - only accessible via direct IP when connected to VPN
    # Access via: postgresql://10.42.42.43:5432/homelab

  internal-api:
    image: your-internal-api:latest
    container_name: internal-api
    networks:
      wg:
        ipv4_address: 10.42.42.50
    # Access via: http://10.42.42.50:8080 when connected to VPN

volumes:
  postgres_data:

networks:
  wg:
    external: true
```

## Example Service Configurations

Let's look at some real-world examples:

### Change Detection Service (Mixed Access)

```yaml
services:
  changedetection:
    image: ghcr.io/dgtlmoon/changedetection.io
    container_name: changedetection
    volumes:
      - ./data:/datastore
    restart: unless-stopped
    networks:
      - proxy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.changedetection.rule=Host(`cd.yourdomain.com`)"
      - "traefik.http.routers.changedetection.entrypoints=websecure"
      - "traefik.http.routers.changedetection.tls.certresolver=letsencrypt"
      - "traefik.http.services.changedetection.loadbalancer.server.port=5000"
      # Allow home network and VPN access
      - "traefik.http.routers.changedetection.middlewares=home-and-vpn"
      - "traefik.http.middlewares.home-and-vpn.ipwhitelist.sourcerange=10.42.42.0/24,192.168.1.0/24,127.0.0.1/32"

networks:
  proxy-network:
    external: true
```

### Portainer (VPN-Only)

```yaml
services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    command: -H unix:///var/run/docker.sock
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    networks:
      - proxy-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.portainer.rule=Host(`portainer.yourdomain.com`)"
      - "traefik.http.routers.portainer.entrypoints=websecure"
      - "traefik.http.routers.portainer.tls.certresolver=letsencrypt"
      - "traefik.http.services.portainer.loadbalancer.server.port=9000"
      # VPN-only access for security
      - "traefik.http.routers.portainer.middlewares=vpn-only"
      - "traefik.http.middlewares.vpn-only.ipwhitelist.sourcerange=10.42.42.0/24"

volumes:
  portainer_data:

networks:
  proxy-network:
    external: true
```

## Testing Your Setup

### 1. Test Public Access

```bash
# Should work from anywhere
curl -I https://blog.yourdomain.com
# Expected: 200 OK
```

### 2. Test VPN-Only Access

```bash
# Without VPN - should be blocked
curl -I https://monitoring.yourdomain.com
# Expected: 403 Forbidden

# With VPN connected - should work
curl -I https://monitoring.yourdomain.com
# Expected: 200 OK
```

### 3. Test Mixed Access

```bash
# From home network - should work
curl -I https://admin.yourdomain.com
# Expected: 200 OK

# From mobile data (without VPN) - should be blocked
curl -I https://admin.yourdomain.com
# Expected: 403 Forbidden

# From mobile data (with VPN) - should work
curl -I https://admin.yourdomain.com
# Expected: 200 OK
```

### 4. Monitor Access Logs

```bash
# Monitor Traefik logs for IP restrictions
docker logs traefik --tail 50 | grep -E "(403|Forbidden|ipwhitelist)"

# Monitor successful VPN connections
docker logs wg-easy --tail 20
```

## Security Considerations

### Understanding IP Ranges

It's crucial to understand how IP whitelisting works:

- **`10.42.42.0/24`**: Your VPN clients (WireGuard users)
- **`192.168.1.0/24`**: Your home network (adjust to match your router's range)
- **`127.0.0.1/32`**: Server localhost access

### Why Private IPs Are Safe

When you're at a friend's house with WiFi using `192.168.1.x`:
- Your device gets `192.168.1.50` (friend's network)
- Friend's router has public IP `203.45.67.89`
- **Traefik sees**: `203.45.67.89` (blocked!)
- **Not**: `192.168.1.50` (which would be allowed)

Private IP ranges only work for actual local network access, not internet requests from similar ranges elsewhere.

### Firewall Configuration

```bash
# Allow WireGuard VPN port
sudo ufw allow 51820/udp

# Allow HTTPS (Traefik)
sudo ufw allow 443/tcp

# Allow HTTP (for redirects)
sudo ufw allow 80/tcp

# Block direct access to service ports
sudo ufw deny 5000  # Example: block direct access to change detection
sudo ufw deny 3000  # Example: block direct access to Grafana
```

### Additional Security Measures

1. **Use strong passwords** for all admin interfaces
2. **Enable 2FA** where available (WireGuard Easy v15 supports TOTP)
3. **Regular updates** of all containers
4. **Monitor access logs** for suspicious activity
5. **Backup configurations** regularly

```bash
# Backup WireGuard configs
docker exec wg-easy cat /etc/wireguard/wg0.json > backup-$(date +%Y%m%d).json

# Backup Traefik dynamic config
cp -r traefik/ backup-traefik-$(date +%Y%m%d)/
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: 404 Not Found from Traefik
```bash
# Check if container is in proxy-network
docker network inspect proxy-network | grep your-service

# Verify Traefik can reach the service
docker exec traefik ping your-service-container
```

#### Issue: VPN Clients Can't Access Services
```bash
# Check WireGuard client logs
# On client: wg show

# Verify routing
# On server: 
docker exec wg-easy wg show
ip route | grep wg0
```

#### Issue: IP Whitelisting Not Working
```bash
# Check what IP Traefik sees
docker logs traefik --tail 50 | grep your-domain

# Test IP detection
curl -H "X-Real-IP: 10.42.42.5" https://your-service.com
```

#### Issue: Certificate Errors
```bash
# Check certificate resolver
docker logs traefik | grep -i acme

# Verify DNS propagation
dig your-domain.com
```

### Network Debugging

```bash
# List all Docker networks
docker network ls

# Inspect specific network
docker network inspect wg
docker network inspect proxy-network

# Check container network connections
docker inspect your-container | grep -A 20 "Networks"

# Test connectivity between containers
docker exec container1 ping container2
```

## Conclusion

This setup gives you the best of both worlds: convenience when you're at home and security when you're traveling. You can:

- **Access everything normally** when on your home network
- **Use VPN for sensitive services** when traveling
- **Keep some services completely public** for legitimate external access
- **Isolate critical services** that should never touch the internet

Happy homelabbing! 🏠🔧

---

*What services are you planning to add to your homelab? Share your setup in the comments below!*