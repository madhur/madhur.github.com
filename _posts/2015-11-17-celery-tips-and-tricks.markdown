---
layout: blog-post
title: "Scaling Celery Task queue"
excerpt: "Experiences of Scaling Celery Task queue"
disqus_id: /2015/11/17/celery-tips-and-tricks/
location: Bangalore, India
time: 9:00 PM
tags:
- Programming
- Python
- Celery
---

Recently, we implemented the [Celery Task queue](http://docs.celeryproject.org/en/latest/index.html) in our production environment for variety of scheduled and periodic tasks. Just to give few numbers, it processes more than 10 million tasks per day, all of which are external HTTP based calls. During the development phase, we encountered various experiences, some of which have been documented below. In my opinion, Celery seems to be more dominant choice where Python is the primary programming language. However, we integrated it with our J2EE based system with quite ease. Perhaps, it is less a question of celery's ability to interoperate,  rather it is more a question of how much your development team is willing to go outside Java's ecosystem and look for alternatives for systems such as [Jesque](https://github.com/gresrun/jesque)


> Celery is a simple, flexible and reliable distributed system to process vast amounts of messages, while providing operations with the    > tools required to maintain such a system.

> It’s a task queue with focus on real-time processing, while also supporting task scheduling.


1.  Use [RabbitMQ](https://www.rabbitmq.com/) as the broker instead of Redis, Mysql or anything else 

    Rabbit's queues reside in memory and will therefore be much faster than implementing this in a database.

	There are some problems with using the database as the broker:
	* polling keeping the database buzy and low performing
	* locking of the table -> again low performing
	* millions of rows of task -> again polling is low performing


2.  Use a process control system such as [Supervisor](http://supervisord.org/) to run Celery in production
    Also, see [Running the worker as daemon](http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#daemonizing)

3.  If you are eying scale, this is a must read:

	[http://spring.io/blog/2011/04/01/routing-topologies-for-performance-and-scalability-with-rabbitmq/](http://spring.io/blog/2011/04/01/routing-topologies-for-performance-and-scalability-with-rabbitmq/)

4.  If you are looking for reliability, use `CELERY_ACKS_LATE = True`

	What does it do? Well, as the docs says

	> When enabled messages for this task will be acknowledged after the task has been executed, and not just before which is the default behavior.

	> Please note that this means the task may be executed twice if the worker crashes mid execution (which may be acceptable for some     applications).

	This also requires that the tasks can be restarted from middle without any side effects. This might require using transactions if the task is involved in db operations.

5.  [`CELERY_TASK_SERIALIZER='json'`](http://docs.celeryproject.org/en/latest/userguide/calling.html#calling-serializers)

	Using JSON as the serializer enables easy debugging as you can inspect stored messages in the AMQP broker easily. However, it comes with the disadvantage of being around 34% larger than an encoding which supports native binary types. 

6.  Logically separate queues for your tasks

	By default celery will create just one queue `celery` for all your tasks. This is undesirable when you are especially targeting for scale. Logically separating your tasks into queues will allow you to separately dedicate different number of workers for each queue.

	`celery -A tasks worker -Q github,email -B`

7.  Run Celery beat scheduler as a separate service than running it with worker. This is documented on celery page:

	[http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)

8.  Intelligently anticipate errors / exceptions and retry only where it makes sense 

	I have seen developers blindly putting `try` `except` block with a `retry` statement and then showing off that how `safe` their code is from failures. This is not a good idea. For example, consider the simple task below, which fails because of division by zero in some case (where random no. zero is generated)

{% highlight Python %}
@app.task(default_retry_delay = 5, bind = True, max_retries = None)
def divbad_noretry(self):
	a = 2
	b = random.randing(-1, 5)
	c  = a/b
	print c
	return c
{% endhighlight %}

	We can blindly put the `except` block with a retry logic, but this is a terrible idea. The tasks will now go into infinite retry loop causing waste of CPU resources unless [back off](https://en.wikipedia.org/wiki/Exponential_backoff) is used

{% highlight Python %}
@app.task(default_retry_delay = 5, bind = True, max_retries = None)
def divbad_retry(self):
	try:
		a = 2
		b = 0
		c  = a/b
		print c
	except:
		print 'exception caught: Divide by zero'
		raise self.retry()
	return c
{% endhighlight %}

	Another example is a programming mistake, for example:

{% highlight Python %}
@app.task(default_retry_delay = 5, bind = True, max_retries = None)
def codebad_noretry(self):
	a = 2
	b = 0
	print d
	return c	
{% endhighlight %}

	Here the variable `d` is getting printed without getting defined. The `except` and `retry` logic below is also unnecessary. The better solution is to resolve the programming error.

{% highlight Python %}
@app.task(default_retry_delay = 5, bind = True, max_retries = None)
def codebad_retry(self):
	try:
		a = 2
		b = 0
		print d
	except:
		print 'exception caught: global name d is not defined'
		raise self.retry()
	return c
{% endhighlight %}

