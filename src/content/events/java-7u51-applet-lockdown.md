---
ai_generated: true
title: "Java 7u51 blocks unsigned applets and tightens RIA security"
date: "2014-01-14"
dependency: "Java applet security model"
event_type: "browser-change"
severity: "total"
summary: "Oracle Java 7u51 tightened Rich Internet Application security, blocking unsigned/self-signed applets at higher settings and requiring manifest attributes — breaking many Java-based net artworks even before browsers removed plugins entirely."
links:
  - url: "https://www.oracle.com/java/technologies/javase/7u51-relnotes.html"
    label: "Oracle JDK 7u51 release notes"
  - url: "https://www.java.com/en/download/help/signed_code.html"
    label: "java.com: signed code / manifest changes"
affected_artworks:
  - artwork: "instance-city"
    severity: total
    status: restored
    note: "Java applet embedded in web page. Unsigned/legacy packaging may be blocked under tightened Java security."
  - artwork: "the-great-game"
    severity: total
    status: dead
    note: "Java applet realtime visualization. Blocked or warning-gated under 7u51+ security changes."
  - artwork: "slow-arrow-of-beauty"
    severity: total
    status: dead
    note: "Java applet UI. Security prompts/blocks prevent normal access."
  - artwork: "art-from-text"
    severity: total
    status: restored
    note: "Java applet. Requires compliant signing/manifest to run under 7u51-era security."
  - artwork: "starrynight"
    severity: total
    status: dead
    note: "Java applet for constellation generation. Security gating and later plugin removal."
fixes:
  - type: workaround
    description: "Re-sign applets with valid code-signing certificates and add required manifest attributes (historically feasible)."
  - type: emulation
    description: "Preserve via VM snapshots and local network isolation; document user prompts and security UX."
---

Java 7u51 introduced stricter requirements (permissions attributes, blocking unsigned applets at higher security), increasing friction for applet-based works. This created a "pre-extinction" even before NPAPI/plugin removal: users saw warnings or outright blocks.

## Notes

This event is useful on the timeline because it shows how security policy changes can "kill" works before a formal runtime EOL.
