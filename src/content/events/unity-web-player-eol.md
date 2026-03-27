---
ai_generated: true
title: "Unity Web Player plugin discontinued, web-based Unity content stranded"
date: "2016-07-28"
dependency: "Unity Web Player (NPAPI plugin)"
event_type: "sdk-deprecation"
severity: "total"
summary: "Unity 5.4, released July 28, 2016, permanently dropped Web Player build support, stranding thousands of browser-based games and interactive art pieces that could no longer be published or played via the plugin."
links:
  - url: "https://blog.unity.com/technology/unity-web-player-roadmap"
    label: "Unity Blog: Web Player Roadmap"
  - url: "https://blog.unity.com/technology/web-publishing-following-chrome-npapi-deprecation"
    label: "Unity Blog: Web Publishing Following Chrome NPAPI Deprecation"
  - url: "https://blog.unity.com/technology/unity-5-4-is-out-heres-whats-in-it"
    label: "Unity Blog: Unity 5.4 release announcement"
fixes:
  - type: rebuild
    description: "Rebuild projects targeting Unity WebGL export instead of Web Player. WebGL builds differ significantly: file sizes balloon (20 MB projects became 200-300 MB), networking is restricted, and multithreading is unavailable."
  - type: archive
    description: "Run legacy content in a virtual machine with an old browser that still supports NPAPI (e.g., Firefox 51 or earlier on Windows)."
---

## What changed

Unity Web Player was an NPAPI-based browser plugin that allowed Unity-authored 3D content to run directly in web browsers. Chrome disabled NPAPI by default in April 2015 (Chrome 42) and removed it entirely in September 2015 (Chrome 45). Firefox and Safari followed. Unity responded by shifting to WebGL as the replacement for browser deployment.

Unity 5.2 and 5.3 could still publish Web Player builds, but Unity 5.4 (released July 28, 2016) permanently removed Web Player as a build target. This was not just a browser-side block — the authoring tool itself dropped the capability, meaning creators could no longer compile or update their Web Player projects without downgrading their development environment.

The WebGL replacement was not a drop-in substitute. Web Player content had access to System.Net sockets, multithreading, and produced compact binaries. WebGL builds ran in a JavaScript sandbox with significant restrictions, much larger file sizes, and worse performance on low-end hardware. Many creative projects — particularly interactive art pieces, experimental games, and student works hosted on platforms like Kongregate and itch.io — were never rebuilt for WebGL and simply stopped working as browsers dropped NPAPI support.

## Notes

This event is closely related to the broader NPAPI removal (documented separately), but represents the SDK-side response: Unity Technologies choosing to discontinue the build target rather than maintain it. The distinction matters for preservation — even if NPAPI were somehow restored in a browser, Unity 5.4+ projects have no path back to the Web Player format without the old toolchain.
