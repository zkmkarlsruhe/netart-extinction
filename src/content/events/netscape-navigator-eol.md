---
ai_generated: true
title: "Netscape Navigator reaches end of life"
date: "2008-03-01"
dependency: "Netscape Navigator browser"
event_type: "browser-change"
severity: "total"
summary: "AOL officially ended support for Netscape Navigator on March 1, 2008, after years of decline following the 1998 acquisition. Netscape-specific features — the <layer> tag, document.layers, server push, and its unique CSS implementation — had no successor in modern browsers."
links:
  - url: "https://www.computerworld.com/article/1573224/rip-aol-kills-netscape.html"
    label: "Computerworld: RIP — AOL kills Netscape"
  - url: "https://en.wikipedia.org/wiki/Netscape"
    label: "Wikipedia: Netscape"
affected_artworks:
  - artwork: mouchette
    severity: minor
    status: degraded
    note: "Originally authored for Netscape-era browsers. Some interactive behaviors relied on Netscape-specific DOM and rendering."
fixes:
  - type: emulation
    description: "Rhizome has used remote Netscape 3 browser instances to present period-accurate renderings of early net art."
  - type: none
    description: "Netscape-specific HTML tags (<layer>, <ilayer>) and JavaScript APIs (document.layers) have no equivalent in modern browsers."
---

AOL officially ended support for Netscape Navigator on March 1, 2008. The final release was version 9.0.0.6 (February 20, 2008). Netscape had been declining since AOL's $4.2 billion acquisition in November 1998, and the Netscape division was closed in 2003.

## What changed

Netscape Navigator introduced proprietary features that became part of the creative vocabulary of early net art:

- **`<layer>` and `<ilayer>` tags** (Netscape 4 only) — used for DHTML absolute/relative positioning before CSS positioning was standardized
- **`document.layers`** — Netscape's DOM model for accessing positioned elements, incompatible with IE's `document.all`
- **Server push** via `multipart/x-mixed-replace` — used for webcam art, live updating pages, and proto-streaming before AJAX existed
- **Netscape's CSS implementation** — fundamentally different from IE's, leading to the "browser wars" era where pages looked completely different in each browser

Many net artworks from 1995–2000 were explicitly authored for Netscape. Olia Lialina's *My Boyfriend Came Back From the War* (1996) is now presented by Rhizome using a remote Netscape 3 browser appropriate to the period of its launch.

## Notes

The death was gradual — Netscape became irrelevant by ~2002–2003, but the 2008 EOL is the official date. Mozilla Firefox inherited Netscape's Gecko rendering engine but did not carry forward any of the proprietary Netscape-specific features. The browser wars gave net artists a rich, if chaotic, landscape of rendering differences to exploit. That landscape has been steadily flattened since.
