---
ai_generated: true
title: "Browser autoplay policies block sound-on-load"
date: "2018-04-17"
dependency: "Browser autoplay policy"
event_type: "browser-change"
severity: "major"
summary: "Modern browsers restrict autoplay with sound (Chrome 66 era), breaking net artworks that rely on immediate audio/video or WebAudio on page load unless redesigned around user gestures."
links:
  - url: "https://developer.chrome.com/blog/autoplay"
    label: "Chrome autoplay policy overview"
affected_artworks:
  - artwork: "sign69"
    severity: major
    status: restored
    note: "Randomized animation loops with audio. Audio may not start automatically; experience changes."
  - artwork: "storytelling-machine"
    severity: major
    status: restored
    note: "Flash/HTML animation coupled with audio playback. Autoplay audio blocked; timing/affect shifts."
  - artwork: "singing-bridges"
    severity: minor
    status: degraded
    note: "Embedded audio players (SoundCloud or similar). Autoplay may be disabled; user must press play."
fixes:
  - type: workaround
    description: "Add explicit 'Start / Enable sound' interaction and treat it as part of the work's dramaturgy."
  - type: workaround
    description: "Use muted-first strategies and prompt unmute."
---

Chrome's autoplay policy (launched in Chrome 66, April 17, 2018) generally allows muted autoplay but blocks autoplay with sound unless the user has interacted with the site or meets engagement heuristics.

## Notes

Autoplay changes are reversible only by redesign; you cannot rely on consistent sound-on-load across browsers.
