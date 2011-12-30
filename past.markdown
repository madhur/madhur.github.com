---
layout: blog
title: Archives
feed: atom.xml
keywords: Blog, Research, Academia
---

Archives
========

<div id="archive">
  {% for post in site.posts %}
			{% capture tmp_year %}{{ post.date|date:'%Y' }}{% endcapture %}
      {% if year != tmp_year %}
				{% assign year = tmp_year %}
        <h1 class="year">{{ year }}</h1>
      {% endif %}
			{% capture tmp_month %}{{ post.date|date:'%B' }}{% endcapture %}
      {% if month != tmp_month %}
        {% assign month = tmp_month %}
        <h2 class="month">{{ month }}</h2>
      {% endif %}
      <div class="archive-link">
        <span class="archive-date">{{ post.date|date:'%d' }}</span>
        <a href="{{ post.url }}">{{ post.title }}</a>
      </div>

  {% endfor %}
</div>
