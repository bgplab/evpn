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

Several labs are already waiting for you (with more [coming soon](3-upcoming.md)), but if this is your first visit to this site, you should start with the [Installation and Setup](1-setup.md) documentation or [run VXLAN/EVPN labs in GitHub codespaces](4-codespaces.md).

## Configure VXLAN {#vxlan}

In these labs, you'll learn how to configure VXLAN with static ingress replication and use it to build VLANs, layer-3 segments, or VRF-Lite deployments:

* [Extend a single VLAN segment with VXLAN](vxlan/1-single.md)
* [More complex VXLAN deployment scenario](vxlan/2-complex.md)
* [Routing between VXLAN segments](vxlan/3-irb.md)
* [Anycast gateways on VXLAN segments](vxlan/4-anycast.md)
* [Implement VRF-Lite with VXLAN](vxlan/5-vrf-lite.md)
* [Running VXLAN over an IPv6-only underlay network](vxlan/6-ipv6.md)

## Configure EVPN {#evpn}

After mastering the basics of using VXLAN to stretch Ethernet segments across an IP network, you'll add EVPN control plane to a VXLAN setup:

* [Build an EVPN-based MAC-VRF instance](evpn/1-bridging.md)
* [More complex EVPN/VXLAN bridging scenario](evpn/2-complex.md)
* Integrated Routing and Bridging (IRB) with EVPN MAC-VRF instances (coming soon)
* Symmetric IRB with IP-VRF EVPN instances (coming soon)
* Anycast gateways in an EVPN environment
* Implementing L3VPN with EVPN and VXLAN
* Intra-subnet routing with proxy ARP
* Using EVPN in an IPv6-only underlay network

## EVPN Designs {#design}

EVPN was designed for use with IBGP sessions, with BGP next hops resolved via an IGP (usually OSPF or IS-IS). Today, you can see a plethora of alternative designs, including:

* Using BGP route reflectors to scale EVPN fabrics (coming soon)
* [EBGP-only EVPN](design/2-ebgp.md)
* Multi-pod EVPN (coming soon)
