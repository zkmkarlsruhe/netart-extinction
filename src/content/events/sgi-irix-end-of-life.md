---
ai_generated: true
title: "SGI IRIX end of life strands CAVE virtual reality artworks"
date: "2006-12-29"
dependency: "SGI IRIX"
event_type: "os-deprecation"
severity: "major"
summary: "SGI ended production of MIPS/IRIX systems on December 29, 2006, with support ending in December 2013, orphaning a generation of immersive VR artworks built for CAVE environments that depended on SGI Onyx hardware and IRIX-specific graphics libraries."
links:
  - url: "https://en.wikipedia.org/wiki/IRIX"
    label: "Wikipedia: IRIX"
  - url: "https://ars.electronica.art/futurelab/en/projects-cave/"
    label: "Ars Electronica Futurelab: CAVE projects"
  - url: "https://www.evl.uic.edu/pape/CAVE/prog/CAVEGuide.html"
    label: "CAVE User's Guide (EVL, University of Illinois at Chicago)"
  - url: "https://tedium.co/2023/05/27/sgi-irix-revival-efforts/"
    label: "Tedium: Can SGI's Enthusiast Community Bring IRIX Back to Life?"
fixes:
  - type: migration
    description: "CAVELib was eventually ported to Linux and Windows, but legacy IRIX-native applications required significant rework to compile against new APIs and different OpenGL implementations."
  - type: emulation
    description: "MAME gained experimental SGI Indy emulation in the 2020s, but performance is insufficient for real-time multi-wall VR rendering."
---

On September 6, 2006, SGI announced the end of the MIPS and IRIX product lines. Production ceased on December 29, 2006, with final system deliveries in March 2007. Support contracts were honored through December 2013, after which no further patches or assistance were available.

## What changed

IRIX was the operating system underpinning the most ambitious immersive art of the 1990s. SGI workstations — particularly the Onyx and Onyx2 with InfiniteReality graphics — powered CAVE (Cave Automatic Virtual Environment) installations at research labs and cultural institutions worldwide. The Electronic Visualization Laboratory (EVL) at the University of Illinois at Chicago, where the CAVE was invented in 1992, ran its systems on IRIX. In 1996, Ars Electronica Center in Linz, Austria opened the world's first publicly accessible CAVE, driven by SGI hardware running IRIX, and presented approximately 50 artistic VR projects between 1996 and 2008, including Maurice Benayoun's "World Skin" (1997 Golden Nica winner) and Peter Kogler's immersive architectural projections.

These artworks were tightly coupled to the IRIX platform. They used SGI's OpenGL Performer for scene-graph rendering, CAVELib for multi-wall projection synchronization, and IRIX-specific audio and input subsystems. When IRIX reached end of life, there was no straightforward migration path. The CAVELib API was eventually made platform-independent for Linux and Windows, but legacy IRIX binaries could not simply be recompiled — they depended on SGI's proprietary graphics pipeline, compiler extensions, and hardware-specific optimizations that had no equivalent on commodity PCs.

By 2009, when Ars Electronica redesigned its center, the original CAVE was retired and replaced by the Deep Space projection environment running on standard PC hardware. The SGI-era VR artworks that had been shown in the CAVE were not migrated; they exist only as documentation, video captures, and memories.

## Notes

The decline of SGI had been gradual — the rise of Linux clusters and the porting of Maya and other creative tools to commodity platforms eroded SGI's market throughout the early 2000s — but the formal end of IRIX support created a hard deadline. Institutions that had maintained aging SGI hardware for legacy art projects lost their last lifeline for replacement parts and OS patches. Today, hobbyist communities maintain IRIX installations on surviving hardware, but these efforts are oriented toward nostalgia and computing history, not the preservation of the VR art that once ran on these machines.
