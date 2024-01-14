---
layout: blog-post
title: "Forbidden error while accessing AWS services on Kubernetes"
excerpt: "Forbidden error while accessing AWS services on Kubernetes"
disqus_id: /2022/01/09/forbidden-aws-eks/
tags:
    - AWS
    - Kubernetes
---

If you have recently moved towards Kubernetes from EC2 and getting forbidden error while accessing AWS services make sure to have aws-sts in classpath.

In nutshell, the following dependency must be present

```xml
<!-- https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-sts -->
<dependency>
    <groupId>com.amazonaws</groupId>
    <artifactId>aws-java-sdk-sts</artifactId>
    <version>1.12.136</version>
</dependency>
```


The corresponding dependency for the AWS SDK v2 will be

```xml
<!-- https://mvnrepository.com/artifact/software.amazon.awssdk/sts -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>sts</artifactId>
    <version>2.16.24</version>
    <scope>test</scope>
</dependency>
```

This is because the credential provider which is concerned with loading the credentials from EKS role lies in sts module

[https://github.com/aws/aws-sdk-java/blob/7bf0fbec42de8a7d54875510f27fb363ca2d19f5/aws-java-sdk-sts/src/main/java/com/amazonaws/services/securitytoken/internal/STSProfileCredentialsService.java](https://github.com/aws/aws-sdk-java/blob/7bf0fbec42de8a7d54875510f27fb363ca2d19f5/aws-java-sdk-sts/src/main/java/com/amazonaws/services/securitytoken/internal/STSProfileCredentialsService.java)

