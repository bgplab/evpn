# VPN IP Routing in EVPN Fabrics

In the [Implement VRF-Lite with EVPN/VXLAN](5-vrf-lite.md) lab exercise, you implemented an extremely awkward way of building a layer-3 VPN with EVPN. The solution required extraneous configuration (transit VLANs and MAC-VRFs) and was clearly unscalable; running a routing protocol instance per VRF is usually a bad idea.

What if there were a better way to implement the same requirements? For example, could we transport IP subnets as EVPN routes and attach all the necessary glue (transit VNI, router MAC addresses) to those routes? Welcome to the brave new world of type-5 EVPN routes[^MVP] defined in [RFC 9136](https://datatracker.ietf.org/doc/html/rfc9136) (IP Prefix Advertisement in Ethernet VPN). You'll practice this new concept using the same topology you used in the previous lab exercise:

![Lab topology](topology-vrf-lite.png)

[^MVP]: If your first reaction was "_this is just MPLS/VPN in disguise_," you're not too far off. It's just that we're using VXLAN segments instead of MPLS LSPs

### Device Requirements {#req}

You can use any device supported by the _netlab_ [OSPF](https://netlab.tools/module/ospf/#platform-support), [BGP](https://netlab.tools/module/bgp/#platform-support), and [VRF](https://netlab.tools/module/vrf/#platform-support) configuration modules. The device should also support:

* VXLAN encapsulation with EVPN control plane
* EVPN transit VNI
* EVPN type-5 routes
* Routing in and out of VXLAN tunnels (VXLAN RIOT)

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `evpn/6-ip-routing`
* Execute **netlab up**
* Log into lab devices with **netlab connect** and verify that the IP addresses and the OSPF are properly configured.

## Existing Device Configuration

* The switches in your lab (S1, S2, and S3) are preconfigured with *red* and *blue* VRFs.
* IPv4 addresses are configured on all links in your lab ([details](#addr)).
* Linux hosts use the adjacent switches as the default gateways
* The switches run OSPF in area 0 in the default VRF with the core router ([details](#ospf)).
* There's a full mesh of IBGP sessions between the three switches.

## Configuration Guidelines

If you want to use the type-5 (IP prefix) EVPN routes, you have to create EVPN IP-VRFs. The configuration process usually includes:

* Creating VRF instances (_netlab_ already did that for you)
* Creating EVPN IP-VRFs, often using **address-family vrf** within the BGP configuration (_netlab_ might have done that for you as well)
* Attaching a route distinguisher and EVPN import/export route targets to IP VRFs, either in the VRF configuration or BGP address family configuration.

!!! tip
    Several implementations use the same IP VRF configuration for MPLS/VPN and EVPN. You might have to use different configuration commands to configure route targets for MPLS/VPN and EVPN address families.

* Attaching a transit VXLAN segment to the EVPN IP VRF. The transit segment will transport encapsulated routed Ethernet frames between PE devices.

!!! tip
    The transit VXLAN segment configuration procedure is extremely implementation-dependent:
    
    * Arista EOS configures it on the VXLAN interface (using **vxlan vrf vni** command)
    * FRRouting, Cisco Nexus OS, or Dell OS10 use **vni** under **vrf**, **vrf context**, or **evpn/vrf**
    * Cisco IOS/XE expects you to configure a full-blown VLAN (or a **bridge domain**) including a VLAN (or BDI) interface.

If you want to advertise VRF IP prefixes as EVPN type-5 routes, you usually have to **redistribute** or **import** or **export**[^DT] them into the BGP VRF instance. Once you have the IP routes in a BGP VRF instance that has EVPN route targets, the transformation into EVPN type-5 routes usually happens automatically.

[^DT]: You guessed it. Different devices, different terminology for the same process. Isn't networking fun?

In our scenario, you only have to redistribute **connected** subnets into the *red* and *blue* BGP VRF instances.

Finally, you must enable the EVPN address family on the IBGP sessions between S1, S2, and S3.

## Verification

* Check the VRF BGP tables. They should include the connected subnets.

BGP table for red VRF on S1 running Arista EOS
{.code-caption}
```text
s1#show bgp ipv4 unicast vrf red
BGP routing table information for VRF red
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast, q - Pending FIB install
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      172.16.0.0/24          -                     -       -          -       0       i
 * >      172.16.1.0/24          10.0.0.2              0       -          100     0       i
 * >      172.16.2.0/24          10.0.0.3              0       -          100     0       i
```

!!! tip
    If you don't see the local IP subnet in the BGP VRF table, you forgot to configure route redistribution (or however it's called)

* Check the EVPN routes on S1, S2, and S3. You should not see any IMET or MAC-IP routes. The only routes in the BGP EVPN table should be the type-5 (IP-PREFIX) routes.

EVPN routes on S1 running Arista EOS
{.code-caption}
```text
s1#show bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 65000:1 ip-prefix 172.16.0.0/24
                                 -                     -       -       0       i
 * >      RD: 65000:1 ip-prefix 172.16.1.0/24
                                 10.0.0.2              -       100     0       i
 * >      RD: 65000:1 ip-prefix 172.16.2.0/24
                                 10.0.0.3              -       100     0       i
 * >      RD: 65000:2 ip-prefix 172.16.3.0/24
                                 -                     -       -       0       i
 * >      RD: 65000:2 ip-prefix 172.16.4.0/24
                                 10.0.0.2              -       100     0       i
```

!!! tip
    * If you have the local subnet in the VRF BGP table but don't see the corresponding IP-PREFIX routes, you probably forgot to configure the route distinguisher or the EVPN route targets. It's also possible that you configured MPLS/VPN route targets instead of EVPN route targets.
    * If you see local IP-PREFIX routes but not the remote ones, you forgot to activate the EVPN address family on the IBGP sessions.
    * If you see IMET (type-3) or MAC-IP (type-2) routes, you probably configured an EVPN MAC-VRF instance

* Check VRF routing tables on S1, S2, and S3 -- they should have BGP (or EVPN) routes for the remote subnets.

Routing table for VRF Red on S1
{.code-caption}
```text
s1#show ip route vrf red | begin Gateway
Gateway of last resort is not set

 C        172.16.0.0/24
           directly connected, Ethernet2
 B I      172.16.1.0/24 [200/0]
           via VTEP 10.0.0.2 VNI 5100 router-mac 00:1c:73:aa:8d:15 local-interface Vxlan1
 B I      172.16.2.0/24 [200/0]
           via VTEP 10.0.0.3 VNI 5100 router-mac 00:1c:73:d0:60:21 local-interface Vxlan1
```

Once the VRF routing tables have all the expected subnets, verify that you can ping between **hr1**, **hr2**, and **hr3** and between **hb1** and **hb2**

Does it all work? Fantastic. You can move on or explore the [behind-the-scenes details](#bds).

## Cheating

Can't get your lab to work? Maybe you can cheat your way to the next step:

* Shut down your lab with the **netlab down** command
* Start the lab from the `solution.yml` topology with the `netlab up solution.yml` command
* Explore the S1/S2/S3 device configuration

## Behind the Scenes {#bds}

If you read the [behind-the-scenes](5-vrf-lite.md#ccmmr) part of the [previous lab exercise](5-vrf-lite.md), you might be wondering how the IP-PREFIX routes set up all the glue we need to make IP routing across VXLAN work. The details are implementation-dependent, but at least in Arista EOS, the IP routing table does most of the heavy lifting.

An EVPN-derived VRF routing table entry on S1 running Arista EOS
{.code-caption}
```text
s1#show ip route vrf red 172.16.1.0/24
...
 B I      172.16.1.0/24 [200/0]
           via VTEP 10.0.0.2 VNI 5100 router-mac 00:1c:73:aa:8d:15 local-interface Vxlan1
```

The route table entry contains all the information we need to forward packets across the transit VXLAN segment:

* Outgoing VXLAN interface name (Vxlan1)
* VXLAN network identifier (VNI, 5100)
* Remote VTEP (10.0.0.2)
* Remote MAC address

Most of these details (route targets, encapsulation type, VNI) are carried *in every EVPN route*, as we explored in the [Build an EVPN-based MAC-VRF instance](1-bridging.md) lab exercise. 

Apart from a different prefix (IPv4 or IPv6 subnet versus MAC-IP information), the EVPN type-5 routes add a new extended community (Router's MAC) that is used to populate the destination MAC address of the Ethernet frames sent over the IP-VRF transit VXLAN segment. You can see the details of an EVPN type-5 route in the next printout:

EVPN IP-PREFIX (type-5) route for 172.16.1.0/24 on S1 running Arista EOS
{.code-caption}
```
s1#show bgp evpn route-type ip-prefix 172.16.1.0/24
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for ip-prefix 172.16.1.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:aa:8d:15
      VNI: 5100
```

After learning how to do *bridging* and *IP routing* across an EVPN fabric, you're probably wondering whether you can *combine the two*? That's the topic of the next lab exercise.

## Reference Information

### Lab Wiring {#wiring}

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| s1 | Ethernet1 | core | eth1 |
| s2 | Ethernet1 | core | eth2 |
| s3 | Ethernet1 | core | eth3 |
| hr1 | eth1 | s1 | Ethernet2 |
| hr2 | eth1 | s2 | Ethernet2 |
| hr3 | eth1 | s3 | Ethernet2 |
| hb1 | eth1 | s1 | Ethernet3 |
| hb2 | eth1 | s2 | Ethernet3 |

### Lab Addressing {#addr}

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **s1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | s1 -> core |
| Ethernet2 | 172.16.0.1/24 |  | s1 -> hr1 (VRF: red) |
| Ethernet3 | 172.16.3.1/24 |  | s1 -> hb1 (VRF: blue) |
| **s2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.6/30 |  | s2 -> core |
| Ethernet2 | 172.16.1.2/24 |  | s2 -> hr2 (VRF: red) |
| Ethernet3 | 172.16.4.2/24 |  | s2 -> hb2 (VRF: blue) |
| **s3** |  10.0.0.3/32 |  | Loopback |
| Ethernet1 | 10.1.0.10/30 |  | s3 -> core |
| Ethernet2 | 172.16.2.3/24 |  | s3 -> hr3 (VRF: red) |
| **core** |  10.0.0.4/32 |  | Loopback |
| eth1 | 10.1.0.1/30 |  | core -> s1 |
| eth2 | 10.1.0.5/30 |  | core -> s2 |
| eth3 | 10.1.0.9/30 |  | core -> s3 |
| **hr1** | 
| eth1 | 172.16.0.5/24 |  | hr1 -> s1 |
| **hr2** | 
| eth1 | 172.16.1.6/24 |  | hr2 -> s2 |
| **hr3** | 
| eth1 | 172.16.2.7/24 |  | hr3 -> s3 |
| **hb1** | 
| eth1 | 172.16.3.8/24 |  | hb1 -> s1 |
| **hb2** | 
| eth1 | 172.16.4.9/24 |  | hb2 -> s2 |

### OSPF Routing (Area 0) {#ospf}

| Router | Interface | IPv4 Address | Neighbor(s) |
|--------|-----------|-------------:|-------------|
| s1 | Loopback | 10.0.0.1/32 | |
|  | Ethernet1 | 10.1.0.2/30 | core |
| s2 | Loopback | 10.0.0.2/32 | |
|  | Ethernet1 | 10.1.0.6/30 | core |
| s3 | Loopback | 10.0.0.3/32 | |
|  | Ethernet1 | 10.1.0.10/30 | core |
| core | Loopback | 10.0.0.4/32 | |
|  | eth1 | 10.1.0.1/30 | s1 |
|  | eth2 | 10.1.0.5/30 | s2 |
|  | eth3 | 10.1.0.9/30 | s3 |

### BGP Routing {#bgp}

| Node | Router ID/<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|------------------|---------------------:|--------------:|
| **s1** | 10.0.0.1 | 65000 |
| | s2 | 65000 | 10.0.0.2 |
| | s3 | 65000 | 10.0.0.3 |
| **s2** | 10.0.0.2 | 65000 |
| | s1 | 65000 | 10.0.0.1 |
| | s3 | 65000 | 10.0.0.3 |
| **s3** | 10.0.0.3 | 65000 |
| | s1 | 65000 | 10.0.0.1 |
| | s2 | 65000 | 10.0.0.2 |
