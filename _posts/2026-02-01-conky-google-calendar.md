---
layout: blog-post
title: "Displaying Google Calendar Events in Conky"
excerpt: "Displaying Google Calendar Events in Conky"
disqus_id: /2026/02/01/conky-google-calendar/
tags:
    - Conky
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

**Disclaimer**: This article was generated with assistance from AI and reflects a technical implementation discussion.

Conky is a popular system monitor for Linux desktops, but its capabilities extend beyond displaying CPU usage and memory stats. This guide shows how to integrate Google Calendar events into your Conky display using Python and Google's Calendar API, with proper support for recurring events.

## Why Use the API Instead of iCal?

While Google Calendar provides iCal feeds, they have significant limitations for recurring events:

- iCal feeds only include expanded instances for a limited time window
- Future recurring events beyond that window aren't included
- No control over the expansion period

The Google Calendar API with `singleEvents=true` parameter properly expands recurring events for any specified time range.

## Prerequisites

- Python 3.8+
- pipenv (for dependency management)
- A Google Cloud Console account
- Conky installed on your Linux system

## Setup Process

### 1. Create Service Account

Navigate to [Google Cloud Console](https://console.cloud.google.com/):

1. Create or select a project
2. Enable the Google Calendar API (APIs & Services → Library)
3. Create a Service Account (IAM & Admin → Service Accounts)
4. Generate a JSON key file for the service account
5. Download and save as `google_calendar_key.json`

### 2. Grant Calendar Access

The service account needs permission to read your calendar:

1. Open the JSON file and copy the `client_email` value
2. In Google Calendar, go to Settings → Your Calendar → Share with specific people
3. Add the service account email with "See all event details" permission

### 3. Project Structure

```bash
mkdir -p ~/.conky/calendar-project
cd ~/.conky/calendar-project
```

Create `Pipfile`:
```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
python-dotenv = "*"
google-auth = "*"
google-auth-oauthlib = "*"
google-auth-httplib2 = "*"
google-api-python-client = "*"

[dev-packages]

[requires]
python_version = "3.8"
```

Install dependencies:
```bash
pipenv install
```

### 4. Configuration

Create `.env` file:
```bash
GOOGLE_SERVICE_ACCOUNT_FILE=google_calendar_key.json
GOOGLE_CALENDAR_ID=primary
MAX_EVENTS=10
CACHE_DAYS=7
```

Set secure permissions:
```bash
chmod 600 .env google_calendar_key.json
```

### 5. Python Script

Create `get_calendar.py`:

```python
#!/usr/bin/env python3
import os
import socket
from datetime import datetime, timedelta
from pathlib import Path

try:
    from dotenv import load_dotenv
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    print(f"Missing dependencies: {e}")

# Load configuration
script_dir = Path(__file__).parent
env_file = script_dir / '.env'
if env_file.exists():
    load_dotenv(env_file)

SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'google_calendar_key.json')
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
MAX_EVENTS = int(os.getenv('MAX_EVENTS', '10'))
CACHE_DAYS = int(os.getenv('CACHE_DAYS', '7'))
CACHE_FILE = os.path.expanduser("~/.conky/calendar_cache.txt")
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def get_calendar_service():
    try:
        script_dir = Path(__file__).parent
        service_account_path = script_dir / SERVICE_ACCOUNT_FILE
        
        if not service_account_path.exists():
            raise FileNotFoundError(f"Service account file not found: {service_account_path}")
        
        credentials = service_account.Credentials.from_service_account_file(
            str(service_account_path), scopes=SCOPES
        )
        return build('calendar', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Error creating calendar service: {e}")
        return None

def get_events():
    try:
        service = get_calendar_service()
        if not service:
            return None
        
        now = datetime.now()
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=CACHE_DAYS)
        
        time_min = start_time.isoformat() + 'Z'
        time_max = end_time.isoformat() + 'Z'
        
        # Key parameter: singleEvents=True expands recurring events
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=MAX_EVENTS * 2,
            singleEvents=True,  # Expands recurring events
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        return events[:MAX_EVENTS]
    except Exception as e:
        print(f"Error fetching events: {e}")
        return None

def format_event(event):
    try:
        summary = event.get('summary', 'No Title')
        start = event.get('start', {})
        
        if 'dateTime' in start:
            dt_str = start['dateTime']
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00')).astimezone()
            time_str = dt.strftime('%m/%d %H:%M' if CACHE_DAYS > 1 else '%H:%M')
        elif 'date' in start:
            date_obj = datetime.fromisoformat(start['date'])
            time_str = date_obj.strftime('%m/%d All Day' if CACHE_DAYS > 1 else 'All Day')
        else:
            time_str = '??:??'
        
        # Truncate long summaries
        max_length = 35 if CACHE_DAYS > 1 else 40
        if len(summary) > max_length:
            summary = summary[:max_length-3] + '...'
        
        # Add recurring indicator
        if event.get('recurringEventId'):
            summary += " ↻"
        
        return f"{time_str} - {summary}"
    except Exception as e:
        return f"Error formatting event: {e}"

def load_cache():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                return f.read().strip()
    except Exception:
        pass
    return None

def save_cache(content):
    try:
        cache_dir = os.path.dirname(CACHE_FILE)
        os.makedirs(cache_dir, exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            f.write(content)
    except Exception as e:
        print(f"Error saving cache: {e}")

def main():
    if not DEPENDENCIES_AVAILABLE:
        print("Required dependencies not installed")
        return
    
    script_dir = Path(__file__).parent
    if not (script_dir / SERVICE_ACCOUNT_FILE).exists():
        print(f"Service account file not found: {SERVICE_ACCOUNT_FILE}")
        return
    
    if not check_internet():
        cached_content = load_cache()
        if cached_content:
            print(cached_content)
        else:
            print("No internet connection and no cached data")
        return
    
    events = get_events()
    
    if events is None:
        cached_content = load_cache()
        if cached_content:
            print("Using cached data:")
            print(cached_content)
        else:
            print("Unable to fetch calendar events")
        return
    
    if not events:
        days_text = f"next {CACHE_DAYS} day{'s' if CACHE_DAYS > 1 else ''}" if CACHE_DAYS > 1 else "today"
        output = f"No events {days_text}"
    else:
        formatted_events = [format_event(event) for event in events]
        output = '\n'.join(formatted_events)
    
    save_cache(output)
    print(output)

if __name__ == '__main__':
    main()
```

Make executable:
```bash
chmod +x get_calendar.py
```

### 6. Conky Integration

Add to your `.conkyrc`:

```lua
conky.text = [[
${color orange}${font DejaVu Sans Mono:bold:size=12}UPCOMING EVENTS${font}${color}
${hr 2}
${color lightblue}${exec cd ~/.conky/calendar-project && pipenv run python get_calendar.py}${color}
${hr 1}
]]
```

## Testing

```bash
cd ~/.conky/calendar-project
pipenv run python get_calendar.py
```

Expected output:
```
08/12 22:00 - Zendesk Redis Withdraw
08/16 08:00 - Weekly Reflection... ↻
08/19 All Day - Credit card bill ↻
```

## Key Features

- **Recurring Event Support**: The ↻ symbol indicates recurring events
- **Offline Caching**: Falls back to cached data when internet is unavailable
- **Configurable Time Range**: Adjust `CACHE_DAYS` for different periods
- **Timezone Awareness**: Properly handles timezone conversions
- **Error Handling**: Graceful degradation on API failures

## Configuration Options

| Variable | Description | Example |
|----------|-------------|---------|
| `CACHE_DAYS` | Days to look ahead | `7` (one week) |
| `MAX_EVENTS` | Maximum events to display | `10` |
| `CALENDAR_ID` | Which calendar to use | `primary` or email |

## Troubleshooting

**"Service account file not found"**
- Verify the JSON file is in the project directory
- Check the filename matches your `.env` configuration

**"Access denied"**
- Ensure the service account email has calendar permissions
- Wait a few minutes after sharing for propagation

**"No events found"**
- Verify `CALENDAR_ID` is correct
- Check if events exist in the specified time range
- Try increasing `CACHE_DAYS`

## Security Considerations

- Service account files contain sensitive credentials
- Use `chmod 600` on credential files
- Consider restricting API key to specific APIs in Google Cloud Console
- The service account only needs read access to calendars

## Limitations

- Requires internet connectivity for fresh data (cached data available offline)
- Service account must be shared with each calendar individually
- Google Calendar API has usage quotas (generous for personal use)

This implementation provides a robust solution for displaying calendar events in Conky with proper support for recurring events and offline functionality.