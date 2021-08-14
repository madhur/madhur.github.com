---
layout: blog-post
title: "Liveness and Readiness Probes"
excerpt: "Liveness and Readiness Probes"
disqus_id: /2021/08/14/liveness-and-readiness-probes/
tags:
    - Kubernetes
---


When working with Kubernetes, [Liveness and Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) are very important concepts to understand.


## Readiness Probe

Kubernetes fires readiness probe to the pod to determine if the pod is ready to serve traffic or not. 

It can simply be defined as 

```yaml
readinessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
```

We can also provide readiness probe as HTTP or TCP commands

## Liveness Probe

Kubernetes fires readiness probe to the pod to determine if the pod is alive. If the pod is not alive, Kubernetes will restart the pod.

An important point to be noted is

` Liveness probes do not wait for readiness probes to succeed. If you want to wait before executing a liveness probe you should use initialDelaySeconds or a startupProbe.`

Which means that liveness probe and readiness probes have no dependency on each other. Some people assume that liveness probe start only after readiness probe is successful. This is misconception and is incorrect.


### How to determine the value of these probes

1. Determine the max start-up time taken by the application server to successfully start accepting http connections.
   For example, in our case pod takes around 15 seconds in all different environments.

2. Assuming a buffer of about 15 seconds we set the liveness probe to 30 seconds, with the default retry of 3 times and time difference between each retry as 5 seconds (these default value are set in periodSeconds and failureThreshold for each probe).

3. This leads to liveness probe being successful in the worst case scenario up to 45 seconds.
 
4. With another buffer of 15 seconds we set the readiness probe for 60 seconds.


## Startup Probes

Kubernetes introduced a new type of probe called startup probe to introduce the delay for liveness probes. 

As per kubernetes

> Sometimes, you have to deal with legacy applications that might require an additional startup time on their first initialization. In > such cases, it can be tricky to set up liveness probe parameters without compromising the fast response to deadlocks that motivated such > a probe. The trick is to set up a startup probe with the same command, HTTP or TCP check, with a failureThreshold * periodSeconds long > enough to cover the worse case startup time.