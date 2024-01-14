---
layout: blog-post
title: "Code linting tools"
excerpt: "Code linting tools"
disqus_id: /2016/09/04/code-linting-tools/
tags:
- Lint
- Programming
---


Recently, I have been involved in integrating [linting](https://en.wikipedia.org/wiki/Lint_(software)) tools with our build tool [Jenkins](https://jenkins.io/)

I have been researching appropriate linting tools for programming languages used in our tech stack, primarily [Java](https://en.wikipedia.org/wiki/Java_(programming_language)), [Python](https://www.python.org/) and [Javascript](https://en.wikipedia.org/wiki/JavaScript)


Given below is my findings and our choosen lint tools.

## Java

* [Findbugs](http://findbugs.sourceforge.net/)
  It looks for bugs in Java programs. It can detect a variety of common coding mistakes, including thread synchronization problems, misuse of API methods, etc.

* [PMD](http://pmd.github.io/)
  It scans Java source code and looks for potential problems: Possible bugs, Dead code, Suboptimal code, Overcomplicated expressions and Duplicate code.

* [Checkstyle](http://checkstyle.sourceforge.net/)  
  It is a development tool to help programmers write Java code that adheres to a coding standard.

## Javascript

* [EsLint](http://eslint.org/)  
  ESLint is the most recent out of the four. It was designed to be easily extensible, comes with a large number of custom rules, and it’s easy to install more in the form of plugins. It gives concise output, but includes the rule name by default so you always know which rules are causing the error messages.

    ESLint documentation can be a bit hit or miss. The rules list is easy to follow and is grouped into logical categories, but the configuration instructions are a little confusing in places. It does, however, offer links to editor integration, plugins and examples all in a single location.

* [JSHint](http://jshint.com/)  
  JSHint was created as a more configurable version of JSLint (of which it is a fork). You can configure every rule, and put them into a configuration file, which makes JSHint easy to use in bigger projects. JSHint also has good documentation for each of the rules, so you know exactly what they do. Integrating it into editors is also simple.

    A small downside to JSHint is that it comes with a relaxed default configuration. This means you need to do some setup to make it useful. When comparing it with ESLint, it’s also more difficult to know which rules you need to change in order to enable or disable certain error messages.

* [JSLint](http://www.jslint.com/)  
  JSLint is the oldest of the four. Douglas Crockford created it in 2002 to enforce what, in his experience, are the good parts of JavaScript. If you agree with the good parts, JSLint can be a good tool—you install it and it’s ready to go.

## Python
* [pychecker](http://pychecker.sourceforge.net/) - executes (be careful)
* [pyflakes](https://pypi.python.org/pypi/pyflakes) - parses, great for finding NameErrors, obsolete imports
* [pylint](https://www.pylint.org/) - parses, very comprehensive (on the excessive-compulsive side).
* [pep8](https://www.python.org/dev/peps/pep-0008/) - parses, a style checker.
* [flake8](https://pypi.python.org/pypi/flake8) - parser, combines pep8 and pyflakes, with added complexity support, extensible.

## Conclusion
For java, we went with [Findbugs](http://findbugs.sourceforge.net/), simply because the kind of problems it can detect. Other java linting tools focus more on code style, indentation, spacing , variable naming etc. Findbugs is only tool which can go deep and find out some real issues in your code.

For Javascript, [ESLint](http://eslint.org/), because of its extensibility. Other contenders like JSHit and JSLint are either obsolete or does not offer extensibility.

For python, we went with [pylint](https://www.pylint.org/) again because of its extensibility.


There are some other tools which are programming language agnostic such as [Sonar](http://www.sonarqube.org/). However, I haven't got a chance to try them.
