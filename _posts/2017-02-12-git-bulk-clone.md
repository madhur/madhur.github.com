---
layout: blog-post
title: "Bulk git clone repositories"
excerpt: "Bulk git clone repositories"
disqus_id: /2017/02/12/git-bulk-clone/
tags:
- Git
---

Recently, I was looking a way to do a git clone in bulk. I came across this nifty little script to do the same

{% highlight bash %}
#!/bin/bash
# The script clones all repositories of an GitHub organization.
# Author: Jens-Andre Koch

# the github organization to fetch all repositories for
GITHUB_ORGANIZATION=$1

# the git clone cmd used for cloning each repository
# the parameter recursive is used to clone submodules, too.
GIT_CLONE_CMD="git clone "

# fetch repository list via github api
# grep fetches the json object key ssh_url, which contains the ssh url for the repository
REPOLIST=`curl --silent https://api.github.com/orgs/${GITHUB_ORGANIZATION}/repos?per_page=200 -q | grep "\"ssh_url\"" | awk -F': "' '{print $2}' | sed -e 's/",//g'`

# loop over all repository urls and execute clone
for REPO in $REPOLIST; do
    ${GIT_CLONE_CMD}${REPO}
done
{% endhighlight %}

You can just invoke it with the argument of either user or organization. For example

`./clone.sh madhur`

The problem with this is that it will not clone the private repos since the API used in this request is unauthenticated and will not have access to the private repos.

I wrote a small little python script which will also clone the private repos.

First, you need to obtain your [personal access token](https://github.com/settings/tokens)

The gist is available [here](https://gist.github.com/madhur/b21e142b529a958ab6413e92bca39e17)

{% highlight bash %}
import requests
import json
import subprocess

GITHUB_ORGANIZATION = "madhur"
ACCESS_TOKEN=""
CLONE_DIR="./"

r = requests.get("https://api.github.com/orgs/" + GITHUB_ORGANIZATION + "/repos?per_page=200&access_token=" + ACCESS_TOKEN)

data = json.loads(r.text)

for repo in data:
    print repo['full_name']
    p = subprocess.Popen(["git","clone", repo['clone_url']], cwd=CLONE_DIR)  
    p.wait()

{% endhighlight %}

