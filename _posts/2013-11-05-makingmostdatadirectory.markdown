---
layout: blog-post
title: "Making most out of _data directory in Jekyll"
excerpt: "Making most out of _data directory in Jekyll"
disqus_id: /2013/11/05/makingmostdatadirectory/
location: New Delhi, India
time: 9:00 PM
tags:
- Jekyll
categories:
- Web Development
---


Jekyll 1.3.0 comes with exiciting new features especially the use of \_data directories. The ***\_data*** directory is very useful in cases where you want to store
metadata related to your site or blog and want to load it in runtime. Earlier people used to put this in \_config.yml which was kind of a hack.

##How can you make most out of \_data directory ?##

If you've a file trucks.yaml under \_data/, then you can access it with **{ for truck in site.data.trucks }**. So you can have members.yaml, projects.yaml, products.yaml under \_data, and access them respectively as site.data.members, site.data.projects and site.data.products.

For instance, this current site itself makes use of \_data directory extensively. Have a look at [Projects](/projects) section.

The entire left navigation of [Projects](/projects) section is driven dynamically through a simple YAML file in \_data directory, which is [projects.yaml](https://github.com/madhur/madhur.github.com/blob/source/_data/projects.yaml) and looks like:

{% highlight yaml %}
---
- project: Hermes
  category: Android
  publish: yes
  description: Hermes is an attempt to provide a sense of security to all the travelers 
  of all over the world and especially the women in India who use the public transport to 
  commute to their work place and back home.
  
- project: Silverlight Organization Chart for SharePoint
  category: SharePoint
  publish: yes
  description: A silverlight Chart control which retrieves data from the SharePoint list. 
  
- project: STP Inspector
  category: SharePoint
  publish: yes
  description: STP Inspector is an site template inspector for WSS/MOSS 2007. 
  It analyzes a site template file (.stp) and basically shows its dependencies on the site 
  features and site collection features.  
{% endhighlight %}  

Now what I can in Jekyll is simply refer to Project Name, cateogy, description using the site variable array as **site.data.projects** and loop through it using

{% highlight html %}
{% raw %} 
{% for project in site.data.projects %}
{{ project.project }}
{% endfor %}
{% endraw %} 
{% endhighlight %}  

Using the simple structure above, I have dynamically generated both my left navigation and content page. In future, if I work on a new project, I just need to edit this ***projects.yaml*** file and Jekyll would automatically update the left navigation and content page.

This is the simple code of generating left navigation which I have done in my includes file  [***projects-left.html***]()

{% highlight html %}
{% raw %} 
<div id="projects">
    <p class="single"><a href="/projects">Projects</a></p>

    {% for category in site.data.categories %}
        <p class="project-category">{{ category.category }}</p>
            <ul class="subcategory">

                {% for project in site.data.projects %}
                
                    {% if project.category == category.category and project.publish == true %}
                        <li><a href="/projects/{{ project.project }}.html">{{ project.project }}</a></li>
                    {% endif %}

                {% endfor %}
        </ul>
    {% endfor %}

</div> 
{% endraw %} 
{% endhighlight %}  

This is how I generate my content page which nicely generates the project names along with descriptions. You can have a look at source [here](https://raw.github.com/madhur/madhur.github.com/source/projects/index.markdown)

{% highlight html %}
{% raw %} 
{% for project in site.data.projects %}
                    
    {% if project.publish == true %}
        <strong><a href="/projects/{{ project.project }}.html">{{ project.project }}</a></strong>
        
        <span class="tag-project">{{ project.category }}</span>
        {{ project.description }}
        <hr/>
    {% endif %}
        
{% endfor %}
</div>
{% endraw %} 
{% endhighlight %} 

This is where \_data directory comes in handly where you don't want to embed little pieces of information regarding your site in dirty repeating html. Using \_data directory, you can make the information which is going to change over the period of time structurable and also provide dynamism at the same time.


