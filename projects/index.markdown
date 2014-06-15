---
title: Projects
layout: project
---

{% for project in site.data.projects %}					
{% if project.publish == true %}
<a href="/projects/{{ project.project }}.html">{{ project.project }}</a>     <span class="tag-project hidden-xs">{{ project.category }}</span>
<br/>
<div class="hidden-xs">
{{ project.description }}
</div>
<hr/>
{% endif %}		
{% endfor %}



