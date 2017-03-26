---
layout: null
---

var cacheName = 'madhur-cache-v12';
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
