---
title: "NPAPI and Java plugin support removed from major browsers"
date: "2015-09-01"
dependency: "NPAPI / Java browser plugins"
event_type: "browser-change"
severity: "total"
summary: "Browser vendors removed the NPAPI plugin architecture (Chrome 45 milestone; later Firefox and Safari), stranding Java applets and other plugin-era net artworks unless run in legacy environments."
links:
  - url: "https://www.chromium.org/developers/npapi-deprecation/"
    label: "Chromium NPAPI deprecation guide"
  - url: "https://developer.apple.com/documentation/safari-release-notes/safari-12-release-notes"
    label: "Safari 12: legacy plugin support removed"
affected_artworks:
  - artwork: instance-city
    severity: total
    status: dead
    note: "Java Applet embedded in HTML. Applet won't load because browsers no longer run Java plugins."
  - artwork: slow-arrow-of-beauty
    severity: total
    status: dead
    note: "Java applet UI + network retrieval. Plugin removal blocks execution."
  - artwork: the-great-game
    severity: total
    status: dead
    note: "Java applet realtime 3D terrain visualization. No Java plugin runtime in modern browsers."
  - artwork: art-from-text
    severity: total
    status: dead
    note: "Java applet generating visuals from user text. Applet blocked/unsupported."
  - artwork: starrynight
    severity: total
    status: dead
    note: "Java applet generates constellations. Requires emulation or legacy setup."
fixes:
  - type: emulation
    description: "Preserve a 'known-good' browser+plugin stack via virtualization (e.g., Windows XP/7 + old Firefox/IE + JRE plugin) with network quarantining."
  - type: rebuild
    description: "Migrate applet logic to JavaScript/WebGL, or capture an archival recording plus source/code documentation."
---

NPAPI was progressively disabled and then removed. Chrome's roadmap explicitly targeted permanent removal by September 2015 (Chrome 45). Firefox later removed NPAPI plugins except Flash (Firefox 52). Safari 12 removed support for most legacy web plugins.

## What changed

The NPAPI plugin architecture had allowed browsers to run Java applets, Silverlight, Unity Web Player, and other plugin-based content. Its removal stranded an entire generation of web-based interactive artworks that depended on these runtime environments.

## Notes

Scope: any artwork relying on Java, Silverlight, Unity Web Player, etc. Reversibility: medium — VM-based access is feasible, but web-native access typically requires rewrite.
