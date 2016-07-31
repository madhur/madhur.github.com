---
layout: blog-post
title: "Caching authenticated requests using NGINX"
excerpt: "Caching authenticated requests using NGINX"
disqus_id: /2016/07/31/nginx-cache-authenticated-requests/
tags:
- Caching
- Nginx
---

To handle the ever increasing load, one of my requirements was to cache the authenticated REST API's for faster processing and decrease the load on backend servers ([Tomcat](http://tomcat.apache.org/) in this case).

We use [Token based authentication](http://stackoverflow.com/questions/1592534/what-is-token-based-authentication) for our REST API's. That means our REST API's are esentially [stateless](http://www.tutorialspoint.com/restful/restful_statelessness.htm)

We use a simple encrypted token passed in a header field, say `X-AUTH-TOKEN`

Now, we have various API's such as user profile, addresses which return data based on this token passed and I don't want them to hit our backend servers everytime. Neither I am looking for unnecesarily storing this simply retrieved data in our [Redis](http://redis.io/) servers. 

Instead, we can use NGINX to cache these requests. We have a very simple architecture where NGINX acts as a reverse proxy for Tomcat servers.

![](/images/Blog/tt.png)

Here, every request is intercepted by NGINX and appropriate requests are passed back to Tomcat server. This is done using [`proxy_pass`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass) directive of NGINX.

{% highlight text %}
location /name/ {
    proxy_pass http://127.0.0.1/remote/;
}
{% endhighlight %}


We can ask NGINX to cache the request using just two directives: [`proxy_cache_path`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.103655616.1528258479.1469009926#proxy_cache_path) and [`proxy_cache`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.103655616.1528258479.1469009926#proxy_cache)

{% highlight text %}
proxy_cache_path /path/to/cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m 
use_temp_path=off;


server {
...
    location / {
        proxy_cache my_cache;
        proxy_pass http://my_upstream;
    }
}
{% endhighlight %}

This sets up the basic caching in NGINX as described [here](https://www.nginx.com/blog/nginx-caching-guide/)

Now comes the fun part, how do we cache the authenticated requests. The key is to understand the What Cache Key Does NGINX use?

The default keys that NGINX generates is MD5 hash of the following NGINX variables: `$scheme$proxy_host$request_uri`

For this sample configuration, the cache key for 
`http://www.example.org/profile` is calculated as 
`md5(“http://my_upstream:80/profile”)`

However, for token based authentiated requests, the cached response of `http://www.example.org/profile` will not be differentiated for different users, because the response is generated based on the `X-AUTH-TOKEN` field coming in the HTTP headers.

To solve for this, we simply add the token field as part of [`proxy_cache_key`](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_key)

`proxy_cache_key "$http_x_auth_token$request_uri";`

This will ensure that a new cache copy is created for each request having different `X-AUTH-TOKEN` in its header field.

To verify this, you can print out the key field in the response headers using

`add_header X-Cache-Key  $http_x_auth_token$request_uri;`




