---
layout: blog-post
title: "How to upgrade your Jekyll Blog/Site to HTML5"
excerpt: "How to upgrade your Jekyll Blog/Site to HTML5"
disqus_id: /2012/02/26/upgradehtml5/
location: New Delhi, India
time: 9:00 PM
tags:
- HTML5
categories:
- Web Development
---

HTML5 is the next big thing. There is no reason which should hold you back from upgrading your site to new HTML5 which adds lot of features some of them which I discussed in my previous blog article.

If you think lack of browser compatiblity is holding you back, then there is good news - there are ways using which you can even have the incompatible browsers work with your new HTML5 site. 

Here, I am going to show you how you can upgrade you site/blog to HTML 5. I am just going to show you very basic things. At a granular level, you might require more changes depending on your site.


* Prepare a development branch. Since we will makeing a lot of changes to HTML/CSS, its good to have a new branch on your repository. You don't want to mess your master/source branch.
	
{% highlight text %}
git branch develop
git checkout develop
{% endhighlight %}
	
Once we have done the changes, we will test it throroughly and merge it back to our main branch.

* Changes to main default.html
{% highlight html hl_lines=2,4,6,7,8,15,16,19,20 %}
<!DOCTYPE html>
<html lang="en">
<head>   
   <meta charset="utf-8" />   
   <meta name="author" content="Madhur Ahuja" />	
	<!--[if lt IE 9]>
		<script src="/files/js/modernizr-2.5.3.js" type="text/javascript"></script>
	<![endif]-->
	
	<script src="/files/js/site.js" type="text/javascript"></script>
</head>
<body>
<div id="gradient">
	<div id="container" class="container">
		<header id="header" class="span-24 last">
		</header>
		<div id="content" class="span-24 last">
		</div>
		<footer id="footer" class="span-24 last">
		</footer>
	</div>
</div>
</body>
</html>
{% endhighlight %}

* Changes to blog-post.html
{% highlight html hl_lines=6,9,10,11,12,17,21,23 %}
---
layout: default
top: Madhur Ahuja
---

<section id="primary" class="span-24 last">
	<div id="blogcontent">

		<aside class="postmeta full span-5">
		</aside>
		<article class="post full span-18 last">			 
			<footer>
				<div class="blocked tags">
					<p>
					</p>
				</div>
			</footer>
			<div class="hr"></div>
			<div>
			</div>
		</article>		
	</div>	
</section>
{% endhighlight %}

* Enable HTML5 input controls

Since I use a search box to search my site, I can use HTML5 **search** type box and also the **required** attribute
{% highlight html %}
<input type="search" required id="q" name="q" value="" placeholder="Site Search" /> 
{% endhighlight %}

* Polyfills for your old incompatible browsers (IE ?)
	
   As I said above, even if your browser doesn't support HTML5, you can use [pollyfills]() using which you can enable most of the HTML 5 features. Keep in mind that its not magic that using pollyfills suddenly enables your browser
   to enable HTML5. Most of the polyfills work by making necessary changes in the DOM behind the scenes so as to emulate HTML5 behaviour. I have already modernizer in the default.html to enable this.
   
* Once we have done all the changes, we will review them, commit and merge into master branch. After that we can delete the development branch

{% highlight text %}
git diff master..develop
git commit -am "Updated my blog to HTML5"
git checkout master
git merge develop
git branch -d develop
{% endhighlight %}	