---
layout: blog-post
title: "Linux Tips and Tricks"
excerpt: "Linux Tips and Tricks"
disqus_id: /2022/11/20/linux-tips-tricks/
tags:
    - Linux
---

## Unuseable terminal in IntelliJ Flatpak apps

If you have installed Intellij apps via Flatpak, the terminal doesn't work  properly, i.e. it won't load the default shell properly.

To work around this, Add the custom command in Settings -> Tools -> Terminal and set the Shell Path as (replace zsh with preferred shell)

```shell
/usr/bin/flatpak-spawn --host --env=TERM=xterm-256color zsh
```


## Select all functionality in terminal

One of my favorite functionality is to output lot of text in terminal and copy it to clipboard.

Sadly, many popular terminal softwares, lack the Select All functionality.

It can be achieved in one of my favorite terminals [Kitty](https://sw.kovidgoyal.net/kitty/) using the following configuration

```
map ctrl+a launch --type=clipboard  --stdin-source=@screen_scrollback
```

## Disable screensaver and DPMS in linux

To disable DMPS (Which turns the monitor off after specified time)

```
xset -dpms
```

To disable screensaver
```
xset s off
```

