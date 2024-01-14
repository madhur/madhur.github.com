---
layout: blog-post
title: "Updating Created By field in SharePoint through Client Object Model"
excerpt: "Updating Created By field in SharePoint through Client Object Model"
disqus_id: /2014/05/09/updatingcreatedby/
location: New Delhi, India
time: 9:00 PM
tags:
- SharePoint 2010
- Client Object Model
categories:
- Development
---

Recently, we did a migration from SharePoint 2010 old site to a new site and as a result imported a bunch of records.

However, the `Created By` field was reset to the Account of the person performing the migration. To overcome this, I wrote a quick script to update the 
`Created By` field. The field was updated from another field `Old_Created_By_Person`

{% highlight csharp %}

using Microsoft.SharePoint.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SPUpdateField
{
    class Program
    {
        static void Main(string[] args)
        {

            ClientContext ctx = new ClientContext("https://teams.aexp.com/sites/excel");
            List list = ctx.Web.Lists.GetByTitle("Idea");
            ListItemCollection items = list.GetItems(CamlQuery.CreateAllItemsQuery());
            ctx.Load(items); // loading all the fields
            ctx.ExecuteQuery();

            foreach (var item in items)
            {
                ctx.Load(item);
                ctx.ExecuteQuery();
                // important thing is, that here you must have the right type
                // i.e. item["Modified"] is DateTime
                FieldUserValue val = item["Old_Created_By_Person"] as FieldUserValue;

                if (val != null)
                {
                    item["Author"] = val;

                    // do whatever changes you want

                    item.Update(); // important, rembeber changes
                    ctx.ExecuteQuery();
                    Console.WriteLine("Updating " + item.Id);
                }
            }
           

            Console.WriteLine("Done");
            Console.ReadLine();
        }

    }
}



{% endhighlight %}