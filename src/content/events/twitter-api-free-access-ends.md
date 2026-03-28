---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Twitter"
title: "Free X/Twitter API access ends"
date: "2023-02-09"
dependency: "X/Twitter API"
event_type: "api-shutdown"
severity: "total"
summary: "On Feb 9, 2023, the platform ended free API access and introduced paid tiers and stricter limits, breaking many bots and live-feed artworks unless they paid, reduced scope, or migrated off-platform."
links:
  - url: "https://devcommunity.x.com/t/starting-february-9-twitter-will-no-longer-support-free-access-to-the-twitter-api/184611"
    label: "X Developers announcement (Feb 2023)"
  - url: "https://docs.x.com/x-api/getting-started/about-x-api"
    label: "X API access tiers / pricing"
affected_artworks:
  - artwork: "schwitters-on-twitter"
    severity: total
    status: degraded
    note: "Automated tweeting via Twitter4J. Bot posting/retrieval fails without valid paid API access."
  - artwork: "tweeting-colors"
    severity: total
    status: unknown
    note: "Reads public tweets to generate visual bars. Live ingestion breaks if endpoint access removed."
  - artwork: "ellsworth-kelly-hacked-my-twitter"
    severity: total
    status: unknown
    note: "Real-time chart from the artist's feed. Feed retrieval breaks without API access."
  - artwork: "date-paintings-twitter"
    severity: major
    status: unknown
    note: "Relies on tweet timestamps and platform time display. If posting/retrieval constrained, the work's core rule-set collapses."
  - artwork: "pentametron"
    severity: total
    status: unknown
    note: "Bot reads tweets and posts/retweets on a schedule. Bots often require paid access or dramatically reduced cadence."
fixes:
  - type: workaround
    description: "Pay for an API tier and refactor to fit new quotas; add caching/backoff."
  - type: migration
    description: "Re-platform: publish outputs to a self-hosted site, RSS/ActivityPub, or other APIs."
  - type: archive
    description: "Capture the bot's output stream and code; emulate 'live' behavior from archived datasets."
---

X/Twitter announced that starting Feb 9, 2023 it would no longer support free API access (v2 and v1.1), shifting to paid tiers and later deprecating legacy access packages. This changed the economic and technical viability of artworks that depended on continuous reading/writing of timelines.

## What changed

This event is highly relevant for contemporary net art because "platform-as-medium" works tend to be operationally fragile under pricing and policy shifts. It affected not just individual artworks but entire genres of creative practice (Twitter bots, data visualizations, sentiment analyses).
