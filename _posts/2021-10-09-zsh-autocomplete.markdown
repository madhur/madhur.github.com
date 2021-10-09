---
layout: blog-post
title: "zsh Autocomplete"
excerpt: "zsh Autocomplete"
disqus_id: /2021/10/09/zsh-autocomplete/
tags:
    - Shell
---

`zsh` shell by default does not come with auto suggestions facility unlike fish shell.

If you are looking for auto suggestions similar to fish, have a look at https://github.com/zsh-users/zsh-autosuggestions

For MAC OS, following steps are required to install

```
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

Add into `~/.zshrc`

```
plugins=( 
    # other plugins...
    zsh-autosuggestions
)
```