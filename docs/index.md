---
title: Labs Overview
---
# Open-Source VXLAN/EVPN Configuration Labs

This series of VXLAN/EVPN hands-on labs will help you master numerous aspects of VXLAN and EVPN on a [platform of your choice](https://netlab.tools/module/vxlan/#platform-support)[^PC], including:

* Arista EOS
* Aruba AOS-CX
* Cisco Nexus OS
* Dell OS10
* Juniper switches
* Nokia SR OS and SR Linux
* Vyatta VyOS

[^PC]: Some assembly required: while some virtual machines or containers are easy to download, you'll have to build a Vagrant box or install a vendor-supplied Vagrant box or Docker container image for most other platforms. See [installation and setup](1-setup.md) for details.

A few labs are already waiting for you (with more [coming soon](3-upcoming.md)), but if this is your first visit to this site, you should start with the [Installation and Setup](1-setup.md) documentation or [run VXLAN/EVPN labs in GitHub codespaces](4-codespaces.md).

## Configure VXLAN {#vxlan}

In these labs, you'll learn how to configure VXLAN with static ingress replication and use it to build VLANs, layer-3 segments, or VRF-Lite deployments:

* [Extend a single VLAN segment with VXLAN](vxlan/1-single.md)
* Routing between VXLAN segments (coming soon)
* Anycast gateways (coming soon)
* Implementing VRF-Lite with VXLAN (coming soon)

The project has [just started](99-about.md); expect to see [more labs](3-upcoming.md) in the near future.
