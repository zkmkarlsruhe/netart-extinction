---
ai_generated: true
title: "macOS Catalina drops legacy QuickTime codecs, breaking old video playback"
date: "2019-10-07"
dependency: "Legacy QuickTime codecs (Sorenson Video 3, Cinepak, MPEG-1, etc.)"
event_type: "format-obsolescence"
severity: "major"
summary: "macOS Catalina (October 2019) dropped all 32-bit application support, killing QuickTime 7 and the QTKit framework. Legacy codecs including Sorenson Video 3, Cinepak, and early MPEG variants — used extensively in 1990s and 2000s web video, CD-ROM art, and QuickTime movies — stopped playing in Apple's own apps."
links:
  - url: "https://www.macworld.com/article/234292/your-old-videos-may-not-play-in-macos-catalina-heres-why.html"
    label: "Macworld: Your old videos may not play in macOS Catalina"
  - url: "https://www.idownloadblog.com/2020/06/17/macos-catalina-video-formats-support-issues/"
    label: "iDownloadBlog: Why macOS Catalina dropped support for old video formats"
  - url: "https://www.loc.gov/preservation/digital/formats/fdd/fdd000066.shtml"
    label: "Library of Congress: Sorenson Video Codec, Version 3"
  - url: "https://en.wikipedia.org/wiki/QuickTime"
    label: "Wikipedia: QuickTime"
fixes:
  - type: workaround
    description: "Third-party players like VLC include their own codec implementations and can still play Sorenson, Cinepak, and other legacy formats on macOS Catalina and later."
  - type: migration
    description: "Legacy video files can be transcoded to H.264 or H.265 using FFmpeg, though this requires identifying affected files and loses the original encoding characteristics."
---

When Apple released macOS 10.15 Catalina on October 7, 2019, it removed support for all 32-bit applications. This killed QuickTime 7 and its underlying QTKit framework — the last bridge to a generation of legacy video codecs that had powered multimedia on the Mac since the early 1990s.

## What changed

QuickTime, first released in 1991, was the dominant multimedia framework for a decade. Apple licensed the Sorenson Video codec for inclusion in QuickTime 3.0 (1998), and Sorenson Video 3 became the standard codec for web video and CD-ROM distribution throughout the late 1990s and early 2000s — years before Flash video or YouTube existed. Cinepak, an even older codec dating to 1991, was the workhorse of early CD-ROM multimedia.

With Catalina's 32-bit purge, Apple's own applications — QuickTime Player, iMovie, Final Cut Pro — could no longer decode these formats. A .mov file encoded with Sorenson Video 3 that had played on every Mac for two decades would simply refuse to open. No error message explained what had changed; the file just would not play.

This affected a broad category of creative work: artist portfolios distributed as QuickTime movies, interactive CD-ROM art projects with embedded video, early web video art archived in .mov containers, educational multimedia, and documentation of performances and exhibitions. The Sorenson codec in particular was the format of choice for artists distributing video online in the pre-YouTube era, when embedding a QuickTime movie on a webpage was the standard approach.

## Notes

Apple's 32-bit purge was technically a platform decision rather than a deliberate format deprecation — Sorenson and Cinepak were collateral damage of the architectural transition. But the practical effect was the same: an entire generation of video became unplayable in the default software environment. VLC and FFmpeg can still handle these codecs, but the average user opening an old .mov file on a modern Mac will simply see a failure. The Library of Congress has documented Sorenson Video 3 in its digital formats registry, recognizing its historical significance and preservation challenges.
