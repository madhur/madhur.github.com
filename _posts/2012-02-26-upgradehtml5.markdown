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

Here, I am going to show you how 


1. Prepare a development branch. Since we will makeing a lot of changes to HTML/CSS, its good to have a new branch on your repository. You don't want to mess your master/source branch.
	
{% highlight text %}
git branch develop
git checkout develop
{% endhighlight %}
	
Once we have done the changes, we will test it throroughly and merge it back to our main branch.

2. Changes to main default.html


5. Polyfills for your old incompatible browsers (IE ?)
	
   As I said above, even if your browser doesn't support HTML5, you can use [pollyfills]() using which you can enable most of the HTML 5 features. Keep in mind that its not magic that using pollyfills suddenly enables your browser
   to enable HTML5. Most of the polyfills work by making necessary changes in the DOM behind the scenes so as to emulate HTML5 behaviour. 
   
6. Once we have done all the changes, we will review them, commit and merge into master branch. After that we can delete the development branch

{% highlight text %}
git diff master..develop
git commit -am "Updated my blog to HTML5"
git checkout master
git merge develop
git branch -d develop
{% endhighlight %}	