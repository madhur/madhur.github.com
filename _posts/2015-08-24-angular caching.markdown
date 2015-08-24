---
layout: blog-post
title: "Caching http requests with Angular"
excerpt: "Caching http requests with Angular"
disqus_id: /2015/08/24/angular-caching/
location: New Delhi, India
time: 9:00 PM
tags:
- AngularJs
- Caching
- Javascript
---

AngularJs provides caching in form of `$cacheFactory`. `$cacheFactory` is basically an in memory javascript dictionary.

[Angular cache module](https://github.com/jmdobry/angular-cache) is a better replacement of `$cacheFactory`. Angular cache module allows to use SessionStorage or LocalStorage for persistent cache.

One of the advantages of Angular cache is 

> The downside of letting $http handle caching for you is that it caches the responses (in string form) to your requests–not the JavaScript Object parsed from the response body. This means you can't interact with the data in the cache used by $http. See below for how to handle the caching yourself, which gives you more control and the ability to interact with the cache (use it as a data store).

For example, I create a cache called `messageCache`

```javascript
if(!CacheFactory.get('messageCache'))
{
	CacheFactory.createCache('messageCache', {
				              deleteOnExpire: 'aggressive',
				              recycleFreq: 60000
				             });
}

var messageCache = CacheFactory.get('messageCache');

```

And then use it in one of my service's http methods:

```javascript
function getUserMessagesByCompany(userId, companyId, showLoader) {
	var userMessages;
						
						
	userMessages = $http.get('/api/mobile/chat/getusermessagesbycompany/'
				   + userId + '/' + companyId + '.json', {ignoreLoadingBar : showLoader, cache: messageCache});
					
							
	return userMessages;

}
```

In this case, `messageCache` is our cache store and it stores the cache in form of key value pair where keys are simply the Url's to the get requests.


Now, how do we modify the data cached for a particular request. Its simple if we understand how the cache is stored for a particular key.

The cache value is simple an array of length 4, where the first index contains the response in stringified form. In our case, the response was in the form of this json structure

```javascript
{
	"userMessages": 
	[
			{  }, {  } 
	]
}
```

Now suppose we want to insert a new message in this response inside our cache

```javascript
function insertMessageIntoCache(userId, companyId, newMessage)
{
	var key = '/api/mobile/chat/getusermessagesbycompany/' + userId + '/' + companyId +'.json';
	
	if(messageCache)
		{
				// Get the response object
				var messagesResponse = messageCache.get(key);
				
				// Get the HTTP response in string form
				var messagesArrayString = messagesResponse[1];
				
				// Parse it into JSON
				var messagesArrayJSON = JSON.parse(messagesArrayString);
				
				// Insert a new message 
				messagesArrayJSON.userMessages.unshift(newMessage);
				
				// Convert the response back into string
				messagesResponse[1] = JSON.stringify(messagesArrayJSON);
				
				// replace the cache key
				messageCache.put(key, messagesResponse);
		
		}
	
}
```





