---
title: "Google adds X-Frame-Options, blocking iframe embedding of google.com"
date: "2011"
dependency: "Iframe embedding of Google homepage"
event_type: "browser-change"
severity: "total"
summary: "Google added X-Frame-Options headers to google.com, blocking iframe embedding of the Google homepage. Several artworks that framed Google as material — including Constant Dullaart's Revolving Internet series — disappeared overnight."
links:
  - url: "https://rhizome.org/editorial/2018/jul/26/the-revolving-revolution/"
    label: "Rhizome: The Internet's Revolutions"
  - url: "https://artsandculture.google.com/story/the-making-of-rhizome-s-net-art-anthology-constant-dullaart-s-the-revolving-internet-rhizome/zwUR0q_QS8FHKg"
    label: "Google Arts & Culture: The Revolving Internet"
fixes:
  - type: workaround
    description: "Dullaart devised a proxy-based workaround to continue serving the framed Google homepage, but this requires active maintenance and can be blocked by Google at any time."
  - type: none
    description: "X-Frame-Options is enforced by the browser. There is no client-side bypass — the embedding site cannot override the framed site's policy."
---

Around 2011, Google added X-Frame-Options and frame-busting scripts to google.com, preventing any external site from embedding the Google homepage in an iframe. The change happened approximately two weeks after Google's viral "do a barrel roll" Easter egg.

## What changed

Several net artworks used the Google homepage as raw material — framing it inside iframes to rotate, distort, multiply, or otherwise transform the most-visited page on the web. When Google blocked iframe embedding, these works simply broke.

Constant Dullaart's series was the most prominent casualty: *The Revolving Internet* (2010), *The Disagreeing Internet* (2008), *The Doubting Internet* (2010), and *The Sleeping Internet* (2011) all displayed the Google homepage in altered states. Some works were also flagged and blacklisted by Google as phishing threats.

## Notes

This represents a category of extinction where the artwork depends on embedding a third-party site that later adds anti-embedding protections. The X-Frame-Options header (and its successor, Content-Security-Policy frame-ancestors) gives any site unilateral power to break any artwork that frames it. Artists working with found web content have no recourse.
