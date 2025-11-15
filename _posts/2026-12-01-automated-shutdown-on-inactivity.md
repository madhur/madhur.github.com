---
layout: post
title: "Automated Shutdown on Computer Inactivity"
excerpt: "Automated Shutdown on Computer Inactivity"
disqus_id: /2026/12/01/automated-shutdown-on-inactivity/
tags:
    - Linux
---

I needed my system to automatically shut down if idle during overnight hours (12 AM - 6 AM). Here's a user-level systemd implementation using `xprintidle` for idle detection.

## Requirements

- Arch Linux (or any systemd-based distro)
- X11 session (AwesomeWM in my case)
- `xprintidle` package

## Architecture

Three components:
1. Bash script to check idle time
2. Systemd service unit
3. Systemd timer unit

The timer triggers every 30 minutes between midnight and 6 AM. If idle time exceeds 30 minutes, the system shuts down.

## Implementation

### Idle Detection Script

```bash
#!/bin/bash

IDLE_THRESHOLD_MINUTES=30
LOG_FILE="$HOME/.local/log/idle-shutdown.log"

mkdir -p "$(dirname "$LOG_FILE")"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

check_time_window() {
    current_hour=$(date +%H)
    current_hour=$((10#$current_hour))
    
    if [ $current_hour -ge 0 ] && [ $current_hour -lt 6 ]; then
        return 0
    else
        return 1
    fi
}

get_idle_time() {
    idle_ms=$(xprintidle 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$idle_ms" ]; then
        echo $idle_ms
        return 0
    else
        log_message "ERROR: Failed to get idle time from xprintidle"
        return 1
    fi
}

main() {
    log_message "Script started - checking idle time"
    
    if ! check_time_window; then
        log_message "Outside time window (12 AM - 6 AM), exiting"
        exit 0
    fi
    
    log_message "Inside time window, checking idle time"
    
    idle_ms=$(get_idle_time)
    
    if [ $? -ne 0 ]; then
        log_message "ERROR: Could not determine idle time, aborting shutdown"
        exit 1
    fi
    
    idle_minutes=$((idle_ms / 60000))
    
    log_message "Current idle time: $idle_minutes minutes (threshold: $IDLE_THRESHOLD_MINUTES minutes)"
    
    if [ $idle_minutes -ge $IDLE_THRESHOLD_MINUTES ]; then
        log_message "SHUTDOWN: Idle time ($idle_minutes min) exceeds threshold ($IDLE_THRESHOLD_MINUTES min)"
        sudo /usr/bin/systemctl poweroff
    else
        log_message "System active - no shutdown needed"
    fi
}

main
```

Save to `~/.local/bin/idle-shutdown-check.sh` and make executable.

### Systemd Service Unit

```ini
[Unit]
Description=Check system idle time and shutdown if inactive
After=graphical-session.target

[Service]
Type=oneshot
ExecStart=%h/.local/bin/idle-shutdown-check.sh

[Install]
WantedBy=default.target
```

Save to `~/.config/systemd/user/idle-shutdown.service`.

### Systemd Timer Unit

```ini
[Unit]
Description=Timer for idle shutdown check (runs every 30 min between 12 AM - 6 AM)

[Timer]
OnCalendar=00/0:00,30
OnCalendar=01/0:00,30
OnCalendar=02/0:00,30
OnCalendar=03/0:00,30
OnCalendar=04/0:00,30
OnCalendar=05/0:00,30

[Install]
WantedBy=timers.target
```

Save to `~/.config/systemd/user/idle-shutdown.timer`.

Note: `Persistent=true` is intentionally omitted. With it, the timer would run on boot if a scheduled time was missed, which could cause unwanted shutdowns if you boot during the 12 AM - 6 AM window.

## Sudo Configuration

The script uses `sudo` for shutdown. Configure passwordless sudo for this specific command:

```bash
sudo visudo -f /etc/sudoers.d/shutdown-nopasswd
```

Add (replace `username`):
```
username ALL=(ALL) NOPASSWD: /usr/bin/systemctl poweroff
```

## Installation

```bash
# Create directories
mkdir -p ~/.local/bin ~/.local/log ~/.config/systemd/user

# Install script
chmod +x ~/.local/bin/idle-shutdown-check.sh

# Install systemd units
systemctl --user daemon-reload
systemctl --user enable idle-shutdown.timer
systemctl --user start idle-shutdown.timer

# Enable lingering (allows timer to run when not logged in)
sudo loginctl enable-linger $USER
```

## Verification

```bash
# Check timer status
systemctl --user list-timers idle-shutdown.timer

# View logs
tail -f ~/.local/log/idle-shutdown.log

# Test manually (safe during daytime)
~/.local/bin/idle-shutdown-check.sh
```
## Idle Detection Methods

`xprintidle` was chosen for X11 sessions as it directly queries the X server for time since last input event. Alternative methods include:

- `/dev/input/event*` modification times (requires root or group permissions)
- `loginctl show-session` idle hints
- `/proc/interrupts` for hardware interrupt counts

For X11 environments, `xprintidle` is the most straightforward approach.

## Notes

- Script only executes shutdown during the configured time window
- If `xprintidle` fails, script aborts (safe default)
- Timer continues running across logout (due to lingering)
- All actions logged for debugging

