---
layout: blog-post
title: "Create local kubernetes cluster using Kind"
excerpt: "Create local kubernetes cluster using Kind"
disqus_id: /2024/09/01/create-local-k8s-cluster-kind/
tags:
    - k8s
    - Kind
---

If you want to quickly spin up a local development environment of kubernets cluster, Kubernetes in docker aka [Kind](https://kind.sigs.k8s.io/) is the way to go

Kind runs the kubernetes inside a docker container as opposed to [Minikube](https://minikube.sigs.k8s.io/docs/) which used to run kubernetes inside a VM

Running Kind on linux requires to create a cluster configuration file `cluster.yaml`

Here is the sample configuration which would work for most of the cases:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:

  - |
     kind: InitConfiguration
     nodeRegistration:
     kubeletExtraArgs:
     node-labels: "ingress-ready=true"
     extraPortMappings:
     - containerPort: 80
       hostPort: 80
       protocol: TCP
     - containerPort: 443
       hostPort: 443
       protocol: TCP
```

```shell
kind create cluster --config=cluster.yaml
```


Upon creating the cluster, `kubectl` context is automatically set to point to `kind` cluster.


```shell
> kubectl cluster-info --context kind-kind
Kubernetes control plane is running at https://127.0.0.1:46251
CoreDNS is running at https://127.0.0.1:46251/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```


