---
layout: post
title: "Setting up SMTP Mail Relay with msmtpd and systemd Socket Activation"
excerpt: "Setting up SMTP Mail Relay with msmtpd and systemd Socket Activation"
disqus_id: /2026/07/01/setup-email-smtp-relay-gmail/
tags:
    - Linux
    - Email
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

Setting up a local SMTP daemon can be incredibly useful for applications that need to send emails. Instead of running a full-featured mail server like Postfix, you can use `msmtpd` with `msmtp` as a lightweight SMTP relay that forwards emails through external providers like Gmail. This guide shows you how to set up `msmtpd` with systemd socket activation for an efficient, on-demand mail relay service.

## Why msmtpd + msmtp?

**msmtp** is a lightweight SMTP client that can relay emails through external SMTP servers (like Gmail's). **msmtpd** is the daemon version that provides a local SMTP server interface, making it perfect for:

- Applications that need to send emails via SMTP
- Development environments requiring mail functionality
- Lightweight mail relay without running a full mail server
- **Gmail integration** - easily send emails through your Gmail account

## Prerequisites

Install the required packages:

```bash
# Ubuntu/Debian
sudo apt install msmtp msmtp-mta

# Arch Linux  
sudo pacman -S msmtp

# RHEL/CentOS/Fedora
sudo dnf install msmtp
```

## Step 1: Configure msmtp Client

First, create the msmtp configuration file. You can place it in `/etc/msmtprc` for system-wide use or `~/.msmtprc` for user-specific configuration:

```bash
# Create system-wide configuration
sudo nano /etc/msmtprc
```

Add your Gmail SMTP configuration:

```ini
# Default values for all accounts
defaults
auth           on
tls            on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        /var/log/msmtp.log

# Gmail account configuration
account        gmail
host           smtp.gmail.com
port           587
from           your-email@gmail.com
user           your-email@gmail.com
password       your-app-password

# Set default account
account default : gmail
```

**Important**: For Gmail, you'll need to:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password (not your regular password)
3. Use the App Password in the configuration above

Set proper permissions:

```bash
# For system-wide config
sudo chmod 600 /etc/msmtprc
sudo chown root:root /etc/msmtprc

# For user config
chmod 600 ~/.msmtprc
```

## Step 2: Test msmtp Client

Verify your msmtp configuration works:

```bash
# Test the configuration
echo "Test message body" | msmtp --debug your-recipient@gmail.com

# Or use mail command
echo "This is a test" | mail -s "Test Subject" your-recipient@gmail.com
```

## Step 3: Create systemd Socket Unit

Now let's set up the systemd socket that will listen on port 25:

```bash
sudo systemctl edit --force --full msmtpd.socket
```

Add the following configuration:

```ini
[Unit]
Description=msmtp daemon socket
Documentation=man:msmtpd(1)

[Socket]
ListenStream=25
Accept=yes

[Install]
WantedBy=sockets.target
```

**Key points**:
- `ListenStream=25` - Listen on SMTP port 25
- `Accept=yes` - Each connection gets its own service instance
- Socket activation means the daemon only runs when needed

## Step 4: Create systemd Service Template

Create the service template that handles incoming SMTP connections:

```bash
sudo systemctl edit --force --full msmtpd@.service
```

Add this configuration:

```ini
[Unit]
Description=msmtp daemon
Documentation=man:msmtpd(1)

[Service]
ProtectHome=false
PrivateTmp=true
NoNewPrivileges=true

StandardInput=socket
ExecStart=/usr/bin/msmtpd --inet --command='/usr/bin/msmtp -C /etc/msmtprc -f %i'
```

**Configuration explanation**:
- `ProtectHome=false` - Allows access to home directories (needed if config is in `/home`)
- `StandardInput=socket` - Receives the socket connection from systemd
- `%i` - systemd specifier replaced with instance identifier
- The `@` in the filename makes this a template unit

## Step 5: Enable and Start the Socket

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable and start the socket
sudo systemctl enable msmtpd.socket
sudo systemctl start msmtpd.socket

# Check status
sudo systemctl status msmtpd.socket

# Verify it's listening on port 25
sudo ss -tlnp | grep :25
```

## Testing Your SMTP Daemon

### netcat (Automated Test)

```bash
{
echo "EHLO localhost"
sleep 1
echo "MAIL FROM:<your-email@gmail.com>"
sleep 1  
echo "RCPT TO:<ahuja.madhur@gmail.com>"
sleep 1
echo "DATA"
sleep 1
echo "Subject: Test via SMTP daemon"
echo ""
echo "This is a test message sent through the msmtpd daemon."
echo "."
sleep 1
echo "QUIT"
} | nc localhost 25
```

## Monitoring and Troubleshooting

### Check Service Status

```bash
# Monitor socket status
sudo systemctl status msmtpd.socket

# Watch for active service instances
watch 'systemctl list-units | grep msmtpd@'

# Check logs
sudo journalctl -f -u msmtpd.socket -u "msmtpd@*"
```

## Socket Activation Benefits

This setup provides several advantages:

1. **On-demand activation**: The daemon only runs when there are connections
2. **Resource efficient**: No memory usage when idle  
3. **Concurrent connections**: Multiple simultaneous SMTP sessions
4. **Fast response**: Socket is always ready, service starts instantly
5. **Automatic cleanup**: Service instances exit after handling connections

## Sending to Gmail Successfully

The beauty of this setup is that **your local applications can send emails to Gmail** (or any email address) through your local SMTP port 25, and msmtpd will relay them through Gmail's SMTP servers. This is perfect for:

- Web applications needing to send notifications
- System monitoring scripts sending alerts  
- Development environments testing email functionality
- Any application that needs SMTP without running a full mail server


## Conclusion

With msmtpd and systemd socket activation, you now have a lightweight, efficient SMTP relay that can send emails through Gmail. The socket activation ensures resources are only used when needed, while the template service allows handling multiple concurrent connections.

Your applications can now send emails by connecting to `localhost:25`, and msmtpd will handle the relay through Gmail's SMTP servers. This setup is perfect for development, testing, or production environments that need simple mail relay functionality without the complexity of a full mail server.

---

*Have questions or run into issues? The systemd journal (`journalctl`) is your friend for debugging, and the msmtp documentation (`man msmtp`) provides additional configuration options.*