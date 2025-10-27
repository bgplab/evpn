# ==LAB EXERCISE NAME==

VXLAN is a data-plane-only technology that encapsulates Ethernet frames in UDP packets (using the VXLAN header defined in the [RFC  7348](https://datatracker.ietf.org/doc/html/rfc7348) as the shim between the two). In this lab exercise, you'll use VXLAN (*overlay* network) to extend a single VLAN across an IP-only backbone (*underlay* network):

![Lab topology](topology-single.png)

### Device Requirements {#req}

You can use any device supported by the _netlab_ [OSPF](https://netlab.tools/module/ospf/#platform-support) and [VLAN](https://netlab.tools/module/vlan/#platform-support) configuration modules. The device should support VXLAN with static ingress replication.

## Start the Lab

Assuming you already [set up your lab infrastructure](../1-setup.md):

* Change directory to `vxlan/1-single`
* Execute **netlab up**
* Log into lab devices with **netlab connect** and verify that the IP addresses and the OSPF are properly configured.

## ==Existing Device Configuration==

* The switches in your lab (S1 and S2) are preconfigured with a *tenant* VLAN with VLAN tag 100.
* IPv4 addresses are configured on Linux hosts, switch loopback interfaces, and the interswitch link ([details](#addr)).
* The switches run OSPF in area 0 across the interswitch link ([details](#ospf)).

## ==Configuration Tasks==

Configuring VXLAN on a switch is usually a multi-step process:

## ==Verification==

Try to ping h2 from h1:

## ==Troubleshooting {#tshoot}==


## Cheating

* Shut down your lab with the **netlab down** command
* Start the lab from the `solution.yml` topology with the **netlab up solution.yml** command
* Explore the switch configurations

## ==Reference Information==

### Lab Wiring {#wiring}

| Origin Device | Origin Port | Destination Device | Destination Port |
|---------------|-------------|--------------------|------------------|
| s1 | Ethernet1 | s2 | Ethernet1 |
| h1 | eth1 | s1 | Ethernet2 |
| h2 | eth1 | s2 | Ethernet2 |

### Lab Addressing {#addr}

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **s1** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.1/30 |  | s1 -> s2 |
| Ethernet2 |  |  | [Access VLAN tenant] s1 -> h1 |
| Vlan100 |  |  | VLAN tenant (100) -> [h1,h2,s2] |
| **s2** |  10.0.0.2/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | s2 -> s1 |
| Ethernet2 |  |  | [Access VLAN tenant] s2 -> h2 |
| Vlan100 |  |  | VLAN tenant (100) -> [h1,s1,h2] |
| **h1** |
| eth1 | 172.16.0.3/24 |  | h1 -> [s1,h2,s2] |
| **h2** |
| eth1 | 172.16.0.4/24 |  | h2 -> [h1,s1,s2] |

### OSPF Routing (Area 0) {#ospf}

| Router | Interface | IPv4 Address | Neighbor(s) |
|--------|-----------|-------------:|-------------|
| s1 | Loopback | 10.0.0.1/32 | |
|  | Ethernet1 | 10.1.0.1/30 | s2 |
| s2 | Loopback | 10.0.0.2/32 | |
|  | Ethernet1 | 10.1.0.2/30 | s1 |
