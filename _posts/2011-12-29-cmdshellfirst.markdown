---
layout: blog-post
title: "Windows command shell(cmd.exe) runs only first command"
excerpt: "Windows command shell(cmd.exe) runs only first command"
disqus_id: /2011/12/29/cmdshellfirst/
location: New Delhi, India
time: 8:00 PM
categories:
- Windows
---

If you written a command shell script and it exits after executing only first command, its probably because one of the command in the
command script is itself a command script. In that case, such script needs to be called using the *call* command.

For example,

{% highlight text %}
@echo off
echo "Building Content"
jekyll --no-server --no-auto

echo "Checking out master"
git checkout master


echo "Copying the updated content to root"
cp -r _site/* . && rm -rf _site/ && touch .nojekyll

echo "Adding the content"
git add .

echo "Updated content"
git commit -am "Updated content"

echo "Pushed content"
git push --all origin
{% endhighlight %}

The above script will simply exit after running the first command. This is because Jekyll itself runs as a batch file in Windows. To correct this, we need to call Jekyll with the use of *call* command

{% highlight text %}
@echo off
echo "Building Content"
call jekyll --no-server --no-auto

echo "Checking out master"
git checkout master


echo "Copying the updated content to root"
cp -r _site/* . && rm -rf _site/ && touch .nojekyll

echo "Adding the content"
git add .

echo "Updated content"
git commit -am "Updated content"

echo "Pushed content"
git push --all origin
{% endhighlight %}