---
title: Projects
layout: project
---

<ul class="project-list">
{% for project in site.data.projects %}
{% assign item = project[1] %}
{% for member in item.projects %}
{% if member.publish == true %}
<li>
    <a href="/projects/{{ member.file }}.html"><strong>{{ member.project }}</strong></a>
    <span class="project-desc">{{ member.description }}</span>
</li>
{% endif %}
{% endfor %}
{% endfor %}
</ul>

<p style="margin-top: 2em;">
<a href="/projects/old.html">View some of my legacy projects</a>
</p>
