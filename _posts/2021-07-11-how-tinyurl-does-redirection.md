---
layout: blog-post
title: "How tinyUrl Does redirection"
excerpt: "How tinyUrl Does redirection"
disqus_id: /2021/07/11/how-tinyurl-does-redirection/
tags:
    - Design    
---

I got curious about how tinyUrl does redirection for its Url. Is it standard browser redirect with 301/302 status code or something else?

With that created this tinyUrl [tinyurl.com/madhur25](https://tinyurl.com/madhur25)

Figured out that it was indeed a browser redirect using 301 status code.

```
$ curl https://tinyurl.com/madhur25 -vvv
* STATE: INIT => CONNECT handle 0x600057310; line 1407 (connection #-5000)
* Added connection 0. The cache now contains 1 members
*   Trying 104.20.138.65...
* TCP_NODELAY set
* STATE: CONNECT => WAITCONNECT handle 0x600057310; line 1460 (connection #0)
* Connected to tinyurl.com (104.20.138.65) port 443 (#0)
* STATE: WAITCONNECT => SENDPROTOCONNECT handle 0x600057310; line 1567 (connection #0)
* Marked for [keep alive]: HTTP default
* ALPN, offering http/1.1
* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
* successfully set certificate verify locations:
*   CAfile: /usr/ssl/certs/ca-bundle.crt
  CApath: none
* TLSv1.2 (OUT), TLS header, Certificate Status (22):
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* STATE: SENDPROTOCONNECT => PROTOCONNECT handle 0x600057310; line 1581 (connection #0)
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS change cipher, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-ECDSA-AES128-GCM-SHA256
* ALPN, server accepted to use http/1.1
* Server certificate:
*  subject: C=US; ST=California; L=San Francisco; O=Cloudflare, Inc.; CN=sni.cloudflaressl.com
*  start date: Jul  3 00:00:00 2021 GMT
*  expire date: Jul  2 23:59:59 2022 GMT
*  subjectAltName: host "tinyurl.com" matched cert's "tinyurl.com"
*  issuer: C=US; O=Cloudflare, Inc.; CN=Cloudflare Inc ECC CA-3
*  SSL certificate verify ok.
* STATE: PROTOCONNECT => DO handle 0x600057310; line 1602 (connection #0)
> GET /madhur25 HTTP/1.1
> Host: tinyurl.com
> User-Agent: curl/7.51.0
> Accept: */*
>
* STATE: DO => DO_DONE handle 0x600057310; line 1664 (connection #0)
* STATE: DO_DONE => WAITPERFORM handle 0x600057310; line 1791 (connection #0)
* STATE: WAITPERFORM => PERFORM handle 0x600057310; line 1801 (connection #0)
* HTTP 1.1 or later with persistent connection, pipelining supported
< HTTP/1.1 301 Moved Permanently
< Date: Sun, 11 Jul 2021 04:11:01 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< X-Powered-By: PHP/7.3.28
< Location: https://www.madhur.co.in/
< Cache-Control: max-age=0, public, s-max-age=900, stale-if-error: 86400
< Referrer-Policy: unsafe-url
< Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
< CF-Cache-Status: DYNAMIC
< Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
* Server cloudflare is not blacklisted
< Server: cloudflare
< CF-RAY: 66cf2f6e7e293c13-BLR
< alt-svc: h3-27=":443"; ma=86400, h3-28=":443"; ma=86400, h3-29=":443"; ma=86400, h3=":443"; ma=86400
<
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="refresh" content="0;url='https://www.madhur.co.in/'" />

        <title>Redirecting to https://www.madhur.co.in/</title>
    </head>
    <body>
        Redirecting to <a href="https://www.madhur.co.in/">https://www.madhur.co.in/</a>.
    </body>
* STATE: PERFORM => DONE handle 0x600057310; line 1965 (connection #0)
* multi_done
* Curl_http_done: called premature == 0
* Connection #0 to host tinyurl.com left intact
</html>
```