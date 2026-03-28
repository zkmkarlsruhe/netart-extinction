---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Display_PostScript"
title: "Display PostScript removed from Mac OS X, orphaning NeXT-era applications"
date: "2001-03-24"
dependency: "Display PostScript (DPS)"
event_type: "format-obsolescence"
severity: "total"
summary: "When Apple released Mac OS X 10.0 in March 2001, it replaced NeXTSTEP's Display PostScript rendering engine with Quartz, a PDF-based system. Applications and interactive content built for DPS — including creative tools, visual experiments, and Interface Builder layouts from the NeXT era — lost their rendering foundation."
links:
  - url: "https://en.wikipedia.org/wiki/Display_PostScript"
    label: "Wikipedia: Display PostScript"
  - url: "https://next.fandom.com/wiki/Display_PostScript"
    label: "NeXT Wiki: Display PostScript"
  - url: "https://www.loc.gov/preservation/digital/formats/fdd/fdd000029.shtml"
    label: "Library of Congress: PostScript Format Family"
fixes:
  - type: emulation
    description: "NeXTSTEP can be run in emulators such as Previous (NeXT hardware emulator), preserving access to DPS-based applications in their original environment."
  - type: none
    description: "DPS applications cannot run natively on any current operating system. The PostScript-based rendering model has no modern equivalent outside of print workflows."
---

Display PostScript (DPS) was a 2D graphics engine that used the PostScript imaging model to render on-screen graphics. Developed jointly by NeXT and Adobe and released in 1987, DPS was the display system for NeXTSTEP — the operating system Steve Jobs built after leaving Apple. It was also adopted by several Unix workstation vendors during the late 1980s and 1990s.

## What changed

DPS made the screen a PostScript device: applications could issue PostScript commands to draw text, vector graphics, and images with the same precision as a laser printer. This enabled true WYSIWYG computing — what appeared on screen was exactly what would print. NeXT's Interface Builder used DPS to render interface elements, and creative applications ported to NeXTSTEP (including Adobe Illustrator) leveraged DPS for print-accurate layout and color work.

When Apple acquired NeXT in 1997, it inherited NeXTSTEP as the foundation for Mac OS X. But Apple chose to replace Display PostScript with Quartz, a new rendering engine based on PDF rather than PostScript. The reason was partly licensing — DPS required royalty payments to Adobe — and partly technical, as PDF offered better support for transparency and modern graphics features.

Mac OS X 10.0, released March 24, 2001, shipped with Quartz and no DPS support. Any NeXTSTEP application that issued raw PostScript drawing commands — rather than using the higher-level OpenStep APIs that Apple had ported — would no longer render correctly. Interactive PostScript content, visual experiments that manipulated the PostScript interpreter directly, and tools that depended on DPS-specific features like user paths and encoded number strings were orphaned.

## Notes

DPS occupied a unique position: it was simultaneously a display technology, a programming language, and a creative medium. Programmers and artists on NeXT hardware could write PostScript code that drew directly to the screen in real time — a form of creative coding that predated Processing by over a decade. The second edition of Adobe's PostScript Language Reference Manual documented DPS extensions, but the third edition removed them entirely, signaling Adobe's own abandonment of the technology. Tim Berners-Lee developed the first web browser and server on a NeXT workstation running DPS, making it part of the web's origin story even though DPS itself never reached the web.
