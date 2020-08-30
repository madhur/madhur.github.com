---
layout: blog-post
title: "Debugging SSL Issues"
excerpt: "Debugging SSL Issues"
disqus_id: /2020/08/21/debugging-ssl-issues/
tags:
    - Java
    - SSL
---

I wrote this article [Debugging SSL Issues in Java]({% post_url
2016-10-30-debugging-ssl-issues-java %}) almost 4 years ago. I am writing again
a new post on the same topic because I faced the same issue and that article
didn't help me. So I'll list my new learnings in this post and it will be to the
point.

### Use -Djavax.net.debug=all to command line

When using Java program, you can add `-Djavax.net.debug=all` to the command line to produce debug output of the complete handshake of SSL.

In short, this is how the handshake looks like

```
Client                          Server

ClientHello         ---->   
                                ServerHello
                                Certificate*
                                ServerKeyExchange*
                                CertificateRequest*
                                ServerHelloDone
                    <---- 
Certificate*
ClientKeyExchange
CertificateVerify*
[ChangeCipherSpec]
Finished
                    ---->
                                [ChangeCipherSpec]
                                Finished
                    <-----

Application Data    <----->     Application Data
```
In our case, server abruptly stopped responding after client sent `[ChangeCipherSpec]` message.


## SSLDump

[SSLDump](https://linux.die.net/man/1/ssldump) is another utility which can show decrypted SSL traffic to debug any issues. So, if you are not using Java, this is the utility to go to debug the SSL issue.

Its output will be as follows, showing each of the SSL handshake. 

```
3 1  0.5765 (0.5765)  C>S  Handshake
      ClientHello
        Version 3.3
        cipher suites
        TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
        compression methods
                  NULL
3 2  0.6972 (0.1207)  S>C  Handshake
      ServerHello
        Version 3.3
        session_id[32]=
          ac f1 e7 3d 87 18 3f 75 f4 b5 d8 bc 61 51 dc 8e
          da 1c db 82 89 c4 d1 df 60 83 e3 8b 56 c7 23 87
        cipherSuite         TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
        compressionMethod                   NULL
3 3  0.6972 (0.0000)  S>C  Handshake
      Certificate
3 4  0.6972 (0.0000)  S>C  Handshake
      ServerKeyExchange
Not enough data. Found 327 bytes (expecting 32767)
3 5    0.6972   (0.0000)    S>C    Handshake
        ServerHelloDone
3 6    0.7427   (0.0454)    C>S    Handshake
        ClientKeyExchange
Not enough data. Found 64 bytes (expecting 16384)
3 7    0.7598   (0.0171)    C>S    ChangeCipherSpec
3 8    0.7605   (0.0007)    C>S      Handshake
3 9    0.8779   (0.1173)    S>C    ChangeCipherSpec
3 10   0.8779   (0.0000)    S>C      Handshake
3 11   0.8956   (0.0177)    C>S      application_data
3 12   1.0474   (0.1517)    S>C      application_data
3 13   11.0491   (10.0017)    S>C      Alert
  3      11.0492   (0.0000)    S>C    TCP FIN
```


## Wireshark

[Wireshark](https://www.wireshark.org/) or [TCPDump](https://www.tcpdump.org/) can give some insights into what is happening. From the server terminal, you can capture the SSL traffic using TCPDump into a file and open it in wireshark

```
sudo tcpdump -i eth0 -v  -dst host x.x.x.x or src host x.x.x.x -w /tmp/test.pcap
```

## SSLLabs Analysis

[SSLLabs](https://www.ssllabs.com/ssltest/) site can give very useful information about server capabilities of SSL certificates. It will show what versions of TLS and list of cipher suites are supported by server.

It can also perform the connection tests to the server using various clients such as Apache HTTP, OkHTTP, browsers, mobile etc.

## Java Runtime parameters

There are various runtime parameters which affect the SSL connectivity in Java.
Watch out for these parameters, if you are facing SSL issue in a Java
application. Note that, its just not enough to look at the arguments while
starting the program, since these runtime parameters can be set at runtime too.

For example, in one our client library, the following snippet of code disabled [Server Name Indication](https://en.wikipedia.org/wiki/Server_Name_Indication) which caused problems with the TLS connections to virtual servers, in which multiple servers for different network names are hosted at a single underlying network address.


```java
if (System.getProperty("jsse.enableSNIExtension") == null) {
	System.setProperty("jsse.enableSNIExtension", "false");
}
```
There are other parameters to watch out for as well. [Java Secure Socket Extension Reference Guide](https://docs.oracle.com/javase/7/docs/technotes/guides/security/jsse/JSSERefGuide.html) is a helpful page to start with.


Hope that helps anyone facing trouble with SSL connections. If you believe, there are some other useful tools to debug SSL issues further, do let me know in the comments.
