---
title: "Heroku eliminates free tier, hobby projects go offline"
date: "2022-11-28"
dependency: "Heroku free dynos / free Postgres"
event_type: "platform-shutdown"
severity: "major"
summary: "Salesforce-owned Heroku permanently discontinued free dynos, free Postgres, and free Redis, forcing millions of hobby web apps offline — including creative coding experiments, art bots, and small-scale web art that relied on free hosting."
links:
  - url: "https://techcrunch.com/2022/08/25/heroku-announces-plans-to-eliminate-free-plans-blaming-fraud-and-abuse/"
    label: "TechCrunch: Heroku announces plans to eliminate free plans"
  - url: "https://www.theregister.com/2022/08/25/heroku_delete_inactive_free_tier/"
    label: "The Register: Heroku to shut down free tier"
fixes:
  - type: migration
    description: "Projects could migrate to alternatives like Railway, Render, or Fly.io, many of which offered free tiers — but migration required active maintainers."
  - type: none
    description: "Unmaintained projects with no active developer went dark permanently."
---

On November 28, 2022, Heroku permanently removed its free tier — free dynos, free Heroku Postgres, and free Heroku Redis — citing fraud and abuse. The minimum hosting cost jumped to $5–7/month per dyno.

## What changed

Heroku's free tier had been the default deployment target for small creative web projects for over a decade. Twitter bots, Mastodon bots, data visualizations, generative art servers, interactive web experiments, and creative coding projects used free dynos as "set and forget" hosting. Many of these projects had no active maintainer — they were launched, shared, and left running indefinitely on the assumption that free meant permanent.

When the free tier was removed, projects without an active developer to migrate them simply went offline. The scale of loss is difficult to quantify because many of these were small, personal, undocumented projects.

## Notes

Alternative platforms (Railway, Render, Fly.io) absorbed some migrations, but the pattern repeats: free tiers attract creative experimentation, then disappear when the business model shifts, taking unmaintained work with them.
