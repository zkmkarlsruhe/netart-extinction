---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Rosetta_(software)"
title: "macOS Lion removes Rosetta, killing all PowerPC applications"
date: "2011-07-20"
dependency: "Apple Rosetta (PowerPC translation layer)"
event_type: "os-deprecation"
summary: "Mac OS X 10.7 Lion removed Rosetta, the PowerPC-to-Intel translation layer, instantly rendering all PowerPC-only applications unlaunchable — including legacy creative tools from Adobe, Macromedia, and independent developers."
links:
  - url: "https://en.wikipedia.org/wiki/Rosetta_(software)"
    label: "Wikipedia: Rosetta (software)"
  - url: "https://lowendmac.com/misc/11mr/mb-rosetta.html"
    label: "Low End Mac: The Implications of Losing Rosetta in OS X 10.7 Lion"
  - url: "https://www.cultofmac.com/news/os-x-lion-kills-rosetta-powerpc-support-heres-what-to-do-about-it"
    label: "Cult of Mac: OS X Lion Kills Rosetta PowerPC Support"
fixes:
  - type: workaround
    description: "Users could remain on Mac OS X 10.6 Snow Leopard to retain Rosetta, but this increasingly conflicted with security updates and new software requirements."
  - type: emulation
    description: "PowerPC Mac OS environments can be run via emulators such as QEMU or SheepShaver, though performance and compatibility vary."
  - type: none
    description: "No native path exists to run PowerPC applications on macOS Lion or later. Apple provided no replacement translation layer for PowerPC code."
---

## What changed

Mac OS X 10.7 Lion, released July 20, 2011, removed Rosetta — the binary translation layer that had allowed PowerPC applications to run on Intel-based Macs since the 2006 processor transition. Applications that had not been recompiled as Universal or Intel-native binaries became "tombstones": their icons displayed a white circle with a slash, and they could no longer launch.

The impact on creative software was severe. Adobe Creative Suite 1 and Creative Suite 2, both PowerPC-only, stopped working entirely. Users with CS2 upgrade CDs could not even install the software, since the installer needed to detect a prior PowerPC installation that could no longer exist. Macromedia FreeHand, a vector illustration tool still used by designers, became permanently unusable on Macs without Rosetta. Apple's own legacy pro applications — older versions of Final Cut Pro, Logic Pro, Soundtrack Pro, and DVD Studio Pro that predated Universal Binary builds — also required Rosetta and stopped functioning.

Beyond commercial software, a generation of experimental creative tools, standalone applications built with Director or HyperCard runtime wrappers, and bespoke art software written for PowerPC Macs in the late 1990s and early 2000s was cut off. Unlike the later Intel-to-Apple-Silicon transition (which introduced Rosetta 2), the PowerPC-to-Intel break offered no grace period — Rosetta was simply absent from Lion, with no option to install it.

For art installations running on Intel Macs that had been configured with a mix of PowerPC-era creative tools, upgrading to Lion was irreversible. Snow Leopard (10.6) became the last refuge for PowerPC software, freezing those machines in an increasingly unsupported state.
