---
layout: blog-post
title: "Setup Cassandra Cluster using Ansible and Vagrant"
excerpt: "Setup Cassandra Cluster using Ansible and Vagrant"
disqus_id: /2022/03/13/setup-cassandra-cluster-using-ansible-vagrant/
tags:    
    - Cassandra
    - Vagrant
    - Ansible
---

If you want to provision a test [Apache Cassandra](https://cassandra.apache.org/_/index.html) cluster for yourself, I recently created an automated solution using [Vagrant](https://www.vagrantup.com/) and [Ansible](https://www.ansible.com/)

Git clone the repository [https://github.com/madhur/vagrant-cassandra-ansible](https://github.com/madhur/vagrant-cassandra-ansible) and use `vagrant up` command to bring up the five Ubuntu 18.0 nodes.

This is a fork of original [https://github.com/apkan/vagrant-cassandra-ansible](https://github.com/apkan/vagrant-cassandra-ansible), however it had couple of issues: 
 * It was using old version of Ubuntu which did not had [systemd](https://systemd.io/) but instead used [upstart](https://upstart.ubuntu.com/)
 * Had 3 node cluster


 