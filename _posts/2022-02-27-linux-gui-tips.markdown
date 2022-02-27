---
layout: blog-post
title: "Linux GUI Tips"
excerpt: "Linux GUI Tips"
disqus_id: /2022/02/27/linux-gui-tips/
tags:    
    - Linux
---

### Show hidden files in file chooser dialog boxes

By Default, Linux Desktop enviornments such as Gnome, Cinnamon, Xfce do not display hidden files in file chooser dialog boxes. I found it to be really inconvienent.

The fix depends on the GTK version used by the application.

For GTK 3.0
```
gsettings set org.gtk.Settings.FileChooser show-hidden true  
```

For GTK 2.0, enter the following in `~/.config/gtk-2.0/gtkfilechooser.ini`

```
ShowHidden=true
```

### Setting up default session for User
If the user has multiple DE's installed such as Gnone, Xfce, Cinnamon etc, the default environment is configured in 
```
/var/lib/AccountsService/users
```

```
[com.redhat.AccountsServiceUser.System]
id='centos'
version-id='8'

[org.freedesktop.DisplayManager.AccountsService]
BackgroundFile='/home/madhur/Desktop/1r1kk9qi00961.png'

[User]
Language=en_US.utf8
Session=xfce
XSession=bspwm
Icon=/usr/share/cinnamon/faces/2_10.png
SystemAccount=false
```

This is atleast the case for Redhat based systems such as Fedora.

If you want the user to get the option to choose the session before logging in, better install the greeter such as [lightdm-gtk-greeter](https://github.com/Xubuntu/lightdm-gtk-greeter) for [LightDM](https://github.com/canonical/lightdm) display manager.
There are others available similarly for [GDM](https://wiki.gnome.org/Projects/GDM) display manager

There are various suggestions to user `~/.xinitrc` . Note that this file is not used in case of interactive graphical login. It is only used whn starting from terminal such as `startx`

