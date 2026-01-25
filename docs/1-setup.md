---
title: Installation and Setup
---
# Software Installation and Lab Setup

It's easiest to use the VXLAN/EVPN labs with _[netlab](https://netlab.tools/)_. While you can use most of them (with reduced functionality) with any other virtual or physical lab environment, we'll assume you decided to use _netlab_; if you want to set up your lab in some other way, read the [Manual Setup](https://bgplabs.net/external/) section of the BGP Labs documentation.

!!! Warning
    EVPN labs work best with _netlab_ release 25.10 or later (some lab exercises require a more recent _netlab_ release). If you're using an earlier release, please upgrade with `pip3 install --upgrade networklab`.

## Select the Network Devices You Will Work With {#devs}

While I usually recommend FRRouting as the simplest-to-deploy network device, FRRouting does not include data-plane VLAN, VXLAN, or anycast gateway configuration. Configuring underlying Linux devices is too complex for an entry-level VXLAN/EVPN  exercise; you'll be better off using one of the other platforms for which we implemented [VXLAN](https://netlab.tools/module/vxlan/#platform-support) and [EVPN](https://netlab.tools/module/evpn/#platform-support) functionality.

You can run Arista EOS in all [_netlab_-supported virtualization environments](https://netlab.tools/providers/) (libvirt virtual machines or Docker containers), and if you want to start practicing VXLAN and EVPN with minimum hassle, consider using Arista EOS for all lab devices. While most network devices require an x86 CPU, you can run Arista cEOS or Nokia SR Linux containers on [MacBooks with Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html).

!!! tip
    If you plan to run the labs in [free GitHub Codespaces](4-codespaces.md), you MUST use container-based network devices, such as Arista cEOS or Nokia SR Linux. Furthermore, the device cannot rely on the Linux VXLAN kernel module (FRRouting and VyOS do).

## Select the Additional Devices in Your Lab {#extradev}

Some labs use additional switches -- preconfigured devices with which your switches exchange EVPN routes. You won't configure those devices, but you might need to log into them and execute **show** commands.

The default setup uses Arista EOS on the lab switches and FRRouting on the external/core routers. All the **show** printouts were generated with Arista EOS.

You can use any other device for which we implemented the basic [VXLAN](https://netlab.tools/module/vxlan/#platform-support) and [EVPN](https://netlab.tools/module/evpn/#platform-support) functionality as the lab switches. Additional limitations (if any) are listed under the *Device Requirements* section of each lab exercise.

## Select the Virtualization Environment

Now that you know which network device to use, check [which virtualization environment](https://netlab.tools/platforms/#supported-virtualization-providers) you can use. Running VXLAN/EVPN labs in a [free GitHub Codespace](4-codespaces.md) is an excellent starting point, but if you decide to build your own infrastructure, _containerlab_ is easier to set up than _libvirt_.

If you want to run the labs on your laptop (including [Macs with Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/)), create a [Ubuntu VM](https://netlab.tools/install/ubuntu-vm/) to run _netlab_. You could also run them in a VM in a private or public cloud or invest in a tiny brick of densely packed silicon ([example](https://www.minisforum.com/)).

Now for a few gotchas:

* Your hardware and virtualization software (for example, VirtualBox or VMware Fusion) must support _nested virtualization_ if you want to run virtual machines on that Ubuntu VM.
* You don't need nested virtualization to run Docker containers unless you're using containers that run virtual machines _within a container_ (the [*vrnetlab* approach](https://netlab.tools/labs/clab/#using-vrnetlab-containers)).

## Software Installation

Based on the choices you made, you'll find the installation instructions in one of these documents:

* [Using GitHub Codespaces](4-codespaces.md)
* [Ubuntu VM Installation](https://netlab.tools/install/ubuntu-vm/) on Windows or MacOS
* [Ubuntu Server Installation](https://netlab.tools/install/ubuntu/)
* [Running netlab on any other Linux Server](https://netlab.tools/install/linux/)
* [Running netlab in a Public Cloud](https://netlab.tools/install/cloud/)
* [Running netlab on Apple silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon.html)

Once you have completed the software installation, you have to deal with the stupidities of downloading and installing network device images ([libvirt](https://netlab.tools/labs/libvirt/#vagrant-boxes), [containers](https://netlab.tools/labs/clab/#container-images)) unless you decided to use Nokia SR Linux or Vyos.

I would love to simplify the process, but the networking vendors refuse to play along. Even worse, their licenses prohibit me from downloading the images and creating a packaged VM with preinstalled network devices for you[^NPAL]. Fortunately, you only have to go through this colossal waste of time once.

[^NPAL]: I'm not going to pay a lawyer to read their boilerplate stuff, and I'm definitely not going to rely on my amateur understanding of US copyright law.

## Setting Up the Labs {#defaults}

We finally got to the fun part -- setting up the labs. If you're not using GitHub Codespaces:

* Select a directory where you want to have the VXLAN/EVPN labs
* Clone the `evpn` [GitHub repository](https://github.com/bgplab/evpn) with `git clone https://github.com/bgplab/evpn.git`. [GitHub UI](https://github.com/bgplab/evpn) gives you other options in the green `Code` button, including _Download ZIP_

After you get a local copy of the repository:

* Change the directory to the top directory of the cloned repository[^BLB].
* Verify the current project defaults with the `netlab defaults --project` command:

```
device = eos (project)
groups.external.device = frr (project)
groups.hosts.device = linux (project)
paths.plugin = ['topology:.', 'topology:../../plugin', 'package:extra'] (project)
provider = clab (project)
```

[^BLB]: `evpn` if you used the simple version of the **git clone** command

* If needed, change the project defaults to match your environment with the `netlab defaults --project _setting_=_value_` command or edit the `defaults.yml` file with a text editor like `vi` or `nano`. For example, use these commands to change your devices to Cisco Nexus OS running as virtual machines[^NXOS]:

```shell
$ netlab defaults --project device=nxos
The default setting device is already set in project defaults
Do you want to change that setting in project defaults [y/n]: y
device set to nxos in /home/user/evpn/defaults.yml

$ netlab defaults --project provider=libvirt
The default setting provider is already set in netlab,project defaults
Do you want to change that setting in project defaults [y/n]: y
provider set to libvirt in /home/user/evpn/defaults.yml
```

[^NXOS]: Assuming you built the [Nexus OS Vagrant box](https://netlab.tools/labs/nxos/) first

* A few labs have core- or external routers. The default lab setup uses FRRouting containers or virtual machines on these routers. If you want to use some other device, change that default:

```shell
$ netlab defaults --project groups.external.device=_your_device_
```

* Even if you run your devices as virtual machines, you might still want to run the attached hosts or external/core routers as containers to minimize the memory utilization. After installing Docker and containerlab with **netlab install containerlab**, set the **provider** parameter for the **hosts** and **external** groups to **clab**:

```shell
$ netlab defaults --project groups.hosts.provider=clab
$ netlab defaults --project groups.external.provider=clab
```

* In a terminal window, change the current directory to one of the lab directories (for example, `basic/1-single`), and execute **netlab up**.
* Wait for the lab to start and use **netlab connect** to connect to individual lab devices
* Have fun.
* When you're done, collect the device configurations with **netlab collect** (if you want to save them) and shut down the lab with **netlab down**
* Change the current directory to another lab directory and repeat.
* Once you run out of lab exercises, create a new one and contribute it with a pull request ;)
