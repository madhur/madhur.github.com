---
layout: blog-post
title: "Integrate node.js logging with Sentry"
excerpt: "Integrate node.js logging with Sentry"
disqus_id: /2016/09/05/integrating-sentry-node/
tags:
- Node.js
- Sentry
---

Effective logging is crucial to any application deployed in production. For node.js, [express](http://expressjs.com/) based applications, we use [Winston](https://github.com/winstonjs/winston) as our logging framework.

In our scenario, we also want some crucial logs to be logged to [Sentry](https://sentry.io/welcome/). 

A simple setup of Sentry is described below. This is same as what is described in [sentry docs](https://docs.sentry.io/clients/node/integrations/express/).

{% highlight javascript %}

var sentry_enabled = false;

if (process.env.NODE_ENV == 'production') {
    sentry_enabled = true;
}

if (sentry_enabled) {
    app.use(raven.middleware.express.requestHandler(config.sentry_dsn));
}

// setup routes
app.use('/', healthcheck);

if (sentry_enabled) {
    app.use(raven.middleware.express.errorHandler(config.sentry_dsn));
}

{% endhighlight %}

All good uptil now, except that this setup logs only unhandled exceptions to Sentry. For sending manual log lines to Sentry, sentry recommends using `client.captureException(e)` or `client.captureMessage(msg)` as per these [docs](http://expressjs.com/)

However, it could be great if we send our winston `error` level logs to sentry.

That's where [winston-sentry](https://github.com/guzru/winston-sentry) packages comes to help. It can send your winston logs to sentry automatically.

All that is needed is to add a Sentry transport to the winston logger.

{% highlight javascript %}
var winston = require('winston');
var Sentry = require('winston-sentry');
winston.emitErrs = true;

var logger = new winston.Logger({
    transports: [
        new winston.transports.File({
            level: '0',
            filename: '/opt/logfile.log',
            handleExceptions: true,
            json: false,
            colorize: false,
            timestamp: function() { return new Date().toLocaleString('ca'); }
        }),
        new winston.transports.Console({
            level: 'info',
            handleExceptions: true,
            json: false,
            colorize: true
        }),
        new Sentry({
            level: 'error',
            dsn: config.sentry_dsn,
            tags: { key: 'value' },
            extra: { key: 'value' }
        })
    ],
    exitOnError: false
});

module.exports = logger;
{% endhighlight %}