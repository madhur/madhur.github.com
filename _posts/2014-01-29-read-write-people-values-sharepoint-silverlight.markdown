---
layout: blog-post
title: "Reading and writing People Values in SharePoint List through Silverlight Client object model"
excerpt: "Reading and writing People Values in SharePoint List through Silverlight Client object model"
disqus_id: /2014/01/29/read-write-people-values-sharepoint-silverlight/
location: New Delhi, India
time: 9:00 PM
tags:
- Silverlight
- SharePoint 2010
categories:
- Web Development
---

While working on the silverlight client object model, I figured out that it is not very straight forward to read and write people values to the list.
Especially reading the people picker field requires enumerating `SiteUserInfoList` list as well. In this post I am going to cover how you can write/read people values to the list.

* Write single selection people field


{% highlight c# %}
Singleuser = context.Web.EnsureUser(SinglePeopleChooser.selectedAccounts[0].AccountName);
newItem["Single"] = Singleuser;
{% endhighlight %}

* Write multiple selection people field

{% highlight c# %}
List<FieldUserValue> usersList = new List<FieldUserValue>();
foreach (AccountList ac in MultiplePeopleChooser.selectedAccounts)
{
        usersList.Add(FieldUserValue.FromUser(ac.AccountName));
}

newItem["Multiple"] = usersList;
{% endhighlight %}

* Read single selection people field

Reading is more complex. First you retrieve the `FieldUserValue` from the people field. Unfortunately, this field only contains the `display name` and `Site User ID` of the user. You will not get the `AccountName` from this object which is a common requirement. You will have to perform the lookup against `SiteUserInfo` list to retrieve the Account Name

{% highlight c# %}
private void LoadButton_Click(object sender, RoutedEventArgs e)
{
	ClientContext ctx = new ClientContext(siteUrl);

	Web web = ctx.Web;

	ctx.Load(web);

	List list = ctx.Web.Lists.GetByTitle("Madhur");
	ctx.Load(list);

	ListItem targetItem = list.GetItemById(1);

	ctx.Load(targetItem);

	ctx.ExecuteQueryAsync((s, ee) =>
	{

		FieldUserValue singleValue = (FieldUserValue)targetItem["Single"];
		FieldUserValue[] multValue = targetItem["Multiple"] as FieldUserValue[];

		Dispatcher.BeginInvoke(() =>
		{
			LoadUser(ctx, singleValue, multValue);

		});

	},
   (s, ee) =>
   {
	   Console.WriteLine(ee.Message);

   });
}

private void LoadUser(ClientContext ctx, FieldUserValue singleValue, FieldUserValue[] multValue)
{
	List userList = ctx.Web.SiteUserInfoList;
	ctx.Load(userList);

	ListItemCollection users = userList.GetItems(CamlQuery.CreateAllItemsQuery());

	ctx.Load(users, items => items.Include(
		item => item.Id, item => item["Name"]));

	ctx.ExecuteQueryAsync((ss, eee) =>
	{
		ListItem principal = users.GetById(singleValue.LookupId);

		ctx.Load(principal);

		ctx.ExecuteQueryAsync((sss, eeee) =>
		{
			string username = principal["Name"] as string;

			string decodedName = Utils.checkClaimsUser(username);
			string dispName = principal["Title"] as string;

			Dispatcher.BeginInvoke(() =>
			{
				SinglePeopleChooser.selectedAccounts.Clear();

				SinglePeopleChooser.selectedAccounts.Add(new AccountList(decodedName, dispName));
				SinglePeopleChooser.UserTextBox.Text = dispName;

			}
				);

		},
		  (sss, eeee) =>
		  {
			  Console.WriteLine(eeee.Message);

		  });


	},
	 (sss, eeee) =>
	 {
		 Console.WriteLine(eeee.Message);

	 });

	userList = ctx.Web.SiteUserInfoList;
	ctx.Load(userList);

	users = userList.GetItems(CamlQuery.CreateAllItemsQuery());

	ctx.Load(users, items => items.Include(
		item => item.Id, item => item["Name"]));


	ctx.ExecuteQueryAsync((s, ee) =>
	{
		ListItem[] principals = new ListItem[multValue.Length];

		for (int i = 0; i < multValue.Length; i++)
		{
			principals[i] = users.GetById(multValue[i].LookupId);
			ctx.Load(principals[i]);
		}

		ctx.ExecuteQueryAsync((ssss, eeeee) =>
		{
			string username;

			for (int i = 0; i < multValue.Length; i++)
			{


				try
				{
					username = principals[i]["Name"] as string;
				}
				catch (IndexOutOfRangeException ii)
				{
					return;
				}

				string decodedName = Utils.checkClaimsUser(username);
				string dispName = principals[i]["Title"] as string;

				Dispatcher.BeginInvoke(() =>
				{
					MultiplePeopleChooser.selectedAccounts.Add(new AccountList(decodedName, dispName));
				}
				);
			}


		},
	   (ssss, eeeee) =>
	   {
		   Console.WriteLine(eeeee.Message);

	   });

	},

	 (ssss, eeeee) =>
	 {
		 Console.WriteLine(eeeee.Message);

	 });

}
{% endhighlight %}
