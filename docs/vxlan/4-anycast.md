# Anycast Gateways on VXLAN Segments

In the [previous lab exercise](3-irb.md), we configured routing between VXLAN segments using a dirty hack: the hosts used the IP address of the adjacent switch as the default gateway. In this exercise, we'll fix our implementation and use the same default gateway (shared among all switches) on all hosts in a subnet.

The lab topology is as simple as it was in the previous exercises: a pair of hosts per VLAN attached to two directly-connected switches:

![Lab topology](topology-anycast.png)

### Device Requirements {#req}

You can use any device supported by the _netlab_ [OSPF](https://netlab.tools/module/ospf/#platform-support) and [VLAN](https://netlab.tools/module/vlan/#platform-support) configuration modules. The device should support VXLAN with static ingress replication and routing between VLAN segments.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `vxlan/4-anycast`
* Execute **netlab up**
* Log into lab devices with **netlab connect** and verify that the IP addresses and the OSPF are properly configured.

## Existing Device Configuration

* The switches in your lab (S1 and S2) are preconfigured with *red* and *blue* VLANs.
* The *red* and *blue* VLANs have these VLAN tags and IPv4 prefixes:

| VLAN | VLAN tag | IPv4 prefix    |
|------|---------:|---------------:|
| red  | 100      | 172.16.10.0/24 |
| blue | 101      | 172.16.11.0/24 |

* IPv4 addresses are configured on Linux hosts, switch VLAN and loopback interfaces, and the interswitch link ([details](#addr)).
* Static routes pointing to the to-be-configured shared default gateways are configured on the Linux hosts:

| Host | IPv4 prefix   | Next hop    |
|------|--------------:|------------:|
| HR1  | 172.16.0.0/16 | 172.16.10.42 |
| HR2  | 172.16.0.0/16 | 172.16.10.42 |
| HB1  | 172.16.0.0/16 | 172.16.11.42 |
| HB2  | 172.16.0.0/16 | 172.16.11.42 |

* The switches run OSPF in area 0 across the interswitch link ([details](#ospf)).

## Configure VXLAN Segments

Using the procedure you mastered in the [Extend a Single VLAN Segment with VXLAN](1-single.md) lab exercise, extend both VLANs across the IP network using these VXLAN network identifiers:

| VLAN | VNI   |
|------|------:|
| red  | 10010 |
| blue | 10011 |

## Configure Shared Gateways

The technology you can use to implement the shared VLAN gateways depends on your equipment. Almost all equipment supports at least one first-hop redundancy protocol (for example, VRRP), but some devices cannot perform active-active forwarding, resulting in a single active per-VLAN gateway. That clearly limits performance and introduces unnecessary delays, as some inter-segment traffic has to traverse the IP core to be routed.

An even simpler technology available on some modern switches is the *anycast gateway*: all switches share a statically-configured IP and MAC address (while usually retaining a unique per-switch IP address).

Use either VRRP or anycast gateway to configure the shared per-VLAN default gateway on all VLANs using the following IP addresses:

| VLAN | Default gateway |
|------|----------------:|
| red  | 172.16.10.42 |
| blue | 172.16.11.42 |

!!! tip
    You might want to read these blog posts if you're curious how anycast gateways work behind the scenes:
    
    * [Optimal L3 Forwarding with VARP and Active/Active VRRP](https://blog.ipspace.net/2013/05/optimal-l3-forwarding-with-varp-and/)
    * [VRRP, Anycasts, Fabrics and Optimal Forwarding](https://blog.ipspace.net/2013/06/vrrp-anycasts-fabrics-and-optimal/)
    * [Arista EOS Virtual ARP (VARP) Behind the Scenes](https://blog.ipspace.net/2013/06/arista-eos-virtual-arp-varp-behind/)
    * [Duplicate ARP Replies with Anycast Gateways](https://blog.ipspace.net/2022/03/duplicate-arp-reply-anycast-gateway/)
    
    You'll find even more information in the ipSpace.net [Anycast Resources](https://blog.ipspace.net/series/anycast/).

## Verification

Use **ping** on hosts to verify that they can all reach each other:

```
$ netlab connect hr1
Connecting to container clab-irb-hr1, starting bash
hr1:/# ping -c 3 hr2
PING hr2 (172.16.10.4): 56 data bytes
64 bytes from 172.16.10.4: seq=0 ttl=64 time=4.142 ms
64 bytes from 172.16.10.4: seq=1 ttl=64 time=2.205 ms
64 bytes from 172.16.10.4: seq=2 ttl=64 time=2.318 ms

--- hr2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.205/2.888/4.142 ms
hr1:/# ping -c 3 hb1
PING hb1 (172.16.11.5): 56 data bytes
64 bytes from 172.16.11.5: seq=0 ttl=63 time=1.758 ms
64 bytes from 172.16.11.5: seq=1 ttl=63 time=0.871 ms
64 bytes from 172.16.11.5: seq=2 ttl=63 time=0.741 ms

--- hb1 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.741/1.123/1.758 ms
hr1:/# ping -c 3 hb2
PING hb2 (172.16.11.6): 56 data bytes
64 bytes from 172.16.11.6: seq=0 ttl=63 time=5.410 ms
64 bytes from 172.16.11.6: seq=1 ttl=63 time=2.072 ms
64 bytes from 172.16.11.6: seq=2 ttl=63 time=2.098 ms

--- hb2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.072/3.193/5.410 ms
```

Use the [troubleshooting hints](1-single.md#tshoot) from the [Extend a Single VLAN Segment with VXLAN](1-single.md) lab exercise if needed (we expect you're familiar with the traditional routing between VLAN segments)

!!! warning
    Traceroute might not work well with anycast gateways. For example, Arista EOS containers do not reply with an ICMP error message when the TTL of an IP packet sent to the anycast MAC address reaches zero.

## Cheating

* Shut down your lab with the **netlab down** command
* Start the lab from the `solution.yml` topology with the **netlab up solution.yml** command
* Explore the S1/S2 device configuration

## Reference Information

### Lab Wiring {#wiring}

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| s1 | Ethernet1 | s2 | Ethernet1 |
| hr1 | eth1 | s1 | Ethernet2 |
| hr2 | eth1 | s2 | Ethernet2 |
| hb1 | eth1 | s1 | Ethernet3 |
| hb2 | eth1 | s2 | Ethernet3 |

### Lab Addressing {#addr}

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **s1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | s1 -> s2 |
| Ethernet2 |  |  | [Access VLAN red] s1 -> hr1 |
| Ethernet3 |  |  | [Access VLAN blue] s1 -> hb1 |
| Vlan100 | 172.16.10.1/24 |  | VLAN red (100) -> [hr1,hr2,s2] |
| Vlan101 | 172.16.11.1/24 |  | VLAN blue (101) -> [hb1,hb2,s2] |
| **s2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | s2 -> s1 |
| Ethernet2 |  |  | [Access VLAN red] s2 -> hr2 |
| Ethernet3 |  |  | [Access VLAN blue] s2 -> hb2 |
| Vlan100 | 172.16.10.2/24 |  | VLAN red (100) -> [hr1,s1,hr2] |
| Vlan101 | 172.16.11.2/24 |  | VLAN blue (101) -> [hb1,s1,hb2] |
| **hr1** |
| eth1 | 172.16.10.3/24 |  | hr1 -> [s1,hr2,s2] |
| **hr2** |
| eth1 | 172.16.10.4/24 |  | hr2 -> [hr1,s1,s2] |
| **hb1** |
| eth1 | 172.16.11.5/24 |  | hb1 -> [s1,hb2,s2] |
| **hb2** |
| eth1 | 172.16.11.6/24 |  | hb2 -> [hb1,s1,s2] |

### OSPF Routing (Area 0) {#ospf}

| Router | Interface | IPv4 Address | Neighbor(s) |
|--------|-----------|-------------:|-------------|
| s1 | Loopback | 10.0.0.1/32 | |
|  | Ethernet1 | 10.1.0.1/30 | s2 |
| s2 | Loopback | 10.0.0.2/32 | |
|  | Ethernet1 | 10.1.0.2/30 | s1 |