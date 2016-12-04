---
layout: blog-post
title: "Couchbase exception handling in Node.js"
excerpt: "Couchbase exception handling in Node.js"
disqus_id: /2016/12/04/handling-couchbase-node/
tags:
- Node.js
- Couchbase
---


We use [Couchbase](http://www.couchbase.com/) as our NOSQL document store. Couchbase provides lots of software development kits (SDKs) in different programming languages, including one in Node.js, so JavaScript development integrates Couchbase into the product very easily. For example:

{% highlight javascript %}
var couchbase = require('couchbase');
var cluster = new couchbase.Cluster('couchbase://127.0.01');
var bucket = cluster.openBucket('default');
bucket.get(userId, function (err, res) {
    if (err) {
        console.log(err);
        //handle error
    }
    else {
        //access data here
    }
});
{% endhighlight %}

However, there are some caveats which we have discovered. Suppose, the application was not able to connect to couchbase when it was started. There will never be a connection to couchbase and `bucket.get` will throw an exception `cannot perform operations on a shutdown bucket`. Note that, this will not fall into an error case, infact this will be treated as an unhandled exception.

This was really undesirable for us, since we were using couchbase as a caching store. An error in connecting to couchbase is ideally a miss, which our code should handle and lookup the data in our persistent store, MySQL.

##Solution

There are few solutions to this problem. I am describing here what we choose.
Some of them are described [here](https://wiredcraft.com/blog/reconnect-couchbase-nodejs/) as well.

First is to track the connection status of couchbase at startup. And then connect to couchbase, only if the status indicated success. For example,

{% highlight javascript %}
var couchbase = require('couchbase');
var cluster = new couchbase.Cluster(config.couch);
var bucket = cluster.openBucket('default');
// connection status
var couchbaseConnected = false;

bucket.on('error', function (err) {
    couchbaseConnected = false;
    console.log('CONNECT ERROR:', err);
});

bucket.on('connect', function () {
    couchbaseConnected = true;
    console.log('connected couchbase');
});
{% endhighlight %}


Now, since we have the status at startup, we can use it to decide weather to connect to couchbase or not.

{% highlight javascript %}
if (couchbaseConnected) {
    bucket.get(userId, function (err, res) {
        if (err) {
            // handle error
        }
        else {
            // access data
        }
    });
}
else {
    // get data from persistent store, such as mysql
}
{% endhighlight %}

The disadvantage of this approach is that if the couchbase later becomes available, the application has no way of knowing it and it will not reconnect.

One solution to it is to try and reconnect the bucket. For example, we modify our code as follows:

{% highlight javascript %}
var couchbase = require('couchbase');
var cluster = new couchbase.Cluster(config.couch);
var bucket;
var couchbaseConnected = false;

tryOpenBucket();

function tryOpenBucket() {

    bucket= cluster.openBucket('default');

    bucket.on('error', function (err) {
        couchbaseConnected = false;
        console.log('CONNECT ERROR:', err);
    });

    bucket.on('connect', function () {

        couchbaseConnected = true;
        console.log('connected couchbase');
    });
}
{% endhighlight %}

And, while accessing any key:

{% highlight javascript %}
 if (couchbaseConnected) {
    bucket.get(userId, function (err, res) {
        if (err) {
            console.log(err);
            // handle error
        }
        else {
            // access data
        }
    });
}
else {
    // We try and open bucket again here. If its successful, couchbaseConnected will bet set to true and next time data will be fetched from couchbase 
    tryOpenBucket();
    // Get data from persistent store, mysql
}
{% endhighlight %}


In this solution, We try and open bucket again everytime we access the key. If its successful, `couchbaseConnected` will bet set to true and next time data will be fetched from couchbase.
