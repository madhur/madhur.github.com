---
layout: blog-post
title: "Improving performance using Batch APIs"
excerpt: "Improving performance using Batch APIs"
disqus_id: /2016/12/25/batch-api-framework/
tags:
- Performance
---

Recently, there is lot of focus on dividing a complex application into small microservices communicating over REST. In most of the cases, REST is implemented over HTTP protocol. All this is great, but HTTP protocol adds lot of communciation overhead. There is a Request header, response headers which adds to considerable bytes in payload. Apart from that, you need to take care of things like `keepalive` to eliminate TCP connection time overhead.

The keepalive does work well for microservices, but it certainly doesn't work well for let's say "mobile REST client applications", where changing network conditions and cell tower will not allow for keep alives. Establishing an HTTP connection, especially when using secure sockets (HTTPS), will result in a handshake being performed between the mobile client and the server. These handshakes will occur N times when N requests are being sent, and your app will incur the associated extra cost of network traffic and battery consumption.

To mitigate these issues, it is generally advisable to batch HTTP requests whenever possible and send them over a persistent HTTP connection.

We implemented a very simple Batch API framework in Node.js. It is very looosely based on Facebook's Graph API documentation, specifically [Graph API, Making Batch Requests](https://developers.facebook.com/docs/graph-api/making-multiple-requests).

The request format is very simple, you just specify the end points and the type of requests they are (GET, POST, PUT DELETE, HEAD) etc. For example,

{% highlight javascript %}
[  
   {  
        "method": "GET",
        "path": "/me"
   },
   {  
        "method": "GET",
        "path": "/me/friends?limit=50"
   },
   {
        "method": "POST",
        "path": "/notification",
        "body": {
            "title": "hi there",
            "body": "hi there as well"
        }
    }
]
{% endhighlight %}

For each operation, the response includes a status code, header information, and the body. These are equivalent to the response you could expect from each operation if performed as raw requests.

{% highlight javascript %}
[
    { "code": 200, 
      "body": "{\"id\":\"…\"}"
    },
    { "code": 200,
      "body":"{\"data\": [{…}]}
    }
]
{% endhighlight %}

One could have also included `headers` in the output if required, but I believe it adds unnecessary overhead in the payload.

###Handling errors

Its possible that one of the requested operations may throw an error.  In this scenario, the batch API throws a similar response to the standard Graph API, but encapsulated in the batch response syntax:

Other requests within the batch should still complete successfully and will be returned, as normal, with a 200 status code.

###Implementation

The batch API framework is implemented in Node.js using [async](https://github.com/caolan/async) and [request](https://github.com/request/request) module. 

{% highlight javascript %}
performBatch: function(req, callback) {

        var items = req.body;
        var headers = util.getHeaders(req);
        var responses = [];

        async.forEachOf(items, function(item, index, callback) {
           performRequest(item, headers, function(err, response) {

               if(err) {
                   responses.push({code:500, body: null, o:index });
               }
               else {
                   responses.push({code: response.statusCode, body: response.body, o: index});
               }
               callback();
           });

        }, function(err) {
            responses.sort(util.keysrt('o'));
            return callback(null, responses);
        });

    }
{% endhighlight %}

The [`eachOf`](http://caolan.github.io/async/docs.html#eachOf) function of [async](http://caolan.github.io/async/docs.html#) is used to send the HTTP request for each item in array in parallel. Note, that since this function calls HTTP request for each item in parallel, there is no guarantee that the  functions will complete in order. Hence, the `index` is used to keep track of order and pushed with each response.

`performRequest` is a simple function which makes an HTTP request according to the parameters and returns the response in a callback. In case of any error, it simply returns `error` parameter as `true`

{% highlight javascript %}
function performRequest(item, headers, callback) {

        request({
            url: config.self_host + item.path,
            method: item.method,
            json: true,
            timeout: 5000,
            headers: headers,
            body: item.body
        }, function (error, response, body) {
            if(error) {
                console.log(error);
                return callback(true);
            } else  {
                return callback(null, response);
            }
        });
}
{% endhighlight %}

Once all the responses are received, they are sorted according to the `index` key using the below function.

{% highlight javascript %}
function keysrt(key, desc) {
    return function(a,b){
        return desc ? ~~(a[key] < b[key]) : ~~(a[key] > b[key]);
    };
}
{% endhighlight %}

