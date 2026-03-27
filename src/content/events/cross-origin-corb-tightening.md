---
ai_generated: true
title: "Cross-origin protections tighten (CORB and Private Network Access)"
date: "2018-05-29"
dependency: "CORS/CORB browser security"
event_type: "browser-change"
severity: "major"
summary: "Chrome-era cross-origin hardening (CORB) and later Private Network Access restrictions reduce what browser code can read or request cross-origin, breaking works that sniff, scrape, or assemble media across domains."
links:
  - url: "https://www.chromium.org/Home/chromium-security/corb-for-developers/"
    label: "CORB for developers"
  - url: "https://developer.chrome.com/blog/private-network-access-update"
    label: "Private Network Access update"
affected_artworks:
  - artwork: those-that-will-die
    severity: total
    status: degraded
    note: "Cross-origin 'sniffing' of YouTube/Flickr-like sources. Browser blocks reads/requests."
  - artwork: onewordmovie
    severity: major
    status: degraded
    note: "Aggregates many remote images in rapid sequence. Cross-origin barriers increase."
  - artwork: ellsworth-kelly-hacked-my-twitter
    severity: major
    status: unknown
    note: "Reads platform data and media across origins. Cross-origin API constraints compound platform lock-ins."
fixes:
  - type: workaround
    description: "Move cross-origin fetching to a server-side component under curatorial control; emit clean CORS headers."
  - type: workaround
    description: "Correct MIME types and enable appropriate CORS on owned endpoints."
---

CORB blocks certain cross-origin responses from being delivered to web contexts when they might leak sensitive data. Later, Private Network Access restricts requests from public sites to private network resources.

## Notes

Cross-origin changes don't "kill the web," but they do kill a class of artworks that treated the browser as a permissive data-mining agent.
