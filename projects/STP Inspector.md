---
title: STP Inspector
layout: project-detail
github: SPProjects 
img:
- https://raw.github.com/madhur/SPProjects/gh-pages/screenshots/stp.jpg
---

<!--{% if site.generate_projects == true %}
{% octokit_contents  SPProjects;STPInspectorWin/Readme.markdown%}
{% endif %}-->


STP Inspector is an site template inspector for WSS/MOSS 2007. It analyzes a site template file (.stp) and basically shows its dependencies on the site features and site collection features. 

I wrote this utility to debug some of the issues which are faced while applying site templates saved from different server. The issues are more often when site template contains custom solution such as custom master page, web parts or features.

If the MOSS/WSS is installed on the machine on which this utility is run, it will show you if there is any feature which is missing on that system. In that case, you must install the missing feature from the source site.

This project was originally hosted on [Codeplex](https://stpinspector.codeplex.com/)