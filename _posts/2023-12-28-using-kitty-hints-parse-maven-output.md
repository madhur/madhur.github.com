---
layout: blog-post
title: "Using Kitty hints to parse maven output"
excerpt: "Using Kitty hints to parse maven output"
disqus_id: /2023/12/28/using-kitty-hints-parse-maven-output/
tags:
    - Kitty
    - Terminal
---

[Kitty](https://github.com/kovidgoyal/kitty) is a very fast and feature rich terminal which has soon become my favourite.

One of the powerful features of Kitty is its customizability.

One such feature is [Kitty hints](https://sw.kovidgoyal.net/kitty/kittens/hints/)

Kitty hints allows you to select text on terminal and perform an action through a shortcut key. It is completely customizeable.

Common kitty hints action include opening files, folders and opening web urls outputted in terminal.

One example where, I was able to customize it was to parse maven output and makes the file links clickable to land directly on the line numbers.

For example, consider this build output:

```
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  0.618 s
[INFO] Finished at: 2023-12-28T10:08:38+05:30
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.8.0:compile (default-compile) on project reactive-programming: Compilation failure: Compilation failure: 
[ERROR] /run/media/madhur/centos/home/madhur/github/personal/reactive-programming/src/main/java/in/co/madhur/mono/FileService.java:[17,9] invalid method declaration; return type required
[ERROR] /run/media/madhur/centos/home/madhur/github/personal/reactive-programming/src/main/java/in/co/madhur/mono/FileService.java:[17,20] illegal start of type
[ERROR] /run/media/madhur/centos/home/madhur/github/personal/reactive-programming/src/main/java/in/co/madhur/mono/Lec08MonoRunnable.java:[15,54] ';' expected
[ERROR] /run/media/madhur/centos/home/madhur/github/personal/reactive-programming/src/main/java/in/co/madhur/mono/Lec06SupplierRefactoring.java:[25,37] ';' expected
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException

```


Using kitty hints, we can make the file paths to `FileService.java` , `Lec08MonoRunnable.java` and `Lec06SupplierRefactoring.java` clickable and land it directly on appropriate line numbers.


This required writing custom regex to parse this line and emitting two named capturing groups `path` and `line`.

This can be done in `kitty.conf` as :

```conf
map kitty_mod+p kitten hints --type=regex --regex="(?<path>(?:\/[\w-_^ ]+)+\/?(?:[\w.])+[^.]):\[(?<line>\d+),\d+\].?" --program "launch /home/madhur/scripts/editor.py"
```

The `editor.py` is a simple program which is invoked with parameters `path=...../FileService.java` and `line=17`

In my case, I launch [`Neovim`](https://github.com/neovim/neovim) or [`IntelliJ`](https://www.jetbrains.com/idea/) depending upon if `Intellij` is previously running.

This can be simply done through following snippet:

```python
#!/usr/bin/env python3

import sys
import os
import subprocess

myObject = {}
for line in sys.argv:
    if '=' not in line:
        continue
    print(line)
    key, value = line.rstrip("\n").split("=")
    myObject[key] = value

print(myObject)

idea_running = False
pl = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
list_ps = pl.decode('utf-8')

if 'intellij' in list_ps:
    idea_running = True

if idea_running is True and 'java' in myObject['path']:
    print("Intellij found")
    os.system("flatpak run com.jetbrains.IntelliJ-IDEA-Community " + myObject['path'])
else:
    print("Intellij not found")
    os.system("nvim " + " +"+myObject['line'] + " " + myObject['path'])
```