---
layout: blog-post
title: "Finding intersection of two lists in shell"
excerpt: "Finding intersection of two lists in shell"
disqus_id: /2020/06/13/find-intersection-lists-shell/
tags:
    - Shell
---

I got thrown up with some more tasks to perform on shell.

First was to extract numbers from long list of text. For ex, you have text as :

```console
[
	NumberLong(90),
	NumberLong(123),
	NumberLong(218),
	NumberLong(221),
	NumberLong(294),
	NumberLong(317),
	NumberLong(319),
	NumberLong(322),
	NumberLong(328),
	NumberLong(344),
	NumberLong(348)
]
```
To simple extract numbers from this file, we'll use [pcregrep](https://www.pcre.org/original/doc/html/pcregrep.html#:~:text=pcregrep%20searches%20files%20for%20character,regular%20expressions%20of%20Perl%205.&text=At%20least%20one%20of%20%2De,argument%20pattern%20must%20be%20provided.) command to capture the regex group and output it.

```shell
#!/bin/bash
cat input.txt | pcregrep -o1 -i '([0-9]+)' > output.txt
```

Second was to compare such two lists and result the numbers which are present in first file but not in second and vice-versa

This is where [comm](https://linux.die.net/man/1/comm) kicks in. It keeps as input two lexically sorted inputs and output the result such as :

> The comm utility reads file1 and file2, which should be sorted lexically, and produces three text columns as output:
> lines only in file1; lines only in file2; and lines in both files.


```shell
#!/bin/bash
comm -23 <(sort first_file.txt ) <(sort second_file.txt) | sort -n
```

Note that comm command expects input to be lexically sorted and not numerically sorted, hence its necesary to sort the file even if its numerically sorted.