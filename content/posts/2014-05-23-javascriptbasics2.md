---
slug: "javascriptbasics2"
title: Javascript Basics Part II
date: '2014-05-23'
year: '2014'
month: '2014-05'
description: Javascript Basics Part II
tags:
  - Javascript
draft: false
categories:
  - Development
params:
  disqus_id: /2014/05/23/javascriptbasics2/
  location: 'New Delhi, India'
  time: '9:00 PM'
---

## Statements ##

* `break` 
* `for` 
* `switch`
* `throw`
* `try`
* `with`


### For statement ###

```javascript
for (var name in object)
{
	if(object.hasOwnProperty(name))
	{
		// within the loop, name is the key of current memeber
		// object[name] is the current value
	}
}
```

### Switch statement ###

* The switch value can be a string. Not restricted to integer
* The cast statements can be expressions, not just constants

### Throw statement ###

```javascript
throw new Error(reason);

throw 
{
	name: exceptionName,
	message: reason
}
```

### Try statement ###

* Because we don't have classes, we just have one `catch` clause. There cannot be multiple catch clauses.
* The javascript implementation can produce these exception names:
	* `Error`
	* `EvalError`
	* `RangeError`
	* `SyntaxError`
	* `TypeError`
	* `URIError`


```javascript
try
{

}
catch(e)
{

}
```


### With statement ###
* Ambiguous and error prone, don't use it. 

```javascript
with (o)
{
	foo = null;
}
```

Either `o.foo = null;` or `foo = null;` depending on if foo is a global variable

### Function statement ###

```javascript
function name(parameters)
{

}
```

### Var statement ###
* Types are not specified
* Initial values are optional

### Scope ###
* Blocks do not have scopes, only function has scopes.
* Because of laziness while writing the compiler :)
* This is a mistake in language

### Return statement ###

`return expression;`
Or
`return;`

* If there is no expression, then the return value is `undefined`
* Exception in constructors, return value is `this`

