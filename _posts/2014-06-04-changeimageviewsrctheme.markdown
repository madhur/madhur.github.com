---
layout: blog-post
title: "Change ImageView src based on Android Application theme"
excerpt: "Change ImageView src based on Android Application theme"
disqus_id: /2014/06/04/changeimageviewsrctheme/
location: New Delhi, India
time: 9:00 PM
tags:
- Android
---

Recently, I had a requirement to change the `ImageView` picture to be changed based on the theme. I was using an `ExpandableListView` and using the `ImageView` as 
a group indicator rather than out of the box group indicator. Since my application supported both light and dark theme, I wanted to switch the group indicators, action bar icons to light and dark versions as well.

I looked at some of the questions in [StackOverflow](http://stackoverflow.com/) , but none answered satisfactorily.

In the end, I found out it was fairly easy, without using any code. Here it is how:

Declare custom attributes in `res/values/attrs.xml` file for each of the ImageView or ActionBar icon to be changed based on theme:

{% highlight xml %}
<declare-styleable name="customAttrs">
	<attr name="actionSearchIcon" format="reference" />
	<attr name="actionAcceptIcon" format="reference" />
	<attr name="actionRefreshIcon" format="reference" />
	<attr name="groupIndicatorIcon" format="reference" />
</declare-styleable>
{% endhighlight %}

In the theme file which would be `res/values/styles.xml` or the suitable one depending upon the version you are targetting, define the same attributes pointing to the
appropriate drawables. For example below, the `Black` theme is pointing to drawables related to dark theme and `Light` theme is pointing to drawables related to light theme.

{% highlight xml %}
<style name="Black" parent="@style/Theme.AppCompat">
	<item name="actionSearchIcon">@drawable/ic_action_search</item>
	<item name="actionAcceptIcon">@drawable/ic_action_accept</item>
	<item name="actionRefreshIcon">@drawable/navigation_refresh</item>
	<item name="groupIndicatorIcon">@drawable/group_indicator</item>
</style>


<style name="Light" parent="@style/Theme.AppCompat.Light">
	<item name="actionSearchIcon">@drawable/ic_action_search_light</item>
	<item name="actionAcceptIcon">@drawable/ic_action_accept_light</item>
	<item name="actionRefreshIcon">@drawable/navigation_refresh_light</item>
	<item name="groupIndicatorIcon">@drawable/group_indicator_light</item>
</style>
{% endhighlight %}

Finally, coming to the actual layouts, ***point the relavant attributes to the attributes you have defined rather than directly to the drawables.*** For example
in case of ActionBar icons:

{% highlight xml %}
<item
android:id="@+id/action_refresh"
android:icon="?attr/actionRefreshIcon"
android:orderInCategory="107"
android:title="@string/action_refresh"
app:showAsAction="always"/>

<item
android:id="@+id/action_accept"
android:icon="?attr/actionAcceptIcon"
android:orderInCategory="108"
android:title="@string/action_accept"
app:showAsAction="always"/>

<item
android:id="@+id/action_search"
android:icon="?attr/actionSearchIcon"
android:orderInCategory="50"
android:title="@string/action_search"
app:actionViewClass="android.support.v7.widget.SearchView"
app:showAsAction="collapseActionView|always"/>
{% endhighlight %}	

Or in case of ImageView:

{% highlight xml %}
<ImageView
android:id="@+id/group_indicator"
android:layout_width="wrap_content"
android:layout_height="wrap_content"
android:layout_alignParentLeft="true"
android:contentDescription="@string/app_name"
android:src="?attr/groupIndicatorIcon"/>
{% endhighlight %}         

The exciting part is that this concept can be applied to any control or any attribute :)