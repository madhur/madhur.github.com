---
layout: blog-post
title: "Homelab Dashboard"
excerpt: "Homelab Dashboard"
disqus_id: /2025/02/01/revealing-hidden-characters/
tags:
    - Shell
---

Recently we faced an issue, where there were some hidden characters inside the hostname of a configuration store of our backend services.

Because of this, we were getting continously getting DNS resolution errors.

One quick way to reveal such hidden characters is to run the command

```shell

echo "string" | cat -v

```

For example try copying the belwo string into dig or a whois website.

```
madhur.​co.​in
```


The above string contains hidden characters which can be reveled as follows


```
echo "madhur.co.in" | command cat -v
madhur.M-bM-^@M-^Kco.M-bM-^@M-^Kin
```

Sometimes these characters are not visible even in terminals, because modern terminals tend to be very good "renderers" and would render these hidden characters.

