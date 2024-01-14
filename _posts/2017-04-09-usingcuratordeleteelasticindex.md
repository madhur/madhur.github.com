---
layout: blog-post
title: "Using curator to delete older elasticsearch indices"
excerpt: "Using curator to delete older elasticsearch indices"
disqus_id: /2017/04/09/using-curator-delete-elasticsearch-indices/
tags:
- Curator
- Elasticsearch
---

Tech Tip : Monitor virtual servers, carry on your scripting work by accessing your essential emulators and tools all at a centralized platform with hosted windows virtual desktop from <a title=Microsoft&nbsp;Virtual&nbsp;Desktop href=https://www.clouddesktoponline.com/>CloudDesktopOnline</a>. Visit <a title=Apps4Rent&nbsp;-&nbsp;Hosting&nbsp;Provider href=http://www.apps4rent.com/>Apps4Rent.com</a> to know more about cloud products suitable for you.

We use [ELK stack](https://www.elastic.co/webinars/introduction-elk-stack) heavily in our production systems for log aggregation and monitoring.

Our daily log size generated is aroudn 100GB. Since, we do not intend to keep the log files in ELK for more than a month, it becomes important that we delete those indices to free up disk space.

Fortunately, [Logstash](https://www.elastic.co/products/logstash) creates a new index every day by default.

Thus, we can ask [Curator](https://github.com/elastic/curator) to simply delete the indices x days old and which follow a particular naming pattern.


### Installing Curator
Simple use `pip install elasticsearch-curator` to install Curator on your machine. I prefer to install it on the Elasticsearch machine itself.

### Configuring Curator
Create a file `curator.yml` with following contents.

{% highlight yaml %}
---
client:
  hosts:
    - 127.0.0.1
  port: 9200
  url_prefix:
  use_ssl: False
  certificate:
  client_cert:
  client_key:
  ssl_no_validate: False
  http_auth:
  timeout: 30
  master_only: False

logging:
  loglevel: INFO
  logfile:
  logformat: default
  blacklist: ['elasticsearch', 'urllib3']

{% endhighlight %}

Now, we need to define an action. i.e. What will curator do.  There are many actions to choose from. Check the [documentation](https://www.elastic.co/guide/en/elasticsearch/client/curator/current/actions.html) for more information

* Alias
* Allocation
* Close
* Cluster Routing
* Create Index
* Delete Indices
* Delete Snapshots
* Open
* forceMerge
* Replicas
* Restore
* Snapshot

For this dicussion, we will use `Delete Indices` as the action, since this is what we want to do.

Below is the sample action file `delete_indices.yml` , which will delete the logstash indices which are older than 10 days.

{% highlight yaml %}
---
actions:
  1:
    action: delete_indices
    description: >-
      Delete indices older than 45 days (based on index name), for logstash-
      prefixed indices. Ignore the error if the filter does not result in an
      actionable list of indices (ignore_empty_list) and exit cleanly.
    options:
      ignore_empty_list: True
      timeout_override:
      continue_if_exception: False
      disable_action: False
    filters:
    - filtertype: pattern
      kind: prefix
      value: logstash-
      exclude:
    - filtertype: age
      source: name
      direction: older
      timestring: '%Y.%m.%d'
      unit: days
      unit_count: 10
      exclude:
{% endhighlight %}


To run this action, simple use the command 

{% highlight text %}
curator ./delete_index.yml --config ./curator.yml --dry-run
2017-04-09 17:27:46,075 INFO      Preparing Action ID: 1, "delete_indices"
2017-04-09 17:27:46,080 INFO      Trying Action ID: 1, "delete_indices": Delete indices older than 45 days (based on index name), for logstash- prefixed indices. Ignore the error if the filter does not result in an actionable list of indices (ignore_empty_list) and exit cleanly.
2017-04-09 17:27:46,538 INFO      DRY-RUN MODE.  No changes will be made.
2017-04-09 17:27:46,538 INFO      (CLOSED) indices may be shown that may not be acted on by action "delete_indices".
2017-04-09 17:27:46,538 INFO      Action ID: 1, "delete_indices" completed.
2017-04-09 17:27:46,538 INFO      Job completed.
{% endhighlight %}

The `--dry-run` mode will not actually delete the index. It can be used to test the output of the action.

If you want to schedule it in a cron, you can do so using `crontab -e`

{% highlight text %}
00 8 * * * root curator /path/delete_index.yml --config /path/curator.yml 
{% endhighlight %}

The above configuration will cleanup the indices older than 10 days everyday at 8 AM.
