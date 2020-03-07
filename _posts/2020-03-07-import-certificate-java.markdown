---
layout: blog-post
title: "Importing certificate into Java Keystore"
excerpt: "Importing certificate into Java Keystore"
disqus_id: /2020/03/07/import-certificate-java/
tags:
- Java
---

If any host is using self-signed certificate, then a typical HTTPS request to that host will fail in the Java code with the following exception:

```
javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

A very NOT recommended solution to this problem is to bypass the certificate check

```java
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import javax.net.ssl.X509TrustManager;

public class TrustAnyTrustManager implements X509TrustManager 
{

    public void checkClientTrusted(X509Certificate[] chain, String authType) throws CertificateException 
    {
    }

    public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException 
    {
    }

    public X509Certificate[] getAcceptedIssuers() 
    {
        return new X509Certificate[] {};
    }
}
```

And then use this `TrustAnyTrustManager` while forming the request

```java
HttpsURLConnection conn = null;
URL url = new URL(serviceUrl);
conn = (HttpsURLConnection) url.openConnection();
SSLContext sc = SSLContext.getInstance("SSL");  
sc.init(null, new TrustManager[]{new TrustAnyTrustManager()}, new java.security.SecureRandom());  
conn.setSSLSocketFactory(sc.getSocketFactory());
```

Let me re-iterate, do not use the above code in production or even development envrionment. This is highly insecure and susceptible to [MITM](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) attacks

A better solution is to import the untrusted certificate into the Java keystore. First, we have to export the certificate. This can be done using Chrome and then import it through command line.

All this can be automated through either a simple shell script, which can be executed on the server itself. For example, the below script can be executed using:

```shell
sudo ./javacert.sh google.com
```

<script src="https://gist.github.com/madhur/bbda66fe8f244a8aef22102f1bd05edd.js"></script>

Though, the above solution works for development servers, this is not a recommended solution for production servers. A situation should not arise where you have to import the un-siged certificate 
into production environment, but even if it arises, its better to go with orchestration solution either using [Ansible](https://www.ansible.com/) or [Chef](https://www.chef.io/)

In my case, the below simple ansible playbook does the job for us:

```yml
---
 - hosts: all
   tasks:
    - name: Import SSL certificate from google.com to a given cacerts keystore
      java_cert:
        cert_url: google.com
        cert_port: 443
        keystore_path: /usr/lib/jvm/jre7/lib/security/cacerts
        keystore_pass: changeit
        state: present
```