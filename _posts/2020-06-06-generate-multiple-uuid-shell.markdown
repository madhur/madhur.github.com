---
layout: blog-post
title: "Generate multiple UUID in shell"
excerpt: "Generate multiple UUID in shell"
disqus_id: /2020/06/06/generate-multiple-uuid-shell/
tags:
    - Shell
---

Recently, I was required to generate multiple UUID's and pass onto HTTP request as a paremeter. I thought of using [Python]() or [Node.js]() for this purpose, but thought why not use a plain old [shell]().

But, is there a way to generate UUID in shell? Turns out, there is using [uuidgen]() command which works on both Linux and MacOS.
