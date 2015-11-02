---
layout: blog-post
title: "CountDownLatch in Python using Condition Objects"
excerpt: "CountDownLatch in Python using Condition Objects"
disqus_id: /2015/11/02/countdownlatch-python/
location: Bangalore, India
time: 9:00 PM
tags:
- Programming
- Python
---

In Java, there is a very useful construct called [`CountDownLatch`](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/CountDownLatch.html) to solve many multithreaded and asynchronous programming scenarios.

In tech terms it is simply
> A synchronization aid that allows one or more threads to wait until a set of operations being performed in 
> other threads completes.

For example, you might have a third party API call which is asynchronous in nature. Many scenarios require that you call multiple of them and perform an action if all of them succeed OR perform another action even if one of them fails.

In the case below, we are using a popular message library called [PubNub](https://www.pubnub.com) to send a message on a channel twice through the `publish()` method which is an [async call](https://www.pubnub.com/docs/java-se-java/api-reference#publish)


{% highlight Java %}
final CountDownLatch latch = new CountDownLatch(2);
final GrantStatus grantStatus = new GrantStatus();

        pubnub.publish(userChannel, msg, new Callback() {
            @Override
            public void successCallback(String s, Object o) {
                // Success case
                grantStatus.setGrantStatus1(true);
                latch.countDown();
            }

            public void errorCallback(String channel, PubnubError error) {
                // Failure case
                grantStatus.setGrantStatus1(false);
                latch.countDown();

            }
        });

        pubnub.publish(userChannel, msg, new Callback() {
            @Override
            public void successCallback(String s, Object o) {
				// success case
                grantStatus.setGrantStatus2(true);
                latch.countDown();

            }

            public void errorCallback(String channel, PubnubError error) {
                // Failure case
                grantStatus.setGrantStatus2(false);
                latch.countDown();

            }
        });


        latch.await(); // This is a blocking call. It will block the thread till latch reaches zero

        if(grantStatus.getGrantStatus1() && grantStatus.getGrantStatus2()) {
        	// Both calls were success
        }
        else
        	// One or both of the calls failed

{% endhighlight %}

In the piece of code above, the thread blocks at `latch.await()` till both the API calls either succeeds or fails. This is preferable since it doesn't uses [Spin lock](https://en.wikipedia.org/wiki/Spinlock) or [Busy waiting](https://en.wikipedia.org/wiki/Busy_waiting)

I was trying to do a similar thing in Python. Without using any multithreading construct, this is the version I came up with. Pretty lame it is

{% highlight Python %}
def send_notification_task(self, user_id, content, **kwargs):

    status = {'result' : 0}

    msg = prepare_message(16182 , 16182, 'Android', 'This is a text message')  

    def _callback(message):
        status['result'] = 1
 
    def _error(message):
            status['result'] = 2
           
    pubnub.publish('16182', msg, _callback, _error)

    while status['result'] == 0:
        time.sleep(.001)

    if status['result'] == 2:
        countdown = int(random.uniform(2, 4) ** self.request.retries)
        raise self.retry(countdown = countdown)
    elif status['result'] == 1:
        return 'success'
{% endhighlight %} 

Here without using any threading constucts, we are using a `while` loop with a `sleep` which is busy waiting.

How do we make it better? Enter [Condition Objects](https://docs.python.org/2/library/threading.html#condition-objects)

Using Condition Objects, we can make a very simple version of `CountDownLatch` as follows:

{% highlight Python %}
import threading

class CountDownLatch(object):
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()

    def count_down(self):
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:
            self.lock.notifyAll()
        self.lock.release()

    def await(self):
        self.lock.acquire()
        while self.count > 0:
            self.lock.wait()
        self.lock.release()
{% endhighlight %} 


With this construct, we can improve our existing version of code significantly as follows:


{% highlight Python %}
def send_notification_task(self, user_id, content, **kwargs):
	latch = CountDownLatch(1)
    status = {'result' : 0}

    msg = prepare_message(16182 , 16182, 'Android', 'This is a text message')  

    def _callback(message):
        status['result'] = 1
        latch.count_down()
 
    def _error(message):
        status['result'] = 2
        latch.count_down()
           
    pubnub.publish('16182', msg, _callback, _error)

	latch.await()

    if status['result'] == 2:
        countdown = int(random.uniform(2, 4) ** self.request.retries)
        raise self.retry(countdown = countdown)
    elif status['result'] == 1:
        return 'success'
{% endhighlight %} 

The above method doesn't uses a spinlock or busy waiting

