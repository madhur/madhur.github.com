---
layout: blog-post
title: "Must have Java code analysis Tools - Part 1"
excerpt: "Must have Java code analysis Tools - Part 1"
disqus_id: /2020/01/26/must-have-java-code-analysis-tools-part1/
tags:
- Java
---

When you are working in a big team ( > 5 engineers), It is very important to have consistent code styling, development environment and code review process. As a reviewer, its very difficult I see different 
class naming conventions everytime, unused variables or imports etc. Hence, its very important that a team shares same coding styles and codingi standards.

In this post, we will look at [checkstyle](https://github.com/checkstyle/checkstyle) , a tool that helps developers adhere to coding standards. Checkstyle operates at the source level, i.e. even befor the compile phase has started

## Running with build process

The code analysis tools such as checkstyle are most useful when integrated with build process as useful reports can be generated and even build can be failed to enforce the standards.

For example, We use the following section in [pom.xml](https://maven.apache.org/guides/introduction/introduction-to-the-pom.html) to run checkstyle as part of build process


```xml
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-checkstyle-plugin</artifactId>
	<version>3.1.0</version>
	<configuration>
		<configLocation>./checks.xml</configLocation>
		<encoding>UTF-8</encoding>
		<consoleOutput>true</consoleOutput>
		<failsOnError>true</failsOnError>
		<linkXRef>false</linkXRef>
	</configuration>
	<executions>
		<execution>
			<id>validate</id>
			<phase>validate</phase>
			<goals>
				<goal>check</goal>
			</goals>
		</execution>
	</executions>
</plugin>
```

Here setting `failsOnError`  attribute `true` causes the build to fail if violations are fail. The file `checks.xml` specifies the styling configuration. I used the modified [google check style](https://google.github.io/styleguide/javaguide.html#s4.1-braces) to make our own styling conventions.

<script src="https://gist.github.com/madhur/745b42c72efa8986340cb05acab91497.js"></script>

