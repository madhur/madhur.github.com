---
slug: "brave-downloads-hang-dbus-display-vnc"
title: >-
  Brave Hung on Every Download, and the Culprit Was a Single DISPLAY=:1 Line for
  My VNC Session
date: '2028-02-01'
year: '2028'
month: '2028-02'
description: >-
  Every download in Brave produced a strange .org.chromium.Chromium.XXXXXX file
  and then froze the browser, and a keyring-backed app stopped showing its unlock
  prompt. Both traced back to one dbus-update-activation-environment call that
  pointed the whole user session at my VNC display.
tags:
  - Linux
  - Debugging
  - D-Bus
  - Brave
  - VNC
draft: false
params:
  disqus_id: /2028/02/01/brave-downloads-hang-dbus-display-vnc/
---

> **Author's Note:** I debugged this with Claude Code. The investigation and the evidence are real; I've kept the dead ends in because they're the useful part.

One day Brave stopped finishing downloads. Every file landed in `~/Downloads` as `.org.chromium.Chromium.a1B2c3`, and then the browser froze until I killed it. A day later an app that stores its secrets in the GNOME keyring (`zapfast`) stopped showing its unlock prompt. These looked like two unrelated bugs. They weren't.

## What the Strange Files Are

`.org.chromium.Chromium.XXXXXX` is Chromium's in-progress download name. A download only gets its real name when it completes, so every one of those files was a download that never finished. I had four, two of them 85 MB.

That told me *what* was left behind, not *why*. So I ruled things out first:

- **Disk:** ext4, 48 GB free. Creating, renaming and deleting a file in `~/Downloads` worked fine.
- **Brave itself:** a package update had landed that day, which explained two of the temp files (downloads cut off by the restart), but not the freezes that kept happening afterwards.

## The Evidence That Mattered

Every freeze lined up with a log line from the file-chooser portal:

```
xdg-desktop-portal-gtk: Failed to create foreign window for XID 44040196
xdg-desktop-portal-gtk: Failed to associate portal window with parent window x11:0x2a00004
```

Chromium on Linux asks `xdg-desktop-portal` to draw its save dialog. The portal backend has to parent that dialog to Brave's window. Here it couldn't. The dialog never appeared, and Brave sat waiting for an answer from a window nobody could see.

My first guess was a portal misconfiguration: the log said `Choosing gtk.portal … as a last-resort fallback`, so I wrote a `portals.conf` pinning the file chooser to the GTK backend and restarted the services. Same problem. (That file turned out to be harmless but unnecessary.)

## The Real Cause: One Line in My VNC Config

"Parent window not found" means the portal was looking for Brave's window on the wrong X display. I run the real desktop on `:0` and a VNC session on `:1`, so I checked what display the portal process had:

```bash
tr '\0' '\n' < /proc/$(pgrep -f xdg-desktop-portal-gtk | head -1)/environ | grep ^DISPLAY=
# DISPLAY=:1
```

Brave was on `:0`. The portal was on `:1`. And the user session's shared environment agreed with the portal:

```bash
systemctl --user show-environment | grep DISPLAY
# DISPLAY=:1
```

The source was one line in my VNC window-manager config:

```lua
awful.spawn.with_shell("dbus-update-activation-environment --systemd DISPLAY=:1")
```

I had added it the day before so that keyring unlock dialogs would show up inside the VNC session. The comment I'd written even described the catch: *"when the real display starts later it overwrites this, so prompts follow the most recently started one."* What I'd underweighted is that this environment is **shared by the whole user session**. Everything D-Bus-activates afterwards inherits it, not just the keyring prompter.

`xdg-desktop-portal-gtk` is D-Bus-activated, so it started with `DISPLAY=:1`. That's the whole Brave bug. The timeline matched too: the edit was at 19:09, and the first stuck temp file was at 20:22 that evening.

## The Second Bug Was the Same Bug

The keyring prompter, `gcr-prompter`, is also D-Bus-activated and also inherited `DISPLAY=:1`. I reset the session to `:0` and commented out the line, and the unlock prompt still didn't show up. Two more things were going on:

1. **A stale prompter.** An instance started earlier was still running with `DISPLAY=:1`, so unlock dialogs kept opening on the VNC display. `kill` fixed that, and D-Bus re-activated it on `:0`.
2. **A wedged keyring daemon.** After that, I asked the Secret Service to unlock the keyring and call `Prompt`, the same way a real client does. The daemon accepted both calls and never started the prompter. Its log was full of `G_IS_DBUS_CONNECTION … failed` assertions.

To reproduce what a client does, you need one process holding the D-Bus connection for both calls. With `busctl` the prompt object vanishes as soon as the first call's connection closes, so I used a small Python script with `Gio`:

```python
import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib
b = Gio.bus_get_sync(Gio.BusType.SESSION, None)
S = "org.freedesktop.secrets"
svc = "org.freedesktop.Secret.Service"
coll = "/org/freedesktop/secrets/collection/Default_5fKeyring"
r = b.call_sync(S, "/org/freedesktop/secrets", svc, "Unlock",
                GLib.Variant("(ao)", ([coll],)), None, 0, 5000, None)
prompt = r.unpack()[1]
b.call_sync(S, prompt, "org.freedesktop.Secret.Prompt", "Prompt",
            GLib.Variant("(s)", ("",)), None, 0, 5000, None)
```

Restarting the daemon fixed it:

```bash
systemctl --user restart gnome-keyring-daemon.service gnome-keyring-daemon.socket
```

After the restart the prompter started on `:0` and the dialog appeared. I don't know why the daemon wedged. The errors began after the display changes, but the log doesn't say what triggered them, so treat "the display mix-up wedged it" as a guess.

Restarting the daemon locks every keyring, including `login`, so expect a password prompt afterwards.

## The Fix

1. Reset the session display: `dbus-update-activation-environment --systemd DISPLAY=:0`
2. Restart the portal services so they re-activate with it.
3. Delete the `DISPLAY=:1` line from the VNC config, with a comment saying why.
4. Kill the stale `gcr-prompter` and restart `gnome-keyring-daemon`.
5. Delete the leftover `.org.chromium.Chromium.*` files (after checking nothing had them open).

## Lessons

- **`dbus-update-activation-environment` is global.** It isn't "this display's setting". It changes what every service activated afterwards sees, so a per-display tweak for one prompt can break unrelated apps.
- **Check a process's environment, not your shell's.** `/proc/<pid>/environ` showed the problem in one command. My shell said `DISPLAY=:0` all along.
- **Portal errors about parent windows usually mean the wrong display.** `Failed to associate portal window with parent window` is worth checking against `DISPLAY` before touching portal config.
- **Restarting a service doesn't reset its environment.** D-Bus-activated services take their environment from the activation environment at start time, so my first portal restart simply re-inherited `:1`.
- **Date your own config changes.** The cause was a line I'd added the day before. Comparing file modification times against the first symptom was the quickest way to find it.

## Trade-off I Accepted

With that line gone, keyring unlock prompts only appear on `:0`, never in the VNC session. For now I'd rather have a keyring prompt on the wrong display than a browser that freezes on every download. If I want both, the answer is a per-display mechanism, not the shared activation environment.
