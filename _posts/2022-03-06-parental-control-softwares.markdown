---
layout: blog-post
title: "Parental Control Softwares for Windows and Linux"
excerpt: "Parental Control Softwares for Windows and Linux"
disqus_id: /2022/03/06/parental-control-softwares/
tags:    
    - Linux
    - Widnows
    - Kids
---

With this pandemic and kids taking classes online from their devices such as Laptops and PCs, it is important that kids do not spend too much spend online and use PCs and laptops only for learning purposes.

My own kid had started playing online games teaming up with his school friends over Google Meet / Zoom.

These online games can be so addictive that having a conversation or arguing with your child does not work, as they crave for the dopamine hits which these online gaming gives.

In this post, I will tell you my experience of researching solutions to this problem:

### Have a frank conversation with your kid

Have a frank conversation about your kid of the dangers of excessive gaming and become addicted to it. There is a difference between playing for couple of hours just for re-creation versus craving for classes to become over and jump onto online gaming. 

Observe, if he is just playing for recreation or there are signs of addiction. Signs of addiction include having food / water at computer table and loss of interests in other activities such as Sports, friends etc.

### Impose Parental control softwares

Tell your kid that you are imposing parental control softwares and that is for his benefit.

The kind of software you are using depends on the Operating System. For windows, I found it helpful to use [QuStudio](https://www.qustodio.com/en/premium/?utm_source=google&utm_medium=cpc&utm_term=brand&utm_campaign=adw_ww_web_brand___brand_ww-Qustodio-WW-B-BMM-All-DT+TA-SE-XX-XX&gclsrc=aw.ds&gclid=CjwKCAiAsYyRBhACEiwAkJFKoq9AukincL-Mjbc62801CyQnNRXMtaN2XPXxUFkNj6TJtwW6OJPF-hoCRPIQAvD_BwE/)

Even with the free version, you can block websites very easily and infact, I prefer to have a whitelist mode where you can just enable specific websites which are needed for kids education and block everything else.

### Install Linux

Apart from freeing distraction from Linux, I wanted my kid to have genuine interest in Computers, Technology and Coding. To enable that interest and curiosity, its much better to have your kid work on Linux rather than Windows. Linux is much more customizable than Windows and somehow I feel is better choice for kids to start working on.

For start, you can give your kids [Zorin OS Education edition](https://zorin.com/os/education/) which can be freely downloaded and installed. It comes with lot of educational softwares preinstalled.

Other than that, [Fedora Labs Astronomy edition](https://labs.fedoraproject.org/en/astronomy/) and vanilla [Linux Mint](https://linuxmint.com/) are preferred for beginners.

Even with Linux, its best to have parental control softwares.

For linux, I found it best to have [http://e2guardian.org/cms/index.php](http://e2guardian.org/cms/index.php) and [Privoxy](https://www.privoxy.org/). Once installed, you need to just enable proxy in your browser to enable them.

The list of blocked sites can simply be entered in `/etc/e2guardian/lists/bannedsitelist` and restart the service using

```
systemctl restart e2guardian
```
to take effect.

Make sure that you don't give `sudo` access to your kid to enable him to override these settings. Kids these days are very smart.


