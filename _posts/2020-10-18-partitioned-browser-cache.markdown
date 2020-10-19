---
layout: blog-post
title: "Partitioned Browser Cache Starting Chrome v86"
excerpt: "Partitioned Browser Cache Starting Chrome v86"
disqus_id: /2020/10/18/partitioned-browser-cache/
tags:
    - HTTP
---

Starting Chrome v86, browser cache is going to be partitioned which are going to
have interesting consequences.

### What does it mean?

Previously, if you would have loaded a file such as js, css from a CDN from a
particular site (lets say Facebook) was cached in the browser cache and
available to be used from cache even in a different site (lets say Reddit)

But this is changing now, which means that a cache is domain specific. So a CDN
file cached from Facebook will be loaded from the cache only if the requesting
domain is Facebook.

### Why is this being done?

This global cache from browser have been misused to track users. For example, I
can setup a server and track which of my users are not requesting the particular
resource (which is same as Facebook) and then make a conclusion that those of my
users have logged on to Facebook recently.

References: 
[Cross site leak](https://portswigger.net/daily-swig/xs-leak)