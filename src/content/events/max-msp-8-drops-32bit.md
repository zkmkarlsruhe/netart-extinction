---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Max_(software)"
title: "Max 8 drops 32-bit support, breaking legacy art installations"
date: "2018-09-25"
dependency: "Max/MSP/Jitter (Cycling '74)"
event_type: "sdk-deprecation"
severity: "major"
summary: "Max 8, released September 25, 2018, dropped all 32-bit external support, breaking art installations and performances that relied on 32-bit-only third-party externals, audio plugins, and hardware drivers."
links:
  - url: "https://support.cycling74.com/hc/en-us/articles/360050778693-Information-about-64-bit"
    label: "Cycling '74: Information about 64-bit vs 32-bit"
  - url: "https://cycling74.com/forums/some-existing-externals-won't-open-in-max-8"
    label: "Cycling '74 Forum: Some existing externals won't open in Max 8"
  - url: "https://resources.culturalheritage.org/emg-review/volume-7-2021-2022/an-analysis-of-software-based-artworks-using-max-msp-through-different-conservation-strategies/"
    label: "Electronic Media Review: Conservation of Software-Based Artworks Using Max/MSP"
  - url: "https://cycling74.com/forums/running-into-issues-building-legacy-applications"
    label: "Cycling '74 Forum: Running into issues building legacy applications"
fixes:
  - type: workaround
    description: "Cycling '74 recommends staying on Max 7.3.5 or 7.3.6 (Mac) for patches that depend on 32-bit externals, but this freezes the project on an older, unsupported version."
  - type: rebuild
    description: "Recompile or replace 32-bit externals with 64-bit equivalents, if source code is available. Many third-party externals were abandoned and never recompiled."
  - type: emulation
    description: "Run legacy Max patches in a virtual machine with an older OS and Max 6 or 7 in 32-bit mode."
---

## What changed

Max/MSP/Jitter, developed by Cycling '74, is one of the most widely used environments for interactive sound, video, and installation art. Max 6 and Max 7 could run in either 32-bit or 64-bit mode. Max 8, released September 25, 2018, was 64-bit only.

This broke any patch that loaded 32-bit externals — compiled C/C++ objects that extend Max's functionality. Many of these externals were written by individual artists, small labs, or academic researchers who had moved on. Without source code, recompilation was impossible. Affected externals included hardware interface drivers (Art-Net DMX controllers, custom serial devices), specialized DSP objects, and Jitter video processing modules.

The impact was particularly acute for museum installations and touring artworks. A 2021-2022 study published in the Electronic Media Review documented the conservation challenges facing Max/MSP-based artworks in institutional collections, examining pieces like "Border Patrol" and "Particle Noise" through storage, migration, and emulation strategies. The study found that version dependencies create cascading fragility: a patch built in Max 4.5 on a PowerPC Mac cannot simply be opened in Max 8 on an Apple Silicon machine — the binary, the externals, and the OS are all incompatible.

## Notes

Max is unusual among creative coding tools because it is commercial, closed-source, and version-locked by license. Artists cannot legally redistribute the runtime without a paid license, and old versions cannot be freely downloaded. This creates a preservation bottleneck: even if a museum owns the source patch, running it requires a specific Max version on a compatible OS with the correct externals — a dependency chain that grows more fragile with each passing year.
