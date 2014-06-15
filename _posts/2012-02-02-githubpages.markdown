---
layout: blog-post
title: "GitHub Pages are served from the Default Branch"
excerpt: "GitHub Pages are served from the Default Branch"
disqus_id: /2012/02/02/githubpages/
location: New Delhi, India
time: 2:00 PM
tags:
- Github
---


Yesterday, after a simple commit, my entire site went down. I spent entire day troubleshotting the issue. In the end, the resolution was simple: change the default branch.

The [GitHub Pages documentation](http://pages.github.com/) says that you can push a file named **index.html** onto your **master** branch to make it automatically available at **username.github.com**

> *Let's say your GitHub username is "Alice" If you create a GitHub repository named alice.github.com, commit a file named index.html into the master branch, and push it to GitHub, then this file will be automatically published to http://alice.github.com/.*

What it doesn't say that, it will not work if you have changed your default branch from **master** to something else. In that case, **index.html** should be pushed to default branch.

Since I use Jekyll with custom plugins, I maintain two branches: **Source**  to store source Jekyll files  and **master** for the published content. I had mistakenly set the **source** branch to be default rendering the whole site to be unavailable.

In nutshell, always remember that pages are always served from the default branch and not **master** branch.