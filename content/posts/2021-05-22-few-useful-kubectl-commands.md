---
slug: "few-useful-kubectl-commands"
title: Few Useful Kubectl commands
date: '2021-05-22'
description: Few Useful Kubectl commands
tags:
  - Kubernetes
draft: false
params:
  disqus_id: /2021/05/22/few-useful-kubectl-commands/
---

Here are a few useful kubernetes commands:

## Login into the one of the pod's shell

```
kubectl exec --stdin --tty <<pod>> -- /bin/bash
```

## View services from all namespaces

```
kubectl get service --all-namespaces
```

## Change the current namespace context

```
kubectl config set-context --current --namespace = <<namespace>>
```

## Describe a pod

```
kubectl describe <<pod>>
```


