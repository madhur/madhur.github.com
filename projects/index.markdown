---
title: Projects
layout: project
---

{% for project in site.data.projects %}					
{% if project.publish == true %}
<a href="/projects/{{ project.project }}.html">{{ project.project }}</a>     <span class="tag-project">{{ project.category }}</span>
<br/>
{{ project.description }}
<hr/>
{% endif %}		
{% endfor %}



