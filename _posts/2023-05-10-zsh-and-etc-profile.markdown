---
layout: blog-post
title: "zsh and /etc/profile"
excerpt: "zsh and /etc/profile"
disqus_id: /2023/05/10/zsh-and-etc-profile/
tags:
    - Zsh
---

I just upgraded from zsh v5.5 to zsh v5.9 and some of my applications broke.

It seems the environment variable `$XDG_DATA_DIRS` was blanked out in the process.


[`$XDG_DATA_DIRS`](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html#introduction) holds the location of directories which can contain `.desktop` files.
The [`.desktop` files](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html) are basically application shortcuts in the Linux desktop world.


The `$XDG_DATA_DIRS` and several such variables are initialized by scripts placed in `/etc/profiles.d` folder. This folder is executed by the `/etc/profile` script.

Now, the twist is that the `/etc/profile` is only invoked by [bash shell](https://en.wikipedia.org/wiki/Bash_(Unix_shell))

zsh uses its own set of configuration files:
* `/etc/zsh/zprofile`
* `/etc/zsh/zshrc`
* `/etc/zsh/zlogin`
* `/etc/zsh/zshenv`

Most modern distros will have a mechanism where in /etc/zsh/zprofile will invoke the `/etc/profile` which in turn will invoke all the scripts placed inside `/etc/profiles.d` folder.

However, if you are using the older distro or a non-Desktop distros such as [CentOS](https://www.centos.org/), [RedHat](https://www.redhat.com/en), this might not be the case.

In that case, you need to setup that linkage manually. In my case, I created the file `/etc/zsh/zprofile` with the contents

```
emulate sh -c 'source /etc/profile'
```

One other thing I found that some distros might invoke `/etc/zprofile` , instead of `/etc/zsh/zprofile`.

In that case, you might want to symlink the files with 

```
sudo ln -s /etc/zsh/zprofile /etc/zprofile  
```