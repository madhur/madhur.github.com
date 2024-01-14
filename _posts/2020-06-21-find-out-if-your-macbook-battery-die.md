---
layout: blog-post
title: "Determine if your Macbook battery is about to die"
excerpt: "Determine if your Macbook battery is about to die"
disqus_id: /2020/06/13/find-out-if-your-macbook-battery-die/
tags:
    - Macbook
---

Recently, one of my Macbook Pro 2014 model started showing this information on battery usage:

<img src='/images/image_480.png' width='240px' />

Naturally, it got me worried as I had lot of code and data which was not backed up.

However, at the same time I was curious to know how Apple is able to determine the degradation in battery health.

Is it a function of age, discharge / charging time OR something else?

Upon further debugging, turns it its a function of a number called Cycle count which is maintained.

### What is cycle count?

As per apple,

> When you use your Mac notebook, its battery goes through charge cycles. A charge cycle happens when you use all of the battery’s power—but that doesn’t necessarily mean a single charge.
> For example, you could use half of your notebook's charge in one day, and then recharge it fully. If you did the same thing the next day, it would count as one charge cycle, not two. In this way, it might take several days to > complete a cycle.

Batteries have a limited amount of charge cycles before their performance is expected to diminish.

[Cycle count](https://support.apple.com/en-in/HT201585) can be viewed by going to Apple  menu -> About this Mac -> System Report -> Hardware -> Power

<img src='/images/cycle count.png' width='489px' />

There is a table in this [Apple support article](https://support.apple.com/en-in/HT201585), which tells you for each Model number, after how many cycle counts, a battery replacement is required.

