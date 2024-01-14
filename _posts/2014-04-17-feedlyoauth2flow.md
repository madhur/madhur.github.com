---
layout: blog-post
title: "Feedly OAuth 2.0 implementation using Scribe in Java"
excerpt: "Feedly OAuth 2.0 implementation using Scribe in Java"
disqus_id: /2014/05/17/feedlyoauth2/
location: New Delhi, India
time: 9:00 PM
tags:
- Feedly
- OAuth2
categories:
- Development
---

Since the Google Reader retirement, [Feedly](http://feedly.com) hasb been slowly becoming more and more popular. Recently, Feedly announced their [API Model](http://developer.feedly.com/) which 
allows developers to create apps which integrate with feedly. Applications authenticate users using a feedly OAuth 2.0 interface. In this post, I am going to cover the Feedly OAuth 2.0 authentication flow 
which can be used in  Mobile/Web apps. I am not going to cover any details into OAuth 2. The official specs of OAuth2 can be read [here](http://tools.ietf.org/html/rfc6749) and a nice tutorial [here](http://www.codecademy.com/tracks/oauth) on [Code Academy](http://www.codecademy.com). Wikipedia too gives a nice little intro about OAuth 2 given below:

Quoting from Wikipedia  

> OAuth is an open standard for authorization. OAuth provides client applications a 'secure delegated access' to server resources on behalf of a resource owner. It specifies a process for resource owners to 
> authorize third-party access to their server resources without sharing their credentials.
> OAuth is a service that is complementary to, and therefore distinct from, OpenID. OAuth is also distinct from OATH, which is a reference architecture for authentication, not a standard.

Since, I am using Java platform, I will be using a nice little OAuth library called [Scribe](https://github.com/fernandezpablo85/scribe-java). It is an open source library hosted on github and is a great resource to learn about OAuth 2.0 flow and specs. Basically, to implement any OAuth 2.0 API, you need to extend a class called `DefaultApi20` and provide some of the obvious parameters such as `Authorization Url`, `Access token URL` and `client id` and `secret`.


The implementation of this class is maintained in [my fork of Scribe repo](https://github.com/madhur/scribe-java). [This](https://github.com/madhur/scribe-java/blob/master/src/main/java/org/scribe/builder/api/FeedlyApi20.java) is the direct link to the sources file. Feel free to use it to build awesome feedly Apps.

I also created a [test Java Program](https://github.com/madhur/scribe-java/blob/master/src/test/java/org/scribe/examples/Feedly20Example.java). And here is the output of running the test:

{% highlight bash %}
=== Feedly's OAuth Workflow ===

Fetching the Authorization URL...
Got the Authorization URL!
Now go and authorize Scribe here:
https://sandbox.feedly.com/v3/auth/auth?client_id=sandbox&redirect_uri=http%3A%2F%2Flocalhost%3A8080&response_type=code&scope=https://cloud.feedly.com/subscriptions
And paste the authorization code here
>>At2PvX57ImkiOiJiZmRiNDVkMi01MmRiLTRkMWUtOWRhOS01OGM5YWVjYzJjMzUiLCJ1IjoiMTAxMjk2MjUyNDE1MzQ5MDM1NzgwIiwicCI6NiwiYSI6IkZlZWRseSBzYW5kYm94IGNsaWVudCIsInQiOjEzOTc3MTg4NzkwNzJ9

Trading the Request Token for an Access Token...
Got the Access Token!
(if your curious it looks like this: Token[AmdDThh7ImEiOiJGZWVkbHkgc2FuZGJveCBjbGllbnQiLCJlIjoxMzk4MzIzNjk1OTUzLCJpIjoiYmZkYjQ1ZDItNTJkYi00ZDFlLTlkYTktNThjOWFlY2MyYzM1IiwicCI6NiwidCI6MSwidiI6InNhbmRib3giLCJ4Ijoic3RhbmRhcmQifQ:sandbox , ] )

Now we're going to access a protected resource...
Got it! Lets see what we found...

200
{"id":"bfdb45d2-52db-4d1e-9da9-58c9aecc2c35","client":"Feedly sandbox client","wave":"2014.7","email":"ahuja.madhur@gmail.com","familyName":"Ahuja","givenName":"Madhur","google":"101296252415349035780","gender":"male","picture":"https://lh3.googleusercontent.com/-YffmYR2CFxI/AAAAAAAAAAI/AAAAAAAAJCw/SIOxMsWmxYQ/photo.jpg?sz=50","created":1392372977783,"windowsLiveConnected":false,"wordPressConnected":false,"facebookConnected":false,"evernoteConnected":false,"pocketConnected":false,"twitterConnected":false,"fullName":"Madhur Ahuja"}

Thats it man! Go and build something awesome with Scribe! :)
{% endhighlight %}