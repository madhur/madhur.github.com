---
layout: blog-post
title: "Adding package suppressions in Checkstyle and Spotbugs"
excerpt: "Adding package suppressions in Checkstyle and Spotbugs"
disqus_id: /2020/03/28/adding-package-suppressions-checkstyle-spotbugs/
tags:
- Checkstyle
- Spotbugs
- Java
---

I was recently trying to add a package level suppression in both checkstyle / spotbugs and found it to be having weird syntax.

For [checkstyle](https://github.com/checkstyle/checkstyle/blob/master/config/suppressions.xml),

First add a module in your checkstyle configuration file

```xml
<module name="SuppressionFilter">
    <property name="file" value="./suppressions.xml"/>
</module>
```

And then in the `suppressions.xml` , specify the package as follows:

```xml
<?xml version="1.0"?>
<!DOCTYPE suppressions PUBLIC
        "-//Puppy Crawl//DTD Suppressions 1.1//EN"
        "http://www.puppycrawl.com/dtds/suppressions_1_1.dtd">

<suppressions>
    <suppress files="[\\/]com[\\/]domain[\\/]package" checks="."/>
</suppressions>
```

For, [Spotbugs](https://spotbugs.readthedocs.io/en/stable/filter.html), you specify the package level suppression in the exclude file as follows

```xml
<FindBugsFilter>
    <Match>
        <Package name="~com\.domain\.package.*"/>
    </Match>
</FindBugsFilter>
```

