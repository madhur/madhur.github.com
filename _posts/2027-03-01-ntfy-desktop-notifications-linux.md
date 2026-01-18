---
layout: blog-post
title: "Getting Native Desktop Notifications from ntfy on Linux"
excerpt: "How to receive ntfy push notifications as native Linux desktop notifications using notify-send, even when the browser is closed."
disqus_id: /2027/03/01/ntfy-desktop-notifications-linux/
tags:
    - Linux
    - ntfy
    - Docker
    - Notifications
    - systemd
---

*This article was written with the assistance of AI.*

---

If you're running [ntfy](https://ntfy.sh) in Docker for push notifications, you might have noticed that browser notifications only work when you have the ntfy tab open. This post shows how to receive native Linux desktop notifications via `notify-send` that work even when the browser is closed.

## The Problem

ntfy's web interface uses browser notifications, which require:
- The browser to be open
- The ntfy tab to be active or at least loaded
- Browser notification permissions granted

This means you miss notifications when working in other applications or when the browser is closed.

## The Solution

Run the ntfy CLI client as a systemd user service that subscribes to your topics and triggers `notify-send` for each incoming message.

## Installation

### 1. Install the ntfy Client

On Arch Linux, install from AUR:

```bash
yay -S ntfysh-bin
```

On other distributions, download the binary:

```bash
curl -sSL https://ntfy.sh/ntfy-linux-amd64.tar.gz | tar xz
sudo mv ntfy-linux-amd64/ntfy /usr/local/bin/
```

### 2. Create the Client Configuration

Create `~/.config/ntfy/client.yml` with your topics:

```yaml
default-host: https://ntfy.example.com
subscribe:
  - topic: alerts
    command: 'notify-send --app-name=ntfy "$t" "$m"'
  - topic: daily
    command: 'notify-send --app-name=ntfy "$t" "$m"'
  - topic: weekly
    command: 'notify-send --app-name=ntfy "$t" "$m"'
  - topic: monthly
    command: 'notify-send --app-name=ntfy "$t" "$m"'
```

Replace `https://ntfy.example.com` with your ntfy server URL and add your own topics.

The variables available in the command are:
- `$t` or `$title` - Message title
- `$m` or `$message` - Message body
- `$p` or `$priority` - Message priority (1-5)
- `$tags` - Comma-separated list of tags

### 3. Create the systemd User Service

Create `~/.config/systemd/user/ntfy-subscribe.service`:

```ini
[Unit]
Description=ntfy desktop notifications
After=network.target

[Service]
ExecStart=/usr/bin/ntfy subscribe --from-config
Restart=on-failure
RestartSec=10
Environment=DISPLAY=:0
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus

[Install]
WantedBy=default.target
```

The `DISPLAY` and `DBUS_SESSION_BUS_ADDRESS` environment variables ensure `notify-send` can communicate with your desktop session.

### 4. Enable and Start the Service

```bash
systemctl --user daemon-reload
systemctl --user enable --now ntfy-subscribe
```

### 5. Verify It's Working

Check the service status:

```bash
systemctl --user status ntfy-subscribe
```

Send a test notification:

```bash
curl -d "Test notification" https://ntfy.example.com/daily
```

You should see a desktop notification appear.

## Customizing Notifications

### Adding Icons

```yaml
subscribe:
  - topic: alerts
    command: 'notify-send --app-name=ntfy --icon=dialog-warning "$t" "$m"'
```

### Setting Urgency

```yaml
subscribe:
  - topic: alerts
    command: 'notify-send --app-name=ntfy --urgency=critical "$t" "$m"'
```

### Playing a Sound

```yaml
subscribe:
  - topic: alerts
    command: 'notify-send --app-name=ntfy "$t" "$m" && paplay /usr/share/sounds/freedesktop/stereo/message.oga'
```

## Troubleshooting

### Notifications Not Appearing

1. Check if the service is running:
   ```bash
   systemctl --user status ntfy-subscribe
   ```

2. Check logs for errors:
   ```bash
   journalctl --user -u ntfy-subscribe -f
   ```

3. Verify `notify-send` works manually:
   ```bash
   notify-send "Test" "This is a test"
   ```

4. Ensure your user ID matches in the `DBUS_SESSION_BUS_ADDRESS` path (replace `1000` with your actual UID from `id -u`)

## Conclusion

With this setup, you'll receive native desktop notifications for all your ntfy topics without needing to keep a browser tab open. The systemd service starts automatically on login and reconnects if the connection drops.
