---
ai_generated: true
title: "Google AJAX/Search APIs discontinued"
date: "2014-05-01"
dependency: "Google Search APIs"
event_type: "api-shutdown"
severity: "major"
summary: "Google deprecated the AJAX Search APIs and related search endpoints on a multi-year schedule, forcing works that relied on programmatic search to migrate, cache results, or replace the data source."
links:
  - url: "https://groups.google.com/g/Google-AJAX-Search-API/c/Ao9TbQbYgHo"
    label: "Discontinuation discussion + official deprecation references"
  - url: "https://developers.googleblog.com/image-results-now-available-from-the-custom-search-api/"
    label: "Custom Search API: image results announcement"
affected_artworks:
  - artwork: "photo-noise"
    severity: total
    status: dead
    note: "Uses the Google API to search in real time for camera-typed photos. Search calls fail or require migration."
  - artwork: "onewordmovie"
    severity: total
    status: degraded
    note: "Builds films from image-search results. Live image pipeline breaks under API restrictions/quotas."
  - artwork: "im-google"
    severity: major
    status: degraded
    note: "Depends on Google Image Search result ecology. Shifts in search access/ranking change the work's material."
  - artwork: "adding-to-the-internet"
    severity: major
    status: restored
    note: "Responds to 'no results' Google image searches. If search behavior/UI/API changes, the condition changes."
fixes:
  - type: migration
    description: "Migrate to a keyed API (Custom Search JSON API) with caching and a 'frozen corpus' mode."
  - type: archive
    description: "Preserve the work as a database of past searches (store URLs + thumbnails + metadata) to reduce dependence on live search."
  - type: workaround
    description: "Replace Google with alternate image sources (institutional APIs, open datasets, self-hosted archives)."
---

Google's AJAX Search API family was deprecated and then discontinued on a three-year policy horizon. Unauthenticated or previously permissive search endpoints stopped working, and developers were pushed toward API keys, quotas, and narrower services.

## Notes

Search-API extinctions can be partial: the artwork "runs" but becomes empty (no media returned), or becomes prohibitively rate-limited.
