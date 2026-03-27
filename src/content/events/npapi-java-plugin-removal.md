---
ai_generated: true
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
  - artwork: "instance-city"
    severity: total
    status: dead
    note: "Java Applet embedded in HTML. Applet won't load because browsers no longer run Java plugins."
  - artwork: "slow-arrow-of-beauty"
    severity: total
    status: dead
    note: "Java applet UI + network retrieval. Plugin removal blocks execution."
  - artwork: "the-great-game"
    severity: total
    status: dead
    note: "Java applet realtime 3D terrain visualization. No Java plugin runtime in modern browsers."
  - artwork: "art-from-text"
    severity: total
    status: dead
    note: "Java applet generating visuals from user text. Applet blocked/unsupported."
  - artwork: "starrynight"
    severity: total
    status: dead
    note: "Java applet generates constellations. Requires emulation or legacy setup."
  - artwork: "60x1-cam-tm-ultimate-interactive-webcam-surveillance-system-"
    severity: total
    status: dead
  - artwork: "60x1-com"
    severity: total
    status: dead
  - artwork: "a-javanized-flesh"
    severity: total
    status: dead
  - artwork: "addiction"
    severity: total
    status: dead
  - artwork: "alphabet-synthesis-machine"
    severity: total
    status: dead
  - artwork: "alteraction"
    severity: total
    status: dead
  - artwork: "anti-capitalist-operating-system"
    severity: total
    status: dead
  - artwork: "apartment"
    severity: total
    status: dead
  - artwork: "artificial-art"
    severity: total
    status: dead
  - artwork: "babel"
    severity: total
    status: dead
  - artwork: "ballettikka-internettikka"
    severity: total
    status: dead
  - artwork: "bardcode"
    severity: total
    status: dead
  - artwork: "bit-101"
    severity: total
    status: dead
  - artwork: "brandon"
    severity: total
    status: dead
  - artwork: "carrier"
    severity: total
    status: dead
  - artwork: "chavirement-d"
    severity: total
    status: dead
  - artwork: "computational-expressionism"
    severity: total
    status: dead
  - artwork: "crash-run"
    severity: total
    status: dead
  - artwork: "cyberpoetry-1995-1997"
    severity: total
    status: dead
  - artwork: "dialtones-a-telesymphony"
    severity: total
    status: dead
  - artwork: "digital-nature-the-case-collection"
    severity: total
    status: dead
  - artwork: "document-9-1-1"
    severity: total
    status: dead
  - artwork: "e-sm-electronic-soul-mirroring"
    severity: total
    status: dead
  - artwork: "every-icon"
    severity: total
    status: dead
  - artwork: "every-time-i-b14-return-from-moscow-i-cry"
    severity: total
    status: dead
  - artwork: "field-guide-to-artificial-life-on-the-web"
    severity: total
    status: dead
  - artwork: "floccus"
    severity: total
    status: dead
  - artwork: "fractal-consciousness"
    severity: total
    status: dead
  - artwork: "gl-v"
    severity: total
    status: dead
  - artwork: "home-transfer"
    severity: total
    status: dead
  - artwork: "hypoem"
    severity: total
    status: dead
  - artwork: "i-want-to-share-you-what-are-you-doing-to-me"
    severity: total
    status: dead
  - artwork: "in-conversation"
    severity: total
    status: dead
  - artwork: "infiltration-dimages-respiratoires-en-milieu-semi-ouvert-sem"
    severity: total
    status: dead
  - artwork: "line"
    severity: total
    status: dead
  - artwork: "memoirs"
    severity: total
    status: dead
  - artwork: "meta4walls"
    severity: total
    status: dead
  - artwork: "metamix"
    severity: total
    status: dead
  - artwork: "metaphorical-clock"
    severity: total
    status: dead
  - artwork: "minitasking"
    severity: total
    status: dead
  - artwork: "mobile-trilogy"
    severity: total
    status: dead
  - artwork: "netomat"
    severity: total
    status: dead
  - artwork: "new-york-city-map"
    severity: total
    status: dead
  - artwork: "nice-page"
    severity: total
    status: dead
  - artwork: "ouija-2000"
    severity: total
    status: dead
  - artwork: "parole"
    severity: total
    status: dead
  - artwork: "photomontage"
    severity: total
    status: dead
  - artwork: "project-dante"
    severity: total
    status: dead
  - artwork: "re-2"
    severity: total
    status: dead
  - artwork: "re-positioning-fear-relational-architecture-3"
    severity: total
    status: dead
  - artwork: "restate-callaps"
    severity: total
    status: dead
  - artwork: "revenances"
    severity: total
    status: dead
  - artwork: "rosie"
    severity: total
    status: dead
  - artwork: "sea-in-motion"
    severity: total
    status: dead
  - artwork: "selbst-los-self-less"
    severity: total
    status: dead
  - artwork: "seme"
    severity: total
    status: dead
  - artwork: "smallnomad"
    severity: total
    status: dead
  - artwork: "statdt-kunst-web-sound-installation"
    severity: total
    status: dead
  - artwork: "t-u-r-n-s"
    severity: total
    status: dead
  - artwork: "the-book-after-the-book"
    severity: total
    status: dead
  - artwork: "the-demon-devil-girls"
    severity: total
    status: dead
  - artwork: "the-secret-lives-of-numbers"
    severity: total
    status: dead
  - artwork: "universal-net-cubism"
    severity: total
    status: dead
  - artwork: "vectorial-elevation-relational-architecture-4"
    severity: total
    status: dead
  - artwork: "what-was-he-thinking-about-berlin-praha-ljubljana-skopje"
    severity: total
    status: dead
  - artwork: "whenever-i-see-a-plane-i-remember-the-smell"
    severity: total
    status: dead
  - artwork: "wnvirus-com"
    severity: total
    status: dead
  - artwork: "workly-collection"
    severity: total
    status: dead
  - artwork: "wtba-championship-boxing"
    severity: total
    status: dead
  - artwork: "z"
    severity: total
    status: dead
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
