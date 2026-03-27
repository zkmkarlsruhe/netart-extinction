---
title: "Adobe Shockwave Player end-of-life"
date: "2019-04-09"
dependency: "Adobe Shockwave Player"
event_type: "plugin-eol"
severity: "total"
summary: "Adobe ended Shockwave Player on April 9, 2019, leaving Director/Shockwave web works dependent on legacy browsers and offline virtualization unless migrated."
links:
  - url: "https://helpx.adobe.com/enterprise/kb/eol-adobe-flash-shockwave-player.html"
    label: "Adobe Shockwave end-of-life notice"
affected_artworks:
  - artwork: carrier
    severity: total
    status: dead
    note: "Shockwave-based multimedia + scripting. Plugin unavailable; content cannot play."
  - artwork: new-lexia
    severity: total
    status: dead
    note: "Shockwave animation/interface. No runtime in modern browsers."
  - artwork: soundboxes
    severity: total
    status: dead
    note: "Shockwave audio interface. Plugin missing/blocked."
  - artwork: micro-modernist-google-gadget
    severity: total
    status: dead
    note: "Shockwave + iGoogle gadget container. Double extinction: Shockwave EOL plus iGoogle platform shutdown."
fixes:
  - type: emulation
    description: "Run in a preserved environment (VM + old browser + plugin)."
  - type: rebuild
    description: "Migrate Director assets/logic to open runtimes (HTML5/Canvas/WebAudio)."
---

Shockwave Player (the browser runtime for Director/Shockwave web content) reached end-of-life and distribution/support ended. With modern browsers already hostile to plugins, Shockwave web works effectively became legacy-only.

## What changed

Shockwave failures are often total: navigation, media, and interaction are bound to Director runtime semantics. Unlike Flash (which has Ruffle), there is no widely-adopted emulator for Shockwave content.
