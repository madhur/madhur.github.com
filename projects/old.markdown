---
title: Legacy Projects
layout: project
---

These are some of the legacy projects which I had worked on. I am not actively maintaining them right now.

<ul class="project-list">
{% for project in site.data.projects %}
{% assign item = project[1] %}
{% for member in item.projects %}
{% if member.publish == false %}
<li>
    <a href="/projects/{{ member.file }}.html"><strong>{{ member.project }}</strong></a>
    <span class="project-desc">{{ member.description }}</span>
</li>
{% endif %}
{% endfor %}
{% endfor %}
</ul>
