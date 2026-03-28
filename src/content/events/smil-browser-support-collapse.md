---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Synchronized_Multimedia_Integration_Language"
title: "SMIL multimedia presentations lose browser and player support"
date: "2015-08"
end_date: "2016"
dependency: "SMIL (Synchronized Multimedia Integration Language)"
event_type: "format-obsolescence"
severity: "major"
summary: "Google Chrome announced intent to deprecate SMIL in August 2015, and while the deprecation was suspended in 2016, SMIL as a standalone multimedia presentation format had already lost its ecosystem — RealPlayer and Internet Explorer, the primary SMIL players, were gone, and no browser ever implemented the full SMIL 3.0 specification for timed multimedia."
links:
  - url: "https://groups.google.com/a/chromium.org/g/blink-dev/c/5o0yiO440LM/m/YGEJBsjUAwAJ"
    label: "Chrome Blink-dev: Intent to deprecate SMIL"
  - url: "https://css-tricks.com/smil-is-dead-long-live-smil-a-guide-to-alternatives-to-smil-features/"
    label: "CSS-Tricks: SMIL is dead! Long live SMIL!"
  - url: "https://en.wikipedia.org/wiki/Synchronized_Multimedia_Integration_Language"
    label: "Wikipedia: SMIL"
  - url: "https://loc.gov/preservation/digital/formats/fdd/fdd000572.shtml"
    label: "Library of Congress: SMIL format description"
  - url: "https://www.w3.org/AudioVideo/"
    label: "W3C Synchronized Multimedia home page"
fixes:
  - type: none
    description: "Full SMIL presentations (timed multimedia with layout, transitions, and synchronized audio/video) have no modern playback path in browsers. SVG SMIL animation attributes remain supported but represent only a fraction of the specification."
  - type: archive
    description: "SMIL files are XML-based and can be preserved as text, but the multimedia assets they reference and the synchronized playback experience cannot be faithfully reproduced without a SMIL-capable player."
affected_artworks:
  - artwork: "latitudes"
    severity: total
    status: degraded
---

SMIL (Synchronized Multimedia Integration Language), a W3C standard first published in 1998, was designed to be the HTML of multimedia — a declarative XML language for authoring timed, synchronized presentations combining text, images, audio, video, and animations with spatial layout and transitions.

## What changed

SMIL was supported in RealPlayer (which used SMIL for its multimedia presentation layer), Internet Explorer (via HTML+TIME, a Microsoft implementation of SMIL's timing model), and the Ambulant open-source player. The W3C published SMIL 1.0 in 1998, SMIL 2.0 in 2001, and SMIL 3.0 in 2008. Artists and researchers used SMIL to create time-based web presentations — synchronized slideshows, interactive documentaries, captioned video experiences, and accessible multimedia — without Flash or JavaScript.

But no major browser ever implemented the full SMIL specification natively. Firefox, Chrome, and Safari implemented only the SVG animation subset of SMIL (the `<animate>`, `<animateTransform>`, and related elements within SVG). The broader SMIL features — timed layout regions, parallel and sequential media scheduling, transition effects, adaptive bandwidth selection — were never available in browsers without plugins.

When RealPlayer's market share collapsed in the mid-2000s and Internet Explorer dropped HTML+TIME support, standalone SMIL presentations lost their primary playback environments. In August 2015, Chrome published an "Intent to Deprecate: SMIL" notice, proposing to remove even SVG SMIL animation support in favor of CSS Animations and the Web Animations API. After pushback from the web development community — who pointed out that certain SVG animation capabilities had no CSS equivalent — Chrome suspended the deprecation in 2016. SVG SMIL attributes survive in browsers today, but full SMIL multimedia presentations remain unplayable.

## Notes

SMIL's fate is unusual: it was a W3C Recommendation (the highest level of web standard) that never achieved the browser implementation needed to sustain it. The full SMIL specification addressed problems — accessible timed media, bandwidth-adaptive streaming, declarative multimedia authoring — that the web industry eventually solved with JavaScript frameworks, DASH/HLS streaming, and HTML5 video. But SMIL presentations authored in the early 2000s, particularly those created for RealPlayer or the Ambulant player in academic and artistic contexts, have no modern playback path. The Ambulant player project, developed at CWI Amsterdam, was one of the last open-source SMIL players but has not been actively maintained.
