---
layout: blog-post
title: "Convert claims based login name in SharePoint Client object model"
excerpt: "Convert claims based login name in SharePoint Client object model"
disqus_id: /2014/01/29/convert-claim-based-login-name/
location: New Delhi, India
time: 9:00 PM
tags:
- Silverlight
- SharePoint 2010
categories:
- Web Development
---

Recently, I was working on a silverlight solution and came across an issue where People WebService returned me the duplicate results for the people who are already 
part of the site collection. This issue can occur if SharePoint is using claim based authentication model.

On close inspection I found that the returned duplicate results were having different login names. For example if one result was `ads\john` then the other one was `i:0#.w|ads\john`.

It is easy to remove such duplicates if you are programming against server side directly with the following API code:

{% highlight c# %}
private string GetLoginName(string name)
{
	 var manager = SPClaimProviderManager.Local;
	 if (manager != null)
	 {
		 return SPClaimProviderManager.IsEncodedClaim(name) ? manager.DecodeClaim(name).Value : name;
	 }
	 return name;
}
{% endhighlight %}

However, if you are programming against Client object model, you do not have luxury of calling such API's. For those scenarios , I wrote a small function which will take the Claim encoded login name and return the pure Windows login name.

{% highlight c# %}
public static string checkClaimsUser(String userName)
{
	string decodedName;

	if (userName.Contains("|"))
	{
		string[] splitUserName = userName.Split(new Char[] { '|' }, StringSplitOptions.None);
		if (splitUserName.Length > 0)
			decodedName = splitUserName[1];
		else
			decodedName = userName;
	}
	else
	{
		decodedName = userName;
	}


	return decodedName.ToLower();

}
{% endhighlight %}