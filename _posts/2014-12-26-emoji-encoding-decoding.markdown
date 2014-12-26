---
layout: blog-post
title: "Emoji Encoding and Decoding"
excerpt: "Emoji Encoding and decoding"
disqus_id: /2014/12/26/emoji-encoding-decoding/
location: New Delhi, India
time: 9:00 PM
tags:
- AngularJs
- Emoji
---


###Note about encoding and decoding
There are various standards to encode and decode emojis. Most popular are:

* **Colon:** The emojis are converted to their colon style strings. This is simple to save in the database since its just a string.
See the mapping at [http://www.emoji-cheat-sheet.com/](http://www.emoji-cheat-sheet.com/)

* **UTF-8 Characters:** Emojis are mapped to their Unicode characters.  The advatage of this method is that some platforms (such as Android, iOS) can render them automatically as emoji unlike colon style encoding which almost always require decoding. On the disadvantage, Saving them in databases require special handling. See [note below](#db)

A comprehensive list of unicode codes can be obtained from [http://apps.timwhitlock.info/emoji/tables/unicode](http://apps.timwhitlock.info/emoji/tables/unicode)

* **HTML:** Emojis are converted to HTML `<img>` tags rendering each emoji as an image either from the single image or a sprite. 
This is the least useful method to adopt as its not cross platform. There is no standardization of Emoji sprite images and hence you will never be sure that target platform has the same emoji images.

## Using MySQL for storage
<a name="db"></a>
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