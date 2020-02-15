---
layout: blog-post
title: "Must have Java code analysis Tools - Part 3"
excerpt: "Must have Java code analysis Tools - Part 3"
disqus_id: /2020/02/15/must-have-java-code-analysis-tools-part3/
tags:
- Java
---

* [Must have Java code analysis Tools - Part 1]({% post_url 2020-01-26-must-have-java-code-analysis-tools-part1 %}) 
* [Must have Java code analysis Tools - Part 2]({% post_url 2020-02-02-must-have-java-code-analysis-tools-part2 %}) 

In the last [post]({% post_url 2020-02-02-must-have-java-code-analysis-tools-part2 %}), we looked at [Spotbugs](https://spotbugs.github.io/), which focuses on the code linting at the bytecode level.

In this post, we will look at [PMD](https://pmd.github.io/), which agains works at the source level to find out possible bugs in your java code.

The list of entire checks which PMD finds can be found [here](https://pmd.github.io/pmd-6.21.0/pmd_rules_java.html)

There is also a [discussion](https://stackoverflow.com/questions/4297014/what-are-the-differences-between-pmd-and-findbugs) of differences between Findbugs and PMD

## Running the PMD

Instead of focusing on running with build process, I will focus on running it manually. Though it still can be integrated with build process and that remains the recommended apporach.

On MAC, it can be simply installed with command `brew install pmd`

On other OS, installation instructures are given [here](https://pmd.github.io/latest/pmd_userdocs_installation.html)

### Configuring Rules

As shown in the documentation, PMD comes with rich set of rules. As opposed to Checkstyle, PMD is lot fuzzier in its analysis i.e. it can flag rules, which sometimes might not be really a violation. For this reason, PMD allows you to assign priorities (a number between 1 to 5) to the rules and then based on your preferences, you can choose to fix, let's say highest priority issues only (1 being the highest).

### Executing PMD

Once PMD is installed, it can be executed simply as below in the root directory of your project.

```bash
pmd pmd -d ./ -language java -R rulesets/java/quickstart.xml
```

Here `rulesets/java/quickstart.xml` specifies the list of rules to be executed which is an inbuilt ruleset to get started with. 

We can also filter the output by priority, such as 

```bash
pmd pmd -d ./ -language java -R rulesets/java/quickstart.xml - min 2
```

I prefer to create my own rules file for my projects. A custom rule file can be specified as

```bash
pmd pmd -d ./ -language java -R ./pmd-rules.xml
```

Finally, here is the list of rules, which I use for my projects. This has served us really well.


<script src="https://gist.github.com/madhur/62e57a851b1dbfbbc3a2646d32dd8897.js"></script>

