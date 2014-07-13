---
title: Silverlight Organization Chart for SharePoint
layout: project-detail
github: SPProjects 
img:
- https://raw.githubusercontent.com/madhur/SPProjects/gh-pages/screenshots/list.png
- https://raw.githubusercontent.com/madhur/SPProjects/gh-pages/screenshots/chart.png
---

<!--{% if site.generate_projects == true %}
{% octokit_contents  SPProjects;OrgChart/Readme.markdown%}
{% endif %}-->

[Live Demo with Sample Data](http://www.madhur.co.in/silverdemo/Index.html)

Features
--------
* Collapse/Expand of Nodes
* Reset Root anywhere within the Org Chart
* Root can be permanently set in web part through parameters
* Optionally draws dotted line based on input data.

Steps 
-----
1. Get the .xap file

2. Insert the Silverlight WebPart in your SharePoint 2010 site and point it to .XAP file.

3. Create the list with schema shown in screenshot

4. Put the GUID of this list in the "Custom Initialization Property" of the web part as following

   "listGuid=48F17F97-77E8-4A38-8FA8-392120D0E899"

5. You can optionally also set the "Root Node" of the Org chart, For example

    "listGuid=48F17F97-77E8-4A38-8FA8-392120D0E899,CurrentRoot=Madhur"

    Here, the person with Title column value as Madhur will become the root.

This project was originally hosted on [Codeplex](https://madhur.codeplex.com/)