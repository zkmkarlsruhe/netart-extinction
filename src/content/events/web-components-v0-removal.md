---
ai_generated: true
title: "Web Components v0 and HTML Imports removed from Chrome"
date: "2019-02-05"
dependency: "Web Components v0 APIs (HTML Imports, Custom Elements v0, Shadow DOM v0)"
event_type: "browser-change"
severity: "major"
summary: "Chrome 73 removed Web Components v0 APIs including HTML Imports in February 2019, breaking early web-component-based artworks and Polymer v1 projects."
links:
  - url: "https://www.chromestatus.com/feature/5144752345317376"
    label: "Chrome Platform Status: HTML Imports removal"
  - url: "https://developers.google.com/web/updates/2019/07/web-components-v0-deprecations"
    label: "Google: Web Components v0 deprecation"
---

Web Components v0 was an early set of browser APIs — HTML Imports, Custom Elements v0, and Shadow DOM v0 — that let developers create reusable custom HTML elements. Artists and creative coders adopted these APIs, often via the Polymer v1 library, to build modular, component-based web artworks with encapsulated styling and behavior.

## What changed

Chrome removed HTML Imports in version 73 (February 2019) and deprecated the remaining v0 APIs, completing removal by Chrome 80 (February 2020). The v1 specifications replaced them but are not backward-compatible — HTML Imports were dropped entirely with no v1 equivalent (ES modules are the replacement). Artworks using `<link rel="import">` or v0 custom element registration fail silently or throw errors in modern browsers.

## Notes

HTML Imports were the most disruptive removal because they had no direct successor — the shift to ES modules requires restructuring how components are loaded. Works built with Polymer v1 need significant rewriting to work with modern Lit or vanilla Web Components v1. Most artistic experiments from the 2014-2017 Web Components era were never updated.
