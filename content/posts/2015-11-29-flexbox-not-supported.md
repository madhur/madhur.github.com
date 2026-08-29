---
slug: "flexbox-not-supported"
title: Flexbox is not supported Android 4.3 and below
date: '2015-11-29'
year: '2015'
month: '2015-11'
description: Flexbox is not supported Android 4.3 and below
tags:
  - Android
  - WebView
  - ionic
draft: false
params:
  disqus_id: /2015/11/29/flexbox-not-supported/
  location: 'Bangalore, India'
  time: '9:00 PM'
---

One of our webview pages had a strange issue in production. We are using an angular component [angularjs-slider](https://github.com/rzajac/angularjs-slider) on one of our pages. On some of the devices, the width of this component was way lesser than we had defined in our code (around 90% of the width of page)

More analysis revealed that the issue occurred on only pre-kitkat devices. The strange thing was that we were using other controls like normal `input` and `label` but they were not affected. We tried every CSS tweak to solve this issue but no avail.

And then, I stumbled upon this [issue](https://github.com/driftyco/ionic/issues/998). Turned out that this issue was because of ionic framework. [Ionic framework](http://ionicframework.com/) by default uses [Flexible Box Layout Module](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Using_CSS_flexible_boxes) called as `flex` in short. As per [this](http://caniuse.com/#feat=flexbox) `flex` is only supported on Android 4.4 and above.

### Solution

The solution was just a one line change where we override the `display` property to `block` instead of `flex`

```html
<div class="item range range-item">
	 <rzslider  rz-slider-model="data.experience" rz-slider-floor="0"   rz-slider-text=" years" rz-slider-min-lable="<1 year" rz-slider-max-lable="10+ years" rz-exp-silder-id="expSlider" rz-slider-ceil="11" ></rzslider>
</div>
```

changed to 

```html
<div class="item range range-item" style="display:block">
	 <rzslider  rz-slider-model="data.experience" rz-slider-floor="0"   rz-slider-text=" years" rz-slider-min-lable="<1 year" rz-slider-max-lable="10+ years" rz-exp-silder-id="expSlider" rz-slider-ceil="11" ></rzslider>
</div>
```

