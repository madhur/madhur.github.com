---
layout: blog
title: Blog
feed: atom.xml
keywords: C/C++, Windbg, Reverse Engineering, important
important: yes
---

Blog
=====================
<span class="low-top quiet large-bottom"><a href="/blog/archives" class="small quiet">Archives</a></span>
<p/>

{% for post in site.posts limit: 50 %}
<p>{{ post.date | date: "%d %b %Y" }} &raquo; <a href="{{ post.url }}">{{ post.title }}</a> {% if post.tags.size > 0 %}<span class="tag-list hidden-xs">{% for tag in post.tags %}<a href="/blog/tags/{{ tag | downcase | slugize }}/">{{ tag }}</a>{% unless forloop.last %} {% endunless %}{% endfor %}</span>{% endif %}</p>
{% endfor %}


[feed]: {{ site.feedname }}



<p>
<a href="/blog/archives">Older Posts &rarr;</a>
</p>
