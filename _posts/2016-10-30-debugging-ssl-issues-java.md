---
layout: blog-post
title: "Debugging SSL Issues in Java"
excerpt: "Debugging SSL Issues in Java"
disqus_id: /2016/10/30/debugging-ssl-issues-java/
tags:
- Java
- SSL
---


Recently we faced an issue, where all are calls to a third party vendor were failing with following stack trace in Java


{% highlight text %}
javax.net.ssl.SSLHandshakeException: Received fatal alert: handshake_failure 
at sun.security.ssl.Alerts.getSSLException(Alerts.java:192) 
at sun.security.ssl.Alerts.getSSLException(Alerts.java:154) 
at sun.security.ssl.SSLSocketImpl.recvAlert(SSLSocketImpl.java:1979) 
at sun.security.ssl.SSLSocketImpl.readRecord(SSLSocketImpl.java:1086) 
at sun.security.ssl.SSLSocketImpl.performInitialHandshake(SSLSocketImpl.java:1332) 
at sun.security.ssl.SSLSocketImpl.startHandshake(SSLSocketImpl.java:1359) 
at sun.security.ssl.SSLSocketImpl.startHandshake(SSLSocketImpl.java:1343) 
at org.apache.http.conn.ssl.SSLConnectionSocketFactory.createLayeredSocket(SSLConnectionSocketFactory.java:394) 
at org.apache.http.conn.ssl.SSLConnectionSocketFactory.connectSocket(SSLConnectionSocketFactory.java:353) 
at org.apache.http.impl.conn.DefaultHttpClientConnectionOperator.connect(DefaultHttpClientConnectionOperator.java:141) 
at org.apache.http.impl.conn.PoolingHttpClientConnectionManager.connect(PoolingHttpClientConnectionManager.java:353) 
at org.apache.http.impl.execchain.MainClientExec.establishRoute(MainClientExec.java:380) 
at org.apache.http.impl.execchain.MainClientExec.execute(MainClientExec.java:236) 
at org.apache.http.impl.execchain.ProtocolExec.execute(ProtocolExec.java:184) 
at org.apache.http.impl.execchain.RetryExec.execute(RetryExec.java:88) 
at org.apache.http.impl.execchain.RedirectExec.execute(RedirectExec.java:110) 
at org.apache.http.impl.client.InternalHttpClient.doExecute(InternalHttpClient.java:184) 
at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:82) 
at org.apache.http.impl.client.CloseableHttpClient.execute(CloseableHttpClient.java:107) 
at HttpURLConnectionExample.sendGet1(HttpURLConnectionExample.java:83) 
at HttpURLConnectionExample.main(HttpURLConnectionExample.java:48) 
at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method) 
at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:57) 
at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) 
at java.lang.reflect.Method.invoke(Method.java:606) 
at com.intellij.rt.execution.application.AppMain.main(AppMain.java:144) [Raw read]: length = 5 
{% endhighlight %}

As per the vendor, there was no issue with their site. Other partners were able to call their API's successfully.

This is one of the peculiar problem which happens with Java 7, due to the mismatch of ciphers between Java 7 and the destination webserver.

In order to debug this in Java, we need to add the parameter `-Djavax.net.debug=all` to the command line. Through this command line, we get full debug output such as follows:

{% highlight text %}
main, READ: TLSv1.2 Handshake, length = 333
*** ECDH ServerKeyExchange
Signature Algorithm SHA512withRSA
Server key: Sun EC public key, 256 bits
  public x coord: 52151221190485581151214316798815876713912665823307283797594930350231973293152
  public y coord: 5451449004300784798879937097030816531206591013653597175688384253361719134656
  parameters: secp256r1 [NIST P-256, X9.62 prime256v1] (1.2.840.10045.3.1.7)
[read] MD5 and SHA1 hashes:  len = 333
...
[Raw read]: length = 5
0000: 16 03 03 00 04                                     .....
[Raw read]: length = 4
0000: 0E 00 00 00                                        ....
main, READ: TLSv1.2 Handshake, length = 4
*** ServerHelloDone
[read] MD5 and SHA1 hashes:  len = 4
0000: 0E 00 00 00                                        ....
*** ECDHClientKeyExchange
ECDH Public value:  { 4, 247, 183, 127, 41, 28, 143, 49, 205, 39, 146, 57, 240, 102, 0, 53, 90, 244, 137, 176, 75, 192, 158, 138, 198, 115, 11, 101, 50, 2, 228, 254, 236, 211, 211, 208, 159, 105, 156, 135, 78, 234, 56, 97, 34, 209, 81, 216, 147, 185, 181, 67, 73, 84, 198, 4, 105, 61, 170, 131, 230, 115, 58, 207, 46 }
[write] MD5 and SHA1 hashes:  len = 70
0000: 10 00 00 42 41 04 F7 B7   7F 29 1C 8F 31 CD 27 92  ...BA....)..1.'.
0010: 39 F0 66 00 35 5A F4 89   B0 4B C0 9E 8A C6 73 0B  9.f.5Z...K....s.
0020: 65 32 02 E4 FE EC D3 D3   D0 9F 69 9C 87 4E EA 38  e2........i..N.8
0030: 61 22 D1 51 D8 93 B9 B5   43 49 54 C6 04 69 3D AA  a".Q....CIT..i=.
0040: 83 E6 73 3A CF 2E                                  ..s:..
main, WRITE: TLSv1.2 Handshake, length = 70
[Raw write]: length = 75
...
... no IV derived for this protocol
main, WRITE: TLSv1.2 Change Cipher Spec, length = 1
[Raw write]: length = 6
0000: 14 03 03 00 01 01                                  ......
*** Finished
verify_data:  { 162, 89, 141, 227, 142, 139, 54, 27, 241, 56, 38, 145 }
***
[write] MD5 and SHA1 hashes:  len = 16
0000: 14 00 00 0C A2 59 8D E3   8E 8B 36 1B F1 38 26 91  .....Y....6..8&.
Padded plaintext before ENCRYPTION:  len = 64
0000: FD AD 67 A2 4D 09 37 F3   4F 7B 53 C5 D9 41 CA 17  ..g.M.7.O.S..A..
0010: 14 00 00 0C A2 59 8D E3   8E 8B 36 1B F1 38 26 91  .....Y....6..8&.
0020: BF 2D 9D 66 AA EB 4C E6   4F 35 51 A2 F7 00 40 77  .-.f..L.O5Q...@w
0030: 2A EA 37 3E 0B 0B 0B 0B   0B 0B 0B 0B 0B 0B 0B 0B  *.7>............
main, WRITE: TLSv1.2 Handshake, length = 64
[Raw write]: length = 69
0000: 16 03 03 00 40 D3 7C 46   86 EE 71 97 63 10 93 8B  ....@..F..q.c...
0010: 16 28 84 D4 72 CB 29 CA   65 FB 08 6E 5F C7 F2 83  .(..r.).e..n_...
0020: A7 45 5D 93 86 5B ED D7   AF A4 18 3A 6E AF 46 88  .E]..[.....:n.F.
0030: 83 0C 09 CC 01 5B BF 8D   AB FD D9 6B 8C D1 E6 A6  .....[.....k....
0040: AD 10 69 1D 81                                     ..i..
[Raw read]: length = 5
0000: 14 03 03 00 01                                     .....
[Raw read]: length = 1
0000: 01                                                 .
main, READ: TLSv1.2 Change Cipher Spec, length = 1
[Raw read]: length = 5
0000: 16 03 03 00 40                                     ....@
[Raw read]: length = 64
0000: 6C 21 89 CD 5E FF 76 BD   95 43 51 F1 E6 58 64 5C  l!..^.v..CQ..Xd\
0010: 97 6D DB 98 3F 1C 25 3D   39 DF C6 D3 8C E1 E2 64  .m..?.%=9......d
0020: 18 BD 91 8A 7F B2 8E 78   82 F7 68 B2 3A 77 08 BE  .......x..h.:w..
0030: B8 2C 94 2D 06 EE 7B CB   40 86 FA 1A B1 9C 06 3F  .,.-....@......?
main, READ: TLSv1.2 Handshake, length = 64
Padded plaintext after DECRYPTION:  len = 64
0000: 15 A8 6B 92 28 EB 61 3B   2A A0 BA 2F 0E D4 6D F5  ..k.(.a;*../..m.
0010: 14 00 00 0C 17 9E 44 19   42 D2 7F 29 74 7F 66 A8  ......D.B..)t.f.
0020: 36 A5 B7 2A 7B A7 D5 B6   DE F2 53 2B 15 E3 CA 5E  6..*......S+...^
0030: 1A 3F 1D D5 0B 0B 0B 0B   0B 0B 0B 0B 0B 0B 0B 0B  .?..............
*** Finished
verify_data:  { 23, 158, 68, 25, 66, 210, 127, 41, 116, 127, 102, 168 }
***
%% Cached client session: [Session-1, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA]
[read] MD5 and SHA1 hashes:  len = 16
0000: 14 00 00 0C 17 9E 44 19   42 D2 7F 29 74 7F 66 A8  ......D.B..)t.f.
{% endhighlight %}

Unless you really know SSL protocol in detail, you won't understand all of it. But atleast I am able to figure out the following:

* The protocol in use is TLSv1.2
* Cipher used was TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
* The handshake was successfully completed

Some of the secure webservers, will only support TLS v1.2 protocol and deny any request on SSLv3 or TSL v1 protocol.

If that is the case, this is easy to fix in Java by adding following command line parameters

`JAVACMD="$JAVACMD -Ddeployment.security.SSLv2Hello=false -Ddeployment.security.SSLv3=false -Ddeployment.security.TLSv1=false -D\
deployment.security.TLSv1.1=true -Ddeployment.security.TLSv1.2=true"`

or even this

`-Dhttps.protocols=TLSv1.1,TLSv1.2`

However, some of the webservers can force the clients to use very strong ciphers which are not available in Java 7. They are only available in Java 8.

The list of ciphers supported by SSL site can be found through 
[https://www.ssllabs.com/index.html](https://www.ssllabs.com/index.html)

In that case, You can download the JCE Unlimited Strength Jurisdiction Policy files for Java 7 from http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html and replace the two JARs (`local_policy.jar, US_export_policy.jar`) under your JRE's `lib/security` directory with the ones from the downloaded package. This will add additional (stronger) ciphersuites and you should be able to connect without having to make any changes to your code or enable TLSv1.2.

For reference, here are the ciphersuites available in Java 7 (1.7.0_79):

{% highlight text %}
  SSL_DH_anon_WITH_3DES_EDE_CBC_SHA
        SSL_DH_anon_WITH_DES_CBC_SHA
        SSL_DH_anon_WITH_RC4_128_MD5
        SSL_RSA_EXPORT_WITH_DES40_CBC_SHA
        SSL_RSA_EXPORT_WITH_RC4_40_MD5
*       SSL_RSA_WITH_3DES_EDE_CBC_SHA
        SSL_RSA_WITH_DES_CBC_SHA
        SSL_RSA_WITH_NULL_MD5
        SSL_RSA_WITH_NULL_SHA
*       SSL_RSA_WITH_RC4_128_MD5
*       SSL_RSA_WITH_RC4_128_SHA
*       TLS_DHE_DSS_WITH_AES_128_CBC_SHA
*       TLS_DHE_DSS_WITH_AES_128_CBC_SHA256
*       TLS_DHE_RSA_WITH_AES_128_CBC_SHA
*       TLS_DHE_RSA_WITH_AES_128_CBC_SHA256
        TLS_DH_anon_WITH_AES_128_CBC_SHA
        TLS_DH_anon_WITH_AES_128_CBC_SHA256
*       TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
*       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
        TLS_ECDHE_ECDSA_WITH_NULL_SHA
*       TLS_ECDHE_ECDSA_WITH_RC4_128_SHA
*       TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
*       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
        TLS_ECDHE_RSA_WITH_NULL_SHA
*       TLS_ECDHE_RSA_WITH_RC4_128_SHA
*       TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA
*       TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256
        TLS_ECDH_ECDSA_WITH_NULL_SHA
*       TLS_ECDH_ECDSA_WITH_RC4_128_SHA
*       TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDH_RSA_WITH_AES_128_CBC_SHA
*       TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256
        TLS_ECDH_RSA_WITH_NULL_SHA
*       TLS_ECDH_RSA_WITH_RC4_128_SHA
        TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA
        TLS_ECDH_anon_WITH_AES_128_CBC_SHA
        TLS_ECDH_anon_WITH_NULL_SHA
        TLS_ECDH_anon_WITH_RC4_128_SHA
*       TLS_EMPTY_RENEGOTIATION_INFO_SCSV
        TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5
        TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA
        TLS_KRB5_EXPORT_WITH_RC4_40_MD5
        TLS_KRB5_EXPORT_WITH_RC4_40_SHA
        TLS_KRB5_WITH_3DES_EDE_CBC_MD5
        TLS_KRB5_WITH_3DES_EDE_CBC_SHA
        TLS_KRB5_WITH_DES_CBC_MD5
        TLS_KRB5_WITH_DES_CBC_SHA
        TLS_KRB5_WITH_RC4_128_MD5
        TLS_KRB5_WITH_RC4_128_SHA
*       TLS_RSA_WITH_AES_128_CBC_SHA
*       TLS_RSA_WITH_AES_128_CBC_SHA256
        TLS_RSA_WITH_NULL_SHA256
{% endhighlight %}

and here are the ones after using the Unlimited Stringth Jurisdiction policy files:

{% highlight text %}
        SSL_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA
*       SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA
        SSL_DHE_DSS_WITH_DES_CBC_SHA
        SSL_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA
*       SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA
        SSL_DHE_RSA_WITH_DES_CBC_SHA
        SSL_DH_anon_EXPORT_WITH_DES40_CBC_SHA
        SSL_DH_anon_EXPORT_WITH_RC4_40_MD5
        SSL_DH_anon_WITH_3DES_EDE_CBC_SHA
        SSL_DH_anon_WITH_DES_CBC_SHA
        SSL_DH_anon_WITH_RC4_128_MD5
        SSL_RSA_EXPORT_WITH_DES40_CBC_SHA
        SSL_RSA_EXPORT_WITH_RC4_40_MD5
*       SSL_RSA_WITH_3DES_EDE_CBC_SHA
        SSL_RSA_WITH_DES_CBC_SHA
        SSL_RSA_WITH_NULL_MD5
        SSL_RSA_WITH_NULL_SHA
*       SSL_RSA_WITH_RC4_128_MD5
*       SSL_RSA_WITH_RC4_128_SHA
*       TLS_DHE_DSS_WITH_AES_128_CBC_SHA
*       TLS_DHE_DSS_WITH_AES_128_CBC_SHA256
*       TLS_DHE_DSS_WITH_AES_256_CBC_SHA
*       TLS_DHE_DSS_WITH_AES_256_CBC_SHA256
*       TLS_DHE_RSA_WITH_AES_128_CBC_SHA
*       TLS_DHE_RSA_WITH_AES_128_CBC_SHA256
*       TLS_DHE_RSA_WITH_AES_256_CBC_SHA
*       TLS_DHE_RSA_WITH_AES_256_CBC_SHA256
        TLS_DH_anon_WITH_AES_128_CBC_SHA
        TLS_DH_anon_WITH_AES_128_CBC_SHA256
        TLS_DH_anon_WITH_AES_256_CBC_SHA
        TLS_DH_anon_WITH_AES_256_CBC_SHA256
*       TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
*       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
*       TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
*       TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384
        TLS_ECDHE_ECDSA_WITH_NULL_SHA
*       TLS_ECDHE_ECDSA_WITH_RC4_128_SHA
*       TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
*       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
*       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
*       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
        TLS_ECDHE_RSA_WITH_NULL_SHA
*       TLS_ECDHE_RSA_WITH_RC4_128_SHA
*       TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA
*       TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256
*       TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA
*       TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384
        TLS_ECDH_ECDSA_WITH_NULL_SHA
*       TLS_ECDH_ECDSA_WITH_RC4_128_SHA
*       TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA
*       TLS_ECDH_RSA_WITH_AES_128_CBC_SHA
*       TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256
*       TLS_ECDH_RSA_WITH_AES_256_CBC_SHA
*       TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384
        TLS_ECDH_RSA_WITH_NULL_SHA
*       TLS_ECDH_RSA_WITH_RC4_128_SHA
        TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA
        TLS_ECDH_anon_WITH_AES_128_CBC_SHA
        TLS_ECDH_anon_WITH_AES_256_CBC_SHA
        TLS_ECDH_anon_WITH_NULL_SHA
        TLS_ECDH_anon_WITH_RC4_128_SHA
*       TLS_EMPTY_RENEGOTIATION_INFO_SCSV
        TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5
        TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA
        TLS_KRB5_EXPORT_WITH_RC4_40_MD5
        TLS_KRB5_EXPORT_WITH_RC4_40_SHA
        TLS_KRB5_WITH_3DES_EDE_CBC_MD5
        TLS_KRB5_WITH_3DES_EDE_CBC_SHA
        TLS_KRB5_WITH_DES_CBC_MD5
        TLS_KRB5_WITH_DES_CBC_SHA
        TLS_KRB5_WITH_RC4_128_MD5
        TLS_KRB5_WITH_RC4_128_SHA
*       TLS_RSA_WITH_AES_128_CBC_SHA
*       TLS_RSA_WITH_AES_128_CBC_SHA256
*       TLS_RSA_WITH_AES_256_CBC_SHA
*       TLS_RSA_WITH_AES_256_CBC_SHA256
        TLS_RSA_WITH_NULL_SHA256
{% endhighlight %}

Hope that helps anyone running into SSL issues with Java.




