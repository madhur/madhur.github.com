---
layout: blog-post
title: "Using sshpass to skip entering passwords for SSH"
excerpt: "Using sshpass to skip entering passwords for SSH"
disqus_id: /2021/10/23/using-sshpass-to-skip-entering-password/
tags:
    - SSH
---

If your server does not allow key based login, you might need to enter password each time you want to ssh into.

`ssh` does not allow entering password into the command line.

There is a nifty tool to allow exactly that `sshpass`

```
$ sudo apt-get install sshpass
$ sshpass -p your_password ssh user@hostname
```

On Mac

```
brew install hudochenkov/sshpass/sshpass
```


