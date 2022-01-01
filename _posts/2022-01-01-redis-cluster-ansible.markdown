---
layout: blog-post
title: "Provision Redis cluster through Vagrant and Ansible"
excerpt: "Provision Redis cluster through Vagrant and Ansible"
disqus_id: /2022/01/01/redis-cluster-ansible/
tags:
    - Redis
    - Ansible
    - Vagrant
---

If you want to provision a test redis cluster for yourself, I recently created an automated solution using [Vagrant](https://www.vagrantup.com/) and [Ansible](https://www.ansible.com/)

Git clone the repository [https://github.com/madhur/redis-cluster-vagrant](https://github.com/madhur/redis-cluster-vagrant) and use `vagrant up` command to bring up the five Centos 7 nodes.

Once the nodes are up, the ansible playbook `setup-redis.yml` can be executed which will install redis on all the five nodes.

```
ansible-playbook playbooks/setup-redis.yml
```

The ansible playbook provisions four redis process on each node running on different ports.

Once the redis is setup, the execute the below command by sshing into any of the nodes (ex `vagrant ssh redis1`) to form the cluster

```
redis-cli --cluster create 192.168.56.10:7000 192.168.56.10:7001 192.168.56.11:7002 192.168.56.11:7003 192.168.56.12:7004 192.168.56.12:7005 192.168.56.13:7006 192.168.56.13:7007 192.168.56.14:7008 192.168.56.14:7009 192.168.56.10:6008 192.168.56.10:6009 192.168.56.11:6000 192.168.56.11:6001 192.168.56.12:6006 192.168.56.12:6007 192.168.56.13:6004 192.168.56.13:6005 192.168.56.14:6002 192.168.56.14:6003  --cluster-replicas 1
```

Cluster info and nodes output

```
[vagrant@redis1 ~]$ redis-cli -c -p 7000
127.0.0.1:7000> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:20
cluster_size:10
cluster_current_epoch:26
cluster_my_epoch:1
cluster_stats_messages_ping_sent:21962
cluster_stats_messages_pong_sent:21933
cluster_stats_messages_fail_sent:19
cluster_stats_messages_auth-ack_sent:6
cluster_stats_messages_update_sent:4
cluster_stats_messages_sent:43924
cluster_stats_messages_ping_received:21914
cluster_stats_messages_pong_received:21920
cluster_stats_messages_meet_received:19
cluster_stats_messages_fail_received:51
cluster_stats_messages_auth-req_received:6
cluster_stats_messages_received:43910
127.0.0.1:7000> cluster nodes
6e5264f6eb7430bf17255019d826a5e4358f6295 192.168.56.10:7001@17001 master - 0 1638032107272 2 connected 8192-9829
00073613e6b6227e63c503012846b89b9644d57e 192.168.56.10:6008@16008 master - 0 1638032106770 25 connected 14746-16383
cbf1264f74e929815df87cb83db7a68400a5bb6f 192.168.56.11:6001@16001 slave 6e5264f6eb7430bf17255019d826a5e4358f6295 0 1638032107000 2 connected
5ed583e52a38b5e7a01adf24b3048b18f5e03732 192.168.56.11:6000@16000 slave be3a72b4386d4c235717d11ae6d5cf456d9ae3cf 0 1638032107272 1 connected
1dab38a32885b6edaa84939ba1a8f21eb3b0756e 192.168.56.12:7004@17004 master - 0 1638032107675 5 connected 3277-4914
be3a72b4386d4c235717d11ae6d5cf456d9ae3cf 192.168.56.10:7000@17000 myself,master - 0 1638032102000 1 connected 0-1637
cc0bf33f88da4c0a987040c0abb61de9274e4c2e 192.168.56.11:7003@17003 master - 0 1638032107000 4 connected 9830-11468
d937a08e1ad1e81743a83a47d14d391aaf322cda 192.168.56.14:6003@16003 slave aa1fcb5c0660937662f0c70b89dfb09186ea0f4f 0 1638032106256 8 connected
996e270ea827c7a40aab9ec17713e10e80534d92 192.168.56.13:6005@16005 slave 38bda2c495194da1bc8db1d3f3aa5316a0c31332 0 1638032106971 6 connected
7e610c0b0ab6fc8a14cb618da205c587d6a451ca 192.168.56.11:7002@17002 master - 0 1638032106770 3 connected 1638-3276
0606dd06e50bc023d5c961de12ab9420ad2319bf 192.168.56.12:6007@16007 slave cc0bf33f88da4c0a987040c0abb61de9274e4c2e 0 1638032107675 4 connected
6ca58a8fd1a2b5418d60447f96101acc7dc229e1 192.168.56.13:6004@16004 slave 1dab38a32885b6edaa84939ba1a8f21eb3b0756e 0 1638032106669 5 connected
aa1fcb5c0660937662f0c70b89dfb09186ea0f4f 192.168.56.13:7007@17007 master - 0 1638032106465 8 connected 13107-14745
38bda2c495194da1bc8db1d3f3aa5316a0c31332 192.168.56.12:7005@17005 master - 0 1638032107675 6 connected 11469-13106
c53eb727d619d127336382736dae2f36b519ed1a 192.168.56.14:7009@17009 slave 00073613e6b6227e63c503012846b89b9644d57e 0 1638032107172 25 connected
8644049d5adb32c8570768d61186b6ea9307ca7a 192.168.56.10:6009@16009 master - 0 1638032107776 26 connected 6554-8191
45493186df74aea9ae31aa6d84421bbf1b0b18f1 192.168.56.14:7008@17008 slave 8644049d5adb32c8570768d61186b6ea9307ca7a 0 1638032106000 26 connected
5ba3d4ce175967027c23e48e884ca549222206b6 192.168.56.13:7006@17006 master - 0 1638032107172 7 connected 4915-6553
915aa483535504cc8ca4662bba40adbfabf95d95 192.168.56.12:6006@16006 slave 7e610c0b0ab6fc8a14cb618da205c587d6a451ca 0 1638032107172 3 connected
6f8ab10161f974f37a97b2e18a52d91878dc799d 192.168.56.14:6002@16002 slave 5ba3d4ce175967027c23e48e884ca549222206b6 0 1638032107776 7 connected
```

