---
ai_generated: true
title: "QuickTime VR and QuickTime web plugin killed"
date: "2016-04"
dependency: "Apple QuickTime VR / QuickTime browser plugin"
event_type: "plugin-eol"
severity: "total"
summary: "QuickTime X dropped QTVR support in 2009, Apple removed the QuickTime browser plugin in 2015, and ended all QuickTime for Windows support in April 2016 with US-CERT urging immediate uninstall. Interactive 360-degree panoramas and object movies became unviewable."
links:
  - url: "https://www.cisa.gov/news-events/alerts/2016/04/14/apple-ends-support-quicktime-windows-new-vulnerabilities-announced"
    label: "CISA: Apple Ends Support for QuickTime for Windows"
  - url: "https://en.wikipedia.org/wiki/QuickTime_VR"
    label: "Wikipedia: QuickTime VR"
fixes:
  - type: migration
    description: "QTVR panoramas can theoretically be converted to modern WebXR or panoramic viewer formats, but the conversion requires extracting source tiles from the proprietary .mov container."
  - type: none
    description: "No modern browser or media player supports QTVR. The interactive navigation experience is lost without conversion."
---

Apple's QuickTime VR (QTVR) died in stages. QuickTime X (2009, Mac OS X Snow Leopard) dropped QTVR support entirely. Apple removed the QuickTime browser plugin via a security update in August 2015. In April 2016, Apple ended all QuickTime for Windows support, and US-CERT issued advisory TA16-105A urging immediate uninstall due to unpatched zero-day vulnerabilities.

## What changed

QTVR (launched 1995) created interactive 360-degree panoramas and "object movies" — rotatable 3D views of objects — viewable in browsers via the QuickTime plugin. It was used extensively for virtual museum tours, architectural visualization, cultural heritage documentation, and by artists exploring immersive/panoramic photography.

The .mov container with QTVR nodes is now unplayable in any current browser or modern QuickTime. Columbia University's CCNMTL and numerous academic institutions had QTVR-based cultural heritage projects that are now inaccessible. Artists who created fictional or impossible panoramic spaces using QTVR lost their exhibition medium.

## Notes

QTVR was a precursor to today's WebXR and 360-degree video, but with a fundamentally different interaction model — discrete tile-based navigation rather than continuous streaming. The specific aesthetic of QTVR panoramas (their particular compression artifacts, their click-and-drag navigation feel) has no modern equivalent.
