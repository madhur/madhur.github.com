---
layout: blog-post
title: "Android SSL Pinning Bypass"
excerpt: "Android SSL Pinning Bypass"
disqus_id: /2023/12/05/android-ssl-pinning-bypass/
tags:
    - Android
---

I have always been a tinkerer and loved to explore internal of applications.

Android has always fascinated me from the beginning partly because its mostly open source and allows you to customize. Other aspect of Android which has been useful is [Rooting](https://en.wikipedia.org/wiki/Rooting_(Android))

Rooting allows you to take complete control over the application and customize some of the aspects which are not possible in non-rooted Android.

One area where rooting helps is capturing SSL network traffic of the applications. This helps in debugging and learning more about how networks works. In this post, we will see how can we capture the network traffic for inspection in Android. This is mostly for debugging and learning purpose.

### [Apk-mitm](https://github.com/shroudedcode/apk-mitm)
---

APK mitm tools modified the original Android application to disable the SSL Pinning. This tool relies on [apktool](https://apktool.org/) heavily.

This tool always doesn't work. Recently there has been lot of [issues](https://github.com/shroudedcode/apk-mitm/issues/141) which have no solutions.

However, if it works, this is the most easiest and straightforward way as the modified app can be installed on non-rooted device and just inspected through proxy such as [Charles](https://www.charlesproxy.com/)

### [Android Unpinner](https://github.com/mitmproxy/android-unpinner)
---

This tool is different from Apk Mitm in a way that it bypasses the SSL pinning code only at runtime. Thus, you no longer have to disassemble and repackage the application.

This tool relies heavily on [Frida tools](https://github.com/frida/frida-tools) for its job.

Again, this tool is not gauranteed to work 100% of the time.

### [Rooting](https://en.wikipedia.org/wiki/Rooting_(Android))
---

If you can root your device, it is very easy to capture network traffic even if its from SSL pinned app. However, rooting can destroy warranty.

These days, most of the Android apps, will refuse to start if they detect that they are running on a rooted software. 

Hence, this option is only viable if you have a spare device.

### [Rooted AVD](https://gitlab.com/newbit/rootAVD)
---

This is my most preferred method and mostly always works. Since the purpose of network inspection is mostly debugging and learning, we can do it on AVD instead of actual device.

[rootAVD](https://gitlab.com/newbit/rootAVD) allows you to seemlessly root the running AVD device, using the simple command

```
./rootAVD.sh system-images/android-33/google_apis_playstore/x86_64/ramdisk.img

```

where `system-images/android-33/google_apis_playstore/x86_64/ramdisk.img` is the path of AVD devices relative to `$ANDROID_HOME`

Next step, would be to install [MagiskTrustUserCerts](https://github.com/NVISOsecurity/MagiskTrustUserCerts) module of [Magisk](https://github.com/topjohnwu/Magisk)

> This module makes all installed user certificates part of the system certificate store, so that they will 
> automatically be used when building the trust chain. This module makes it unnecessary to add the 
> network_security_config property to an application's manifest.

Once installed, your Magisk modules section should look like this

<img src='/images/magisk.png' height="600px" />

Now, the only step remaining is enabling proxy to intercept traffic. I use [Charles proxy](https://www.charlesproxy.com/) and this opens the port 8888 for listening to traffic.

Enabling proxy on AVD is as simple as executing:


```
adb shell settings put global http_proxy 192.168.1.252:8888 

```

where `192.168.1.252` is the local IP address of the host machine.

Disabling proxy can be done using:

```
adb shell settings put global http_proxy :0
```
---

If you guys have been using more preferred way to inspect SSL traffic. Let me know in the comments.