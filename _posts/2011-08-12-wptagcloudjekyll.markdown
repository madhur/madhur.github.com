---
layout: blog-post
title: "Integrating Wordpress Tag cloud Plugin in Jekyll"
excerpt: Integrating Wordpress Tag cloud Plugin in Jekyll
disqus_id: /2011/09/12/wptagcloudjekyll/
location: Delhi, India
time: 11:00 PM
categories:
- Jekyll
- Code
---

#{{ page.title }}
[Earlier](http://localhost:4000/blog/2011/06/11/tagcloudjekyll.html) I showed you how we can integrate a simple HTML based tag cloud in Jekyll blog.

In this post, Let's take a look at how we can integrate Wordpress Tag cloud plugin in Jekyll blog as shown in the right hand pane on this [blog](/blog).
Wordpress Tag cloud plugin is a simple Flash based plugin which accepts a group of Url encoded Anchor Hyperlinks as the parameter to display as the tag cloud.
The flash file can be downloaded [here](/files/tagcloud.swf).

To output this plugin we use a normal embed tag as shown below

{% highlight html %}
<embed type="application/x-shockwave-flash" 
src="/files/tagcloud.swf" 
id="tagcloudflash" 
name="tagcloudflash" 
bgcolor="#474c52" 
quality="high" 
wmode="transparent"
allowscriptaccess="always"
flashvars="tcolor=0xffffff&amp;tcolor2=0xb6bcc1&amp;hicolor=0xa1ff66&amp;tspeed=100&amp;distr=true&amp;mode=tags&amp;tagcloud=%3Ctags%3E%3Ca+href%3D%27http%3A%2F%2Fcoda.co.za%2Fblog%2Ftag%2Fadvertising%27+class%3D%27tag-link-40%27+title%3D%2720+topics%27+style%3D%27font-size%3A+6.36046511628pt%3B%27%3Eadvertising%3C%2Fa%3E%3C%2Ftags%3E" 
height="300" width="250"></embed>
{% endhighlight %}

Most of the parameters are self explanatory which you can customize based on your needs. The parameter to our interest is **flashvars**. In the above example, the decoded value of **flashvars** would be

{% highlight html %}
flashvars=
"tcolor=0xffffff
&tcolor2=0xb6bcc1
&hicolor=0xa1ff66
&tspeed=100
&distr=true
&mode=tags
&tagcloud=%3Ctags%3E%3Ca+href%3D%27http%3A%2F%2Fcoda.co.za%2Fblog%2Ftag%2Fadvertising%27+class%3D%27tag-link-40%27+title%3D%2720+topics%27+style%3D%27font-size%3A+6.3604651628pt%3B%27%3Eadvertising%3C%2Fa%3E%3C%2Ftags%3E" 
{% endhighlight %}

**flashvars** is an array of parameters itself out of which the one of our most interest is **tagcloud**. This param again accepts a list of anchor hyperlinks which are Url encoded.
The example of the input is shown below

{% highlight html %}
<tags>
<a href='/blog/tag/advertising' class='tag-link-40' title='20 topics' style='font-size: 6pt;'>advertising</a> 
<a href='/blog/tag/advocacy' class='tag-link-41' title='25 topics' style='font-size: 7pt;'>advocacy</a> 
<a href='/blog/tag/backpacking' class='tag-link-101' title='23 topics' style='font-size: 7pt;'>backpacking</a> 
<a href='/blog/tag/blogging' class='tag-link-147' title='35 topics' style='font-size: 9pt;'>blogging</a>
</tags> 
{% endhighlight %}

The value above needs to Url encoded and assigned to flashvars variable. In order to achieve this in Jekyll, we have two tasks

* Generating list of tags dynamically
* Dynamically resizing the text of each tag based on its cound

The first task can be simply achieved using standard Liquid Markup which is supported by Jekyll


{% highlight html %}
{{ "{% for tag in site.categories" }}%}

{{ "{ % endfor "}}%}
{% endhighlight %}

To achieve the second task, we can augment our first code cleverly as shown below

{% highlight html %}
{{ "{% for tag in site.categories" }}%}
  {{ "{% assign t = tag.first" }}%}
  {{ "{% assign posts = tag.last" }} %}
	  <a class="tag tag{{ posts | size }}" title="{{ posts | size }} posts" href="/categories/{{ t | to_id }}.html">{{ t }}</a>
{{ "{ % endfor "}}%}
{% endhighlight %}

Note that the above code will generate the list of anchor tags in loop and assign the appropriate Url, title and class attributes. You can modify these as per your convinience. This needs to be encoded before you put in use. You can use this [site](http://meyerweb.com/eric/tools/dencoder/) to do the encoding.

Our final Jekyll code looks like this

{% highlight html %}
<div class="category">
	<h4>Tag Cloud</h4>

<div id="wpcumuluscontent">
	<embed 
	type="application/x-shockwave-flash" 
	src="/files/tagcloud.swf" 
	id="tagcloudflash" 
	name="tagcloudflash" 
	bgcolor="#474c52" 
	quality="high" 
	wmode="transparent" 
	allowscriptaccess="always" 
	flashvars="tcolor=0xffffff&amp;tcolor2=0xb6bcc1&amp;hicolor=0xa1ff66&amp;tspeed=100&amp;distr=true&amp;mode=tags&amp;tagcloud=%3Ctags%3E{% for tag in site.categories %}{% assign t = tag.first %}{% assign posts = tag.last %}%3Ca+style%3d%27font-size:12pt%27+class%3D%27tag tag{{ posts | size }}%27+title%3D%27{{ posts | size }}+posts%27+href%3D%27%2Fcategories%2F{{ t | to_id }}.html%27%3E{{ t }}%3C%2Fa%3E{% endfor %}%3C%2Ftags%3E" 
	height="300" 
	width="250">
	</embed>
</div>
</div>
{% endhighlight %}

To make sure that the text is resized according to the number of posts, we add the following CSS in the CSS file

{% highlight css %}
.tag { font-size: 6pt; }
.tag1 { font-size: 6pt; }
.tag2 { font-size: 6pt; }
.tag3 { font-size: 12pt; }
.tag4 { font-size: 12pt; }
.tag5 { font-size: 12pt; }
.tag6 { font-size: 13pt; }
.tag7 { font-size: 14pt; }
.tag8 { font-size: 15pt; }
.tag9 { font-size: 16em; }
.tag10 { font-size: 17pt; }
.tag11 { font-size: 18pt; }
.tag12 { font-size: 19pt; }
.tag13 { font-size: 20pt; }
.tag14 { font-size: 21pt; }
.tag15 { font-size: 22pt; }
.tag16 { font-size: 23pt; }
.tag17 { font-size: 24pt; }
.tag18 { font-size: 25pt; }
.tag19 { font-size: 26pt; }
.tag20 { font-size: 27pt; }
{% endhighlight %}
