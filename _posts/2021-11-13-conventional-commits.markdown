---
layout: blog-post
title: "Conventional Commits"
excerpt: "Conventional Commits"
disqus_id: /2021/11/13/conventional-commits/
tags:
    - Git
---

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#specification) is a an effort to standardizing writing better git commit messages.

As per it, a commit message should be structured as follows

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

We recently standardized writing commit messages in our team according to this spec. This can be even forced through [git commit hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)


```shell
#!/bin/sh

commit_regex_normal="(((feat|docs|style|refactor|perf|test|build|ci|chore|revert)(\((\w{0,15})\))?))(\:.*\S.*)";
commit_regex_bug_fix="(((Fix)(\((\w{0,15})\))?))(\:)([A-Z]+-[0-9]+:)(.*\S.*)";
commit_regex_auto_gen="(Merge.*)|(Revert.*)";
o="|"
commit_regex="$commit_regex_normal$o$commit_regex_bug_fix$o$commit_regex_auto_gen"

error_msg='       /‾‾‾‾‾‾‾‾
    <  Please use semantic commit messages(see https://www.conventionalcommits.org/en/v1.0.0 )
       \________

  <type>[<scope>]: <short summary>
     │     |              │
     │   (optional)       └─> Summary in present tense. Not capitalized. No period at the end.
     │
     └─> Type: chore, docs, feat, fix, refactor, style, or test.
    fix[<scope>]: ABC-1234 summary (Jira id mandatory for type -fix)

'
if ! grep -iqE "${commit_regex}" "$1"; then
    echo "${error_msg}" >&2
    exit 1
fi
```