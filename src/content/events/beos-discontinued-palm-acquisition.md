---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/BeOS"
title: "BeOS discontinued after Palm acquisition, orphaning multimedia art tools"
date: "2001-11-13"
dependency: "BeOS"
event_type: "os-deprecation"
severity: "major"
summary: "Be, Inc. was acquired by Palm on November 13, 2001 and immediately dissolved, ending development of BeOS — an operating system purpose-built for real-time multimedia that had attracted audio artists, video creators, and experimental media developers."
links:
  - url: "https://en.wikipedia.org/wiki/BeOS"
    label: "Wikipedia: BeOS"
  - url: "https://en.wikipedia.org/wiki/Be_Inc."
    label: "Wikipedia: Be Inc."
  - url: "https://www.haiku-os.org/about/faq/"
    label: "Haiku OS FAQ: BeOS compatibility"
  - url: "https://hackaday.com/2020/01/09/beos-the-alternate-universes-mac-os-x/"
    label: "Hackaday: BeOS — The Alternate Universe's Mac OS X"
fixes:
  - type: migration
    description: "Haiku OS, an open-source reimplementation of BeOS, achieved source-level and partial binary-level compatibility with BeOS R5. The 32-bit version can run many original BeOS binaries unmodified, though the 64-bit version lacks binary compatibility."
  - type: none
    description: "Palm refused community requests to open-source or license BeOS, and the intellectual property passed through PalmSource to ACCESS Co., Ltd., where it remains unavailable."
---

On August 16, 2001, Be, Inc. announced that Palm, Inc. would acquire the company for $11 million. Shareholders approved the deal on November 13, 2001, and Be, Inc. was dissolved. BeOS R5 (released March 2000) became the final official release. A near-complete R5.1 update codenamed "Dano" was leaked after the company's closure but was never officially released.

## What changed

BeOS was explicitly designed as a "media OS." Its microkernel architecture, pervasive multithreading, and 64-bit journaling file system with rich metadata support made it exceptionally capable for real-time audio and video work at a time when Windows and classic Mac OS struggled with multimedia. The BeOS audio system could handle dozens of simultaneous real-time audio streams with latencies that consumer Windows and Mac systems could not match until years later.

This attracted a community of audio artists and experimental media creators. Applications like CL-Amp (audio player), SoundPlay, and various tracker-style music tools were built natively for BeOS. Roland Corporation built the Edirol DV-7 series of dedicated video editors on a modified BeOS, and TuneTracker developed radio automation software on the platform. Creative tools like Cinema 4D were ported to BeOS, and the native WonderBrush drawing application was developed specifically for its graphics APIs.

When Palm acquired and dissolved Be, Inc., it had no interest in maintaining the operating system. The community petitioned Palm to open-source BeOS, but Palm refused. The intellectual property eventually passed to PalmSource (when Palm split its hardware and software divisions in 2003) and then to ACCESS Co., Ltd., which acquired PalmSource in 2005. BeOS remains proprietary and unavailable.

Artists and audio creators who had built workflows around BeOS's unique real-time capabilities were left with an OS that would receive no further hardware support, no security updates, and no path forward as hardware evolved beyond what BeOS drivers could address.

## Notes

The Haiku project, begun in 2001 as OpenBeOS, has spent over two decades building a compatible open-source replacement. Haiku R1 targets binary compatibility with BeOS R5 on 32-bit systems, and many original BeOS applications do run unmodified. However, Haiku did not reach its first beta release until 2018, leaving a gap of nearly two decades during which BeOS software existed in a preservation limbo — too old to run on modern hardware, too niche for mainstream emulation efforts, and legally locked away from the community that wanted to maintain it.
