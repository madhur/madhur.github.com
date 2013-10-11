---
layout: blog-post
title: "Best fonts for programming"
excerpt: Best fonts for programming
disqus_id: /2011/09/09/bestfontscode/
location: Delhi, India
time: 8:00 PM
tags:
- Code
- Programming
---

Recently I have been observing the change in the trend in the preferred font for programming.   

Back in the earlier days *Courier New* used to be the preferred font for programming. This was the default font in Visual Studio 2008.
However, with later operating Systems and tools such as Visual Studio 2010, *Consolas* is becoming the top preferred font for programming.

The screenshot below shows the same code with Courier New and Consolas.

![](/images/courier-vs.png)
![](/images/consolas-vs.png)

The prime difference between two fonts is that Consolas is Clear Type optimized font. [Clear Type](http://en.wikipedia.org/wiki/ClearType) is the Microsoft implementation of [True Type](http://en.wikipedia.org/wiki/TrueType).

Programmers also need to work with Console and terminals as well be it Win OS or Linux. Still in Windows 7, 2008 R2, font in Command Prompt or Powershell is by default set to 
*Raster fonts* which by default maps to either *Terminal*.

You might be wondering why there are only limited options to set the font in Command prompt or Powershell. You can enable more options by editing the registry as outlined in this 
[KB article](http://support.microsoft.com/default.aspx?scid=kb;EN-US;Q247815).

The reasoning for this is also detailed by veteran MS employee **Raymond Chen** in his [The Old new thing blog](http://blogs.msdn.com/b/oldnewthing/archive/2007/05/16/2659903.aspx)

Consolas works even better with Consoles and terminal windows as well. The screen shot below compares *Terminal* and *Consolas* in command prompt. Decide for yourself.

![](/images/raster-con.png)
![](/images/consolas-con.png)

I have also switched from *Terminal* to *Consolas* in my favourite editor [Notepad++](http://notepad-plus-plus.org/). It definitely looks better, see below

![](/images/notepad-term.png)
![](/images/notepad-cons.png)

##Installing Consolas in Linux##
You might also want to use Consolas in Linux terminal and Gedit, Gvim or vim.

##Method 1##
Create a '.fonts' folder in your home directory and copy the necessary fonts into it. Now you have access to the fonts on a per user basis.

##Method 2##

First find out in which location linux has installed the truetype fonts.

{% highlight text %}
find /usr -iname \*.ttf |head -n 5
{% endhighlight %}

Once you know the path of the fonts directory, move to this directory and create a folder there (it can be any name). Next copy all the windows ttf fonts to the windowsfonts directory that was just created.

Now change the ownership of the fonts as well as make sure they have a right of 644 .

{% highlight text %}
# chown root.root *.ttf
# chmod 644 *.ttf
{% endhighlight %}

Run the command mkfontdir while in the windowsfonts directory.

{% highlight text %}
# mkfontdir
{% endhighlight %}

This will create an index of the fonts in the directory. It will also create two files fonts.dir and fonts.cache-1 .
Now moving to the parent directory, edit the file fonts.cache-1 using your favourate editor and append the following line to it.

{% highlight text %}
File: /usr/share/fonts/truetype/fonts.cache-1
...
"windowsfonts" 0 ".dir"
{% endhighlight %}

Lastly run the command fc-cache.
{% highlight text %}
 fc-cache
{% endhighlight %} 

##Other good programming fonts##
* Inconsolata
* Proggy Clean
* Terminus
* Fixed Sys
* Andale Mono
* Anonymous
* Terminus

##References##
* [http://www.codeproject.com/KB/work/FontSurvey.aspx](http://www.codeproject.com/KB/work/FontSurvey.aspx)
