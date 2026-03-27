---
ai_generated: true
title: "Google Images removes View Image button and direct image URLs"
date: "2018-02-15"
dependency: "Google Image Search direct image links"
event_type: "api-shutdown"
severity: "major"
summary: "Google removed the 'View Image' button and 'Search by Image' from Image Search results after a settlement with Getty Images — breaking art projects that depended on direct image URLs from search results and causing a 63% drop in image search referrals."
links:
  - url: "https://searchengineland.com/google-image-search-removes-view-image-button-search-image-feature-292183"
    label: "Search Engine Land: Google removes View Image button"
  - url: "https://petapixel.com/2018/02/16/google-removes-view-image-button-image-search-protect-photos/"
    label: "PetaPixel: Google removes View Image button"
affected_artworks:
  - artwork: "im-google"
    severity: major
    status: degraded
    note: "Depends on Google Image Search result ecology. Changes to how results are displayed and linked alter the material basis of the curation process."
  - artwork: "photo-noise"
    severity: major
    status: degraded
    note: "Uses Google API for real-time image search. Already broken by the 2014 API shutdown; the 2018 changes made workaround scraping approaches harder."
  - artwork: "onewordmovie"
    severity: major
    status: degraded
    note: "Builds films from image search results. The live image pipeline was already degraded; removal of direct image links compounds the problem."
  - artwork: "adding-to-the-internet"
    severity: minor
    status: restored
    note: "Responds to 'no results' Google image searches. Changes to search UI and behavior affect whether the triggering condition occurs."
fixes:
  - type: none
    description: "No official replacement for direct image URLs in search results. The change was driven by a legal settlement with Getty Images and is unlikely to be reversed."
---

On February 15, 2018, Google removed both the "View Image" button and the "Search by Image" button from Google Image Search results. This was the result of a settlement with Getty Images, which had filed a competition complaint alleging Google's image search facilitated piracy.

## What changed

Users could no longer directly access full-resolution image URLs from search results — they were forced to visit the hosting webpage instead. Google also introduced complex double-URL-encoding of image source URLs in the page source, making even scraping-based workarounds unreliable.

Analysis of 87 domains showed a 63% decrease in image search referrals after the change, with some publishers seeing declines of nearly 80%. For art projects that treated Google Image Search as a live data source or creative medium, this was a second wave of breakage after the 2014 API shutdown (already documented as a separate event).

## Notes

This event is distinct from the Google Search API discontinuation (2011–2014). That killed programmatic access; this killed the visual/interactive relationship between search results and source images that several net artworks depended on as creative material.
