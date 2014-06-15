---
layout: blog-post
title: "Building portable Jekyll for Windows"
excerpt: "Building portable Jekyll for Windows"
disqus_id: /2013/07/20/buildportablejekyll/
location: New Delhi, India
time: 9:00 PM
tags:
- Jekyll
categories:
- Web Development
---

Recently, I was trying to install Jekyll on Windows on multiple computers and got frustrated with enormous amount of work I had to do.

If anyone of you have seen my earlier blogpost on [Installing Jekyll on Windows]({% post_url 2011-09-01-runningjekyllwindows %}) , you would agree that it requires considerable amount of effort.

Hence, I decided to build a portable version of Jekyll for myself, which I could easily copy on multiple computers. The portable version contains 
everything which is required to run Jekyll on Windows:

* Ruby 2.0
* Ruby development Kit
* Git 1.9.2
* Python 2.7.5

You can download the Complete PortableJekyll package [here from my github repo](https://github.com/madhur/PortableJekyll)

It comes with following pre-installed gems including Jekyll 2.0.1

{% highlight text %}
activesupport (3.1.12)
addressable (2.3.5)
bigdecimal (1.2.0)
blankslate (2.1.2.4)
builder (3.2.2)
celluloid (0.15.2)
celluloid-io (0.15.0)
chronic (0.10.2)
classifier (1.3.3)
coffee-script (2.2.0)
coffee-script-source (1.7.0)
colorator (0.1)
commander (4.1.5)
cub (0.0.4)
curb (0.8.5, 0.7.18)
directory_watcher (1.4.1)
execjs (2.0.2)
faraday (0.8.8)
fast-stemmer (1.0.2)
feedzirra (0.1.3)
ffi (1.9.3)
hashie (2.0.5)
highline (1.6.19)
i18n (0.6.5)
io-console (0.4.2)
jekyll (2.0.1)
jekyll-coffeescript (1.0.0)
jekyll-sass-converter (1.0.0, 1.0.0.rc4, 1.0.0.rc3)
json (1.7.7)
kramdown (1.3.2)
liquid (2.5.5, 2.5.3, 2.5.1, 2.5.0)
listen (2.7.1, 1.3.1)
loofah (1.2.1)
maruku (0.7.0, 0.6.1)
mercenary (0.3.2, 0.2.1)
mini_portile (0.5.1)
minitest (4.3.2)
multi_json (1.8.1)
multipart-post (1.2.0)
nio4r (1.0.0)
nokogiri (1.6.0 x86-mingw32)
ocra (1.3.1)
octokit (2.4.0)
parslet (1.5.0)
posix-spawn (0.3.6)
psych (2.0.0)
pygments.rb (0.5.0)
rake (0.9.6)
rb-fsevent (0.9.3)
rb-inotify (0.9.2)
rb-kqueue (0.2.0)
rdoc (4.0.0, 3.12.2)
redcarpet (3.1.1, 2.3.0)
rouge (1.3.2)
safe_yaml (1.0.1, 0.9.7, 0.7.1)
sass (3.2.12)
sawyer (0.5.1)
sax-machine (0.1.0)
syntax (1.0.0)
test-unit (2.0.0.0)
timers (1.1.0)
toml (0.1.0)
wdm (0.1.0)
yajl-ruby (1.1.0)
{% endhighlight %}




