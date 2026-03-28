---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Instagram"
title: "Instagram API locked down, Basic Display API deprecated"
date: "2024-12-04"
dependency: "Instagram Legacy API / Basic Display API"
event_type: "api-shutdown"
severity: "major"
summary: "In the wake of Cambridge Analytica, Instagram slashed API access in April 2018, then progressively restricted it further until the Basic Display API was fully deprecated in December 2024 — breaking art projects that used Instagram as a live data source."
links:
  - url: "https://techcrunch.com/2018/04/04/facebook-instagram-api-shut-down/"
    label: "TechCrunch: Facebook restricts APIs, axes old Instagram platform"
  - url: "https://developers.facebook.com/blog/post/2024/09/04/update-on-instagram-basic-display-api/"
    label: "Meta: Update on Instagram Basic Display API"
affected_artworks:
  - artwork: "excellences-and-perfections"
    severity: minor
    status: degraded
    note: "The performance itself survives as documentation, but any re-presentation pulling live Instagram data would be broken."
fixes:
  - type: none
    description: "Meta's Instagram Graph API requires business accounts and app review, making casual art integrations impractical."
---

In April 2018, Instagram slashed API rate limits from 5,000 to 200 requests per user per hour and removed endpoints for follower lists, relationships, and public content. The Legacy API was fully retired by March 2020. Then on December 4, 2024, Meta deprecated the Basic Display API entirely.

## What changed

The lockdown happened in three phases. First, the post-Cambridge Analytica panic (April 2018) gutted the API overnight. Second, the Legacy API sunset (2020) removed the last permissive endpoints. Third, the Basic Display API deprecation (2024) cut off personal accounts from external data access entirely.

Art projects that consumed Instagram as a data source — feed-based installations, data visualizations of social behavior, live gallery displays pulling from hashtags — were progressively broken across these phases. The API went from open and permissive to essentially inaccessible for individual artists and small projects.

## Notes

This follows the broader pattern of post-2018 API lockdowns across social platforms, where data access policies optimized for privacy and platform control made artistic and research use of social media APIs effectively impossible without institutional resources.
