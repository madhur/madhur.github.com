---
layout: blog-post
title: "Useful Javascript Design patterns"
excerpt: "Useful Javascript Design patterns"
disqus_id: /2014/12/15/javascript-design-patterns/
location: New Delhi, India
time: 9:00 PM
tags:
- Javascript
---

* Functions as asbstractions

A function can be passed as a pointer and wrapped in a call.

```Javascript
var work = function()
{
	console.log("working hard");
}

var doWork = function(f)
{
	console.log("starting");
	
	try
	{
		f();
	}
	catch(ex)
	{
		console.log(ex);
	}

	console.log("ending");
}

doWork(work);


```

* Function to build modules

Functions can be used as objects which has data, methods, private variables.



```Javascript
var worker = createWorker();

worker.job1();

worker.job2();
```
How do we create something like above ?

```Javascript
var createWorker = function()
{
	return
	{
		job1: function()
		{
			console.log("task1");
		},

		job2: function()
		{
			console.log("task2");
		}

	};

}
```

Or, even better

```Javascript
var createWorker = function()
{
	// Private variable
	var workCount = 0;

	var task1 = function()
	{
		workCount+=1;
		console.log("task1" + workCount);
	};

	var task2 = function()
	{
		workCount+=1;
		console.log("task2" + workCount);
	};

	return
	{
		job1: task1,
		job2: task2
	};

};

var worker = createWorker();

```

* Eliminating global variables

One drawback of above patterns is that we are creating global variables. For ex, `createWorker` is a variable in global space.

`createWorker` creates scopes and variables such as `workCount, task1, task2` are only visible inside it.

In Javascript, global variables are evil. Its very easy to override global variable defined by somebody else.

How can we eliminate global variables?

One way is to wrap `createWorker` inside another function `program`

```Javascript

var program = function()
{
	var createWorker = function()
	{
		// Private variable
		var workCount = 0;

		var task1 = function()
		{
			workCount+=1;
			console.log("task1" + workCount);
		};

		var task2 = function()
		{
			workCount+=1;
			console.log("task2" + workCount);
		};

		return
		{
			job1: task1,
			job2: task2
		};

	};

	var worker = createWorker();
	worker.job1();
	worker.job2();

}

program();

```

However, we still have one global variable `program`. How do we get down to zero ?

Introducing `IFFE`  -  `immediately invoked function expression`


```Javascript

(function()
{
	var createWorker = function()
	{
		// Private variable
		var workCount = 0;

		var task1 = function()
		{
			workCount+=1;
			console.log("task1" + workCount);
		};

		var task2 = function()
		{
			workCount+=1;
			console.log("task2" + workCount);
		};

		return
		{
			job1: task1,
			job2: task2
		};

	};

	var worker = createWorker();
	worker.job1();
	worker.job2();

}());

```

Now, all variables are defined inside `iffy`. Lot of javascript libraries like Jquery use this design pattern.