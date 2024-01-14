---
layout: blog-post
title: "Executing commands in parallel in Shell and other fun stuff"
excerpt: "Executing commands in parallel in Shell and other fun stuff"
disqus_id: /2020/06/06/generate-multiple-uuid-shell/
tags:
    - Shell
---

Recently, I was required to generate multiple UUID's and pass onto HTTP request as a parameter. I thought of using [Python](https://www.python.org/) or [Node.js](https://nodejs.org/en/) for this purpose, but thought why not use a plain old [shell](https://en.wikipedia.org/wiki/Unix_shell).

But, is there a way to generate UUID in shell? Turns out, there is using [uuidgen](https://www.man7.org/linux/man-pages/man1/uuidgen.1.html) command which works on both Linux and MacOS.

Hence, using the power of another command called [seq](https://en.wikipedia.org/wiki/Seq_(Unix)), and [xargs](https://man7.org/linux/man-pages/man1/xargs.1.html) we can achieve many powerful things on shell

Sequentially print 1 to 10000:

```console
seq 1 10000
```

Print and pipe to `xargs` command for printing the output using single thread

```console
seq 1 10000 | xargs -I {} -P 1 printf '{}\n'
```

Parallelly print 1 to 10000 using 10 threads:

```console
seq 1 10000 | xargs -I {} -P 10 printf '{}\n'
```

You can test out the parallelism using [time](https://www.man7.org/linux/man-pages/man1/time.1.html) command, which will print the output for above 2 commands. For me output is:

```console
________________________________________________________
Executed in   14.23 secs   fish           external
   usr time    3.88 secs  167.00 micros    3.88 secs
   sys time    9.31 secs  1005.00 micros    9.31 secs
```

```
________________________________________________________
Executed in    5.08 secs   fish           external
   usr time    4.77 secs  229.00 micros    4.77 secs
   sys time   16.05 secs  1027.00 micros   16.05 secs
```

Another way to confirm the parallelism, is to observe that, with parallelism, numbers are printed slightly jumbled in between.

Using, the above fundamental knowledge, we can generate multiple UUID's using `uuidgen` command as follows:

```console
seq 1 10 | xargs -I {} -P 1 uuidgen
```

Output will be:
```console
C327AB74-D84B-43C1-B188-550AE86DD398
6B6E541D-74BE-4FB8-892A-03C8FD3E7F59
101B2E23-F6AC-4AB3-82DA-08C22F1A35CF
0F3E72C8-56A9-438D-8785-9D1DC9242E63
C7326E3E-C79A-46AB-BCA4-FBE935D01700
CCBC8496-71A9-4CDF-B38F-8A13A565C191
245862F7-6087-4730-96CC-B21FF25846A6
052A9889-262E-4513-AFF2-62E71BC4A2D2
AF969198-0DA8-49BA-9931-D38709510354
74497908-6E59-402A-93EE-514B541B308F
```


How about using this uuid's in a curl command:

```console
seq 1 10 | xargs -I {}  uuidgen | xargs -I{} -n1 -P 10 curl -X GET 'http://google.com/{}'
```

Hope you enjoyed little fun tricks in shell