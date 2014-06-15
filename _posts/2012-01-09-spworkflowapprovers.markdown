---
layout: blog-post
title: "Invoke SharePoint 2010 Approval Workflow with Dynamic Approvers using Web Services and Jquery"
excerpt: "Invoke SharePoint 2010 Approval Workflow with Dynamic Approvers using Web Services and Jquery"
disqus_id: /2012/01/09/spworkflowapprovers/
location: New Delhi, India
time: 12:00 PM
tags:
- SharePoint 2010
- Jquery
---

In this post, I am going to show you how you can execute out of the box SharePoint 2010 approval workflow with dynamic approvers.

Let's say, you have a list on which you have Approval workflow configured and you want the approver to be picked from the Person or Group type field from within the list.

Let's assume , the ID is being specified in the query string of the page such as 

**StartWorfklow.aspx?ItemID=5**

I will be making use of [Jquery](http://jquery.com) and [SPServices](http://spservices.codeplex.com) from codeplex for this purpose.

* First of all, we will retrieve the our specified item from this list and then retrieve the value of this Person or Group field. 



{% highlight javascript %}
var ItemID= getParameterByName("ItemID");

// Construct the CAML Query
var CamlQuery = "<Query><Where><Eq><FieldRef Name='ID' /><Value Type='Counter'>"+ItemID+"</Value></Eq></Where></Query>";

 
// Fire GetListItems web service to find the Approval contact
$().SPServices({
    operation: "GetListItems",
    async: false,
    CAMLQuery: CamlQuery ,
    listName: "Intake Requests",
    CAMLViewFields: "<ViewFields><FieldRef Name='Band_x0020_45_x0020_Approval' /></ViewFields>",
    completefunc: function (xData, Status) 
	{
        
        events = new Array();
        $(xData.responseXML).find("z\\:row").each(function() 
		{
				
                approverName=$(this).attr("ows_Band_x0020_45_x0020_Approval");
				var index=approverName.indexOf(";");
				approverID=approverName.slice(0,index);
				
				approverName=approverName.substring(index+2,approverName.length);
				
          
			
        })
    }
})
{% endhighlight %}

* When we retrieve the person or group field from the web services, it is returned as **1;#Madhur Ahuja**. Where 1 is the ID of the row in User Information List and **Madhur Ahuja** is the display name.
To pass it to Approval Workflow, we need the login name.

We will query the **User Information List** to obtain the login name.


{% highlight javascript %}
// We will just get the DisplayName and ID, but not the Login Name, we will fire another web service to fetch the loginName of the User 
if(approverName!=null)
{
		
		 var xmlData ="<soap:Envelope xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema'><soap:Body><GetListItems xmlns='http://schemas.microsoft.com/sharepoint/soap/'><listName>User Information List</listName><query><Query xmlns=''><Where><Eq><FieldRef Name='ID' /><Value Type='Counter'>"+approverID+"</Value></Eq></Where><OrderBy><FieldRef Name='Title' /></OrderBy></Query></query><viewFields><ViewFields xmlns='' /></viewFields><queryOptions><QueryOptions xmlns='' /></queryOptions></GetListItems></soap:Body></soap:Envelope>";

		 $.ajax({
		   url: "/sites/nishantverma/_vti_bin/lists.asmx",
		   type: "POST",
		   async: false,
		   dataType: "xml",
		   data: xmlData, 
		   complete:SuccessFunc,
		   error: ErrorFunc,
		   contentType: "text/xml; charset=\"utf-8\""
		  });
		  
		  function SuccessFunc(result)
		  {
			//xml node with namespace need to be handled differently for jQuery
			 $(result.responseXML).find("z\\:row").each(function() 
			 {
				
				loginName=$(this).attr("ows_Name");
				
				
			});
		}

		function ErrorFunc(result) 
		{
					alert(result.responseText);
		}
		
}
{% endhighlight %}

* We get the login name in the variable **ows_Name**. Now we can fire the Approval workflow passing it the login name.
Note the **templateId** below, its the GUID of the SharePoint 2010 Approval workflow which is associated with the list. 

{% highlight javascript %}
 $().SPServices({
				operation: "StartWorkflow",
				item: "http://sp.madhurmoss.com/sites/nishantverma/GBSRequest/Lists/Intake%20Requests/" + ItemID + "_.000",
				templateId: "{10E4D465-A9B6-4146-BD50-E9A78888548D}",
				workflowParameters: assocData,
				completefunc: function() 
				{
					$("#intake").html("Your Intake Request has been sent to "+approverName+" for his approval. Thanks for submitting the request. This page will redirect to homepage after few seconds");
					
					window.setTimeout(function() 
					{
						window.location.href = '/sites/nishantverma/GBSRequest';
					}, 5000)
				}
			  });
			  
{% endhighlight %}			  

Here, the key is the variable *assocData*, which is nothing but the Association Data of the workflow. In SharePoint 2010 Approval workflow, its the serialized XML of the infopath form. This variable is defnied as the XML string as below:

{% highlight javascript %}
			var assocData='<dfs:myFields xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:dms="http://schemas.microsoft.com/office/2009/documentManagement/types" xmlns:dfs="http://schemas.microsoft.com/office/infopath/2003/dataFormSolution" xmlns:q="http://schemas.microsoft.com/office/infopath/2009/WSSList/queryFields" xmlns:d="http://schemas.microsoft.com/office/infopath/2009/WSSList/dataFields" xmlns:ma="http://schemas.microsoft.com/office/2009/metadata/properties/metaAttributes" xmlns:pc="http://schemas.microsoft.com/office/infopath/2007/PartnerControls" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'+
'<dfs:queryFields></dfs:queryFields>'+
'<dfs:dataFields>'+
'<d:SharePointListItem_RW>'+
'<d:Approvers>'+
 
 
'<d:Assignment>'+
 
'<d:Assignee>'+
'<pc:Person><pc:DisplayName></pc:DisplayName><pc:AccountId>'+loginName+'</pc:AccountId><pc:AccountType>User</pc:AccountType></pc:Person>'+
'</d:Assignee>'+
 
'<d:Stage xsi:nil="true" />'+
'<d:AssignmentType>Serial</d:AssignmentType>'+
 
'</d:Assignment>'+
 
'</d:Approvers>'+
 
 
'<d:ExpandGroups>true</d:ExpandGroups>'+
'<d:NotificationMessage>Please approve</d:NotificationMessage>'+
'<d:DueDateforAllTasks xsi:nil="true" /><d:DurationforSerialTasks xsi:nil="true" />'+
'<d:DurationUnits>Day</d:DurationUnits>'+
'<d:CC />'+
'<d:CancelonRejection>true</d:CancelonRejection>'+
'<d:CancelonChange>false</d:CancelonChange>'+
'<d:EnableContentApproval>false</d:EnableContentApproval>'+
'</d:SharePointListItem_RW>'+
'</dfs:dataFields>'+
'</dfs:myFields>';
{% endhighlight %}


The full code can be downloaded from my [gist](https://gist.github.com/1584225) here.		