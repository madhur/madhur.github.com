---
layout: blog-post
title: "Javascript Basics Part III"
excerpt: "Javascript Basics Part III"
disqus_id: /2014/05/24/javascriptbasics3/
location: New Delhi, India
time: 9:00 PM
tags:
- Javascript
categories:
- Development
---

## Collections ##
* An object is an unordered collection of name/value pairs
* Names are strings
* Values are any type, including other objects
* Every object is a little database

## Object Literals ##
* Object literals are wrapped in {}
* Values can be expressions
* : separate names and values
* , separates pairs
* Can be used anywhere value is required
* New members can be added to any object by simple assignment
	`myObject[name]=value`

## Maker function ##


{% highlight javascript %}
function maker(name, where)
{
	var it={};
	it.name=name;
	it.where=where;
	return it;
}

myObject = maker("Madhur Ahuja", "Jail");
{% endhighlight %}

## Linkage ##
* Objects can be created with a secret link to another object
* The `object(o)` function will be used with a secret link to object o
* The linkage cannot be changed once created. It is possible in Mozilla implementation, but is non-standard.

`var myNewObject = object (myOldObject);`

* All objects are linked to `Object.prototype`
* All objects inherit some methods, none of them are useful
* Objects doesn't have copy or equals methods. Omission from the language.


## Object construction##
1. `new Object()`
2. `{}`
3. `object(Object.protype)`

* Second is the most preferred

* Objects are passed by reference
* === or == compares references not values

* members can be removed by using `delete` operator

## Arrays ##

* Inherits from `object`
* No need to provide a length or type when creating array
* Have a special `length` member
* Array literal uses []
* `myList = ['Oats' , 'peas']`
* New items can be added `myList[myList.length]='barley'`
* The dot notation cannot be used. Should use subscript notation
* Methods: `concat, join, pop, push, slice, sort , splice`
* `delete array[number]` Removes the element, but leaves the hole
* `array.splice(number, 1)` Removes the element and renumbers all the following elements
* Use `objects` when names are arbitrary strings
* Use `arrays` when names are sequential integers
