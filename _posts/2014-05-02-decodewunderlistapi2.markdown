---
layout: blog-post
title: "Decoding the hidden Wunderlist API (Part II)"
excerpt: "Decoding the hidden Wunderlist API (Part II)"
disqus_id: /2014/05/02/decodewunderlistapi2/
location: New Delhi, India
time: 9:00 PM
tags:
- Wunderlist
- API
- REST
categories:
- Development
---

In [part I]({% post_url 2014-05-02-decodewunderlistapi %}) we discovered the hidden Wunderlist API. In this post, I am to show partial implementation of this API client in Java using [Retrofit](http://square.github.io/retrofit/).
The implementation is hosted in my [Git repository](https://github.com/madhur/wunder-java). Feed free to fork, extend or submit appropriate pull requests. I will be glad to accept your contribution.

[Retrofit](http://square.github.io/retrofit/) is a java library which turns your REST API into java interfaces. 
