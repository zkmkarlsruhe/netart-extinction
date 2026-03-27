---
ai_generated: true
title: "VRML browser plugins become inaccessible"
date: "2003"
dependency: "VRML browser plugins (Cosmo Player, Cortona)"
event_type: "plugin-eol"
severity: "total"
summary: "VRML (Virtual Reality Modeling Language), the first web standard for interactive 3D, required browser plugins like Cosmo Player. When SGI sold Cosmo Software in 1998, the plugin was abandoned — and no modern browser supports VRML, leaving early 3D web art permanently inaccessible."
links:
  - url: "https://ipres2024.pubpub.org/pub/ruud1i2r/release/2"
    label: "iPRES 2024: Condition Assessment for Net Art"
  - url: "https://en.wikipedia.org/wiki/VRML"
    label: "Wikipedia: VRML"
affected_artworks:
  - artwork: "bodies-incorporated"
    severity: total
    status: dead
    note: "VRML-based participatory 3D world. Interactive 3D navigation no longer functions in any modern browser."
  - artwork: "apartment"
    severity: total
    status: dead
  - artwork: "brooklyn01"
    severity: total
    status: dead
  - artwork: "carrier"
    severity: total
    status: restored
  - artwork: "cyberpoetry-1995-1997"
    severity: total
    status: restored
  - artwork: "helix"
    severity: total
    status: dead
  - artwork: "plural-maps-lost-in-s"
    severity: total
    status: dead
  - artwork: "position"
    severity: total
    status: dead
  - artwork: "prototype-for-static-vehicle"
    severity: total
    status: restored
  - artwork: "revenances"
    severity: total
    status: dead
  - artwork: "the-great-game"
    severity: total
    status: dead
  - artwork: "trails"
    severity: total
    status: dead
  - artwork: "vectorial-elevation-relational-architecture-4"
    severity: total
    status: dead
  - artwork: "voxels"
    severity: total
    status: restored
  - artwork: "weightless-sculpture-project"
    severity: total
    status: restored
  - artwork: "world"
    severity: total
    status: dead
  - artwork: "google-3d-warehouse"
    severity: total
    status: dead
  - artwork: "vr-arcade-project"
    severity: total
    status: dead
  - artwork: "reconnoitre"
    severity: total
    status: dead
  - artwork: "virtual-urban"
    severity: total
    status: restored
  - artwork: "translate-expression"
    severity: total
    status: restored
  - artwork: "lincoln-3d-scans"
    severity: total
    status: dead
fixes:
  - type: emulation
    description: "Some VRML content can be converted to X3D or viewed with standalone VRML viewers, but browser-integrated interactive experience is lost."
  - type: none
    description: "No modern browser supports VRML plugins. The interactive web experience cannot be faithfully reproduced."
---

VRML (Virtual Reality Modeling Language) was the first web standard for interactive 3D content, standardized in 1994–1997. Experiencing VRML worlds required browser plugins — most commonly Cosmo Player, which was bundled with Netscape Communicator.

## What changed

When Silicon Graphics (SGI) restructured in 1998, it sold Cosmo Software to Platinum Technology, which was then acquired by Computer Associates. The Cosmo Player plugin was abandoned. Other VRML plugins (Cortona, Contact) lingered longer but all became incompatible with modern browsers as plugin architectures changed.

VRML was technically succeeded by X3D (2004), but the legacy VRML content was not automatically compatible, and the web had moved on to Flash for rich interactivity. When browsers dropped NPAPI plugin support entirely (2015–2021), the last theoretical path to viewing VRML in a browser was closed.

## Notes

This is one of the earliest net art extinction events. Works like Victoria Vesna's "Bodies INCorporated" (1996) — a participatory 3D world where users built virtual bodies to critique corporate identity — have lost their defining interactive dimension. The 3D models may survive as files, but the experience of navigating them in a browser is gone.
