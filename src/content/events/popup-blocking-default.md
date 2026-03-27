---
title: "Popup blocking becomes default in major browsers"
date: "2004-08"
dependency: "window.open() / popup windows"
event_type: "browser-change"
severity: "major"
summary: "Windows XP SP2 added popup blocking to Internet Explorer in August 2004, and Firefox 1.0 shipped with it on by default in November. Multi-window net artworks — especially JODI's popup-cascade pieces — were silently neutralized."
links:
  - url: "https://anthology.rhizome.org/automatic-rain"
    label: "Rhizome Net Art Anthology: Automatic Rain / JODI"
fixes:
  - type: workaround
    description: "Users can manually disable popup blocking per site, but the default-on behavior means most viewers will never see the intended experience."
  - type: none
    description: "The artistic gesture of overwhelming the user's desktop with cascading windows is fundamentally incompatible with modern browser security defaults."
---

Windows XP Service Pack 2 (August 2004) added popup blocking to Internet Explorer. Firefox 1.0 (November 2004) shipped with popup blocking on by default. Other browsers quickly followed.

## What changed

Early net art frequently used `window.open()` as a creative medium. Artists spawned cascading, multiplying, or carefully positioned popup windows to create multi-window compositions that broke out of the single-page frame. JODI's *OSS* (1998) is the canonical example — the work spawns a swarm of popup windows that cascade across the desktop, deliberately overwhelming the browser. With popup blocking on, the work simply does nothing.

The change was driven by the explosion of popup advertising in the early 2000s, which had made the web genuinely unusable. Popup blocking was a necessary and popular reform. But it also eliminated an entire creative vocabulary — the ability of a webpage to open other windows was an expressive capability that artists had used since the mid-1990s.

## Notes

As Rhizome's Net Art Anthology notes of JODI's work: "OSS will not always function properly today, since many browsers are set to block pop-ups, and such intrusions cannot occur at all when browsing on a phone or tablet OS." The popup as creative medium is doubly dead — blocked on desktop, impossible on mobile.
