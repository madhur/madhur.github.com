---
layout: blog-post
title: "Hosting Git repository on a Windows LAN"
excerpt: "Hosting Git repository on a Windows LAN"
disqus_id: /2014/05/09/hostgitwindowslan/
location: New Delhi, India
time: 9:00 PM
tags:
- Git
categories:
- Development
---

Recently, I had a small team of developers and was looking to setup a version control system for them.

I evaluated many tools like VSTS, Subversion and finally decided on Git repository hosted on a Windows LAN.

First of all, find or create a network share on which everybody will have a read/write access. For example:
`\\Group03\Silverlight_Projects\EXCEL\Solution`

First of all, you need to create a blank bare repository at this location. However, since you cannot `cd` into a network
shared location, we will use `pushd` command as follows:

{% highlight text %}
pushd \\Group03\Silverlight_Projects\EXCEL\Solution
{% endhighlight %}

This command will map it to a network drive and `cd` into it.

Create a bare git repository.
{% highlight bash %}
git init --bare
{% endhighlight %}

Now all we need to do is add the newly created remote bare repository to our local repo and push our code up.

{% highlight bash %}
git remote add origin //Group03/Silverlight_Projects/EXCEL/Solution
git push origin master
{% endhighlight %}
