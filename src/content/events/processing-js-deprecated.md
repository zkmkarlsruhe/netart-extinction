---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Processing_(programming_language)"
title: "Processing.js deprecated, 100,000+ browser sketches affected"
date: "2018-12-05"
dependency: "Processing.js (Java-to-JavaScript transpiler)"
event_type: "other"
severity: "major"
summary: "Processing.js was officially archived on December 5, 2018. Over 100,000 sketches on OpenProcessing that used the Java-to-JavaScript transpiler broke or degraded, as p5.js — the successor — is a different API, not a drop-in replacement."
links:
  - url: "https://github.com/processing-js/processing-js"
    label: "GitHub: Processing.js (archived)"
  - url: "https://intercom.help/openprocessing/en/articles/3250763-processingjs-deprecation-notice"
    label: "OpenProcessing: Processing.js Deprecation Notice"
fixes:
  - type: migration
    description: "Sketches can be ported to p5.js, but this requires rewriting — p5.js is a different API, not a drop-in replacement for Processing.js."
  - type: workaround
    description: "OpenProcessing still allows running Processing.js sketches with 'limited features' and no further updates."
---

Processing.js, created by John Resig in 2008, automatically transpiled Processing (Java) sketches to run in the browser via HTML5 Canvas. Its GitHub repository was officially archived on December 5, 2018.

## What changed

Processing.js enabled an enormous ecosystem of browser-based creative coding. OpenProcessing hosted over 100,000 sketches using this approach. When Processing.js was deprecated in favor of p5.js (released 2014 by Lauren McCarthy), these existing sketches did not automatically work — p5.js is a reimagining of Processing for the web with a different JavaScript-native API, not a transpiler for Java syntax.

Many sketches on OpenProcessing now display "This sketch is created with an older version of Processing, and doesn't work on browsers anymore." With 100,000+ sketches, most were never ported.

## Notes

This is a case where the successor technology is excellent but intentionally incompatible. p5.js is a thriving creative coding community, but the migration from Processing.js requires rewriting code — even if sometimes only a few lines. For the long tail of unmaintained sketches, that rewrite will never happen.
