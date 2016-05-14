---
layout: blog-post
title: "Things to learn for Modern Web Development"
excerpt: "Things to learn for Modern Web Development"
disqus_id: /2016/05/13/things-learn-modern-web-development/
location: Bangalore, India
time: 9:00 PM
tags:
- Programming
- ES6
- React
- Web
---

Almost 4 years ago, I wrote a blog post called [Future of Web and Mobile: HTML5, CSS3 and Javascript]({% post_url 2012-02-15-futurewebmobile %}), wherein I mentioned emergence of Javascript and explosion of Javascript frameworks such as [Jquery](http://jquery.com/), [Knockout](http://knockoutjs.com/) etc...

Fast forward to now, I see modern web development again going through a overwhelming change. There is tons of information out there which can be very confusing especially for beginners. The prime reason is there are new frameworks coming up such as [Angular 2](https://angular.io/) and [ReactJs](https://facebook.github.io/react/) which make use of [EcmaScript 6](https://github.com/lukehoban/es6features) features which is yet not fully finalized. And then there are more tools to convert your [ES6](https://github.com/lukehoban/es6features) code to plain old javascript a.k.a [ES5](https://en.wikipedia.org/wiki/ECMAScript)

I am outlining series of programming language/tools in a sequence which should be learnt to understand the overwhelming and fast changing modern web development.

* [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)  
This is the one and only language understood by all the browsers and it is the backbone of front end development. It is also referred to as ECMAScript, ES 5.
It is essential to have good grasp of this programming language before going any further. [This](https://www.youtube.com/watch?v=v2ifWcnQs6M) video is gold.

* [ES6](https://github.com/lukehoban/es6features)  
This is an extension of Javascript language which is being implemented by many browsers. The good thing is you can start writing ES6 code even now, because there are transpilers available such as [Babel]() to convert your ES6 code to ES5 code. It is good to go through these and get a sense of what are the new features. Don't go too much deep because they are subject to change.

* [Babel](https://babeljs.io/)  
This is one of the most popular ES6 to ES5 transpiler. It is also recommended by many frameworks such as React. To convert the ES6 to ES5 code in realtime, there is a REPL available at [https://babeljs.io/repl/](https://babeljs.io/repl/).  
Note that Babel just not ES6 to ES5 transpiler. It is also JSX to JavaScript transpiler. What is JSX? Read on below.

* [NodeJs](https://nodejs.org/en/)  
NodeJs is a server side platform which allows you to build your backend in JavaScript language. Why I am mentioning it here? Because, even if you are not interested in bakend development, there is lot of front tooling which depends on NodeJs. It is good to get atleast familar with node and its command line tools.

* [NPM](https://www.npmjs.com/)  
NPM is the package manager for node. It is just like [pip](https://pypi.python.org/pypi/pip) for Python, [ruby gems](https://rubygems.org/) for Ruby and [Maven](https://maven.apache.org/) for Java. Learn how to install/remove/upgrade packages and especially [package.json](https://docs.npmjs.com/files/package.json) file structure.

* [Grunt](http://gruntjs.com/) and [Gulp](http://gulpjs.com/)   
These are two most popular task runners available which run on Node platform. Technically, they are packages for npm. They allow you to automate many mundane frontend tasks such as Linting your source files, concatenating, minifying and deploying and much much more .... 

* [Bower](http://bower.io/)  
It is a package management tool for frontend libraries itself. Want to add Jquery to your application? As easy as using `bower install jquery`

The knowledge of above tools is enough for any basic front end development. I will cover the tools for two most popular frameworks [React](https://facebook.github.io/react/) and [Angular](https://angular.io/) below. 

* [ReactJs](https://facebook.github.io/react/)  
It is the most popular frontend library to build your views. Note that it is only a V in MVC and hence no comparison should be made with frameworks such as Angular. ReactJs is written in ES6 and can be transpiled to ES5 with Babel. It also uses [JSX](https://jsx.github.io/) which is also transpiled to Javascript using Babel.

* [WebPack](https://webpack.github.io/) and [Browserify](http://browserify.org/)  
These are 2 most popular module bundlers. They can take your Js source code, identify right dependencies and emit a single Javascript file which can power your entire application. I prefer Webpack. Have a look at this [WebPack how to](https://github.com/petehunt/webpack-howto)

* [Angular 2](https://angular.io/)  
Angualr 2 is the next version of one of the most popular MVC framework for Javascript. It is completely re-designed and has a steep learning curve. Comes with full support of two way data binding. Careful evalaution need to be made if Angular2 is the right choice for the development. Its not released for production as of writing.

* [TypeScript](https://www.typescriptlang.org/)  
Angular 2 recommends the user of Typescript as its choice of programming language. I am not very familar with TypeScript but I guess it adds static type to the dynamic nature of Javascript. In the end, I am sure its just a transpiler.

* [Service workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)  
Experimental API. Its like a background thread available to you in a browser for doing all sorts of work. I guess it also adds support for offline browsing.

* [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) and [Push API](https://developers.google.com/web/updates/2015/03/push-notifications-on-the-open-web)  
Read on the links. I have little idea about these as of now.


