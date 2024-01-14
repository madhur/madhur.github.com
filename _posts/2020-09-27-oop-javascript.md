---
layout: blog-post
title: "Object Oriented Programming in JavaScript"
excerpt: "Object Oriented Programming in JavaScript"
disqus_id: /2020/09/27/oop-javascript/
tags:
    - Javascript
---

I have been always fascinated by Object oriented programming in JavaScript. Its
different from usually OOPs provided by languages such as Java.

In this post, we will look at various approaches of achieving Object oriented
programming in JavaScript, and their pros and cons


## Solution 1 : Generate objects using a function

```javascript
function userCreator(name, score) {
    const newUser = {};
    newUser.name = name;
    newUser.score = score;
    newUser.increment = function() {
        newUser.score++;
    };
    return newUser;
};

const user1 = userCreator("Will", 3);
const user2 = userCreator("Tim", 5);
user1.increment();
```

The above approach is a very naïve approach, but its absolutely useless.

- The code in the function is replicated for each of the object. If we have million users, it will have million copies of `increment` function
- If we want to add a new functionality, we will have to add it to each of the
  object, once it has been created.

+ There is beauty of closure in above code. The function definition `increment`
  has reference to `newUser` but there is no reference to `newUser` once the
  object has been created through `userCreator` function.


## Solution 2: Using the prototype chain


```javascript
function userCreator(name, score) {
    const newUser = Object.create(userFunctionStore);
    newUser.name = name;
    newUser.score = score;
    return newUser;
};

const userFunctionStore = {
    increment: function() {this.score++;},
    login: function() {console.log("Logged in");}
};

const user1 = userCreator("Will", 3);
const user2 = userCreator("Tim", 5);
user1.increment();
```

In the above solution we create a link between two objects using a hidden
property `__proto__`. This property has a link to `userFunctionStore`.

All objects link back to `Object.prototype`


## Solution 3: Using the new keyboard

Using the `new` keyword does the above `__proto__` link automatically

All functions have a property called `prototype` defined on them which points to
`{}` by default.

```javascript
function userCreator(name, score) {
    this.name = name;
    this.score = score;
}

userCreator.prototype.increment = function() { this.score++; };
userCreator.prototype.login = function() { console.log("login");};

const user1 = new userCreator("Eva", 9);
user1.increment();
```

In the above code, the `new` keyword automates lot of things for us:

* It links the `__proto__` property of the returned object to the `prototype`
  property of `userCreator` function object.

* returns `this` and stores in the global variable `user1`

## Solution 4 - Using the class syntactic sugar

```javascript
class UserCreator {
    constructor(name, score) {
        this.name = name;
        this.score = score;
    }

    increment() { this.score++; }
    login() { console.log("login"); }   
}

const user1 = new UserCreator("Eva", 9);
user1.increment();
```

In ES6 the class keyword was introduced. The class keyword is no more than syntactic sugar on top of the already existing prototypal inheritance pattern. Classes in JavaScript is basically another way of writing constructor functions which can be used in order to create new object using the new keyword.