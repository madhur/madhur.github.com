---
layout: blog-post
title: "Exploring Web Application vulnerabilities"
excerpt: Exploring Web Application vulnerabilities
disqus_id: /2011/07/26/explorwebappsecurity/
location: New Delhi, India
time: 12:00 PM
categories:
- Security
- Hacking
---



There are many kinds of web application vulnerabilities which an attacker can exploit. Some of them common are SQL Injection, XSS. Let's look at the tools which are available to detect these vulnerabilities in an application.

***Sql Injection***
Sqlmap is a SQL Injection vulnerability scanner. You can give an Url input for example, http://www.salk.edu/events/index.php?id=150  to it and it will try to find out if the Url is susceptible to SQL injection attacks. For ex:

{% highlight bash %}
./sqlmap.py -u http://www.salk.edu/events/index.php?id=150 
{% endhighlight %}

Sqlmap takes different parameters for example, -D , -T, --dump to dump out different tables, databases and information within the databases.

***Cross Site Request Forgery***


***Remote command Execution***

***Remote file inclusion***


***Cross Site Scripting (XSS)***
