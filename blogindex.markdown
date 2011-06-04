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

More [information](/info) about this blog and a complete archive of [past](past.html) posts, are 
available via links at the top of the page.

[![Feed icon](/files/css/feed-icon-14x14.png){:title="Atom feed of recent posts" .right}][feed]
A [feed][] of the most recent posts is also available.

[feed]: {% include feedname.txt %}

###Latest Blog updates###

<table id="highlight" cellpadding="0" cellspacing="0" border="0">
{% for post in site.posts %}


<tr>

  
  <td class="title"><a  href="{{ post.url }}" data-disqus-identifier="{{ post.disqus_id }}">{{ post.title }}</a></td>
  <td class="date">{{ post.date | date_to_string }}</td>
  <td class="time"><a class="comments" data-disqus-identifier="{{ post.disqus_id }}" href="{{ post.url }}#disqus_thread">View Comments</a></td>
  

</tr>

{% endfor %}
</table>

<p>
<a href="past.html">Older Posts &rarr;</a>
</p>

{% include commentcount.js %}
