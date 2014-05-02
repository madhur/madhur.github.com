---
layout: blog-post
title: "Decoding the hidden Wunderlist API (Part I)"
excerpt: "Decoding the hidden Wunderlist API (Part I)"
disqus_id: /2014/05/02/decodewunderlistapi/
location: New Delhi, India
time: 9:00 PM
tags:
- Wunderlist
- API
- REST
categories:
- Development
---

Without any doubt, [Wunderlist](https://www.wunderlist.com) is the most popular to do list manager. With its increasing popularity, demand is growing for people to let Wunderlist expose 
its API to public so that users can build great apps around it and integrate it with their systems. Posts such as [this](https://wunderlist.uservoice.com/forums/136230-wunderlist-feature-requests/suggestions/2378704-developers-api) on Wunderlist support forum clearly indicate the popularity and demand for such an API.

Although, Wunderlist has yet not exposed any public API but it seems there are definite plans for that going by post such as [this](http://techcrunch.com/2013/11/12/to-do-app-wunderlist-confirms-19m-series-b-and-expands-to-the-us-while-sequoia-heads-into-germany/)
Nevertheless, what I found is that it is easy to discover the Wunderlist API by simply inspecting the HTTPS traffic over the Wunderlist web site. If we see their Licenses section, it is easy to see that they 
use [backbone.js]() along with [Jquery]() and [RequireJs]() giving the clear indication of MVC pattern being in use along with [JSON]() as the data exchange format

![](/images/Blog/screenshot.1.png)

Now, lets head over to the browser to inspect the HTTPS traffic and see if we can get some information about their API. What I am going to do is login to Wunderlist website with my credentials and record the 
HTTPS traffic in the Chrome inspector. I have also turned on the button for `Preserve log upon Navigation`

![](/images/Blog/screenshot.2.png)
![](/images/Blog/screenshot.3.png)

If we filter by requests of type XML HTTP Request(XHR), we will see a `POST` request `/login` to the host `api.wunderlist.com`. In the request payload, I also see my username and password in cleartext. Although
I do not have anything to worry since this is transmitted over SSL

![](/images/Blog/screenshot.4.png)

If we just scroll few lines down, I see another request `/batch` to `api.wunderlist.com` with this JSON payload and the response is a considerable JSON response. I could the names of lists and tasks in the JSON response.

![](/images/Blog/screenshot.5.png)

{% highlight json %}
{"ops":[
{"method":"put","url":"/me/settings","params":{"web_significant_event_count":"5","web_shortcut_add_new_task":"CTRL + 0"}},
{"method":"get","url":"/me"},{"method":"get","url":"/me/settings"},
{"method":"get","url":"/me/contacts","params":{}},
{"method":"get","url":"/me/services","params":{}},
{"method":"get","url":"/me/lists","params":{"since":"1399004140"}},
{"method":"get","url":"/me/tasks","params":{"before":1399141799,"limit":1000,"compact":true}},
{"method":"get","url":"/me/reminders","params":{}},
{"method":"get","url":"/me/shares","params":{}},
{"method":"get","url":"/me/events","params":{"locale":"en_US"}},
{"method":"get","url":"/me/quota","params":{}}],
"sequential":true}
{% endhighlight %}

Great, it seems that we have just discovered a bunch of REST API calls. These are batched together in single HTTP request for optimization. We also know the method `GET` or `POST` of these requests and also the parameters some of them. The next step is to take this request individually and test it one by one. But how do we do it?

For this purpose, I am using an excellent Chrome extension called [Dev HTTP Client](https://chrome.google.com/webstore/detail/dev-http-client/aejoelaoggembcahagimdiliamlcdmfm?hl=en)

First, lets authenticate ourselves using the `/login` API. This will be a post request containing the `username` and `password` for the Wunderlist.

[![](/images/Blog/screenshot.7.png)](/images/Blog/screenshot.7.png)

The result is the following JSON response:

{% highlight json %}
{
"id":"AAAEAABXCxQ",
"created_at":"2014-04-30T11:59:36Z",
"updated_at":"2014-04-30T11:59:36Z",
"name":"madhur",
"type":"User",
"avatar":"https://graph.facebook.com/522955158/picture?width=0&height=0",
"email":"ahuja.madhur@gmail.com",
"token":"8758a4a0f983177a427a879a30b144d92bc2f01e",
"terms_accepted_at":"2013-07-07",
"confirmation_state":"confirmed_email",
"email_confirmed":true,
"channel":"me.updates.2ea715786fc5ed6af21a97d2104ac4a095349e9b",
"product":null,
"group_product":null,
"facebook":"522955158",
"settings":{
"account_locale":"en",
"background":"wlbackground03",
"campaign_iyf4_notification":"true",
"campaign_iyf4_notification_last_date":"2013-12-16T00:47:14Z",
"campaign_iyf4_notification_variation":"c",
"consumed_quota_assigning_daily":"0",
"consumed_quota_assigning_daily_date":"2013-09-26",
"consumed_quota_assigning_overall":"0",
"consumed_quota_comments_daily":"0",
"consumed_quota_comments_daily_date":"2013-09-26",
"consumed_quota_comments_overall":"0",
"consumed_quota_files_daily":"0",
"consumed_quota_files_daily_date":"2013-09-26",
"consumed_quota_files_overall":"0",
"created_by_compound_id":"AAAEAABXCxQ",
"created_by_id":"5704468",
"created_by_type":"User",
"experiment_chatter_notifications":"compacted",
"notifications_email_enabled":"false",
"notifications_push_enabled":"true",
"setting":"{}",
"show_completed_items":"false",
"sound_checkoff_enabled":"false",
"sound_notification_enabled":"false",
"start_of_week":"mon",
"use_badge_icon":"notifications",
"web_app_open_count":"2",
"web_coach_mark_detail_view":"completed",
"web_coach_mark_inbox":"completed",
"web_coach_mark_smart_list":"completed",
"web_last_app_open_date":"1398969000000",
"web_last_used_release":"2.3.8.3",
"web_new_installation":"true",
"web_shortcut_add_new_task":"CTRL + 0",
"web_significant_event_count":"5",
"web_uuid":"d45186f5-0699-4986-906d-c6ad3f88c180"
}
{% endhighlight %}

This piece of information is very important for us in JSON response: `token:8758a4a0f983177a427a879a30b144d92bc2f01e`. This is the token which we need to send in 
any of the other REST API requests otherwise you will get this error in response:


{% highlight json %}
{
"errors":
	{
	"message":"You must be authenticated to continue.",
	"type":"unauthorized"
	}
}
{% endhighlight %}


Let's try to retrieve the lists using the `/lists` API and the token:

[![](/images/Blog/screenshot.8.png)](/images/Blog/screenshot.8.png)

The result is the list of Wunderlist lists I have in my account:


{% highlight json %}
	{
	"id":"ABAEAAS9pWM",
	"type":"List",
	"local_identifier":"localId:prepopulated:AAAEAABXCxQ:List:private",
	"owner_id":"AAAEAABXCxQ",
	"position":4.37502,
	"title":"Private",
	"created_at":"2013-07-07T01:25:06Z",
	"updated_at":"2014-04-29T11:05:46Z"
	},
	{
	"id":"ABAEAAS9pWQ",
	"type":"List",
	"local_identifier":"localId:prepopulated:AAAEAABXCxQ:List:work",
	"owner_id":"AAAEAABXCxQ",
	"position":1.87502,
	"title":"Work",
	"created_at":"2013-07-07T01:25:06Z",
	"updated_at":"2014-04-11T07:52:33Z"
	}
{% endhighlight %}

Using a similar approach, we can invoke the following REST API's and get their responses in JSON:

`/me/settings`  
`/me`  
`/me/contacts`  
`/me/services`  
`/me/lists`  
`/me/tasks`  
`/me/reminders`  
`/me/shares`  
`/me/events`  
`/me/quota`  

##A note about authentication##

At this moment, there is no OAuth implementation for the authorization on this API and probably this is the reason the API is not public yet.
This means, the token we recieve in response `/login` call will have some expiry date attached to it. Hence, if we plan to build some functionality based on this information,
it is sufficient to assume that we need to re-authenticate using the `username` and `password` once the token expires.

In the part II of this blog post, I am going to share a partial implementation of this API in java using [Retrofit](http://square.github.io/retrofit/)