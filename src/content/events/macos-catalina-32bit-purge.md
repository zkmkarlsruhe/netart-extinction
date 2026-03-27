---
title: "macOS Catalina drops all 32-bit application support"
date: "2019-10-07"
dependency: "32-bit macOS applications and plugins"
event_type: "hardware-obsolescence"
severity: "major"
summary: "macOS 10.15 Catalina dropped all 32-bit application support, instantly breaking thousands of creative tools — audio plugins, MIDI drivers, standalone art applications, and legacy creative software that had never been updated to 64-bit."
links:
  - url: "https://en.wikipedia.org/wiki/MacOS_Catalina"
    label: "Wikipedia: macOS Catalina"
fixes:
  - type: workaround
    description: "Users can avoid upgrading past Mojave (10.14) to retain 32-bit support, but this increasingly conflicts with security updates and new software requirements."
  - type: none
    description: "32-bit macOS applications cannot run on Catalina or later. No translation layer exists (unlike Rosetta for PowerPC/Intel)."
---

macOS 10.15 Catalina, released October 7, 2019, dropped all support for 32-bit applications. Unlike previous transitions (PowerPC to Intel, which had Rosetta), there was no translation layer — 32-bit apps simply stopped launching.

## What changed

Thousands of creative tools broke overnight. Pro audio was disproportionately affected — hundreds of 32-bit VST/AU plugins, including freeware and art-oriented audio tools, became unusable. MIDI hardware drivers for older devices often had no 64-bit updates. Legacy Max/MSP standalone applications built with 32-bit runtimes stopped working. Creative coding tools, art applications, and experimental software from the 2000s and early 2010s that had never been updated to 64-bit were stranded.

## Notes

Apple had been warning developers since 2017 (macOS High Sierra showed alerts for 32-bit apps), but many creative tools — especially freeware, abandoned projects, and small-developer audio plugins — were never updated. For art installations relying on specific legacy software configurations, the upgrade to Catalina was a one-way door to incompatibility.
