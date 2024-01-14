---
layout: blog-post
title: "Timing function / task execution in Celery"
excerpt: "Timing function / task execution in Celery"
disqus_id: /2015/12/14/timing-function-calls/
location: Bangalore, India
time: 9:00 PM
tags:
- Celery
- Python
---

With one of our current project, I had to debug performance issues related to DNS resolution. A nasty networking issue was taking 5 seconds to resolve one of our internal DNS hostname. I wanted to time all the python functions and celery tasks. I wrote a `@timeit` decorator that allows your to time the python function execution times.

However, this decorator doesn't work for celery tasks, since those functions are returned immediately. Instead, for celery, I used [`task_prerun`](http://docs.celeryproject.org/en/latest/userguide/signals.html#task-prerun) and [`task_postrun`](http://docs.celeryproject.org/en/latest/userguide/signals.html#task-postrun) signals which are called before and after every task execution.


{% highlight python %}
from celery.signals import task_prerun, task_postrun

d = {}

@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs):
    d[task_id] = time()


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state):
    try:
        cost = time() - d.pop(task_id)
    except KeyError:
        cost = -1
    print task.__name__ + ' ' + str(cost)

{% endhighlight %}

`@timeit` decorator


{% highlight python %}
import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed
{% endhighlight %}

And here is the output looks like:

{% highlight text %}
'get_followers' ((u'madhur',), {}) 1.42 sec
'prepare_message' (([], u'madhur', ([], [])), {}) 0.02 sec
{% endhighlight %}
