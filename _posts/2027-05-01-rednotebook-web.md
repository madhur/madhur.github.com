---
layout: blog-post
title: "RedNotebook Web: A Self-Hostable Web Interface for RedNotebook"
excerpt: "How I built a full-stack web interface for the RedNotebook journal app using FastAPI and React, with Docker packaging and PWA support."
disqus_id: /2027/05/01/rednotebook-web/
tags:
    - Self-Hosting
    - Python
    - React
    - Docker
    - Journal
---

*This article was written with the assistance of AI.*

---

I've been using [RedNotebook](https://rednotebook.app/) as my daily journal for years. It's a solid desktop application—offline, open-source, and stores entries in plain YAML files. The one thing it lacks is a web interface, which means I can't write journal entries from my phone or from any machine where the desktop app isn't installed.

I decided to build one.

## The Problem

RedNotebook stores all data in `~/.rednotebook/data/` as monthly YAML files:

```
~/.rednotebook/data/
├── 2024-01.txt
├── 2024-02.txt
└── 2026-03.txt
```

Each file is a YAML map where the top-level keys are day numbers:

```yaml
1:
  text: "Today I started a new project..."
  tags:
    work: null
22:
  text: "Finished the web interface."
  tags:
    coding: null
    projects: null
```

The constraint was non-negotiable: the web interface had to read and write this exact format, with zero migration. I still want to open the desktop app on my laptop and see everything I wrote on my phone.

## The Solution

[RedNotebook Web](https://github.com/madhur/rednotebook-web) is a self-hosted web application that provides full read/write access to your RedNotebook data. The backend is FastAPI serving a React frontend, packaged as a single Docker container.

### Architecture

```
rednotebook-web/
├── backend/
│   └── main.py          # FastAPI app + JournalService
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── Editor.tsx
│   │   ├── Calendar.tsx
│   │   ├── SearchModal.tsx
│   │   └── TagSidebar.tsx
│   └── vite.config.ts
└── Dockerfile
```

FastAPI serves the production build of the React app as static files, so there's only one process to run and one port to expose.

## Backend: FastAPI + PyYAML

The backend is a single `main.py` file with a `JournalService` class that handles all file I/O:

```python
class JournalService:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir).expanduser()
        self._lock = threading.RLock()
        self._cache: dict[str, dict] = {}

    def get_entry(self, year: int, month: int, day: int) -> str:
        with self._lock:
            data = self._load_month(year, month)
            return data.get(day, {}).get("text", "")

    def save_entry(self, year: int, month: int, day: int, text: str):
        with self._lock:
            data = self._load_month(year, month)
            if day not in data:
                data[day] = {}
            data[day]["text"] = text
            self._save_month(year, month, data)
```

File writes are atomic—write to a `.new` file first, then rename:

```python
def _save_month(self, year: int, month: int, data: dict):
    path = self._month_path(year, month)
    new_path = path.with_suffix(".new")
    old_path = path.with_suffix(".old")

    with open(new_path, "w") as f:
        yaml.dump(data, f, allow_unicode=True)

    if path.exists():
        path.rename(old_path)
    new_path.rename(path)
    if old_path.exists():
        old_path.unlink()
```

This ensures a crash mid-write never corrupts the data file.

The API surface is minimal:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/entries/{year}/{month}/{day}` | Read a day's entry |
| PUT | `/api/entries/{year}/{month}/{day}` | Write a day's entry |
| GET | `/api/entries/{year}/{month}` | Get all days with entries for a month |
| GET | `/api/months` | List all months that have data |
| GET | `/api/search` | Full-text search across all entries |
| GET | `/api/tags` | Get all hashtags with counts |

## Frontend: React + CodeMirror

The editor is CodeMirror 6 with markdown syntax highlighting. The state management splits neatly into two layers:

- **Zustand** for UI state (current date, which view is active)
- **TanStack Query** for server state (entry content, search results, tag list)

Auto-save triggers after 2 seconds of inactivity using a debounced mutation:

```typescript
const saveMutation = useMutation({
    mutationFn: (text: string) => saveEntry(year, month, day, text),
});

const debouncedSave = useMemo(
    () => debounce((text: string) => saveMutation.mutate(text), 2000),
    [year, month, day]
);
```

The calendar shows which days have entries by fetching the month summary on navigation:

```typescript
const { data: monthSummary } = useQuery({
    queryKey: ["month", year, month],
    queryFn: () => getMonthSummary(year, month),
});
```

Days with entries are highlighted, giving you a quick visual overview of how often you've been writing.

## Features

**Full-text search**: Searches across all YAML files in real time. The backend iterates over all month files and returns matching entries with surrounding context.

**Hashtag sidebar**: RedNotebook supports `#hashtags` inline in entries. The sidebar lists all tags with counts and filters the view when clicked.

**Dark mode**: Toggled with a button, persisted to `localStorage`.

**Responsive layout**: On mobile, the sidebar collapses behind a hamburger menu. The editor and calendar stack vertically.

**PWA**: Installable on Android and iOS via the browser's "Add to Home Screen". Requires HTTPS in production (localhost works without it).

## Deployment

The simplest setup with Docker Compose:

```yaml
services:
  rednotebook-web:
    image: ghcr.io/madhur/rednotebook-web:latest
    ports:
      - "8000:8000"
    volumes:
      - ~/.rednotebook/data:/data
    environment:
      - JOURNAL_DATA_DIR=/data
```

```bash
docker compose up -d
```

Open `http://localhost:8000` and you're done. The desktop app and web interface can run simultaneously—both read and write the same files, and the locking in `JournalService` prevents corruption on the web side.

## What I Learned

**YAML append semantics matter.** PyYAML's `dump` doesn't preserve the original file's formatting or key order. RedNotebook's own parser is lenient enough that this doesn't break anything, but it's worth knowing if you try to diff the files manually.

**CodeMirror 6 setup is verbose.** The API is extremely flexible but requires wiring together several extension packages to get a basic markdown editor with keybindings. Worth the effort once you understand the extension model, but the documentation assumes you already know what you need.

**Single-container packaging simplifies self-hosting.** Serving the React build from FastAPI means users don't need to think about a reverse proxy for the frontend. One container, one port, one thing to update.

## Source Code

The full source is at [github.com/madhur/rednotebook-web](https://github.com/madhur/rednotebook-web). The project was built end-to-end using [Claude Code](https://claude.ai/claude-code).
