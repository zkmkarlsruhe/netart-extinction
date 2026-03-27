---
title: "Microsoft removes Windows Mixed Reality from Windows 11"
date: "2024-10"
dependency: "Windows Mixed Reality platform"
event_type: "platform-shutdown"
severity: "total"
summary: "Microsoft deprecated Windows Mixed Reality in December 2023 and removed it entirely in Windows 11 24H2 (October 2024), bricking an estimated 80,000 WMR headsets from Acer, Dell, HP, Lenovo, and Samsung."
links:
  - url: "https://www.theregister.com/2023/12/27/windows_mixed_reality_is_dead/"
    label: "The Register: Windows Mixed Reality is dead"
  - url: "https://www.pcworld.com/article/2490448/windows-11s-2024-update-finally-abandons-this-once-promising-feature.html"
    label: "PCWorld: Windows 11 abandons WMR"
fixes:
  - type: workaround
    description: "Users can avoid updating to Windows 11 24H2, but this increasingly conflicts with security and software requirements."
  - type: none
    description: "WMR headsets have no alternative runtime. Unlike Oculus headsets, which use standalone firmware, WMR headsets depend entirely on Windows for tracking and rendering."
---

Microsoft announced the deprecation of Windows Mixed Reality in December 2023. The platform was removed from Windows 11 in the 24H2 update (October 2024). Consumer support ends November 1, 2026; commercial support ends November 1, 2027.

## What changed

An estimated 80,000 users lost headset functionality upon upgrading. WMR headsets from five manufacturers (Acer, Dell, HP, Lenovo, Samsung) became non-functional paperweights. Unlike standalone VR headsets, WMR headsets depend entirely on Windows for inside-out tracking computation and rendering — removing the WMR runtime from Windows makes the headsets physically unusable.

The Mixed Reality Portal app, Windows Mixed Reality for SteamVR, and the SteamVR WMR beta were all discontinued. VR experiences created specifically for WMR headsets — including spatial computing experiments and mixed reality art — lost their platform.

## Notes

WMR headsets were the most affordable entry point to PC VR, making them attractive for educational and artistic use. Their sudden obsolescence through an OS update — rather than through hardware failure — represents a new pattern: platform holders can remotely disable functional hardware by removing software support.
