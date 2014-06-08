---
layout: blog-post
title: "Guide to building Git 2.0.0 from sources on Windows"
excerpt: "Guide to building Git 2.0.0 from sources on Windows"
disqus_id: /2014/06/08/guidebuildgit2/
location: New Delhi, India
time: 9:00 PM
tags:
- Git
---


[Git 2.0.0](https://git.kernel.org/cgit/git/git.git/tree/Documentation/RelNotes/2.0.0.txt) just released few days back.

However, just like many other popular Linux tools, Windows Community is ignored. There is no official build of Git 2.0.0 for Windows.

As of this writing, [MysysGit for Windows](http://msysgit.github.io/) has latest version 1.9.2 availalbe for download.

Eager to try out this new version, I decided to build it myself. I have published the binaries [here]() incase you directly want to grab the 2.0.0 build for Windows.
Note that I have not tested it thoroughly myself. If you face any issues, do bring it to my notice but I am in no way responible for it. Use it at your own risk.


1. Download MysysGit build envrionment for Windows from here - [https://github.com/msysgit/msysgit](https://github.com/msysgit/msysgit)

Place it in a directory such as `C:\gitbuild`

2. Download official Git 2.0.0 from here - [https://github.com/msysgit/git](https://github.com/msysgit/git)

Copy this entire source into the `git` directory  in `C:\gitbuild\git`

> Note: Actually, the git repository in the first step has a submodule pointing to the second repository in `C:\gitbuild\git`. If you are familiar with Git          > submodules, you can download via submodule command as well.

3. Execute `msys.bat` from `C:\gitbuild\`. You should be now in bash console as follows:

{% highlight text %}
Welcome to msysGit


Run 'git help git' to display the help index.
Run 'git help <command>' to display help for specific commands.
Run '/share/msysGit/add-shortcut.tcl' to add a shortcut to msysGit.

It appears that you installed msysGit using the full installer.
To set up the Git repositories, please run /share/msysGit/initialize.sh

madhur@MADHUR-PC /
$
{% endhighlight %}

> Note: In some envrionments, the build process should automatically begin after executing msys.bat. If it doesn't go to the next step.

4. `cd` to `C:\gitbuild\git` and execute `make` command. The build process should now begin:

C:\gitbuild>msys.bat

{% highlight text %}
-------------------------------------------------------
Building and Installing Git
-------------------------------------------------------
GIT_VERSION = 2.0.0
    * new build flags
    CC credential-store.o
    * new link flags
    CC abspath.o
    CC advice.o
    CC alias.o
    CC alloc.o
    CC archive.o
    CC archive-tar.o
{% endhighlight %}

Once the build is complete, you may exit the bash shell.

5. The build process automatically places the git binaries in `C:\gitbuild\bin`. To confirm you have successfully built, `cd` to `C:\gitbuild\bin` and execute `git.exe`

{% highlight text %}
C:\gitbuild\bin>git --version
git version 2.0.0
{% endhighlight %}

5. Congratulations you have just built Git 2.0.0 froms sources. However, there are some quirks and tweaks required to be corrected, which we cover in next steps.

6. `git gui` command throws an error as follows:

{% highlight text %}
git-gui: line 3: exec: wish: not found
fatal: 'gui' appears to be a git command, but we were not
able to execute it. Maybe git-gui is broken?
{% endhighlight %}

The reason of error is because `git gui` depends on `Tcl/Tl 8.5.13` package. I just copied the binaries from my old build and it works fine.

Following folders are required:
`git\lib\tcl8`
`git\lib\tcl8.5`
`git\lib\tk8.5`
`git\lib\tclConfig.sh`
`git\lib\tkConfig.sh`
`git\bin\wish.exe`
`git\bin\wish85.exe`
`git\bin\tcl85.dll`
`git\bin\tclpip85.dll`
`git\bin\tclsh.exe`
`git\bin\tclsh85.exe`
`git\bin\tk85.exe`

After copying these files, `git gui` works fine.

7. Another quirk