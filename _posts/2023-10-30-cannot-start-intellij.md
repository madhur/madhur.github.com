---
layout: blog-post
title: "Intellij cannot launch because 'process 2' already running"
excerpt: "Intellij cannot launch because 'process 2' already running"
disqus_id: /2023/10/30/cannot-start-intellij/
tags:
    - Linux
    - IntelliJ
---


I have occasionally got the error while starting [IntelliJ](https://www.jetbrains.com/idea/)

```
IntelliJ cannot launch because 'process 2' already running
```

The process ID sometimes changed, restarting or even re-installing Intellij doesn't solve the problem.

I run the [Flatpak](https://flatpak.org/) version of [IntelliJ](https://flathub.org/apps/com.jetbrains.IntelliJ-IDEA-Community)

There are multiple threads for this online which suggest different solutions:

[https://intellij-support.jetbrains.com/hc/en-us/community/posts/13541697317906-Error-while-opening-intellij-Cannot-connect-to-already-running-IDE-instance-Exception-Process-2-837-is-still-running-](https://intellij-support.jetbrains.com/hc/en-us/community/posts/13541697317906-Error-while-opening-intellij-Cannot-connect-to-already-running-IDE-instance-Exception-Process-2-837-is-still-running-)

[https://intellij-support.jetbrains.com/hc/en-us/community/posts/10865358461202-Intellij-cannot-launch-because-process-2-already-running](https://intellij-support.jetbrains.com/hc/en-us/community/posts/10865358461202-Intellij-cannot-launch-because-process-2-already-running)

[https://askubuntu.com/questions/1462372/ubuntu-cannot-launch-intellij-anymore](https://askubuntu.com/questions/1462372/ubuntu-cannot-launch-intellij-anymore)


[https://www.reddit.com/r/pycharm/comments/15esk6r/cannot_connect_to_already_running_ide_instance/](https://www.reddit.com/r/pycharm/comments/15esk6r/cannot_connect_to_already_running_ide_instance/)

The root of the problem is the `.lock` file which IntelliJ creates while starting up. If there is a unclean shutdown, there are chances that this file will exist and the product will throw the mentioned error.

Solution is to simply delete this file. This file resides in the preferences folder, which can be anywhere depending on the Operating System.

For me it resided in 

```shell
rm ~/.var/app/com.jetbrains.IntelliJ-IDEA-Community/config/JetBrains/IdeaIC2023.2/.lock
```

simply deleting this file, solves the problem.

For Mac OS, this file would potentially reside in 

```
/Library/Application Support/JetBrains/
```