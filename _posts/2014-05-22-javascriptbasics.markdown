---
layout: blog-post
title: "Javascript Basics Part I"
excerpt: "Javascript Basics Part I"
disqus_id: /2014/05/22/javascriptbasics/
location: New Delhi, India
time: 9:00 PM
tags:
- Javascript
categories:
- Development
---


I was going through many of the Douglas Crockford videos on Javascript and came across many of the oddities in the Javascript language. I was highly impressed by his outspoken admission on some of the features of the languages being "bad". But at the same time, he highlighted that Javascript is one of the most widely mis-understood programming languages and there are many powerful features which are quite powerful.

##Value Types (Everything else is objects)## 

* Number
* Strings
* Booleans
* Objects
* null
* undefined

Few points about NaN:  

* `NaN` stands for Not a number
* `NaN` does not equal to anything, including `Nan`
* `Nan` is a number type. 
* `type of Nan` is `Number`


### Number function ###

`Number(value)`

* Convert a string to a number

###parseInt function###

`parseInt(value, 10)`

* The radix (10) should be required

###Math object###

* Math object is modeled on Java's `Math` class

###Strings###

* Strings are immutable
* Similar strings are equal (==). Jave got that wrong
* Strings literals can use single or double quotes
* `string.length` determines the length of string

###String function###
`string(value)`

* Convert a number to String

###Boolean function###
`Boolean(value)`

* returns `true` if the value is truthy
* returns `false` if the value is falsy
* Similar to `!!` operator

###Falsy Values###

* false
* null
* undefined
* ""
* 0
* Nan

###Truthy Values###

* All other values (including all objects) are truthy including `"0"` , `"false"`

* `undefined` is the default value for variables
* Thus, a variable can be defined and also `undefined` at the same time :)

###Dynamic objects###

* `new Object()` produces an empty container of name/value pairs
* A name can be any string, a value can be any value except `undefined`
* members can be accessed with dot notation or subscript notation

###Loosely typed###

* Any variable can recieve or send any type of parameter
* Language is not untyped


###Reserved words###

* Many of hte words are reserved but only handful of them are being used in language


###== and != operators###

* These operators can do type coercion
* It is better to use === and !==, which do not do type coercion.


### && Guard operator (Logical AND)###

* If first operand is truthy
	then result is second operand
	else result is first operand
* It can be used to avoid null references

{% highlight javascript %}
if (a)
{
	return a.member;
}
else
{
	return a;
}
{% endhighlight %}

* It can be written as `return a && a.member;`


### || Default operator (Logical OR)###

* If first operand is truthy
	then result is first operand
	else result is second operand
* It can be used to fill in default values.
	`var last = input || nr_items;`