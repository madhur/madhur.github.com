---
layout: blog-post
title: "Angular Chat popup"
excerpt: "Angular Chat popup"
disqus_id: /2015/09/14/angular-chat-popup/
location: Bangalore, India
time: 9:00 PM
tags:
- AngularJs
- Javascript
---

Recently, I was required to write a popup menu for our chat application. The popup menu looked very similar to ones in [Slack](https://slack.com/) and [Flock](http://www.flock.co/).

I looked some sample impementations. [Flock](http://www.flock.co/) uses [DOJO Toolkit](https://dojotoolkit.org/) to power its entire UI and its popup menu is also powered by it.  Our application was already using [AngularJs](https://angularjs.org/) as a framework and I did not want to introduce another framework just for the sake of popup menu.


Looking at slack, it seems to use its own custom implementation. I liked the slack implementation better than the flock one.

Finally, I decided to write my own directive in angular for this feature. Take a look at this [github repository](https://github.com/madhur/angular-chat-popup) for the soure code and how to use it in your own project.

## How does this work

Upon `/` character, a popup menu is rendered. Its template is fetched from `partials/popupmenu.html` file.


## How do I configure the popup

The input data is fetched from the `appsettings.js` file. Currently 3 levels are supported. In actual case, this data may come from a 
`$http` service.


```javascript
        [{
                id: 0,
                text: "Macros",
                desc: "Includes greetings, apologies, goodbyes",
                commands:[]

            },

            {
                id: 1,
                text: "Upload image",
                desc: "Allows to select an image to upload",
                action_type: "upload_image"
            },

            {
                id: 2,
                text: "Redirect",
                desc: "Redirect user to a different channel",
                action_type: "redirect_chat"
            },


            {
                id: 3,
                text: "Rate card",
                desc: "Send a rate card to the user",
                action_type: "rate_card"
            },

            {
                id: 4,
                text: "Share card",
                desc: "Send a share card to the user",
                commands: [

                	 {
		                id: 6,
		                text: "WhatsApp",
		                desc: "Share Request",
		                action_type: "share_whatsapp",
            		},

            		{
		               id: 7,
		                text: "Facebook",
		                desc: "Share Request",
		                action_type: "share_facebook",
            		},

            		{
		                id: 8,
		                text: "Facebook Messenger",
		                desc: "Share Request",
		                action_type: "share_messenger",
            		},

            		{
		                id: 9,
		                text: "Twitter",
		                desc: "Share Request",
		                action_type: "share_twitter",
            		},

            		{
		                id: 10,
		                text: "Google Plus",
		                desc: "Share Request",
		                action_type: "share_gplus",
            		}

                ]
            },

            {
                id: 5,
                text: "Address card",
                desc: "Send a address card to the user",
                action_type: "address_card"
            },

        ];
```

## Next Steps

* Add filtering through keyboard
* Include scrollbar for long menus

 


