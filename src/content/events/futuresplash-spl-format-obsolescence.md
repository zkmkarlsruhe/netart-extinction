---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/FutureSplash_Animator"
title: "FutureSplash (.spl) format becomes unplayable"
date: "2021-01"
dependency: "FutureSplash Animator (.spl) format"
event_type: "format-obsolescence"
severity: "total"
summary: "FutureSplash Animator's .spl format, the direct predecessor to Flash, was nominally supported by Flash Player through backward compatibility — but when Adobe killed Flash Player on January 12, 2021, .spl files lost their last remaining playback path, and the format's distinct compression and animation characteristics are not handled by modern Flash emulators like Ruffle."
links:
  - url: "https://en.wikipedia.org/wiki/Adobe_Animate#FutureSplash_Animator"
    label: "Wikipedia: FutureSplash Animator history"
  - url: "https://web.archive.org/web/19970701000000*/futurewave.com"
    label: "Wayback Machine: FutureWave Software website"
  - url: "https://www.ruffle.rs/"
    label: "Ruffle: Flash emulator (limited .spl support)"
fixes:
  - type: emulation
    description: "Run in a virtual machine with a pre-2021 Flash Player installation. Some .spl files may play if Flash Player's legacy compatibility layer handles them."
  - type: workaround
    description: "Ruffle, the open-source Flash emulator, can handle some early SWF content but has incomplete support for the oldest FutureSplash-era features and the .spl container format itself."
  - type: none
    description: "The FutureSplash Animator authoring tool has not been available since Macromedia acquired FutureWave in December 1996. Source .spl files cannot be edited."
---

## What changed

FutureSplash Animator was created by FutureWave Software and released in May 1996. It was a vector animation tool for the web at a time when the web was almost entirely static. The software produced .spl files — compact vector animations that played in the FutureSplash Viewer browser plugin. In December 1996, Macromedia acquired FutureWave and rebranded FutureSplash Animator as Macromedia Flash 1.0, with the .spl format evolving into .swf.

The .spl format was used for some of the earliest animated content on the web. MSN and Disney Online were notable early adopters in 1996. Early web artists experimenting with animation and interactivity before Flash became dominant created works in FutureSplash. These .spl files were technically a predecessor to .swf but used a slightly different container format and feature set from the very first version of Flash.

Flash Player maintained backward compatibility with .spl files for years, but this was always a legacy accommodation rather than a documented, tested feature. When Adobe terminated Flash Player on January 12, 2021, activating its built-in killswitch, .spl files lost their last viable playback path.

The Ruffle project, which is re-implementing Flash Player in Rust, focuses on SWF files and has limited support for the earliest Flash/FutureSplash content. The .spl container format itself is largely undocumented and untested in Ruffle. Works created in FutureSplash Animator before the Macromedia acquisition exist in a format that is both historically significant — representing the very beginning of vector animation on the web — and almost completely unplayable.

FutureSplash's extinction is a case study in format succession failure: even when a format is nominally absorbed by its successor (SWF), the original works can still be lost if backward compatibility is never formally preserved.
