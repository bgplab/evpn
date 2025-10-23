# About the Project

In 2023, I started the [Open-Source BGP Labs project](https://bgplabs.net/) to recreate the labs I created in the early 1990s. As I [posted a status update a year later](https://blog.ipspace.net/2024/07/bgp-labs-year-later/), Henk Smit suggested I do the same for [IS-IS](https://isis.bgplabs.net/).

Those two projects were largely complete in late 2025, and it was time for another one. VXLAN/EVPN seemed like a no-brainer; welcome to the [Open-Source VXLAN/EVPN Configuration Labs](https://evpn.bgplabs.net/) project.

The project uses _[netlab](https://netlab.tools)_[^HT] to set up the labs.  You can use [whatever networking devices](1-setup.md#devs) you wish to work on, and if they happen to be supported by _netlab_, you'll get lab topology and basic device configuration for each lab set up in seconds[^XR]. Some lab exercises use additional (external) VXLAN/EVPN devices. We tested the labs with Arista EOS switches; you could also choose a [few other devices](1-setup.md#extradev).
 
You'll find the lab topology files in a [GitHub repository](https://github.com/bgplab/evpn), but you might [explore the lab exercises first](https://evpn.bgplabs.net/).

As always, everything starts with a [long wish list](3-upcoming.md). I probably missed something important -- please [open an issue](https://github.com/bgplab/isis/issues) or a [discussion](https://github.com/bgplab/isis/discussions), or (even better) become a contributor and submit a PR.

[^HT]: When you happen to have a Hammer of Thor handy, everything looks like a nail waiting to be hit ;)

[^XR]: Unless you love using resource hogs like Nexus OS or some Junos variants.
