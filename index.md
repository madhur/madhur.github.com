---
layout: name
title: Home
section: Home
---

Hi, I'm Madhur — a software developer who likes building things and writing about technology.

Check out my [projects](/projects) or browse recent posts below.

Recent Posts
------------
<ul class="recent-posts">
{% for post in site.posts limit:5 %}
{% assign words = post.content | number_of_words %}
{% assign minutes = words | divided_by: 200 %}
{% if minutes < 1 %}{% assign minutes = 1 %}{% endif %}
<li>
    <a href="{{ post.url }}">{{ post.title }}</a>
    <span class="post-info">{{ post.date | date: "%b %d, %Y" }} · {{ minutes }} min read</span>
</li>
{% endfor %}
</ul>

[View all posts →](/blog)

Contact
--------
Feel free to reach out through any of the channels below or through this [contact form](/contact).

<ul class="contact-icons">
<li><a href="http://www.linkedin.com/in/madhurahuja"><i class="fa fa-linkedin-square fa-3x"></i></a></li>
<li><a href="http://stackoverflow.com/users/507256/madhur-ahuja"><i class="fa fa-stack-overflow fa-3x"></i></a></li>
<li><a href="https://github.com/madhur"><i class="fa fa-github fa-3x"></i></a></li>
<li><a href="mailto:ahuja.madhur@gmail.com"><i class="fa fa-inbox fa-3x"></i></a></li>
</ul>
