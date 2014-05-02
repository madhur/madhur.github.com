---
layout: blog-post
title: "Decoding the hidden Wunderlist API (Part II)"
excerpt: "Decoding the hidden Wunderlist API (Part II)"
disqus_id: /2014/05/02/decodewunderlistapi2/
location: New Delhi, India
time: 9:00 PM
tags:
- Wunderlist
- API
- REST
categories:
- Development
---

In [part I]({% post_url 2014-05-02-decodewunderlistapi %}) we discovered the hidden Wunderlist API. In this post, I am to show partial implementation of this API client in Java using [Retrofit](http://square.github.io/retrofit/).
The implementation is hosted in my [Git repository](https://github.com/madhur/wunder-java). Feed free to fork, extend or submit appropriate pull requests. I will be glad to accept your contribution.

[Retrofit](http://square.github.io/retrofit/) is a java library which turns your REST API into java interfaces. For example, the REST API which we discovered in Part I will be defined as:

{% highlight java %}
public interface WunderAPI
{
	@FormUrlEncoded
	@POST("/login")
	  LoginResponse login(@Field("email") String username, @Field("password")String password);
	
	@GET(value = "/me")
	  Me getUserInfo(@Header("Authorization") String authorization);
	
	@GET(value = "/me/tasks")
	List<WTask> GetWunderTasks(@Header("Authorization") String authorization);
	
	@POST(value = "/me/tasks")
	List<WTask> CreateWunderTask(@Header("Authorization") String authorization, String listId, String title,  String isStarred, String dueDate);
	
	@GET(value = "/me/lists")
	List<WList> GetLists(@Header("Authorization") String authorization);
}
{% endhighlight %}

Java Classes such as `WList`, `WTask`  and `Me` all map to the JSON response returned by individual REST API. 


## How do I invoke the API? ##

Invoking the API is simple. There is a helper class `WunderList` which is basically a singleton and you have get its instance by providing the wunderlist `username` and `password`. Once we have
the instance we can invoke the corresponding helper methods such as `GetLists` and `GetTasks`. 

{% highlight java %}
wunderList=WunderList.getInstance(username, password);

List<WList> wlists=wunderList.GetLists();

List<WTask> wTasks=wunderList.GetTasks();

{% endhighlight %}

## Contributing ##

I will be glad to accept pull requests to make this API client as complete as possible. Since this is still a very partial implementation, I look forward to the contributions from people who want to build something awesome using Wunderlist API.

The project is an Eclipse java application. You can either use eclipse or gradle to build it. For example, using gradle use the task `mainjar` to build the executable jar


{% highlight text %}
D:\Users\madhur\workspace\location\Wunderjava>gradle mainjar
:mainjar UP-TO-DATE

BUILD SUCCESSFUL

Total time: 3.945 secs
D:\Users\madhur\workspace\location\Wunderjava>cd build

D:\Users\madhur\workspace\location\Wunderjava\build>cd libs

D:\Users\madhur\workspace\location\Wunderjava\build\libs>java -jar Wunderjava.jar
Enter the Wunderlist username:
ahuja.madhur@gmail.com
Enter the Wunderlist password:
thisisnottherightpassword
Name: madhur
Authorization Toekn: 8758a4a0f983177a427a879a30b144d92bc2f01e
Press enter to print out the lists

Printing out the lists:
Private
Work
Shopping
Movies to Watch
Wishlist
Places
Activities
App ideas
Healthy foods
Lunch
Role models
Friends
Kanika session
Learning
Blog Articles
Coconut milk
Home shpng
Kwality bazar
Saturday
Press enter to print out the tasks
{% endhighlight %}