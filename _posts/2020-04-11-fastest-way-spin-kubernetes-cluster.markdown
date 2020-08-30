---
layout: blog-post
title: "Fastest way to spin up Kubernetes cluster on AWS"
excerpt: "Fastest way to spin up Kubernetes cluster on AWS"
disqus_id: /2020/04/11/fastest-way-spin-kubernetes-cluster/
tags:
- Kubernetes
---

Recently, I was trying to do a POC on Kubernetes and required a kubernetes Cluster.

Its easy to spin up a single machine cluster using [Minkube](https://kubernetes.io/docs/tasks/tools/install-minikube/) on Windows, Linux and MacOS

But the behavior of Minkube is not as close to real Kubernetes cluster primarily because:

* You can't simulate multiple nodes
* You cannot have a public DNS for your services unless you use [minikube tunnel](https://minikube.sigs.k8s.io/docs/handbook/accessing/#using-minikube-tunnel)
* The way minikube runs either in Docker, VirtualBox or over HyperV makes it difficult to test some of the networking features which would be as close to real Kubernetes cluster

Because of the above disadvantages, I decided to setup my own Kubernetes cluster in AWS. Sure it would cost me some $$$ but atleast my testing would as close to real.

Couple of years ago, I remember following long series of steps to setup cluster on AWS. But now, thanks to [AWS CLI and eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html), it takes a few terminal commands to run AWS Kubernetes cluster without even logging onto AWS UI.

Assuming, you have AWS CLI installed and configured with your AWS Credentials,

```shell
eksctl create cluster \
--name prod \
--region ap-south-1 \
--nodegroup-name standard-workers \
--node-type t3.medium \
--nodes 3 \
--nodes-min 1 \
--nodes-max 4 \
--ssh-access \
--ssh-public-key ~/.ssh/id_rsa.pub \
--managed
```

Here is the output of `kubectl cluster-info` after running the above command

```shell
~ ./kubectl cluster-info
Kubernetes master is running at https://92797800687320683968AF0937C2B5D3.yl4.ap-south-1.eks.amazonaws.com
CoreDNS is running at https://92797800687320683968AF0937C2B5D3.yl4.ap-south-1.eks.amazonaws.com/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```
