---
layout: blog-post
title: "Read Google docs spreadsheet using Python"
excerpt: "Read Google docs spreadsheet using Python"
disqus_id: /2016/05/13/google-docs-spreadsheet-python/
location: Bangalore, India
time: 9:00 PM
tags:
- Python
---

One of the many useful and productive feature for me personally is to programmatically read a Google docs spreadsheet in Python. This is very useful to automate a task to insert some data in MySQL/NOSQL/ElasticSearch, which would have otherwise required to build a custom user interface for data input.

Reading is actually quite simple. For example, you have a spreadsheet like this:

![](/images/Blog/spreadsheet.png)

First, you need to grab the file id. In the image below, file id is 
`19Y_Oi5_riecwonPbtxN4sfDntZO62s_vJbXoogFFp9o`

![](/images/Blog/spreadsheet_url.png)

Make sure to give the read permission to anyone having the link, otherwise our python program won't be able to read the file.

First, we make a simple `GET` request on the export url of the spreadhseet using the [requests](http://docs.python-requests.org/en/master/) module

{% highlight python %}
headers={}
headers["User-Agent"]= "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"
headers["DNT"]= "1"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
headers["Accept-Encoding"] = "deflate"
headers["Accept-Language"]= "en-US,en;q=0.5"
lines = []

file_id="19Y_Oi5_riecwonPbtxN4sfDntZO62s_vJbXoogFFp9o"
url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(file_id)

r = requests.get(url)
{% endhighlight %}

Once we have the response, it is easy to read it using the [csv](https://docs.python.org/2/library/csv.html) module

{% highlight python %}
sio = io.StringIO( r.text, newline=None)
reader = csv.reader(sio, dialect=csv.excel)

for row in reader:
    # Do something with each row

{% endhighlight %}

For example, to read the data as a dictionary, we can do something like this:

{% highlight python %}
for row in reader:
    if rownum == 0:
        for col in row:
            data[col] = ''
            cols.append(col)

    else:
        i = 0
        for col in row:
            data[cols[i]] = col
            i = i +1

        print data
    rownum = rownum + 1
{% endhighlight %}

This will print the following output on console:

{% highlight text %}
{'Col C': '3', 'Col B': '2', 'Col A': '1', 'Col D': '4'}
{'Col C': '2', 'Col B': '3', 'Col A': '4', 'Col D': '1'}
{'Col C': '2', 'Col B': '4', 'Col A': '3', 'Col D': '1'}
{'Col C': '3', 'Col B': '4', 'Col A': '2', 'Col D': '1'}
{% endhighlight %}

Incase, we are using unicode characters with our file. We can make use of [unicodecsv](https://pypi.python.org/pypi/unicodecsv) module. It is a drop in replacement of the `csv` module.

{% highlight python %}
import unicodecsv as csv
reader = csv.reader(
        urllib2.urlopen(url),
        encoding='utf-8'
    )

for row in reader:
{% endhighlight %}


The complete program is given in this [gist](https://gist.github.com/madhur/13ef5a810d495e9c638232263ea49fd5) and as well as below. You just need to replace the `file_id` parameter to start using it. Feel free to fork it :)

<script src="https://gist.github.com/madhur/13ef5a810d495e9c638232263ea49fd5.js"></script>

