---
layout: post
title: "Systemd timer running on every boot"
excerpt: "Systemd timer running on every boot"
disqus_id: /2026/03/01/systemd-timer-running-every-boot/
tags:
    - Systemd
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

## Problem Description

A systemd timer configured with `OnCalendar=daily` and `Persistent=true` was executing its associated service on every system boot, in addition to the scheduled execution time. The expected behavior was execution only at the scheduled time, with persistent timers catching up on missed runs only when the system was offline during the scheduled time.

## Environment

- **System**: User systemd instance (`systemctl --user`)
- **Timer**: `rednotebook-backup.timer`
- **Service**: `rednotebook-backup.service`
- **Systemd version**: Standard systemd installation

## Observed Behavior

```
Aug 13 20:59:24 - Service executed after boot
-- Boot f6bac27bcb034b92807c437ec2834916 --
Aug 13 21:10:50 - Service executed after boot
-- Boot 18a831a9d19b415da72eb836e78ad866 --
Aug 13 21:11:20 - Service executed after boot
```

The service executed immediately after each boot, regardless of the last execution time or scheduled interval.

## Configuration Analysis

### Original Timer Configuration

```ini
[Unit]
Description=Run RedNotebook backup daily
Requires=rednotebook-backup.service

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

### Service Configuration

```ini
[Unit]
Description=RedNotebook GitHub Backup Service
After=network-online.target 
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=%h/bin/rednotebook-backup.sh
ExecStartPre=/bin/sleep 30
Environment=HOME=%h
StandardOutput=journal
StandardError=journal
Environment=SSH_AUTH_SOCK=%t/ssh-agent.socket
```

## Root Cause Analysis

The issue stems from the `Requires=rednotebook-backup.service` directive in the timer unit's `[Unit]` section.

### Systemd Dependency Resolution

1. **Timer activation**: The timer unit is started by `timers.target` during boot
2. **Dependency resolution**: Due to `Requires=rednotebook-backup.service`, systemd immediately activates the service unit when the timer starts
3. **Unintended execution**: The service executes on boot, independent of the timer schedule

### Systemd Timer Mechanics

Systemd timers automatically establish relationships with their target services through:

1. **Implicit naming convention**: `foo.timer` automatically targets `foo.service`
2. **Automatic dependencies**: Timer units gain an implicit `Before=` dependency on their target service
3. **No explicit linking required**: The `Unit=` directive in `[Timer]` section is only needed when targeting a service with a different name

From `systemd.timer(5)`:
> Timer units automatically gain a Before= dependency on the service they are supposed to activate.

## Solution

Remove the `Requires=` directive from the timer unit:

```ini
[Unit]
Description=Run RedNotebook backup daily
# Removed: Requires=rednotebook-backup.service

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

### Implementation

```bash
systemctl --user stop rednotebook-backup.timer
systemctl --user edit rednotebook-backup.timer
# Add override: [Unit]\nRequires=
systemctl --user daemon-reload
systemctl --user start rednotebook-backup.timer
```

## Verification

Post-fix timer state:

```
NEXT                            LEFT     LAST PASSED UNIT                     ACTIVATES                 
Thu 2025-08-14 00:02:17 IST    2h 54min  -    -      rednotebook-backup.timer rednotebook-backup.service
```

Multiple reboot test results:
- Service does not execute on boot
- Timer maintains correct scheduling
- Service executes only at scheduled intervals

## Related Issues

### Common Misconceptions

1. **Explicit linking requirement**: Many assume timers require explicit service dependencies
2. **Cargo-cult configuration**: Copy-pasting examples with unnecessary `Requires=` directives
3. **Documentation gaps**: Some tutorials incorrectly show `Requires=` as standard practice

### Alternative Diagnostic Approaches

If removing `Requires=` doesn't resolve the issue:

1. **Check service enablement**:
   ```bash
   systemctl --user is-enabled rednotebook-backup.service
   ```
   Services triggered by timers should show `static` or `disabled`

2. **Verify service dependencies**:
   ```bash
   systemctl --user list-dependencies rednotebook-backup.service
   ```

3. **Check for WantedBy directives**: Remove `WantedBy=` from service `[Install]` section

### Timer State Management

Systemd maintains timer state in:
- System timers: `/var/lib/systemd/timers/`
- User timers: `~/.local/share/systemd/`

State corruption can cause similar symptoms but is less common than configuration issues.

## Technical References

- `systemd.timer(5)` - Timer unit configuration
- `systemd.unit(5)` - Unit configuration directives  
- `systemd.special(7)` - Special systemd units
- [systemd GitHub Issue #14642](https://github.com/systemd/systemd/issues/14642) - Timer runs on every boot

## Conclusion

The `Requires=` directive in systemd timer units creates an unnecessary dependency that causes service execution on timer activation (boot). Systemd's implicit timer-to-service binding mechanism eliminates the need for explicit dependencies in standard configurations. This issue affects both user and system timer units and represents a common configuration anti-pattern in systemd timer implementations.