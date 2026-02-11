# Open-Source VXLAN/EVPN Configuration Labs

This repository contains _netlab_ topology files for a series of hands-on labs that will help you master numerous aspects of VXLAN and EVPN technologies on a platform of your choice[^PC]. 

You can run them on [your laptop](https://netlab.tools/install/ubuntu-vm/) (including [Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html)), on a [local server](https://netlab.tools/install/ubuntu/), in the [cloud](https://netlab.tools/install/cloud/), or in a (free) [GitHub codespace](https://evpn.bgplabs.net/4-codespaces/).

The labs cover:

**VXLAN Configuration**

* [Extend a Single VLAN Segment with VXLAN](vxlan/1-single)
* [More Complex VXLAN Deployment Scenario](vxlan/2-complex)
* [Routing between VXLAN segments](vxlan/3-irb)
* [Anycast gateways on VXLAN segments](vxlan/4-anycast)
* [Implement VRF-Lite with VXLAN](vxlan/5-vrf-lite)
* [Running VXLAN over an IPv6-only underlay network](vxlan/6-ipv6)

**EVPN Configuration**

* [Build an EVPN-based MAC-VRF instance](evpn/1-bridging)
* [More complex EVPN/VXLAN bridging scenario](evpn/2-complex)
* [Integrated Routing and Bridging (IRB) with EVPN MAC-VRF instances](evpn/3-irb)
* [EVPN Asymmetric Integrated Routing and Bridging (IRB)](evpn/4-asym-irb)
* [Implement VRF-Lite with EVPN/VXLAN](evpn/5-vrf-lite)

**Complex EVPN Services**

* [Private VLANs](services/1-pvlan)

**EVPN Designs**

* [BGP Route Reflectors in EVPN Fabrics](design/1-rr)
* [EBGP-only EVPN](design/2-ebgp)

See [lab documentation](https://evpn.bgplabs.net/) for more details and the complete list of planned labs.

[^PC]: Some assembly required: while the Arista cEOS or Nokia SR Linux containers are easy to download, you might have to build a Vagrant box or a Docker container image for your platform.
