---
layout: blog-post
title: "Hacking Router password using Hydra"
excerpt: Hacking Router password using Hydra
disqus_id: /2011/07/25/hackrouterpassword/
location: New Delhi, India
time: 9:00 PM
tags:
- Security
- Hacking
---



[Hydra](http://thc.org/thc-hydra/) is a popular password cracker which can be used to crack passwords from various services such as http, ftp, telnet etc.

Most of our internet is routed through a router which has a http interface. If you are using web browser, try typing 192.168.0.1 or 192.168.1.1 in the web browser
and see if the authentication prompt is issues. If yes, it is prompted most probably from your router. Router web interface is useful to configure port forwarding for torrents
or if you want to play multiplayer online games such as AOE etc. If you do not know the password of your router, hacking using hydra can be fun and easy. 

For example, if my router web interface is on 192.168.0.1, the simple command will be

{% highlight bash %}
hydra -l admin -P password.lst 192.168.1.1 http-get -m /
{% endhighlight %}

Here *password.lst* is the password list which contains the list of passwords to be bruteforced. **admin** is the username we will be trying for. The usernames can also be bruteforced with -L option.
