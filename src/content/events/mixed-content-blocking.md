---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Mixed_content"
title: "Mixed-content autoupgrade and blocking"
date: "2019-12-10"
dependency: "Browser mixed-content policy"
event_type: "browser-change"
severity: "major"
summary: "Chrome's rollout (starting Chrome 79) autoupgraded and then blocked HTTP subresources on HTTPS pages, breaking artworks that combine many remote media sources when hosted or archived under HTTPS."
links:
  - url: "https://blog.chromium.org/2019/10/no-more-mixed-messages-about-https.html"
    label: "Chromium Blog: No More Mixed Messages About HTTPS"
affected_artworks:
  - artwork: "photo-noise"
    severity: major
    status: degraded
    note: "Loads remote images discovered via search. If embedded assets resolve to HTTP-only hosts, they may be blocked."
  - artwork: "those-that-will-die"
    severity: major
    status: degraded
    note: "Aggregates third-party media across origins. HTTP-only endpoints or legacy embeds can be blocked in HTTPS context."
  - artwork: "onewordmovie"
    severity: major
    status: degraded
    note: "Pulls large sets of image URLs from the wider web. Mixed-content blocking can silently drop images, altering the film."
fixes:
  - type: workaround
    description: "Rewrite asset URLs to HTTPS, or proxy through an HTTPS 'asset relay' under curatorial control."
  - type: workaround
    description: "Use Content Security Policy directives (upgrade-insecure-requests) during migration testing."
---

Chrome began a phased rollout: introduce per-site unblock settings (Chrome 79, Dec 2019), autoupgrade and block mixed audio/video (Chrome 80, Jan 2020), and autoupgrade/block mixed images (Chrome 81, Feb 2020).

## Notes

Mixed-content is a frequent "archival regression": moving a work to HTTPS (or embedding it in an HTTPS archive player) can break it if its dependencies are still HTTP.
