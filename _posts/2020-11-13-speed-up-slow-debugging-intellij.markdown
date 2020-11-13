---
layout: blog-post
title: "Speed up debugging in IntelliJ"
excerpt: "speed-up-slow-debugging-intellij"
disqus_id: /2020/11/13/speed-up-slow-debugging-intellij/
tags:
    - IntelliJ
---

Yesterday, I observed painfully slow debugging in IntelliJ. Every step over or
step in took almost 10 seconds to perform.

It was a simple Java console application having about some 88k entries in
few arrays. I had successfully debugged applications having millions of entries
in arrays, lists and maps before without any performance issues.

Then I looked at the `toString()` implementation of the custom object which I
was holding in the array


```java
 public String toString() {
        StringBuilder s = new StringBuilder();
        s.append(V + " vertices, " + E + " edges " + NEWLINE);
        for (int v = 0; v < V; v++) {
            s.append(String.format("%d: ", v));
            for (int w : adj[v]) {
                s.append(String.format("%d ", w));
            }
            s.append(NEWLINE);
        }
        return s.toString();
    }
```

This `toString()` implementation was looping over all the 88k items and IntelliJ
is configured to evaluate `toString()` after every step.

Turning off the setting `Enable toString() data views` solved this problem of
slow debugging.

Incase you are experiencing slow debugging issues on IntelliJ, do make sure that
this setting is turned off.

<img src='/images/Blog/screenshot67.jpg'  />