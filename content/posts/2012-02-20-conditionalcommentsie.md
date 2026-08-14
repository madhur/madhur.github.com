---
title: Conditional comments in Internet Explorer
date: '2012-02-20'
description: Conditional comments in Internet Explorer
tags:
  - IE
draft: false
categories:
  - Web Development
params:
  disqus_id: /2012/02/20/conditionalcommentsie/
  location: 'New Delhi, India'
  time: '9:00 PM'
---

Since IE5, Internet Explorer supports something called [Conditional Comments](http://en.wikipedia.org/wiki/Conditional_comment)

Conditional comments can be used to provide and hide code to and from Internet Explorer. For example, I can find the version of Internet Explorer you are running as follows:

<div class="notice">
<!--[if IE]>
According to the conditional comment this is IE<br />
<![endif]-->
<!--[if IE 6]>
According to the conditional comment this is IE 6<br />
<![endif]-->
<!--[if IE 7]>
According to the conditional comment this is IE 7<br />
<![endif]-->
<!--[if IE 8]>
According to the conditional comment this is IE 8<br />
<![endif]-->
<!--[if IE 9]>
According to the conditional comment this is IE 9<br />
<![endif]-->
<!--[if gte IE 8]>
According to the conditional comment this is IE 8 or higher<br />
<![endif]-->
<!--[if lt IE 9]>
According to the conditional comment this is IE lower than 9<br />
<![endif]-->
<!--[if lte IE 7]>
According to the conditional comment this is IE lower or equal to 7<br />
<![endif]-->
<!--[if gt IE 6]>
According to the conditional comment this is IE greater than 6<br />
<![endif]-->
<!--[if !IE]> -->
According to the conditional comment this is not IE<br />
<!-- <![endif]-->
</div>



The snippet below is used to show this:

```text
<!--[if IE]>
According to the conditional comment this is IE<br />
<![endif]-->
<!--[if IE 6]>
According to the conditional comment this is IE 6<br />
<![endif]-->
<!--[if IE 7]>
According to the conditional comment this is IE 7<br />
<![endif]-->
<!--[if IE 8]>
According to the conditional comment this is IE 8<br />
<![endif]-->
<!--[if IE 9]>
According to the conditional comment this is IE 9<br />
<![endif]-->
<!--[if gte IE 8]>
According to the conditional comment this is IE 8 or higher<br />
<![endif]-->
<!--[if lt IE 9]>
According to the conditional comment this is IE lower than 9<br />
<![endif]-->
<!--[if lte IE 7]>
According to the conditional comment this is IE lower or equal to 7<br />
<![endif]-->
<!--[if gt IE 6]>
According to the conditional comment this is IE greater than 6<br />
<![endif]-->
<!--[if !IE]> -->
According to the conditional comment this is not IE<br />
<!-- <![endif]-->
```

Also, checkout conditional comments on [MSDN](http://msdn.microsoft.com/en-us/library/ms537512.aspx)
