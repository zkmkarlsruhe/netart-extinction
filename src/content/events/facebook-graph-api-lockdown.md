---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Facebook_Platform"
title: "Facebook Graph API restrictions and platform lockdown"
date: "2018-04-04"
dependency: "Facebook Graph API"
event_type: "terms-of-service"
severity: "major"
summary: "In 2018, Facebook announced major platform changes that limited data access and tightened permissions/app review, causing projects that depended on broad graph access to fail or require redesign."
links:
  - url: "https://developers.facebook.com/blog/post/2018/04/04/facebook-api-platform-product-changes/"
    label: "Meta: update on platform changes (Apr 2018)"
  - url: "https://developers.facebook.com/docs/graph-api/changelog/"
    label: "Graph API changelog"
affected_artworks:
  - artwork: "face-to-facebook"
    severity: major
    status: degraded
    note: "Relies on Facebook as data-source. Increased controls reduce feasibility and increase takedown risk."
fixes:
  - type: workaround
    description: "Reduce scope: shift from live friend-graph access to user-consented exports or curated datasets."
  - type: archive
    description: "Preserve as 'performed documentation' (screen capture + datasets + code) when live operation is no longer feasible."
---

Facebook reduced access to several categories of data and placed stronger requirements on apps (permissions, review, compliance monitoring). This made "social graph as material" artworks harder to run live, especially those relying on friend/relationship/event data or broad search.

## Notes

This entry is framed as a platform-policy extinction mode. Future submissions should add concrete artworks with confirmed Graph API dependencies (endpoint + version + permission set).
