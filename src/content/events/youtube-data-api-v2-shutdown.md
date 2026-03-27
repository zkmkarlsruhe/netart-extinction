---
title: "YouTube Data API v2 shutdown"
date: "2015-04-20"
dependency: "YouTube Data API v2"
event_type: "api-shutdown"
severity: "major"
summary: "YouTube turned down Data API v2 after a staged retirement plan, with v2 calls later returning HTTP 410 Gone — breaking works and tools that relied on v2 feeds unless migrated to v3."
links:
  - url: "https://www.googblogs.com/bye-bye-youtube-data-api-v2/"
    label: "Bye-bye, YouTube Data API v2 (Apr 20, 2015)"
  - url: "https://developers.google.com/youtube/v3/docs"
    label: "YouTube Data API v3 docs"
affected_artworks:
  - artwork: those-that-will-die
    severity: total
    status: degraded
    note: "Sniffs/aggregates YouTube media to generate an 'infinite intimacy movie'. APIs for retrieval stop returning data."
  - artwork: hello-world
    severity: major
    status: unknown
    note: "Uses large pools of online video. If the work depends on API-based retrieval, v2 shutdown breaks ingestion."
  - artwork: seven-video-responses
    severity: major
    status: unknown
    note: "YouTube-era video contexts and embeds. Embed/API behavior changes can break playback or listing."
  - artwork: vvebcam
    severity: major
    status: degraded
    note: "Originally published on YouTube. Platform policy removals + embed changes can de-list the work."
fixes:
  - type: migration
    description: "Migrate retrieval to YouTube Data API v3; re-auth and re-budget quotas."
  - type: archive
    description: "Archive videos and metadata (IDs, titles, descriptions) to avoid total dependence on live platform availability."
---

YouTube announced v2 retirement and, after April 20, 2015, began returning warning feeds and then HTTP 410 Gone for most v2 calls. Migration to v3 required new auth patterns and quota accounting.

## Notes

YouTube-related extinctions combine API shutdowns with platform moderation, geo-restrictions, and embed churn; separating these causes is often a key conservation task.
