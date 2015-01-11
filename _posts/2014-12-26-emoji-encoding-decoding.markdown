---
layout: blog-post
title: "Encoding and Decoding Emoji for Cross platform"
excerpt: "Encoding and decoding Emoji for Cross platform"
disqus_id: /2014/12/26/emoji-encoding-decoding/
location: New Delhi, India
time: 9:00 PM
tags:
- AngularJs
- Emoji
---

Recently, I have been working on an Android app which communicates with a web platform. One of the challenges we have been faced with is cross platform emoji solution. There are just too many emoji standards out there. There is no standard as of now although Google have come together to formalize [Emoji Symbols](http://www.unicode.org/~scherer/emoji4unicode/snapshot/full.html)

GitHub introduced [emoji pngs](https://github.com/blog/816-emoji) and here you see that in action :smile: throughout their application. Campfire [supports emoji](https://signalvnoise.com/posts/3059-2011-year-end-campfire-feature-blowout). Both GitHub, Campfire, and others support a simple set of codes to inject these pngs into an html page. [http://www.emoji-cheat-sheet.com/](http://www.emoji-cheat-sheet.com/) has emerged to guide users and has almost formalized how these codes should work.

Most of the above techniques can be categorized into three basic categories:

* **Colon:** The emojis are converted to their colon style strings. This is simple to save in the database since its just a string.
See the examples: [http://www.emoji-cheat-sheet.com/](http://www.emoji-cheat-sheet.com/). [Web interface of telegram](https://web.telegram.org/#/im) uses this technique of rendering and storing emoji. [Github flavored markdown](https://help.github.com/articles/writing-on-github/) also uses this.

* **UTF-8 Characters:** Emojis are mapped to their Unicode characters.  The advatage of this method is that some platforms (such as Android, iOS) can render them automatically as emoji unlike colon style encoding which almost always require decoding. On the disadvantage, Saving them in databases require special handling. See [note below](#db).
A comprehensive list of unicode codes can be obtained from [http://apps.timwhitlock.info/emoji/tables/unicode](http://apps.timwhitlock.info/emoji/tables/unicode)

* **HTML:** Emojis are converted to HTML `<img>` tags rendering each emoji as an image either from the single image or a sprite. 
This is the least useful method to adopt as its not cross platform. There is no standardization of Emoji sprite images and hence you will never be sure that target platform has the same emoji images. Though, this solution works perfect for a single isolated website.

##Our Solution - [Github Repo](https://github.com/madhur/angular-emoji-popup) and [demo page](http://coraza.github.io/angular-emoji-popup)

Since we are using AngularJs as our frontend, We have come up with an AngularJs directive and set of filters to handle all of above cases for Emoji. The solution supports encoding and decoding emoji from various formats. For us, We decided to go with storing Emoji as UTF-8 characters for the simple reason that Android can render them natively and hence, no special effort is required to implement this on Android side. Though, it did require tweaking our MySql tables and database to switch from `utf8` to `utf8mb4`. I will not go into the details of their differences.

I also realize that this might be a far from perfect solution especially when we plan to introduce support more devices such as iOS and Windows Phone. But, this works for us perfectly and I believe changing it in future will not be difficult.

Feel free to check out tis project, fork and send me pull requests for any issues or enhancements.

This solution utilizes snippets and ideas from following awesome open source projects:

* [emoji-cheat-sheet](https://github.com/arvida/emoji-cheat-sheet.com) - Complete reference for emoji in colon style
* [jquery-emojiarea](https://github.com/diy/jquery-emojiarea) - We wrapped this awesome Jquery plugin in angular directive
* [nanoScrollerJS](https://github.com/jamesflorentino/nanoScrollerJS) - The above jquery plugin utilzes nanoScroller as its scrollbar
* [js-emoji](https://github.com/iamcal/js-emoji)

<a name="db"></a>
## Using MySQL for storage
The following text is taken verbatim from [https://github.com/iamcal/js-emoji](https://github.com/iamcal/js-emoji)

> Some special care may be needed to store emoji in your database. While some characters (e.g. Cloud, U+2601) are
> within the Basic Multilingual Plane (BMP), others (e.g. Close Umbrella, U+1F302) are not. As such, 
> they require 4 bytes of storage to encode each character. Inside MySQL, this requires switching from `utf8` 
> storage to `utf8mb4`.

> You can modify a database and table using a statement like:

>  `ALTER DATABASE my_database DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;`
>  `ALTER TABLE my_table CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;`

> You will also need to modify your connection character set.

> You don't need to worry about this if you translate to colon syntax before storage.