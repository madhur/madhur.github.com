---
layout: blog-post
title: "Capacity Estimation Examples"
excerpt: "Capacity Estimation Examples"
disqus_id: /2021/06/27/capacity-estimation/
tags:
    - Design    
---

Capacity estimation is one of the most important exercises in design.

Twitter Example

1B Total Users
200 M DAU
100 M new tweets everyday
Each user follows 200 people avg

How many favorites per day?
Each user 5 favorite per day
200M *5 = 1B favorite

Total tweet views
A User visits their timeline 2 times a day and visits 5 other people pages
Each page has 20 tweets

200M *(2+5)*20 = 28B / day

Storage

140 characters ~ 280 bytes
100M*(280+30) bytes => 30 GB / day

Not all tweets will have media, let’s assume that on average every fifth tweet has a photo and every tenth has a video. Let’s also assume on average a photo is 200KB and a video is 2MB. This will lead us to have 24TB of new media every day.
(100M/5 photos * 200KB) + (100M/10 videos * 2MB) ~= 24TB/day

Bandwidth Estimates Since total ingress is 24TB per day, this would translate into 290MB/sec.

Remember that we have 28B tweet views per day. We must show the photo of every tweet (if it has a photo), but let’s assume that the users watch every 3rd video they see in their timeline. So, total egress will be:
(28B * 280 bytes) / 86400s of text => 93MB/s
+ (28B/5 * 200KB ) / 86400s of photos => 13GB/S
+ (28B/10/3 * 2MB ) / 86400s of Videos => 22GB/s

Total ~= 35GB/s
