---
layout: blog-post
title: "Javascript Basics Part IV"
excerpt: "Javascript Basics Part IV"
disqus_id: /2014/05/25/javascriptbasics4/
location: New Delhi, India
time: 9:00 PM
tags:
- Javascript
categories:
- Development
---

###Distinguishing Arrays###
* `value.constructor === Array`
* `value instanceof Array`
* Neither work when value comes from different frame

### Arrays and inheritance##

* Don't use arrays as prototypes
	The object produced this way does not have array nature. IUt will inherit array's values and methods, but not its length

* You can augment an individual array. Assign a method to it. This works because arrays are objects.

* You can augment all arrays. Assign methods to `Array.prototype`

###Functions###
* Functions are first class objects. Functions can be passed, returned and stored just like any other value
* Functions inherit from `Object` and can store name/value pairs. Very strange.
* Can anywhere appear expression is required
* function statement is just a short-hand for a `var` statement with a function value.

	`function foo() {}`

	expands to

	`var foo = function foo() {};`

* An inner function has access to the variables and parameters of functions that it is contained within.
* A function inside a object is called method
* If a function is called with too many arguments, the extra arguments are ignored
* If a function is called with too few arguemnts, the missing values will be `undefined`
* There is no type checking on the arguements


###Closure###
* The scope that an inner function enjoys continues even after the parent functions have returned
* This is what makes javascript worth attention.


##Invocation##

###Method form : `thisObject.methodName(arguments)`###

* When a function is called in method form, `this` is set to `thisObject`, the object containing the function
* This allows function to have reference object

###Function form - `functionObject(arguments)`###

* `this` is set to global object. That is not very useful. Error in design
* Harder to write helper functions.
	`var that=this`

### Constructor form - `new functionObject(arguments)`###

* a new object is created and assigned to `this`
* If there is not an explicit return value, then `this` will be returned

* function is invoked, it also gets a special parameter called `arguments`
* It contains all of the arguments. Contains the `length` parameter. It's not a real array.

##Misc##
* The `typeof` prefix operator returns a string identifying the type of a value
* `typeof null` is `Object`. This is wrong.
* `eval` is the most dangerous feature. Don't use it. Browser uses it.

* Avoid `new Boolean(), new String(), new Number()`. This is an error.
* On browsers, `window` is the global object. 
* Global variables are evil.
* Any `var` not declared is assumed global. Use `JsLint` tool to identify weaknesses

##Namespace##
* Every object is a separate namespace
* Use an object to organize your variables and functions.
* Use an anonymous function to wrap your application

{% highlight javascript %}
YAHOO.Trivia = function ()
{
	// define your common vars
	// define your common functions here

	return 
	{
		getNextPoser: function (cat, diff)
		{

		},

		showPoser: function()
		{
			...
		}

	};

}();
{% endhighlight %}


