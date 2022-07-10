---
layout: blog-post
title: "Gracefully shutting down JVM applications"
excerpt: "Gracefully shutting down JVM applications"
disqus_id: /2022/07/10/gracefully-shutting-down-jvm-applications/
tags:    
    - JVM
---

When writing applications for JVM which are long running such as application servers and web servers, it is very important to make sure that they shut down cleanly as and when required.

This is very important in cloud computing, as cloud technologies such as Kubernetes might kill the pod due to low resources or as part of scale up  / scale down processes.

Similarly, applications deployed on VMs in AWS, Azure or GCE can be terminated due to underlying hardware issues.

These technologies typically send a [SIGTERM](https://man7.org/linux/man-pages/man7/signal.7.html) signal to the running task to ensure it is able to clean up gracefully and finally after some threshold, the process is sent a [SIGKILL](https://man7.org/linux/man-pages/man7/signal.7.html) signal to terminate the container.


In JVM, we can register a hook to be executed whenever processes recieves SIGTERM signal


```java
Runtime.getRuntime().addShutdownHook(new Thread() {
  public void run() {
    // shutdown gracefully
  }
});
```

When running containerized applications, it is important to ensure that whenever a pod / container is sent SIGTERM, our JVM process recieves it.

This can be done by ensuring that our JVM process is the root process inside the container.

For example when writing [`Dockerfile`](https://docs.docker.com/engine/reference/builder/) for our container:

```bash
ENTRYPOINT ["java","-jar","/message-server-1.0.0.jar"]
```
Will ensure that our java process is the root process.

There could be few instances, where the entry point needs to execute some complex logic upon startup, such as when using shell scripts as follows:

```bash
ENTRYPOINT ["/bin/sh","/startup.sh"]
```

In those cases, it is important to use [`exec`](https://stackoverflow.com/questions/18351198/what-are-the-uses-of-the-exec-command-in-shell-scripts)

`exec` replaces the current program in the current process, without forking a new process, ensuring that our java program remains the root process in the container.

```shell
exec java -jar message-server-1.0.0.jar
```

Quick tip: How do we know if our process recieved any signal?

We can monitor the signals sent to any process through [`strace`](https://man7.org/linux/man-pages/man1/strace.1.html) as follows

```bash
$ strace -e 'trace=!all' -p 128278                                                                                                           
strace: Process 128278 attached
--- SIGTERM {si_signo=SIGTERM, si_code=SI_USER, si_pid=103440, si_uid=1000} ---
```