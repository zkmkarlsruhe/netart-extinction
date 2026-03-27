---
ai_generated: true
title: "Browsers block third-party cookies by default"
date: "2020-03"
dependency: "Third-party cookies for cross-site state"
event_type: "browser-change"
severity: "minor"
summary: "Safari fully blocked third-party cookies by March 2020 (ITP since 2017), Firefox added Total Cookie Protection, and Chrome began phased deprecation. Multi-domain artworks that shared state via cookies lost cross-site functionality."
links:
  - url: "https://www.infoq.com/news/2020/04/safari-third-party-cookies-block/"
    label: "InfoQ: Safari blocks third-party cookies by default"
  - url: "https://developer.mozilla.org/en-US/blog/goodbye-third-party-cookies/"
    label: "MDN: Saying goodbye to third-party cookies"
fixes:
  - type: migration
    description: "Artworks can migrate to server-side session management, first-party cookies with SameSite attributes, or the Storage Access API."
  - type: none
    description: "The implicit cross-site state sharing that cookies provided has no drop-in replacement."
---

Safari Intelligent Tracking Prevention (ITP) launched in September 2017 and progressively tightened restrictions until fully blocking third-party cookies by March 2020. Firefox added Enhanced Tracking Protection (September 2019) and Total Cookie Protection. Chrome announced deprecation in 2020, though implementation has been delayed.

## What changed

Third-party cookies allowed web pages to share state across different domains — an embedded iframe could read cookies set by its origin site, enabling cross-site authentication, personalization, and state management. When browsers began blocking these cookies by default, multi-domain artworks lost the ability to share state across sites.

Interactive works relying on third-party authentication cookies embedded in iframes, artworks that used cross-site tracking as a creative medium, and multi-domain compositions that shared user state all broke.

## Notes

This is part of a broader trend of browsers enforcing privacy through origin isolation. While driven by legitimate anti-tracking goals, each isolation boundary added by browsers narrows the ways web pages can interact with each other — reducing the creative surface area available to web artists.
