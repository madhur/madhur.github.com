---
layout: blog-post
title: "Faking time in JVM Process"
excerpt: "Faking time in JVM Process"
disqus_id: /2024/07/01/mocking-jvm-time/
tags:
    - Java
    - Faketime
---

Recently, we were doing automation testing for one of our backend services and encountered an unique scenario wherein we wanted to forward the time by 24 hrs because we had entities which were created on daily basis at certain time.

To automate these scenarios, we had to wait for 24 unless we did either of these things:

* Somehow create those entities every few minutes instead of every 24 hours - This would require making the implementation generic for both scenarios.

* Fast forward the system time - Since we were running in containers and containers inherit the date time settings of host machine, we had to change the time of host machine. However, that means lot of other containers running in the same machine getting affected by these side effect.

We did not go with first option either, since there were lot of backend validations implemented and removing those validations means making the implementation susceptible to errors.

We looked through many solutions and finally arrived by using a library called [faketime](https://github.com/faketime-java/faketime)

In short,
> FakeTime uses a native Java agent to replace `System.currentTimeMillis()` implementation with the one you can control using system properties.

### Getting started with Faketime

Faketime is implemented as a native agent and hence it needs to be built for every platform such as Linux, Mac OS x86, Mac M1 etc.

Fortunately, there exists maven modules for each of the architectures

```xml
<!-- Windows 32bit -->
<dependency>
  <groupId>io.github.faketime-java</groupId>
  <artifactId>faketime-agent</artifactId>
  <version>0.8.0</version>
  <classifier>windows32</classifier>
</dependency>

<!-- Windows 64bit -->
<dependency>
  <groupId>io.github.faketime-java</groupId>
  <artifactId>faketime-agent</artifactId>
  <version>0.8.0</version>
  <classifier>windows64</classifier>
</dependency>

<!-- macOS 32bit -->
<dependency>
  <groupId>io.github.faketime-java</groupId>
  <artifactId>faketime-agent</artifactId>
  <version>0.8.0</version>
  <classifier>mac32</classifier>
</dependency>

<!-- macOS 64bit -->
<dependency>
  <groupId>io.github.faketime-java</groupId>
  <artifactId>faketime-agent</artifactId>
  <version>0.8.0</version>
  <classifier>mac64</classifier>
</dependency>

<!-- Linux 32bit -->
<dependency>
  <groupId>io.github.faketime-java</groupId>
  <artifactId>faketime-agent</artifactId>
  <version>0.8.0</version>
  <classifier>linux32</classifier>
</dependency>

<!-- Linux 64bit -->
<dependency>
  <groupId>io.github.faketime-java</groupId>
  <artifactId>faketime-agent</artifactId>
  <version>0.8.0</version>
  <classifier>linux64</classifier>
</dependency>
```

I have implemented a [small github project](https://github.com/madhur/faketime-example) to demonstrate faking the time using this library.

Here is how you would run it...



### Run using Maven
```shell
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-agentpath:./src/main/resources/libfaketime -XX:+UnlockDiagnosticVMOptions -XX:DisableIntrinsic=_currentTimeMillis -XX:CompileCommand=quiet -XX:CompileCommand=exclude,java/lang/System.currentTimeMillis -XX:CompileCommand=exclude,jdk/internal/misc/VM.getNanoTimeAdjustment"
```


### Get current time

```shell
curl --location 'localhost:8080/time/getTime'

{
    "localDateTime": "2024-06-29T15:42:41.973356",
    "timestamp": 1719655961973,
    "instant": "2024-06-29T10:12:41.973377Z",
    "date": "2024-06-29T10:12:41.973+00:00"
}
```

### Set fake time
```shell
curl --location --request POST 'localhost:8080/time/setTime?dateTime=2024-08-01T00%3A00%3A00'

Time set
````

### Get current time
```shell
curl --location 'localhost:8080/time/getTime'

{
    "localDateTime": "2024-08-01T00:00:35.085",
    "timestamp": 1722450635085,
    "instant": "2024-07-31T18:30:35.085Z",
    "date": "2024-07-31T18:30:35.085+00:00"
}
```

### Reset back to real time
```shell
curl --location --request POST 'localhost:8080/time/resetTime'
```
