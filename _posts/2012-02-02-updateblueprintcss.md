---
layout: blog-post
title: "Updated with Blueprint CSS Framework"
excerpt: "Updated with Blueprint CSS Framework"
disqus_id: /2012/02/02/updateblueprintcss/
location: New Delhi, India
time: 12:00 PM
tags:
- Jekyll
- CSS
---


I have updated this Jekyll site with [BluePrint CSS Framework](http://blueprintcss.org/). For those are not familiar with Blueprint, Blueprint is a grid based CSS framework. The grid is 950px wide, with 24 columns spanning 30px, and a 10px margin between columns.
First step in designing the layout is to surround your grid with a container and use div's with one of the .span-x classes to set the number of columns the elements should span. The **last** class, which every last element inside a container or another column needs.


Earlier, I had a lot of different CSS files to maintain this page. After revamp, here is how my head section looks:
{% highlight html %}
	<link rel="stylesheet" href="/files/css/blueprint/screen.css" type="text/css" />  
	<link rel="stylesheet" href="/files/css/site.css" type="text/css" />	
{% endhighlight %}	
	
I use ***screen.css, print.css*** from the framework and just override the styles in ***site.css***.
	
Achieving the sidebars, present on this site is very simple. We just add the relevant classes such as **span-x** depending upon the width you need. In my case, I divided into two blocks consisting of 6 and 18 columns respectively.

{% highlight html %}
<div id="primary" class="span-18">
	
</div>

<div id="secondary" class="span-6 last">
	
</div>
{% endhighlight %}	

You may not notice any change in look and feel of the site, but internally its CSS structure has been completely re-designed.
