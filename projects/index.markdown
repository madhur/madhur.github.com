---
title: Projects
layout: project
---

<h3>Check out my projects. All projects are open source.</h3>
<br/>
<div>
{% for project in site.data.projects %}
					
						{% if project.publish == true %}
							<strong><a href="/projects/{{ project.project }}.html">{{ project.project }}</a></strong>
							
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


