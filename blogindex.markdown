---
layout: blog
title: Blog
section: Blog
feed: atom.xml
keywords: C/C++, Windbg, Reverse Engineering, important
important: yes
---

Blog
=====================

This is [my](/) technical blog on C/C++, Windbg, Reverse Engineering, Assembly.

More [information](info.html) about this blog, its [kith](kith.html) (blogroll, 
bookmarks, _etc._), and a complete archive of [past](past.html) posts, are 
available via links at the top of the page.

[![Feed icon](/files/css/feed-icon-14x14.png){:title="Atom feed of recent posts" .right}][feed]
A [feed][] of the most recent posts is also available.

[feed]: /blog/atom.xml

Recent Posts
------------

{% for post in site.categories.blog limit:5 %}
<div class="section list">
  <h1>{{ post.date | date_to_string }}</h1>
  <p class="line">
  <a class="title" href="{{ post.url }}" data-disqus-identifier="{{ post.disqus_id }}">{{ post.title }}</a>
  <a class="comments" data-disqus-identifier="{{ post.disqus_id }}" href="{{ post.url }}#disqus_thread">View Comments</a>
  </p>
  <p class="excerpt">{{ post.excerpt }}</p>
</div>
{% endfor %}

<p>
<a href="past.html">Older Posts &rarr;</a>
</p>

{% include commentcount.js %}
