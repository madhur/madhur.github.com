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
* Git 1.8.3
* Python 2.7.5

You can download the Complete PortableJekyll package [here from my dropbox link](https://www.dropbox.com/sh/40l6mgbl1ce2kej/lF6ykQxt9d)

It comes with following pre-installed gems including Jekyll 1.0.3

{% highlight text %}
bigdecimal (1.2.0)
classifier (1.3.3)
colorator (0.1)
commander (4.1.3)
directory_watcher (1.4.1)
fast-stemmer (1.0.2)
highline (1.6.19)
io-console (0.4.2)
jekyll (1.0.3)
json (1.7.7)
kramdown (1.0.2)
liquid (2.5.0)
maruku (0.6.1)
mini_portile (0.5.1)
minitest (4.3.2)
posix-spawn (0.3.6)
psych (2.0.0)
pygments.rb (0.5.0)
rake (0.9.6)
rdoc (4.0.0)
safe_yaml (0.7.1)
syntax (1.0.0)
test-unit (2.0.0.0)
yajl-ruby (1.1.0)
{% endhighlight %}


There is a command prompt script which you might want to change

{% highlight text %}
SET PATH=%PATH%;D:\PortableJekyll\ruby\bin;D:\PortableJekyll\devkit\bin;D:\PortableJekyll\git\bin;D:\PortableJekyll\Python\App;
{% endhighlight %}

This script above sets the PATH variable so that jekyll can be exeucted from any directory.

