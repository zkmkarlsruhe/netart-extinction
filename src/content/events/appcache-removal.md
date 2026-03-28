---
ai_generated: true
title: "Application Cache (AppCache) removed from browsers"
date: "2021-09-14"
dependency: "HTML5 Application Cache (AppCache) API"
event_type: "browser-change"
severity: "major"
summary: "Browsers removed support for the Application Cache API in 2021, breaking offline-capable web artworks that used AppCache manifest files."
links:
  - url: "https://web.dev/articles/appcache-removal"
    label: "web.dev: AppCache removal"
  - url: "https://developer.mozilla.org/en-US/docs/Web/HTML/Using_the_application_cache"
    label: "MDN: Application Cache (deprecated)"
---

The Application Cache (AppCache) was an HTML5 feature that let web applications specify resources for offline use via a manifest file. Web artists used it to create self-contained offline artworks that could be "installed" in a browser and experienced without a network connection — a form of browser-native distribution that felt closer to software than websites.

## What changed

Chrome removed AppCache in version 93 (September 14, 2021) after a gradual deprecation. Firefox and other browsers followed similar timelines. The replacement technology is Service Workers, which offer more powerful offline capabilities but require significant code rewriting. Artworks using AppCache manifests no longer cache for offline use; in some cases, cached resources fail to load entirely, breaking the work even when online.

## Notes

AppCache was attractive to artists precisely because of its simplicity — a single manifest file listing resources to cache. Service Workers require JavaScript programming, a different mental model, and HTTPS. The migration path is non-trivial, and many artists who created offline web art in the AppCache era have not updated their works.
