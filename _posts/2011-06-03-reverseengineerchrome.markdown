---
layout: blog-post
title: "Reverse engineering Google chrome extensions"
excerpt: How to reverse engineer Google Chrome extensions
disqus_id: /2011/06/03/reverse engineer/
location: Pittsburgh, US
time: 12:18 AM
tags:
- Reverse Engineering
- Chrome
---


Google chrome extensions are basically zip files with .crx extension. As mentioned in this [post](http://www.google.com/support/forum/p/Chrome/thread?tid=7ead9bcf1528fbe3&hl=en) by Google, the chrome extensions can be opened by simply zip programs such as 7zip or Winzip.

This is easy when you have direct access to the .crx file. However, most of the Google chrome extensions on its website do not have the link to the .crx file exposed.
There are some wierd ways to grab the CRX file as mentioned [here](http://www.google.com/support/forum/p/Chrome/thread?tid=76ac2782e7f28bd4&hl=en), however this might or might not work.

<div class="notice">
First Method 
</div>

Google actualy stores all the CRX files in a secure location which is accessed through SSL connection by a javascript function located on the Install button. If we do an inspect element over the Install button, we can see a call to the function 

{% highlight javascript %}
onclick="cxBuyFlow.installItem ('emailaddress');
{% endhighlight %}

This javascript function makes a remote call to download the CRX file over the HTTP SSL connection. As see in this [image](/images/Blog/devtool.png)

<img src='/images/Blog/devtool.png' height='364px' width='1436px' />

From the dev tools itself, we can see the location of CRX file, which is given as:

**https://clients2.googleusercontent.com/crx/download/OQAAABjsL_XrywSJJgbO4iAqQN_92ggziQyqudDAep70GniUAqlNUxYhj289n5H0ljizk9d6MeMuV59czHo6y6dk_YAAxlKa5dxpPBSCnNDQ5ZAz5TwR5AAeY5yy/extension_1_6.crx**

To simple download this file, we can use wget as

{% highlight bash %}
wget https://clients2.googleusercontent.com/crx/download/OQAAABjsL_XrywSJJgbO4iAqQN_92ggziQyqudDAep70GniUAqlNUxYhj289n5H0ljizk9d6MeMuV59czHo6y6dk_YAAxlKa5dxpPBSCnNDQ5ZAz5TwR5AAeY5yy/extension_1_6.crx
{% endhighlight %}

<div class="notice">
Update: There is second method as well. See below. Credit goes to http://blog.gerardin.info/archives/763
</div>

1. Find the ID of the extension you're interested in. When on the details page of the extension, it will be something like "bfbmjmiodbnnpllbbbfblcplfjjepjdn" after "https://chrome.google.com/extensions/detail/" in the page URL
2. Paste this URL into your browser: "https://clients2.google.com/service/update2/crx?response=redirect&x=id%3D____%26uc" replacing ____ with the extension ID.
3. You'll be prompted to save a CRX file. Drag this file to a Chrome window and proceed with installation