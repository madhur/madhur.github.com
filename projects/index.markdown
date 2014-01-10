---
title: Projects
layout: project
---

<br/>
<div>
{% for project in site.data.projects %}
					
						{% if project.publish == true %}
							<a href="/projects/{{ project.project }}.html">{{ project.project }}</a>
							
							<span class="tag-project">{{ project.category }}</span>
							<br/>
							<br/>
							{{ project.description }}
							<br/>
							<br/>
							<hr/>
						{% endif %}
		
{% endfor %}
</div>


