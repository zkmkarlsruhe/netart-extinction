---
ai_generated: true
title: "Java Web Start (.jnlp) removed from Java SE"
date: "2018-09"
dependency: "Java Web Start / JNLP (.jnlp)"
event_type: "format-obsolescence"
severity: "total"
summary: "Oracle deprecated Java Web Start in Java SE 9 (March 2018) and removed it entirely in Java SE 11 (September 2018), rendering .jnlp launcher files permanently non-functional and stranding interactive artworks, creative tools, and generative art pieces that relied on one-click browser-to-desktop deployment."
links:
  - url: "https://www.oracle.com/java/technologies/javase/javaclient-roadmap.html"
    label: "Oracle Java Client Roadmap: Web Start removal"
  - url: "https://en.wikipedia.org/wiki/Java_Web_Start"
    label: "Wikipedia: Java Web Start"
  - url: "https://openwebstart.com/"
    label: "OpenWebStart: community replacement project"
fixes:
  - type: workaround
    description: "OpenWebStart is an open-source reimplementation that can launch some .jnlp files, but compatibility with older applications is inconsistent and it requires manual installation."
  - type: emulation
    description: "Preserve a Java 8 JRE in a virtual machine to run .jnlp applications, though network-dependent features will likely fail."
  - type: none
    description: "For works that relied on the seamless browser-to-application handoff — clicking a link to launch a rich Java application — the user experience cannot be reproduced in any modern environment."
---

## What changed

Java Web Start (JWS), introduced in Java SE 1.2 in 2001, allowed developers to deploy full Java applications via a .jnlp (Java Network Launching Protocol) file linked from a webpage. Clicking the link would download, cache, and launch a Java application outside the browser sandbox — offering the richness of a desktop application with the convenience of a web link. Unlike Java applets, which ran inside the browser, Web Start applications ran as standalone programs but were launched from and updated through the web.

Oracle marked Java Web Start as deprecated in JDK 9 (released September 2017, with the deprecation announced March 2018 in the client roadmap). JDK 11 (September 2018) removed it entirely. Since Oracle simultaneously ended free public updates for Java 8 in January 2019, the only JRE that still supported .jnlp files became a paid commercial product. The format was effectively dead for general users.

The .jnlp format was used extensively by Processing-based artworks and creative coding projects deployed to the web. Ben Fry and Casey Reas's Processing environment used Java Web Start as its primary web deployment mechanism before Processing.js and p5.js emerged. Generative artists distributed interactive sketches as .jnlp links, expecting viewers to click and experience the work. When JWS was removed, these links became dead — the .jnlp XML file still exists but nothing on a modern system knows how to handle it.

The format's death is distinct from the Java applet/NPAPI removal (documented separately). Applets ran inside the browser; Web Start applications ran outside it. An artist who migrated from applets to Web Start in 2008 — following Sun Microsystems' own recommendation — found that migration path also terminated a decade later.
