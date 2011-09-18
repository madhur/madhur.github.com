---
layout: blog-post
title: "Crack or Reset Windows Passwords"
excerpt: "Crack or Reset Windows Passwords"
disqus_id: /2011/09/18/crackresetwindows/
location: Delhi, India
time: 11:00 AM
categories:
- Hacking
- Windows
---

If you have forgotten the Windows Administrator password, you can either reset or even crack it.
Windows XP stored it username and password information in file named SAM at %SystemDrive%:\Windows\system32\config\. The SAM file is encrypted using LM hashes, which is vulnerable to rainbow table attack and bruteforce attack.

I am going to do this  with already available tools in Backtrack.

{% highlight text %}
cd /mnt/hda1/WINDOWS/system32/config/
bkhive system key
samdump2 SAM key > /root/pass1
{% endhighlight %}  

This will dump the hashes in /root/pass1 file as shown below

{% highlight text %}
Root Key : CMI-CreateHive{C4E7BA2B-68E8-499C-B1A1-371AC8D717C7}
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
madhurdesk:1000:aad3b435b51404eeaad3b435b51404ee:ba03a114def8d5c913983436960e592c:::
HomeGroupUser$:1002:aad3b435b51404eeaad3b435b51404ee:cdaac87aeeac96724b4a2af3c4879242:::
{% endhighlight %}  

Cracking using John the ripper,

{% highlight text %}
john --format=NT /root/pass1
Loaded 1 password hash (NT MD4 [128/128 SSE2 + 32/32])
{% endhighlight %} 

Or, you can directly reset it with chntpw

{% highlight text %}
/pentest/password/chntpw -u administrator SAM
{% endhighlight %}
