# EVPN Designs: EBGP-Only EVPN

EVPN was designed for use on IBGP sessions within an autonomous system, with IGP (OSPF or IS-IS) providing paths to BGP next hops. However, after the *[BGP as a better IGP](https://nanog.org/news-stories/nanog-tv/top-talks/building-scalable-data-centers-bgp-better-igp/)* idea (formalized in [RFC 7938](https://datatracker.ietf.org/doc/html/rfc7938)) became popular, multiple vendors started implementing EVPN in various combinations of IBGP and EBGP.

In this lab exercise, you'll deploy EVPN in a straightforward EBGP-only fabric in which every device belongs to a different BGP autonomous system:

![Lab topology](topology-ebgp.png)

!!! tip
    For more details, read the ipSpace.net [Data Center BGP](https://www.ipspace.net/Data_Center_BGP/) article (in particular the [BGP in EVPN-Based Data Center Fabrics](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) section) and the [design-related](https://blog.ipspace.net/tag/evpn/#designs) ipSpace.net EVPN blog posts.

### Device Requirements {#req}

You can use any device supported by the _netlab_ [BGP](https://netlab.tools/module/bgp/#platform-support) and [VLAN](https://netlab.tools/module/vlan/#platform-support) configuration modules. The device should support VXLAN and EVPN, and be able to run EVPN over EBGP sessions.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `design/2-ebgp`
* Execute **netlab up**
* Log into lab devices with **netlab connect** and verify that the IP addresses and the BGP routing are properly configured.

## Existing Device Configuration

* The switches in your lab (l1, l2, spine) are preconfigured with *tenant* VLAN using VLAN tag 100 and VXLAN VNI 1000.
* IPv4 addresses are configured on Linux hosts, switch loopback interfaces, and the interswitch link ([details](#addr)).
* The switches have EBGP sessions on directly-connected interfaces ([details](#bgp)). These sessions are configured to exchange IPv4 prefixes.

## Configuration Tasks

Using the procedures you mastered in the [Extend a Single VLAN Segment with VXLAN](../vxlan/1-single.md) lab exercise:

* Configure VXLAN VTEP on L1 and L2. The Spine device is not running VXLAN.
* Configure MAC-VRF for the *tenant* VLAN on L1 and L2. The Spine device is an IPv4 router and is not involved in VLAN/VXLAN forwarding.

!!! warning
    You must use the same EVPN route targets on L1 and L2 even though they're in different autonomous systems.

* Activate EVPN address family on all EBGP sessions.

You'll probably need to tweak the EVPN address-family parameters to get a working EVPN fabric. The parameters you might have to fine-tune include:

* Propagation of extended BGP communities. EVPN does not work correctly without extended BGP communities attached to EVPN routes.
* BGP next hop handling (configured on individual neighbors or with an address-family route-map). The EVPN next hop must remain the IP address of the ingress VTEP; *Spine* switch must not change the BGP next hops when propagating EVPN routes between L1 and L2.
* Retention and propagation of all EVPN routes. Some devices do not retain or propagate third-party EVPN routes unless they are a route reflector or have a corresponding local VNI.
* Acceptance of EBGP routes with next hops that are not directly connected.
* Device-specific tweaks that enable EVPN route propagation on EVPN sessions.

## Verification and Troubleshooting

If you did everything correctly, H1 should be able to ping H2.

If you have to troubleshoot your configuration, start with the [troubleshooting steps](../vxlan/1-single.md#tshoot) outlined in the [Extend a Single VLAN Segment with VXLAN](../vxlan/1-single.md) lab exercise.

However, you'll most likely encounter errors in the EVPN-over-EBGP configuration, where these blog posts might come in handy (the blog posts talk about multi-pod EVPN designs, but focus on troubleshooting EVPN address family on EBGP sessions):

* [Troubleshooting Multi-Pod EVPN: Overview](https://blog.ipspace.net/2025/10/troubleshoot-multi-pod-evpn/)
* [Fixing Next Hops](https://blog.ipspace.net/2025/11/evpn-multi-pod-tshoot-example/)
* [Troubleshooting Route Targets](https://blog.ipspace.net/2025/11/evpn-multi-pod-tshoot-rt/)
* [Extended BGP Communities](https://blog.ipspace.net/2025/12/evpn-multi-pod-tshoot-xc/)

## Cheating

* Shut down your lab with the **netlab down** command
* Start the lab from the `solution.yml` topology with the **netlab up solution.yml** command
* Explore the L1/L2/Spine device configuration

## Reference Information

### Lab Wiring {#wiring}

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| l1 | Ethernet1 | spine | Ethernet1 |
| l2 | Ethernet1 | spine | Ethernet2 |
| h1 | eth1 | l1 | Ethernet2 |
| h2 | eth1 | l2 | Ethernet2 |

### Lab Addressing {#addr}

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **spine** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | spine -> l1 |
| Ethernet2 | 10.1.0.6/30 |  | spine -> l2 |
| **l1** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | l1 -> spine |
| **l2** |  10.0.0.3/32 |  | Loopback |
| Ethernet1 | 10.1.0.5/30 |  | l2 -> spine |
| **h1** |
| eth1 | 172.16.0.4/24 |  | h1 -> [l1,h2,l2] |
| **h2** |
| eth1 | 172.16.0.5/24 |  | h2 -> [h1,l1,l2] |

### BGP Routing {#bgp}

| Node | Router ID/<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|------------------|---------------------:|--------------:|
| **spine** | 10.0.0.1 | 65000 |
| | l1 | 65101 | 10.1.0.1 |
| | l2 | 65102 | 10.1.0.5 |
| **l1** | 10.0.0.2 | 65101 |
| | spine | 65000 | 10.1.0.2 |
| **l2** | 10.0.0.3 | 65102 |
| | spine | 65000 | 10.1.0.6 |
