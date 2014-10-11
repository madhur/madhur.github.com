---
layout: blog-post
title: "An awesome conky configuration"
excerpt: "An awesome conky configuration"
disqus_id: /2014/10/10/awesomeconkyconfiguration/
location: New Delhi, India
time: 9:00 PM
tags:
- Linux
---


My simple but awesome conky configuration. Feel free to [fork my repo](https://github.com/madhur/awesome-conky) and use it yourself. Though it will require some work to setup.

###Screenshots
Click [here](https://raw.githubusercontent.com/madhur/awesome-conky/master/screenshots/conky.png) to see how it looks on a desktop when nicely arranged

<div style="float:left;width:100%">
<a href=https://raw.githubusercontent.com/madhur/awesome-conky/master/screenshots/conky-core.png><img alt=conky-core src=https://raw.githubusercontent.com/madhur/awesome-conky/master/screenshots/conky-core.png height=485 width=200 /></a><a href=https://raw.githubusercontent.com/madhur/awesome-conky/master/screenshots/conky-social.png><img alt=conky-social src=https://raw.githubusercontent.com/madhur/awesome-conky/master/screenshots/conky-social.png width=199 height=366 /></a><a href=https://raw.githubusercontent.com/madhur/awesome-conky/master/screenshots/conky-weather.png><img alt=conky-weather src=https://raw.githubusercontent.com/madhur/awesome-conky/master/screenshots/conky-weather.png width=141 height=135 /></a>
</div>
<div style="float:clear"></div>
<p/><p/><p/>
 


###Features
* Fetches Gmail using Atom feed 
* Fetches Facebook friend requests, notifications using [fbcmd](http://fbcmd.dtompkins.com/)
* Fetches Pocket unread items
* Fetches Stackoverflow overall reputation, week, month and day change
* Fetches twitter followers count
* Fetches github statistics


###Prerequisites
* Python 3 - `sudo apt-get install python3`
* [lm-sensors](http://www.lm-sensors.org/) for monitoring Core temperatures - `sudo apt-get install lm-sensors`


###Usage
1. All the files need to be dropped into `.conky` folder inside your home directory i.e. `~/.conky/`

2. Fonts should be installed to `/usr/share/fonts/` and then executing `sudo fc-cache -fv`

3. You need to rename the file `.password-sample.json` inside `scripts` folder to `.passwords.json` and provide the credentials, user ids, yahoo weather code and access tokens for various social networks. See [OAuth setup](#oauth) below

4. Install [fbcmd](http://fbcmd.dtompkins.com/) for facebook notifications

5. `conky_start.sh` is a main executable which fires up all the three conkies. You might want to put it in your startup of your X Window.

There are 3 conky configurations as follows:

* conky-core: Displays CPU/RAM/Disk metrics. Does not fetch anything from web except the WAN IP

* conky-social: Displays data from various social networks such as Facebook, Feedly, Github, Stackoverflow, Pocket etc.

* conky-weather: This is a fork of [https://github.com/mariusv/conky-google-now](https://github.com/mariusv/conky-google-now). Full credit to him. I just converted inline unreadable curl calls to python script and bit of UI hacks



###OAuth Setup<a name="oauth"></a>
Most of the social networks use OAuth as their authentication mechanism. You will need to setup your own OAuth access tokens for the conky to work and update it in `.password.json` file. Given below is each social network which this conky reads data from and its authentication mechanism.

* Gmail - Username / password
* Github - Username / password
* Facebook - Access via [fbcmd](http://fbcmd.dtompkins.com/)
* Stackoverflow - Uses unauthenticated API. No setup required except userid
* Twitter - Uses OAuth [Application only authentication](https://dev.twitter.com/oauth/application-only) 
* Pocket - OAuth. See [developer docs](http://getpocket.com/developer/)
* Feedly - OAuth token must be requested via email


###Fonts
It utilizes few fonts to render social icons. They are present in the fonts folder

* [Poky](https://github.com/madhur/awesome-conky/raw/master/fonts/Poky.ttf)
* [Zocial](https://github.com/madhur/awesome-conky/raw/master/fonts/zocial-regular-webfont.ttf)
* [Open Sans Light](https://github.com/madhur/awesome-conky/raw/master/fonts/OpenSans-Regular.ttf)


###Update Intervals
There are different intervals configured for each conky and individual social networks within conky configuration file. I am not describing it out here as I assume that user knows how to tweak conky configurations.


###Credits
I would like to thank following people for their awesome open source projects used in this conky:

* [fbcmd](http://fbcmd.dtompkins.com/)
* [https://github.com/mariusv/conky-google-now](https://github.com/mariusv/conky-google-now)
* [https://github.com/zgw21cn/FeedlyClient](https://github.com/zgw21cn/FeedlyClient)