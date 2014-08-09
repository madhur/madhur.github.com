---
title: Vintage Projects
layout: project
---

<div class="row">
{% for project in site.data.oldprojects %}		
{% assign item = project[1] %}

{% for member in item.projects %}		



	<div class="col-md-4 col-xs-12 col-sm-6 col-lg-4">
	<div class="panel panel-default">

		<div class="project-title panel-title">
			<h3><a href="{{ member.file }}"> {{ member.project }}</a> </h3>    
	
		</div>
		
			<div class="panel-body">
				
				
				<div class="project-description ">
				{{ member.description }}
				</div>
		</div>
		
	</div>
	</div>



{% endfor %}
{% endfor %}

</div>

