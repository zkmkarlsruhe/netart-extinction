---
ai_generated: true
title: "Google Maps JavaScript API v2 retired"
date: "2021-05-26"
dependency: "Google Maps JavaScript API v2"
event_type: "api-shutdown"
severity: "major"
summary: "Google retired the Maps JavaScript API v2 on May 26, 2021, breaking locative and cartographic net art that had not migrated to v3."
links:
  - url: "https://developers.google.com/maps/documentation/javascript/v2/v2tov3"
    label: "Google: Migrating from v2 to v3"
  - url: "https://cloud.google.com/blog/products/maps-platform/google-maps-platform-101-how-to-get-started"
    label: "Google Maps Platform billing and key requirements"
---

The Google Maps JavaScript API v2 launched in 2006 and became the foundation for a wave of locative media art, psychogeographic mapping projects, and cartographic interventions. Artists embedded custom map layers, placemarks, and interactive overlays using the v2 API's relatively simple interface.

## What changed

Google deprecated the Maps JS API v2 in 2011, encouraging migration to v3, but kept v2 running for years. On May 26, 2021, v2 was fully retired. All pages loading the v2 script received errors instead of maps. Artworks had to be rewritten for v3, which also requires a billing-enabled API key (free tier with limits) — a second barrier that did not exist in the v2 era when API keys were optional and free.

## Notes

The double impact — API incompatibility plus mandatory billing — means that even artists willing to update their code face an ongoing cost. Many locative artworks from the 2006-2011 period were created by artists who have since moved on and have no interest in maintaining API keys or rewriting JavaScript. These works now display grey boxes or error messages where maps once appeared.
