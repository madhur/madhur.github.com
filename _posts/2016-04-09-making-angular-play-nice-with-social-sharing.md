---
layout: blog-post
title: "Making AngularJs play nice with Social sharing"
excerpt: "Making AngularJs play nice with Social sharing"
disqus_id: /2016/04/09/making-angular-play-nice-with-social-sharing/
location: Bangalore, India
time: 9:00 PM
tags:
- AngularJs
---


Recently, We were designing a mobile web view for the news article shared on the app. I simply choose AngularJs for the ease of use and flexibility it provies.

However, after complete implementation. When someone tried to share the story on Facebook, we saw this:

![](/images/Blog/angular1.png)

This happens because of social media sites like [Facebook]() do not evalaute Javascript while fetching the meta tags. In our case, the meta tags were defined like this:


{% highlight html %}
{% raw %}
<title ng-bind="title"></title>
<meta property="og:title" content="{{ data.caption }}" />
<meta property="og:image" content="{{ data.xImage}}" />
<meta property="og:description" content="{{ data.caption }}" />
{% endraw %}
{% endhighlight %}

We were relying on Angular's interpolation to evaluate the meta tags which didn't work since AngularJs is entirely executed on client side. This caused facebook to show raw values i.e. 
`{{ data.caption }}`

To solve this problem, we moved the meta tags evaluation to server side. Since we were using Java stack along with Spring, it was easy to do so. We made sure that our HTML markup was filtered through JSP tags. It was as easy as adding these directives on top of page:

{% highlight html %}
<%@ page isELIgnored="false" %>
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
         pageEncoding="ISO-8859-1"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
{% endhighlight %}

Now with JSTL tags in place, we replaced the meta tags with JPS tags:

{% highlight html %}
 <title><c:out value="${title}"></c:out></title>
 <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no, width=device-width">
 <meta property="og:title" content="<c:out value="${title}"></c:out>" />
 <meta property="og:image" content="<c:out value="${image}"></c:out>" />
 <meta property="og:description" content="<c:out value="${description}"></c:out>" />
{% endhighlight %}

Before returning the JSP page through an API call, we evaluated these meta tags on the server side itself:

{% highlight java %}
@RequestMapping(value = "/view/{newsId}", method = RequestMethod.GET)
	public String getNews(HttpServletRequest request, @PathVariable("newsId") String slug, ModelMap mv, HttpServletResponse response) {

		NewsArticlesV2 newsArticlesV2 = newsServiceV2.getByExternalId(slug);

		String title = newsArticlesV2.getArticleTitle();
		String description = newsArticlesV2.getNewsContent();

		String image = newsArticlesV2.getImage();
		response.setContentType("text/html");
		mv.addAttribute("title", title);
		mv.addAttribute("image", image);
		mv.addAttribute("description", description);
		mv.addAttribute("slug",slug);
		logger.debug("request",request);
		return "webforms/news";
	}
{% endhighlight %}

And the result becomes:

![](/images/Blog/angular2.png)


