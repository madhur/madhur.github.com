---
title: "Wake on LAN: Remotely Power On Your PC"
excerpt: "How to configure Wake on LAN on your PC and use an Android app to remotely turn it on from anywhere"
disqus_id: /2027/01/01/wake-on-lan-remote-pc/
tags:
    - Linux
    - Homelab
    - Networking
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the ideas and configuration described are based on real usage and genuine user needs.

Wake on LAN (WoL) is a networking standard that allows you to remotely power on a computer over a network. This is incredibly useful when you want to access your home PC remotely but don't want to leave it running 24/7.

In this post, I'll show you how I configured Wake on LAN on my PC and how I use an Android app to turn it on remotely.

## What is Wake on LAN?

Wake on LAN works by sending a special network packet called a "magic packet" to your computer's network interface card (NIC). Even when your PC is powered off, the NIC remains in a low-power state, listening for this magic packet. When it receives one, it signals the motherboard to power on the system.

The magic packet contains:
- 6 bytes of `0xFF`
- The target MAC address repeated 16 times

## Prerequisites

For Wake on LAN to work, you need:

1. A motherboard that supports WoL (most modern motherboards do)
2. A wired Ethernet connection (Wi-Fi WoL is unreliable)
3. WoL enabled in BIOS/UEFI
4. WoL enabled on your network adapter
5. The MAC address of your network interface

## Step 1: Enable WoL in BIOS/UEFI

First, you need to enable Wake on LAN in your BIOS/UEFI settings:

1. Restart your PC and enter BIOS/UEFI (usually by pressing `Del`, `F2`, or `F12` during boot)
2. Look for power management or network settings
3. Enable options like:
   - "Wake on LAN"
   - "Wake on PCI/PCIe"
   - "Power On By PCI-E"
   - "Resume on LAN"

The exact naming varies by motherboard manufacturer. Save and exit BIOS.

## Step 2: Find Your MAC Address

On Linux, find your network interface and MAC address:

```bash
ip link show
```

Look for your Ethernet interface (usually `eth0`, `enp3s0`, or similar). The MAC address is shown after `link/ether`.

You can also use:

```bash
ip addr show enp3s0 | grep ether
```

Note down your MAC address - you'll need it for the Android app.

## Step 3: Enable WoL on Your Network Adapter

Check if WoL is currently enabled:

```bash
sudo ethtool enp3s0 | grep Wake-on
```

You'll see something like:
```
Supports Wake-on: pumbg
Wake-on: d
```

The `Wake-on: d` means WoL is disabled. To enable it:

```bash
sudo ethtool -s enp3s0 wol g
```

The `g` flag enables wake on magic packet.

Verify the change:

```bash
sudo ethtool enp3s0 | grep Wake-on
```

Now it should show:
```
Wake-on: g
```

## Step 4: Make WoL Persistent Across Reboots

The `ethtool` setting doesn't persist after a reboot. To make it permanent, create a systemd service:

```bash
sudo nano /etc/systemd/system/wol.service
```

Add the following content:

```ini
[Unit]
Description=Enable Wake on LAN
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/ethtool -s enp3s0 wol g

[Install]
WantedBy=multi-user.target
```

Replace `enp3s0` with your actual interface name.

Enable and start the service:

```bash
sudo systemctl enable wol.service
sudo systemctl start wol.service
```

## Step 5: Test Wake on LAN Locally

Before setting up the Android app, test WoL from another machine on your network.

Shut down your PC:

```bash
sudo shutdown now
```

From another Linux machine, install `wakeonlan`:

```bash
# Debian/Ubuntu
sudo apt install wakeonlan

# Arch Linux
sudo pacman -S wakeonlan
```

Send the magic packet:

```bash
wakeonlan AA:BB:CC:DD:EE:FF
```

Replace `AA:BB:CC:DD:EE:FF` with your PC's MAC address. Your PC should power on within a few seconds.

## Step 6: Configure the Android App

I use the [Wake on LAN](https://play.google.com/store/apps/details?id=co.uk.mrwebb.wakeonlan) app by Mike Webb. It's simple and works great.

### For Local Network (Same Wi-Fi)

1. Open the app and tap the `+` button to add a device
2. Enter a nickname for your PC
3. Enter your PC's MAC address
4. For the IP address, use the broadcast address (e.g., `192.168.1.255`)
5. Leave the port as `9` (default WoL port)
6. Save and tap on the device to send the magic packet

### For Remote Wake (Over the Internet)

To wake your PC from outside your home network, you need to configure port forwarding on your router:

1. Log into your router's admin interface
2. Set up port forwarding:
   - External port: `9` (or any port you prefer)
   - Internal IP: Your network's broadcast address (e.g., `192.168.1.255`)
   - Internal port: `9`
   - Protocol: UDP

3. In the Wake on LAN app:
   - Set the IP address to your public IP or dynamic DNS hostname
   - Set the port to match your external port

**Note:** Some routers don't allow forwarding to broadcast addresses. In that case, you can forward to your PC's static IP address, but this is less reliable.

## Troubleshooting

If Wake on LAN isn't working:

1. **Check BIOS settings**: Ensure WoL is enabled and your PC isn't in a deep sleep state (S4/S5)
2. **Verify ethtool settings**: Run `sudo ethtool enp3s0 | grep Wake-on` and confirm it shows `g`
3. **Check your router**: Some routers block broadcast packets or have WoL features that interfere
4. **Use a static IP**: DHCP leases can expire while the PC is off, making the ARP table stale
5. **Test locally first**: Always verify WoL works on your local network before trying remote access

## Conclusion

Wake on LAN is a simple yet powerful feature that lets you power on your PC remotely. Combined with remote access tools like SSH or RDP, you can have full access to your home computer from anywhere without leaving it running 24/7.

The Wake on LAN Android app makes it incredibly convenient - just tap a button on your phone and your PC boots up, ready for you to connect.
