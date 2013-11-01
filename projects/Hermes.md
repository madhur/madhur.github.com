---
title: Hermes
layout: project-detail
github: mapmylocation
---

<div style=";text-align:center">
<a  href="/images/projects/apphermes1.png" title="Hermes"><img  src='/images/projects/apphermes1.png' style="height:284px; width:160px" /></a>
<a  href="/images/projects/apphermes2.png" title="Hermes"><img  src='/images/projects/apphermes2.png' style="height:284px; width:160px" /></a>
<a  href="/images/projects/apphermes3.png" title="Hermes"><img  src='/images/projects/apphermes3.png' style="height:284px; width:160px" /></a>
<a  href="/images/projects/apphermes4.png" title="Hermes Facebook post"><img  src='/images/projects/apphermes4.png' style="height:284px; width:160px" /></a>
</div>  

<p></p>

##Hermes (a.k.a Map My Location)

Hermes is an attempt to provide a sense of security to all the travelers of all over the world and especially the women who use the public transport to commute to their work place and back home.

Hermes is an application that lets a commuter be tracked while on the road, posting the whereabouts at regular intervals on popular social network. The posts are secured and are visible to only those whom the commuter has provided permissions to view. It also enables your friends and family to know your whereabouts by sending you a SMS containing a secret code.

Hermes is available for free in the Google Play Store, there will never be a pro / paid version.

But if you find the app useful and want to support the development of it you can make a donation through [paypal](http://www.madhur.co.in/donate/)

## <a name="usage">Usage</a>

The application consists of two main features:
* Track Me
* Live Track

###TrackMe
Track Me enables your friends and family to locate you easily. They just need to send you a SMS containing a secret code ("hermes" by default). Upon receipt of this SMS, the application automatically sends a SMS reply to the sender containing the Google Maps link of your location.

### Live Track
LiveTrack enables you to automatically publish your location on Facebook at regular intervals tagged ONLY to your friends and families. You just need to connect to Facebook and specify which specific 
friends in your friend list will be able to see the posted location on your timeline.

## <a name="faq">FAQ</a>


### Why does it need so many permissions?

* **Read Contacts** - Need to get the Name of the person sending request for Track Me
* **Storage (modify/delete SD card contents)** - Needed to create logs and caching
* **Connect to Internet** - Required to make post to Facebook on your behalf
* **Read SMS** - Required to capture an SMS contaning Hermes secret code
* **Send SMS** - TrackMe automatically sends SMS reply to the sender with Google Maps location. Note: Your carrier standard outgoing SMS charge may apply.
* **Access fine location** - To capture your location
* **Access network state** - Used to determine if application can post to facebook through network connection.
* **Run at Startup** - Used to enable live track service after reboot
* **Prevent phone from sleeping** - Used to wakeup phone so that LiveTrack can make a post to social network.


### Why the application requires Facebook permissions?

Facebook permissions are required only in case you are using LiveTrack, since LiveTrack automatically publishes your location automatically at defined time inteval. Following permission is required:

* Post on your behalf

### The app posts my old/wrong location through TrackMe SMS

The application tries to retrieve your location from both GPS and cellular network and latest one is used. To ensure accurate location posting, the application will require either of following in order of preference. All of them might not be practically possible because of various reasosn such as battery constraints (GPS) or your current location (WiFi connected)

* Your GPS is turned on
* Your Mobile Data (2G/3G) is turned on
* Your Wifi is connected

If none of the above is true, the application will post your last available location.

### The application fails to post my location on facebook

If the application fails to post your location on facebook. Check the below conditions:

* Your mobile have working internet connection (2G/3G/WiFi)
* Your facebook account is connected in the application
* You have selected the friends option (either Everyone, Friends, Friends of Friends, Custom)

If the internet is not available at the specified time of the making a facebook post, the application will post the location as soon as the network becomes available.

### What is the ideal data/WIFI/GPS connection for this application

During my testing, the application works well with 2G connection, providing fairly accurate locations.
GPS can be turned on if precise location is preferred during LiveTrack

### I want to file a bug report, What should I do ?

Check [github issues](https://github.com/madhur/MapMyLocation/issues?state=open). Create a new issue and include the following details:

* Version of the Hermes used
* Version of Android/brand of phone used
