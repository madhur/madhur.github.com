---
layout: blog-post
title: "Facebook Vulnerability - Session sidejacking"
excerpt: Facebook Vulnerability - Session sidejacking
disqus_id: /2011/06/12/facebooksessionhijacking/
location: Pittsburgh, US
time: 11:00 AM
tags:
- Facebook
- Session Sidejacking
- Security
---


Recently, there was a [vulnerability](http://www.wtfuzz.com/blogs/linkedin-ssl-cookie-vulnerability/) discovered in popular professional networking site [LinkedIn](www.linkedin.com) in which an attacker could steal an authentication cookie used by the site to authenticate the client. It was a classic case of Session sidejacking, which is desribed by [Wikipedia](http://en.wikipedia.org/wiki/Session_hijacking) as

*where the attacker uses packet sniffing to read network traffic between two parties to steal the session cookie. Many web sites use SSL encryption for login pages to prevent attackers from seeing the password, but do not use encryption for the rest of the site once authenticated. This allows attackers that can read the network traffic to intercept all the data that is submitted to the server or web pages viewed by the client. Since this data includes the session cookie, it allows him to impersonate the victim, even if the password itself is not compromised. Unsecured Wi-Fi hotspots are particularly vulnerable, as anyone sharing the network will generally be able to read most of the web traffic between other nodes and the access point.*

One of the basic solution implemented by the web sites for this problem is SSL. Almost all of the web sites use SSL during the authentication phase to encrypt the cookie data which is transmitted on the network. However, this is only a partial solution to the problem since most of the clients transmit this cookie data during further HTTP POST and GET requests. This is the reason many  websites such as Gmail, Facebook have an option to turn on SSL for the entire session, because they know that sensitive bytes are being transmitted all the time even if the user has authenticated. Let us see how a user's security can be compromised if he has not turned on full SSL settings for these web sites such as Facebook. Consider a home LAN network where users are using WiFi hotspots to browse the internet. Its easy to set up a MITM attack on this network by spoofing the ARP. For example, on linux,  it can be done using [Ettercap](http://ettercap.sourceforge.net/) or [Arpspoof](http://arpspoof.sourceforge.net/)

{% highlight bash %}
echo 1 > /proc/sys/net/ipv4/ip_forward
arpspoof -t "target ip(person to own)" "gateway ip(router)"
{% endhighlight %}

Use any packet sniffer such as [Wireshark](http://www.wireshark.org/) to sniff the packets between the target IP and the host www.facebook.com. The following is an example of a POST request sniffed from wireshark:

From this screen, we are mainly interested in grabbing the cookies, which are specified in this header

![Pic](/images/Blog/facebook.png)

{% highlight bash %}
Cookie: datr=09bXXXQ2oOgQuUK0yAzK_JU9; lu=wgj9pmpkAsdXXXTp5vthfh2w; locale=en_US; L=2; act=13078123502562F3; c_user=xxxxxx; sct=1123416461; xs=603Afe43db8a71239bd8d7b2a831xxx6241f; presence=EM307818375L26REp_5f123422481F22X3078XXX1367K1H0V0Z21G307818375PEuoFD769839560FDexpF1307818409174EflF_5b_5dEolF-1CCCC; e=n
{% endhighlight %}

In my proof of concept, I was just required to copy the **xs** and **c_user** cookies to hijack the target session. **c_user** is the user ID of the user which is not at all a secret. However, **xs** does seems to be the authentication token and which should not be passed around in cleartext. 

{% highlight bash %}
c_user:xxxxxx
xs:603Afe43db8a71239bd8d7b2a831aad6241f
{% endhighlight %}

Since now we have the cookies and one of it is indeed an authentication cookie. We can plug this in browser manually or using a Chrome extension such as 
[Edit this Cookie](https://chrome.google.com/webstore/detail/fngmhnnpilhplaeedifhccceomclgfbg)

Once the values are plugged, browse to http://www.facebook.com , you would have intercepted the target user session.

***This post is just for educational purposes regarding the implications of using unencrypted communication. I am not responsible for any damage or harm done using any
knowledge contained in this article***




