---
layout: blog-post
title: "Close look at proxy_cache_lock and proxy_cache_use_stale in Nginx"
excerpt: "Close look at proxy_cache_lock and proxy_cache_use_stale in Nginx"
disqus_id: /2016/12/25/proxy-cache-lock-nginx/
tags:
- Nginx
- Caching
---

If you have worked with Nginx cache, one must know and understand [`proxy_cache_lock`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_lock) and [`proxy_cache_use_stale`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_use_stale) directives.

To configure simply Nginx caching, we basically add these 2 lines in our configuration block:

{% highlight text %}
proxy_ignore_headers X-Accel-Expires Expires Cache-Control;
proxy_cache_valid any 30s;
{% endhighlight %}

This will ignore any of the cache related headers from upstream and keep the cache valid for 30 seconds. This means that a request will only go out to upstream every 30 seconds. But it won't be one request: it's very possible that multiple requests will be made when multiple people request the same stale cache. To solve this problem, we add two more configuration directives:

{% highlight text %}
proxy_cache_lock on; 
{% endhighlight %}

{% highlight text %}
proxy_cache_use_stale updating;
{% endhighlight %}

Using these two extra configuration directives, Nginx will send only one request to upstream every 30 secs while still responding quickly with stale data.

An important point to consider here is that default value of [`proxy_cache_use_stale`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_use_stale) is `off`. That means, if you have set, [`proxy_cache_lock`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_lock) to `on`, all the requests which will arrive at Ngix while the cache is being updated will "essentially wait". During heavy traffic, this can considerably slowdown the performance and response times of the requests.

Quoting from NGINX docs:

> When enabled, only one request at a time will be allowed to populate a new cache element identified according to the proxy_cache_key directive by     passing a request to a proxied server. Other requests of the same cache  element will either wait for a response to appear in the cache or the cache lock for this element to be released, up to the time set by the proxy_cache_lock_timeout directive

Thus, it is very important to consider the scenarios in which [`proxy_cache_lock`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_lock) is being used. If it is not possible to serve the stale data to the client, it becomes even more important to configure the [`proxy_cache_lock_timeout`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_lock_timeout) value, otherwise performance can be severely degraded during heavy traffic. The default value of [`proxy_cache_lock_timeout`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_lock_timeout) is 5 seconds which is quite high.


