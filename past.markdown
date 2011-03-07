---
layout: blog
title: Archives
section: Past

feed: atom.xml
keywords: Blog, Research, Academia
---

Archives
========

This is the complete archive of posts from _[my blog](/blogindex.html)_
in reverse chronological order.

{% for post in site.posts%}

<div class="section list">
  <h1>{{ post.date | date_to_string }}</h1>
  <p class="line">
  <a class="title" href="{{ post.url }}">{{ post.title }}</a>
  <a class="comments" href="{{ post.url }}#disqus_thread">View Comments</a>
  </p>
  <p class="excerpt">{{ post.excerpt }}</p>
</div>
{% endfor %}

<ul>
{% for y in (2007..2025) reversed %}
{% for post in site.posts%}
  {% if {{y}} == {{post.date | date: '%Y'}} %}
    <li>{{ y }}
    <ul>
      {% for m in (1..12) reversed %}
        {% if site.posts[y][m] %}
          <li><a href='/{{ y }}/{{ m }}/'>{{ m | to_month}}</a></li>
        {% endif %}
      {% endfor %}
    </ul>
    </li>
  {% endif %}
{% endfor %}
{% endfor %}
</ul>
  



<script type="text/javascript">
//<![CDATA[
(function() {
		var links = document.getElementsByTagName('a');
		var query = '?';
		for(var i = 0; i < links.length; i++) {
			if(links[i].href.indexOf('#disqus_thread') >= 0) {
				query += 'url' + i + '=' + encodeURIComponent(links[i].href) + '&';
			}
		}
		document.write('<script type="text/javascript" src="http://disqus.com/forums/madhur/get_num_replies.js' + query + '"></' + 'script>');
	})();
//]]>
</script>
