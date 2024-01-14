---
layout: blog-post
title: "Ansible roles for installing and configuring Vitess"
excerpt: "Ansible roles for installing and configuring Vitess"
disqus_id: /2023/08/30/ansible-vitess/
tags:
    - Vitess
    - Ansible
---

### What is vitess?
Vitess is a scaleable databases built on top of MySQL. One key feature of vitess is that it supports sharding.
Checkout [Vitess website](https://vitess.io/) for more information

As part of working with Vitess, I have provisioned a [set of Ansible roles](https://github.com/madhur/ansible-vitess) which help in setting up Vitess in [vagrant](https://www.vagrantup.com/) / staging / production infrastructure.

Check out the [github repo](https://github.com/madhur/ansible-vitess) for more information.