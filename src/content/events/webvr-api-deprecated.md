---
ai_generated: true
title: "WebVR API deprecated in favor of WebXR"
date: "2019"
end_date: "2020"
dependency: "WebVR browser API"
event_type: "browser-change"
severity: "major"
summary: "The WebVR API was deprecated and replaced by WebXR, breaking backwards compatibility by design. WebVR art experiences and demos do not work on modern VR headsets without migration to the WebXR API. Unmaintained WebVR art sites are permanently broken."
links:
  - url: "https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API"
    label: "MDN: WebVR API (deprecated)"
  - url: "https://developers.meta.com/horizon/documentation/web/port-vr-xr/"
    label: "Meta: Porting WebVR to WebXR"
fixes:
  - type: migration
    description: "WebVR code can be ported to WebXR. A-Frame, Babylon.js, and THREE.js frameworks updated their APIs. A WebXR polyfill exists for backwards compatibility."
  - type: none
    description: "Unmaintained WebVR sites with no active developer will remain broken on modern VR headsets."
---

The WebVR API was deprecated in favor of WebXR starting in 2019. WebVR was never ratified as a formal web standard — it existed as an experimental API that browsers progressively dropped.

## What changed

WebVR and WebXR are intentionally incompatible APIs. WebXR unified VR and AR under a single interface with a different session management model, input handling, and reference space system. WebVR demos and art experiences do not work on modern VR headsets (e.g., Meta Quest 2/3) without code changes.

Frameworks like A-Frame, Babylon.js, and THREE.js updated to WebXR, so projects built on these frameworks have a migration path. But standalone WebVR experiments — often single-file HTML art pieces — require manual porting by their original developers.

## Notes

The WebVR-to-WebXR transition represents the tension between standards improvement and preservation. WebXR is a better API, but its adoption broke the first generation of browser-based VR art — an ironic outcome for a medium that was supposed to be more durable than native VR apps.
