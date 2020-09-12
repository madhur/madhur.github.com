---
layout: blog-post
title: "Javascript Event loop and call stack"
excerpt: "Javascript Event loop and call stack"
disqus_id: /2020/09/12/javascript-event-loop-call-stack/
tags:
    - Javascript
---

Its amazing how after working so many years on Javascript, I still get some of
the basic concepts wrong.

The concept in question is Event loop and Call Stack.

To get it refreshed, here is the teaser.

What is the output of the below snippet.

```javascript
function printHello() {
    console.log("Hello");
}
function blockFor1Sec() {
    let arr = [];
    for (let i = 0; i < 100000; ++i) {
        arr.push(i);
    }

}

setTimeout(printHello, 0);

blockFor1Sec();

console.log("Me first!");
```


I thought that, since `printHello` is scheduled to run after 0ms, it will run as
soon as event loop gets chance to execute it. I assumed the execution order to
be:

```
Hello
Me first!
```

However, it turns out that answer is

```
Me first!
Hello
```

The reason for it is the documented behavior when the items in call stack are
executed.

> The specified amount of time (or the delay) is not the guaranteed time to 
> execution, but rather the minimum time to execution. The callbacks you pass to
> these functions cannot run until the stack on the main thread is empty.

> As a consequence, code like setTimeout(fn, 0) will execute as soon as the 
> stack is empty, not immediately. If you execute code like setTimeout(fn, 0) 
> but then immediately after run a loop that counts from 1 to 10 billion, your 
> callback will be executed after a few seconds.