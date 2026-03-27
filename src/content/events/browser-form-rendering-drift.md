---
ai_generated: true
title: "Browser native UI rendering drifts from original form element aesthetics"
date: "2006"
end_date: "2012"
dependency: "OS-native HTML form element rendering"
event_type: "browser-change"
severity: "major"
summary: "Browsers progressively replaced OS-native widget rendering of HTML form elements (dropdowns, checkboxes, scrollbars, buttons) with custom-drawn versions. Artworks that used form elements as their medium — like Alexei Shulgin's Form Art (1997) — became nearly unrecognizable."
links:
  - url: "https://artsandculture.google.com/story/form-art-preserving-the-browser-with-oldweb-today/ewUhHbXmUf76Kw"
    label: "Google Arts & Culture: Form Art"
  - url: "https://anthology.rhizome.org/form-art"
    label: "Net Art Anthology: Form Art"
affected_artworks:
  - artwork: form-art
    severity: total
    status: degraded
    note: "Designed for Netscape 3 form elements. Nearly unrecognizable in modern browsers — the 'material' of the work has changed."
fixes:
  - type: emulation
    description: "Rhizome's oldweb.today tool can render the work in emulated period browsers, restoring the original form element appearance."
  - type: none
    description: "No modern browser renders form elements like Netscape 3 or IE 4. The visual language of OS-native widgets is extinct in browsers."
---

From approximately 2006 to 2012, browsers progressively shifted from rendering HTML form elements (dropdown menus, radio buttons, checkboxes, scrollbars, text inputs, buttons) using the host operating system's native widget toolkit to using custom browser-drawn versions.

## What changed

This was not a single event but a gradual mutation. Each browser version subtly changed how native UI controls looked — rounded corners replaced sharp ones, shadows appeared and disappeared, scrollbar styles evolved, button rendering diverged from the operating system's look. The changes were invisible to most users but devastating to artworks that used form elements as their primary visual material.

Alexei Shulgin's *Form Art* (1997) composed visual arrangements entirely from HTML form elements — radio buttons, checkboxes, dropdown menus, scrollbars, text inputs, and buttons arranged as abstract compositions. As Rhizome's preservation notes document: "Even when an old website remains technically intact, like Form Art, it can be rendered unrecognizable by changing software." The work was designed for Netscape 3 and is nearly unrecognizable in modern browsers.

## Notes

This is the most insidious category of extinction: the artwork "works" — no errors, no missing plugins, no broken links — but it looks completely different. The medium itself has mutated. Rhizome's oldweb.today tool, which runs emulated period browsers, is the primary preservation approach.
