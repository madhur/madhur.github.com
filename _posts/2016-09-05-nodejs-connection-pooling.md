---
layout: blog-post
title: "Effect of connection pooling on node.js performance"
excerpt: "Effect of connection pooling on node.js performance"
disqus_id: /2016/09/05/nodejs-connection-pooling/
tags:
- Node.js
- Programming
---

[Node.js](https://nodejs.org/en/) is popularly known for its asynchronous, non-blocking and event-driven I/O model and the scalability it can achieve in executing [I/O bound](https://en.wikipedia.org/wiki/I/O_bound) operations.

However, a developer must keep in mind that there are some things which can severely limit the scalability of the Node.js application. I have earlier already covered [How DNS resolution is a blocking call in node and must be handled to achieve scalability]({% post_url 2016-05-28-nodejs-dns-cache %})

In this post, I am going to cover [connection pooling](https://en.wikipedia.org/wiki/Connection_pool). I have observed that connection pooling is a critical engineering decision which is easily ignored while developing node.js applications.  While interacting with any external resource such as [MySQL](https://www.mysql.com/), [PostgreSQL](https://www.postgresql.org/), [Redis](http://redis.io/) or [MongoDB](https://www.mongodb.com/), each of it requires a connection pool for any sizeable node.js application.

To demonstrate this, I am going to compare two programs, one without pooling and one with pooling and a simple database query.


I have this simple function which makes a call to database.

{% highlight javascript %}

function callback(){
	process.exit();
}

function hitQuery(callback) {
    var user_query = "select count(*) from user u, access_code uac, user_location_info uli   where u.id = uac.user_id and u.id = uli.user_id"


    connection.query(user_query, function(err, rows, fields) {
        if (err) throw err;

        if (rows.length == 0) {
            console.log("No device token found for user: " + 16182);
            callback(null, null);
        } else {
            var deviceToken = rows[0]['device_token'];
            callback(null, rows[0]);
        }
    });
}

hitQuery(callback);

{% endhighlight %}


If I execute this and time it, it takes an average of 1.5 - 2 seconds

{% highlight text %}
$ time node paralleltest.js

real	0m1.756s
user	0m0.159s
sys	    0m0.017s
{% endhighlight %}


Lets, now run multiple of such queries in series first. I slightly change my program to this version:

{% highlight javascript %}
async.series([function(callback) {
        hitQuery(callback);
    }, function(callback) {
        hitQuery(callback);
    },
    function(callback) {
        hitQuery(callback);
    },
    function(callback) {
        hitQuery(callback);
    },
    function(callback) {
        hitQuery(callback);
    }
], function done(err, results) {
    console.log(results);
    process.exit()
});
{% endhighlight %}

When I execute this version where I am making 5 calls in series, I get an average of 8 - 9 seconds

{% highlight text %}
$ time node paralleltest.js

real	0m8.579s
user	0m0.178s
sys	    0m0.019s
{% endhighlight %}

Lets make this to parallel now, common sense says that the wall clock time should be much faster in case of parallel.

{% highlight javascript %}
async.parallel([function(callback) {
        hitQuery(callback);
    }, function(callback) {
        hitQuery(callback);
    },
    function(callback) {
        hitQuery(callback);
    },
    function(callback) {
        hitQuery(callback);
    },
    function(callback) {
        hitQuery(callback);
    }
], function done(err, results) {
    console.log(results);
    process.exit()
});
{% endhighlight %}

Now, If I time this verison, where I am making 5 calls in parallel.

{% highlight text %}
$ time node paralleltest.js

real	0m8.168s
user	0m0.165s
sys	    0m0.018s
{% endhighlight %}

I still get the almost same wall time clock. If you closely observe the time output, the bulk of the time is not even spent in our program. Bulk of the time is actually spent in waiting to get the connection back from mysql, since we are re-using the single connection again and again. Thus, there is literally no performance gain inspite of making the calls in "parallel"


To fix this, I am going to change the program to use a connection pool. I am creating a simple pool as follows:

{% highlight javascript %}
var pool = mysql.createPool({
    connectionLimit: 100, //important
    host: '127.0.0.1',
    user: '***',
    password: '***',
    database: 'user',
    debug: false
});
{% endhighlight %}

And change our function to use the connection pool: 

{% highlight javascript %}
function hitQuery(callback) {
    var user_query = "select count(*) from user u, access_code uac, user_location_info uli   where u.id = uac.user_id and u.id = uli.user_id"

    pool.getConnection(function(err, connection) {
        if (err) {
            connection.release();
            res.json({ "code": 100, "status": "Error in connection database" });
            return;
        }

        connection.query(user_query, function(err, rows, fields) {
            if (err) throw err;

            if (rows.length == 0) {
                console.log("No device token found for user: " + 16182);
                callback(null, null);
            } else {
                callback(null, rows[0]);

            }
        });

    });
}
{% endhighlight %}

Again, If I time the single execution time here. I get

{% highlight text %}
$ time node paralleltest1.js

real	0m1.763s
user	0m0.163s
sys	    0m0.020s
{% endhighlight %}

Not much has changed, we got `1.756` while using without connection pooling. The benefit of connection pooling is only when we run multiple requests together. So now, lets execute in series of 5 queries as done earlier.

{% highlight text %}
$ time node paralleltest1.js

real	0m8.192s
user	0m0.182s
sys	    0m0.019s
{% endhighlight %}

Again, no real benefit. What is happening here is that [the second query is executed only after the first query is executed](http://caolan.github.io/async/docs.html#.series). Hence, this time is perfectly fine. Its just that bulk of time is wasted.

Let's move this to 5 parallel queries.

{% highlight text %}
$ time node paralleltest1.js

real	0m2.311s
user	0m0.175s
sys	    0m0.019s
{% endhighlight %}

This time we have brought it down to `2.311 seconds` from `8.168 seconds` which was the time it took to execute without having a connection pool.
