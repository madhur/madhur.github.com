---
slug: "using-ns-image"
title: NSImage Caching
date: '2016-01-25'
description: NSImage Caching
tags:
  - OSX
  - Swift
  - Cocoa
draft: false
params:
  disqus_id: /2016/01/25/using-ns-image/
  location: 'Bangalore, India'
  time: '9:00 PM'
---


Recently, I encountered an issue where an `NSImage` instance was cached inspite of setting `NSImageCacheMode.Never`

Specifically, the issue was:  
I have bunch of images in my assets. What I am trying to do is render the image in status bar of OSX as following:

```swift
let icon = NSImage(named: "statusIcon")
icon?.size = NSSize.init(width: 18, height: 18)

icon?.template = true
statusItem.image = icon
statusItem.menu = statusMenu
```

and also using it in one of my view which opens:

```swift
self.dayIcon.image = NSImage(named: "statusIcon")
```

The problem is as soon as I set the status bar image, the image in the view also changes, i.e. both the color and the size(changes to 18x18)

I have tried using `icon?.cacheMode = NSImageCacheMode.Never` but there is no effect.

### Solution

`[NSImage imageNamed:]` may return an existing cached instance of the image.

They are not, and that is, indeed, your problem.

If you want to change the size on the image without affecting anyone else who may be holding a reference, make a copy of it. The copy of the NSImage is lightweight - it doesn't duplicate the underlying image representations which hold the rendering (bitmap, in the PNG case) data.

This is the correct code:

```swift
let icon = NSImage(named: "statusIcon").copy() as! NSImage
icon.size = NSSize.init(width: 18, height: 18)

icon.template = true
statusItem.image = icon
statusItem.menu = statusMenu
```


