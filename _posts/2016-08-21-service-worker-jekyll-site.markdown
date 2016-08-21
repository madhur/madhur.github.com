---
layout: blog-post
title: "Adding Service worker to Jekyll Site"
excerpt: "Adding Service worker for to Jekyll Site"
disqus_id: /2016/08/21/service-worker-jekyll-site/
tags:
- Jekyll
- Service worker
---

I finally added the [service worker](http://www.html5rocks.com/en/tutorials/service-worker/introduction/) for my Jekyll site [madhur.co.in](https://madhur.co.in).

For introduction, Service workers enable rich offline experiences, periodic background syncs and push notifications.

For start, I have just implemented offline caching of JS/CSS/HTML files so that the site can be browsed even when offline. 

Here is the simplest definition of a service worker which generates the Url of pages so that they can be cached

{% highlight javascript %}
---
layout: null
---

{% raw %}
var cacheName = 'madhur-cache-v1';
var filesToCache = [
    // Stylesheets
    // Pages and assets
    {% for page in site.html_pages %}
        {% if page.url contains 'projects' or page.url contains '404'   %}
            
        {% else %}
            '{{ page.url }}',
        {% endif %}
        
    {% endfor %}

    // Blog posts
    {% for post in site.posts %}
        '{{ post.url }}',
    {% endfor %}

    // JS files, Portfolio assets and main video
    // (!) This will throw a Liquid error. Read below.
    {% for file in site.static_files %}
        {% if file.extname == '.js' or file.path contains '/portfolio/screenshots' or file.path contains '/portfolio/thumbnails' %}
              '{{ file.path }}',
        {% endif %}
    {% endfor %}
];
{% endraw %}

// serviceWorker.js
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(cacheName).then(function(cache) {
            return cache.addAll(filesToCache);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    console.log('[*] Serving cached: ' + event.request.url);
                    return response;
                }

                console.log('[*] Fetching: ' + event.request.url);
                return fetch(event.request);
            }
        )
    );
});

{% endhighlight %}

The generated file can be seen at [http://www.madhur.co.in/serviceWorker.js](http://www.madhur.co.in/serviceWorker.js)

In current implementation, the service worker will always return the response from the cache if one exists. However, there are lot of strategies which can be implemented for example:

* Cache Only
* Network only
* Cache First
* Network First
* Fastest

These and many other such patterns are documented in [offline cookbook](https://jakearchibald.com/2014/offline-cookbook/) 
