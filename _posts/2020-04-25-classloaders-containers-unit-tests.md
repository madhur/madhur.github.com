---
layout: blog-post
title: "Classloaders, Containers & Unit Tests"
excerpt: "Classloaders, Containers & Unit Tests"
disqus_id: /2020/04/25/classlaoders-containers-unit-tests/
tags:
- Java
---

Classloaders are an important concept for every engineer to be aware of.

Classloaders are basic building blocks of Containers like Tomcat. Suppose, we have written a java application and have a singleton instance, we might say its singleton across JVM. Wrong. Its not singleton across JVM, its a singleton across classloader.

The same application can be deployed in a container like Tomcat, as two different application. In that case, there will be 2 copies of the Singleton object with exact same package and class names inside a single JVM.

Tomcat has a [dedicated page](http://tomcat.apache.org/tomcat-8.0-doc/class-loader-howto.html) on how it loads the classloaders.

