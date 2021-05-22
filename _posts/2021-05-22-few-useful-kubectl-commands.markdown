---
layout: blog-post
title: "Few Useful Kubectl commands"
excerpt: "Few Useful Kubectl commands"
disqus_id: /2021/05/22/few-useful-kubectl-commands/
tags:
    - Kubernetes
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


