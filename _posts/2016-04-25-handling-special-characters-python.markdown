---
layout: blog-post
title: "Handling special characters in Python 2"
excerpt: "Handling special characters in Python 2"
disqus_id: /2016/04/25/handling-special-characters-python/
location: Bangalore, India
time: 9:00 PM
tags:
- Python
---

Recently, we implemented a method in Python to send push notifications to users.

In some of the cases, the notification was being received like this:

![](/images/Blog/notif1.png)

This was due to specially encoded UTF-8 characters, which we were not handling in Python.

Typically, whenever your Python source encounters a UTF-8 character, you get the following:

`SyntaxError: Non-ASCII character in file on line`

For example, try out this program:

{% highlight python %}
a = 'India’s escalating water crisis'
print a
{% endhighlight %}

Here we have a UTF-8 chracter `’` in the string. Running this program will result in :

`SyntaxError: Non-ASCII character '\xe2' in file pychar.py on line 3, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details`

As the error suggests, the first step is to declare encoding on top of file:

`# encoding: utf-8`

Hence,the program becomes:

{% highlight python %}
# encoding: utf-8
a = 'India’s escalating water crisis'
print a
{% endhighlight %}

Now, the program will happily print out the string in the output.

Apart from that,  it is also helpful to know that in python, these utf8 characters can be represented in both encoded and decoded forms.

For example, if I slightly modify my program as:

{% highlight python %}
# encoding: utf-8
import json

a = 'India’s escalating water crisis'
a = a.decode('unicode_escape')
print a

b=json.dumps(a)
print b
{% endhighlight %}

The output becomes,

`Indiaâs escalating water crisis`
`"India\u00e2\u0080\u0099s escalating water crisis"`

Here the characters have been represented in escaped forms. This is good for internal representation , but not something you want when you want to transfer the text for push notification to mobile devices or web pages.

In case, you want to completely strip out the special characters:

{% highlight python %}
# encoding: utf-8
import json

a = 'India’s escalating water crisis'

d = a.decode('unicode_escape').encode('ascii','ignore')
print d
{% endhighlight %}

The output is:
`Indias escalating water crisis`

Notice in the output above, the apostophe character has been trimmed.

Using this knowledge, we are able to send notifications which contain all special characters:

![](/images/Blog/notif2.png)

