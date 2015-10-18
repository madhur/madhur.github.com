---
layout: blog-post
title: "Why is only UI thread allowed to modify the UI"
excerpt: "Why is only UI thread allowed to modify the UI"
disqus_id: /2015/10/18/ui-thread-modify/
location: Bangalore, India
time: 9:00 PM
tags:
- Programming
- Threading
---

After working in various frameworks such as Win32 API, WPF, Silverlight, Android and iOS over the years, one theme which has been common throughout all these frameworks is the restriction to modify the UI only through UI thread.

There are various ways in these frameworks to modify the UI through a thread other than UI thread. Some of them are captured in the articles below:

* Android - [Communicating with UI Thread](http://developer.android.com/training/multiple-threads/communicate-ui.html)
* Silverlight - [Dispatchign in Silverlight](http://www.wintellect.com/devcenter/jlikness/dispatching-in-silverlight)
* iOS - [About threaded programming](https://developer.apple.com/library/ios/documentation/Cocoa/Conceptual/Multithreading/AboutThreads/AboutThreads.html)
* WPF  - [Threading model](https://msdn.microsoft.com/en-us/library/vstudio/ms741870(v=vs.100).aspx)

Why is such a restriction in place ? Some of these links provide insight:

* [Why are most UI frameworks single threaded?](http://stackoverflow.com/questions/5544447/why-are-most-ui-frameworks-single-threaded)
* [Multithreaded toolkits: A failed dream?](https://weblogs.java.net/blog/kgh/archive/2004/10/multithreaded_t.html)
* [Why are GUIs single threaded](http://codeidol.com/java/java-concurrency/GUI-Applications/Why-are-GUIs-Single-threaded/)