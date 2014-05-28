---
layout: blog-post
title: "Javascript Basics Part II"
excerpt: "Javascript Basics Part II"
disqus_id: /2014/05/23/javascriptbasics2/
location: New Delhi, India
time: 9:00 PM
tags:
- Javascript
categories:
- Development
---

##Statements##

* `break` 
* `for` 
* `switch`
* `throw`
* `try`
* `with`


###For statement###

{% highlight javascript %}
for (var name in object)
{
	if(object.hasOwnProperty(name))
	{
		// within the loop, name is the key of current memeber
		// object[name] is the current value
	}
}
{% endhighlight %}

###Switch statement###

* The switch value can be a string. Not restricted to integer
* The cast statements can be expressions, not just constants

###Throw statement###

{% highlight javascript %}
throw new Error(reason);

throw 
{
	name: exceptionName,
	message: reason
}
{% endhighlight %}

###Try statement###

* Because we don't have classes, we just have one `catch` clause. There cannot be multiple catch clauses.
* The javascript implementation can produce these exception names:
	* `Error`
	* `EvalError`
	* `RangeError`
	* `SyntaxError`
	* `TypeError`
	* `URIError`


{% highlight javascript %}
try
{

}
catch(e)
{

}
{% endhighlight %}


###With statement###
* Ambiguous and error prone, don't use it. 

{% highlight javascript %}
with (o)
{
	foo = null;
}
{% endhighlight %}

Either `o.foo = null;` or `foo = null;` depending on if foo is a global variable

###Function statement###

{% highlight javascript %}
function name(parameters)
{

}
{% endhighlight %}

###Var statement###
* Types are not specified
* Initial values are optional

###Scope###
* Blocks do not have scopes, only function has scopes.
* Because of laziness while writing the compiler :)
* This is a mistake in language

###Return statement###

`return expression;`
Or
`return;`

* If there is no expression, then the return value is `undefined`
* Exception in constructors, return value is `this`

