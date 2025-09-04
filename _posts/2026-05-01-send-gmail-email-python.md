---
layout: post
title: "How to Send Emails from Python Using msmtp and Gmail"
excerpt: "How to Send Emails from Python Using msmtp and Gmail"
disqus_id: /2026/05/01/send-gmail-email-python/
tags:
    - Linux
    - Email
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

When building monitoring scripts or automation tools in Python, you often need to send email notifications. While you could use Python's built-in `smtplib` directly with Gmail, this approach requires hardcoding credentials in your code. A cleaner solution is to use **msmtp** as an email relay, keeping your authentication separate from your Python scripts.

In this guide, we'll set up msmtp with Gmail and create Python scripts that can send emails without exposing credentials.

## Why Use msmtp?

- **Security**: Keep Gmail credentials out of your Python code
- **Centralized Configuration**: One configuration file for all scripts
- **Lightweight**: No need for heavy mail servers like Postfix
- **Reliable**: Battle-tested SMTP client
- **Easy Maintenance**: Change email providers without touching your code

## Prerequisites

- Linux system with msmtp installed
- Gmail account with 2-Factor Authentication enabled
- Python 3.6+ 

## Step 1: Install msmtp

```bash
# Ubuntu/Debian
sudo apt install msmtp

# CentOS/RHEL/Fedora
sudo dnf install msmtp

# Arch Linux
sudo pacman -S msmtp
```

## Step 2: Generate Gmail App Password

Since Gmail requires 2FA for app passwords:

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Go to **App passwords** section
4. Select **Mail** as the app type
5. Generate a 16-character app password
6. **Important**: Copy this password without spaces or dashes

## Step 3: Configure msmtp

Create the msmtp configuration file:

```bash
# Create config file
touch ~/.msmtprc
chmod 600 ~/.msmtprc

# Edit configuration
nano ~/.msmtprc
```

Add the following configuration:

```bash
# Default settings
defaults
auth           on
tls            on
tls_starttls   off
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        ~/.msmtp.log

# Gmail account
account        default
host           smtp.gmail.com
port           465
from           your-email@gmail.com
user           your-email@gmail.com
password       your16characterapppassword
```

**Replace:**
- `your-email@gmail.com` with your actual Gmail address
- `your16characterapppassword` with the app password (no spaces/dashes)

## Step 4: Test msmtp Configuration

Test that msmtp works:

```bash
echo "Hello from msmtp!" | msmtp your-email@gmail.com
```

If successful, you should receive the email. Check logs if there are issues:

```bash
tail ~/.msmtp.log
```

## Step 5: Python Integration

Now you can send emails from Python using msmtp:

### Simple Email Function

```python
import subprocess
from datetime import datetime

def send_email_via_msmtp(recipient, subject, body, account="default"):
    """Send email using msmtp - no credentials needed!"""
    
    # Create email message with proper headers
    email_message = f"""From: system@localhost
To: {recipient}
Subject: {subject}
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}

{body}"""
    
    try:
        # Use msmtp command
        cmd = ['msmtp', '-a', account, recipient]
        
        result = subprocess.run(
            cmd, 
            input=email_message, 
            text=True,
            capture_output=True,
            check=True,
            timeout=30
        )
        
        print(f"✅ Email sent successfully to {recipient}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ msmtp failed: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Email sending timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

# Usage example
send_email_via_msmtp(
    "your-email@gmail.com",
    "Test Email from Python",
    "This email was sent using Python and msmtp!"
)
```

### Advanced Email with Attachments

```python
import subprocess
import os
from email.message import EmailMessage
from datetime import datetime

class MsmtpMailer:
    def __init__(self, account="default", sender="system@localhost"):
        self.account = account
        self.sender = sender
    
    def send_email(self, recipients, subject, body, attachments=None):
        """Send email with optional attachments via msmtp"""
        
        if isinstance(recipients, str):
            recipients = [recipients]
        
        success_count = 0
        
        for recipient in recipients:
            if self._send_to_recipient(recipient, subject, body, attachments):
                success_count += 1
        
        return success_count == len(recipients)
    
    def _send_to_recipient(self, recipient, subject, body, attachments):
        """Send email to a single recipient"""
        
        # Create email message
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # Add attachments
        if attachments:
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    with open(attachment_path, 'rb') as f:
                        file_data = f.read()
                        file_name = os.path.basename(attachment_path)
                        
                        # Determine MIME type
                        if attachment_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            maintype, subtype = 'image', attachment_path.split('.')[-1]
                            if subtype == 'jpg': subtype = 'jpeg'
                        else:
                            maintype, subtype = 'application', 'octet-stream'
                        
                        msg.add_attachment(file_data, maintype=maintype, 
                                         subtype=subtype, filename=file_name)
        
        try:
            cmd = ['msmtp', '-a', self.account, recipient]
            
            result = subprocess.run(
                cmd,
                input=msg.as_string(),
                text=True,
                capture_output=True,
                check=True,
                timeout=30
            )
            
            print(f"✅ Email sent to {recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send to {recipient}: {e}")
            return False

# Usage examples
mailer = MsmtpMailer()

# Simple email
mailer.send_email(
    "your-email@gmail.com",
    "Python Notification",
    "Server monitoring alert: CPU usage is high!"
)

# Email with multiple recipients and attachment
mailer.send_email(
    ["admin@example.com", "your-email@gmail.com"],
    "Daily Report",
    "Please find the daily system report attached.",
    attachments=["system_report.pdf", "usage_chart.png"]
)
```

### System Monitoring Example

```python
import psutil
import subprocess
from datetime import datetime

def check_system_and_alert():
    """Check system resources and send alerts if needed"""
    
    # Check CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    alerts = []
    
    if cpu_percent > 80:
        alerts.append(f"🔥 High CPU usage: {cpu_percent}%")
    
    if memory.percent > 85:
        alerts.append(f"💾 High memory usage: {memory.percent}%")
    
    if disk.percent > 90:
        alerts.append(f"💿 Low disk space: {disk.percent}% used")
    
    if alerts:
        subject = f"🚨 System Alert - {len(alerts)} issue(s) detected"
        
        body = f"""System Alert Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Issues Detected:
{''.join(f'• {alert}' for alert in alerts)}

System Summary:
• CPU Usage: {cpu_percent}%
• Memory Usage: {memory.percent}%
• Disk Usage: {disk.percent}%

Please investigate these issues promptly.
"""
        
        send_email_via_msmtp("your-email@gmail.com", subject, body)

# Run the check
check_system_and_alert()
```

## Step 6: Automating with Cron/Systemd

### Cron Example

```bash
# Edit crontab
crontab -e

# Add entry to run every 15 minutes
*/15 * * * * /usr/bin/python3 /path/to/your/monitor_script.py
```

### Systemd Timer Example

Create a service file:

```ini
# /etc/systemd/system/system-monitor.service
[Unit]
Description=System Monitor
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/your/monitor_script.py
User=your-username
```

Create a timer file:

```ini
# /etc/systemd/system/system-monitor.timer
[Unit]
Description=Run System Monitor every 15 minutes
Requires=system-monitor.service

[Timer]
OnCalendar=*:0/15
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable system-monitor.timer
sudo systemctl start system-monitor.timer
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify 2FA is enabled on Gmail
   - Regenerate app password
   - Check for spaces/dashes in password

2. **TLS Handshake Failed**
   - Try port 587 with `tls_starttls on`
   - Update certificate bundle path

3. **Permission Denied**
   - Check file permissions: `chmod 600 ~/.msmtprc`

### Debug Commands

```bash
# Test msmtp with debug output
echo "test" | msmtp -d your-email@gmail.com

# Check msmtp log
tail -f ~/.msmtp.log

# Test server connection
msmtp --serverinfo -a default
```
## Conclusion

Using msmtp with Python provides a clean separation between email configuration and application code. This approach offers better security, maintainability, and flexibility compared to hardcoding SMTP credentials in your scripts.

The combination of msmtp's reliability and Python's flexibility makes it an excellent choice for system monitoring, alerting, and automation tasks.

---

*Have questions or suggestions? Feel free to reach out in the comments below!*