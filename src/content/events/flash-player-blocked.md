---
title: "Flash Player blocked from running"
date: "2021-01-12"
end_date: "2021-01-12"
dependency: "Adobe Flash Player"
event_type: "plugin-eol"
severity: "total"
summary: "After Flash support ended at the end of 2020, Flash content was actively blocked from running starting Jan 12, 2021, and browsers removed/disabled the plugin — instantly breaking Flash-based net artworks unless emulated or migrated."
links:
  - url: "https://www.adobe.com/products/flashplayer/end-of-life-alternative.html"
    label: "Adobe Flash Player EOL FAQ"
  - url: "https://rhizome.org/editorial/2020/dec/21/before-flash-sunset/"
    label: "Rhizome: Before Flash Sunset"
  - url: "https://ruffle.rs/"
    label: "Ruffle Flash emulator"
affected_artworks:
  - artwork: telepresence-2
    severity: total
    status: dead
    note: "Flash-based interface and playback. No Flash runtime in modern browsers; content will not load."
  - artwork: resume-i
    severity: total
    status: unknown
    note: "Flash animation/timing + audio. Some YHCHI works have been migrated; verify per-work."
  - artwork: superstitious-appliances
    severity: total
    status: dead
    note: "Flash clickable scene navigation. Needs migration or emulation."
  - artwork: genesis
    severity: total
    status: unknown
    note: "HTML + Flash elements. Actively researched for migration in conservation literature."
fixes:
  - type: emulation
    description: "Ruffle, an open-source Flash emulator written in Rust/WebAssembly, can run many Flash works in modern browsers."
    url: "https://ruffle.rs"
  - type: archive
    description: "The Internet Archive's Flashpoint project has preserved thousands of Flash works."
    url: "https://archive.org/details/softwarelibrary_flash"
  - type: rebuild
    description: "Re-author Flash content as HTML5 video/audio or Canvas animations, though interaction logic and timing precision are often lost."
---

Flash Player support ended on December 31, 2020, and Adobe blocked Flash content from running beginning January 12, 2021 ("kill switch"). Browsers simultaneously removed or disabled Flash playback, leaving most Flash net art non-functional in default modern setups.

## What changed

Flash had been the dominant platform for interactive web content from the late 1990s through the early 2010s. Entire genres of net art — interactive animations, generative pieces, browser games, experimental interfaces — were built exclusively in Flash. The EOL rendered an estimated millions of creative works inaccessible in their original form.

## Notes

The Flash EOL was announced years in advance (July 2017), giving developers time to migrate. However, many historical artworks had no active maintainer to perform the migration. Reversibility is limited — Flash often encoded not just media, but interaction logic and typography timing.
