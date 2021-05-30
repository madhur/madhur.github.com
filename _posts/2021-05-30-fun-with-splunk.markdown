---
layout: blog-post
title: "Fun with Splunk"
excerpt: "Fun with Splunk"
disqus_id: /2021/05/30/fun-with-splunk/
tags:
    - Splunk
---

Many organizations aggregate their logs on [Splunk](https://www.splunk.com/en_us/software.html), which is a popular product for data ingestion and building intelligence on top of it.

I too have been playing with data hosted on Splunk in last few weeks. Recently, I encountered a problem, where-in the data needs to be extracted based on some specified condition within a JSON array.

For example, the splunk record was as follows:

```json
{
    "name": "Test Name",
    "id": "ac646022-fa55-4e04-9856-a25a41b30014",
    "phases": [
        {
            "name": "query.slots",
            "elapsedTime": 2000.0
        },
        {
            "name": "viewPage",
            "elapsedTime": 565.0
        }
    ]
}
```

The requriement was to retrieve all the recods which has the phase `query.slots` and `elapsedTime` is greater than some specified value, for example 1000 ms.

The query required unearthing some commands which I was unfamiliar with:

* [mvexpand](https://docs.splunk.com/Documentation/SplunkCloud/latest/SearchReference/mvexpand)
* [mvzip](https://docs.splunk.com/Documentation/Splunk/8.2.0/SearchReference/MultivalueEvalFunctions)


Here is the final query

```
"phases{}.name"="query.slots" | rename phases{}.elapsedTime as eTime, phases{}.name as name | eval temp=mvzip(eTime,name) | mvexpand temp | table temp  | eval eTimeParsed=mvindex(split(temp,","),0),nameParsed=mvindex(split(temp,","),1)  | table eTimeParsed, nameParsed |  search nameParsed="query.slots" eTimeParsed > 2000 | table nameParsed, eTimeParsed
```