---
title: "Google Maps Platform requires billing account and API key"
date: "2018-06-11"
dependency: "Google Maps Platform"
event_type: "api-shutdown"
severity: "total"
summary: "As of June 11, 2018, access to core Google Maps APIs required a valid API key plus a billing account, pushing map-based artworks into quota, key-management, and cost constraints."
links:
  - url: "https://developers.googleblog.com/introducing-google-maps-platform/"
    label: "Google Developers Blog: Introducing Google Maps Platform"
affected_artworks:
  - artwork: google-is-not-the-map
    severity: total
    status: degraded
    note: "Uses Google's publicly released API code for map-based poetry. Without keys/billing, maps fail or watermark."
  - artwork: liquid-prairie
    severity: total
    status: unknown
    note: "Google Maps API used in narrative documentation. Key requirements can break embedded maps."
  - artwork: in-absentia
    severity: total
    status: unknown
    note: "HTML/JS + Google Maps API for non-linear narrative. Maps API access changes affect navigation and meaning."
fixes:
  - type: workaround
    description: "Add and secure API keys; implement caching and usage monitoring."
  - type: migration
    description: "Replace with open map stacks (OpenStreetMap + Leaflet/MapLibre) when feasible."
  - type: archive
    description: "Preserve 'reference captures' (screens/tiles) to document intended geography."
---

Google consolidated plans into a pay-as-you-go model. Beginning June 11, developers needed an API key and a Google Cloud billing account to access core products, with limited free usage per month.

## Notes

This is a prototypical API monetization extinction: the API still exists, but access conditions changed enough to break artworks.
