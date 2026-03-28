---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Polymer_(library)"
title: "Google deprecates Polymer in favor of Lit, orphaning Web Components-based creative projects"
date: "2018-08"
dependency: "Polymer (Google Web Components library)"
event_type: "sdk-deprecation"
severity: "minor"
summary: "Google placed Polymer and all Polymer elements into maintenance mode in mid-2018, redirecting development to the new lit-html and LitElement libraries; projects built with Polymer's two-way data binding and HTML Imports could not migrate without significant rewrites."
links:
  - url: "https://www.polymer-project.org/blog/2018-10-02-webcomponents-v0-deprecations"
    label: "Polymer Project: Web Components v0 Deprecations"
  - url: "https://lit.dev/articles/lit-for-polymer-users/"
    label: "Lit: Guide for Polymer Users"
  - url: "https://github.com/nicholasgasior/nicholasgasior.github.io/issues/1"
    label: "Example: Polymer portfolio site broken by deprecation"
fixes:
  - type: migration
    description: "Polymer projects can be migrated to Lit incrementally -- first converting to Polymer 3 (npm/JS modules), then rewriting components as LitElement classes. The two libraries can coexist during migration."
  - type: workaround
    description: "Polymer 3 continues to function in modern browsers for now, but receives only critical bug fixes and no new features."
---

Polymer was Google's flagship library for building web applications using Web Components. First released in 2013, it was prominently featured at Google I/O and used in Google's own products. In mid-2018, alongside the release of Polymer 3.0, Google announced that all Polymer elements were placed into "maintenance mode" -- critical bug fixes only, no new development. The team shifted focus to lit-html and LitElement (later consolidated as Lit).

## What changed

Polymer's deprecation was compounded by the simultaneous deprecation of Web Components v0, the underlying browser APIs that Polymer 1.x and 2.x were built on. Chrome removed HTML Imports support in Chrome 73 (March 2019), which was the mechanism Polymer originally used to load components. Projects that had not upgraded to Polymer 3 (which used ES modules instead of HTML Imports) broke in the browser with no code changes on the developer's part.

For creative web projects, Polymer had been used to build interactive portfolios, data visualization dashboards, and experimental web apps that leveraged Web Components for encapsulated, reusable UI elements. Google's own promotion of Polymer at developer conferences and through codelabs had encouraged adoption in creative tech circles. The shift to Lit required rewriting data binding logic (Polymer's two-way binding has no Lit equivalent), replacing observers with reactive properties, and restructuring template syntax.

The long tail of Polymer-based personal sites, creative project pages, and experimental web apps that were deployed and never updated gradually degraded as HTML Imports were removed and Web Components v0 APIs disappeared from browsers.

## Notes

This event illustrates a pattern where a major technology company promotes a framework, builds community adoption, then deprecates it in favor of a successor that is technically superior but migration-incompatible. The creative web suffers disproportionately because art projects and experiments are rarely maintained after their initial deployment.
