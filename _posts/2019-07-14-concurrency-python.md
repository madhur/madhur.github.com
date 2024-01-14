---
layout: blog-post
title: "Concurrency in Python"
excerpt: "Concurrency in Python"
disqus_id: /2019/07/14/concurrency-python/
tags:
- Concurrency
- Python
---

Recently, I was required to process bunch of huge CSV and perform the output. I wrote a simple python program but it was dreadfully slow.

I thought why not make it process through multiple threads. Python is notorious for not having a good support for concurrency. Some of it is because of its [Global Interpreter lock](https://realpython.com/python-gil/)

Recent versions of python > 3.x , do have multiprocessing and multithreading modules built in.

Honestly, I find the whole world of multiprocessing / multithreading very confusing in python world. 

Below is a sample program, which reads the CSV line by line and submits it to a pool of 50 workers, running concurrently.

```python
from multiprocessing import Pool
from random import randint
from time import sleep
import csv
import requests
import json



def orders_v4(order_number):
    response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
    return response.json()

newcsvFile=open('gom_acr_status.csv', 'w')
writer = csv.writer(newcsvFile)

def process_line(row):
    ol_key = row['ORDER_LINE_KEY']
    order_number=row['ORDER_NUMBER']
    orders_json = orders_v4(order_number)
    oms_order_key = orders_json['oms_order_key']

    order_lines = orders_json["order_lines"]
    for order_line in order_lines:
        if ol_key==order_line['order_line_key']:
            print(order_number)
            print(ol_key)
            ftype = order_line['fulfillment_spec']['fulfillment_type']
            status_desc = order_line['statuses'][0]['status_description']
            print(ftype)
            print(status_desc)
            listrow = [ol_key, order_number, ftype, status_desc]            
            writer.writerow(listrow)
            newcsvFile.flush()


def get_next_line():
    with open("gom_acr.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row

f = get_next_line()
t = Pool(processes=50)

for i in f:
    results = t.map_async(process_line, (i,))
results.get()
```