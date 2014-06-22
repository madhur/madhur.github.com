---
title: Projects
layout: project
---

{% for project in site.data.projects %}					
{% if project.publish == true %}
<div class="project-title">
<a href="/projects/{{ project.project }}.html">{{ project.project }}</a>     <span class="tag-project hidden-xs">{{ project.category }}</span>
<br/>
</div>
<div class="project-description hidden-xs">
{{ project.description }}
</div>

{% endif %}		
{% endfor %}



