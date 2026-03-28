---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Indeo"
title: "Microsoft security-blocks Indeo codec, breaking legacy video playback"
date: "2009-12"
dependency: "Intel Indeo video codec"
event_type: "format-obsolescence"
severity: "major"
summary: "Microsoft disabled the Indeo video codec in Internet Explorer and Windows Media Player via a December 2009 security advisory, and Windows Vista and later shipped with the codec unregistered — rendering video art, CD-ROM multimedia, and game cutscenes encoded with Indeo 3/4/5 unplayable on modern Windows."
links:
  - url: "https://support.microsoft.com/en-us/topic/microsoft-security-advisory-vulnerabilities-in-the-indeo-codec-could-allow-remote-code-execution-december-8-2009-680127c6-f4fd-e533-b641-6ab3a25fb4f4"
    label: "Microsoft Security Advisory 954157: Indeo codec vulnerabilities"
  - url: "https://www.microsoft.com/en-us/msrc/blog/2012/02/ms12-014-indeo-a-blast-from-the-past"
    label: "Microsoft Security Response Center: Indeo, a blast from the past"
  - url: "https://en.wikipedia.org/wiki/Intel_Indeo"
    label: "Wikipedia: Indeo"
  - url: "https://www.kb.cert.org/vuls/id/228561"
    label: "CERT: Microsoft Indeo video codecs contain multiple vulnerabilities"
fixes:
  - type: workaround
    description: "Third-party codec restoration patches exist (e.g., manually re-registering Indeo DLLs on Windows 10/11), but these bypass the security mitigations Microsoft put in place."
  - type: migration
    description: "Video files encoded in Indeo can be transcoded to modern codecs using tools like FFmpeg or VLC, but only if the original files are still accessible."
---

Intel's Indeo codec, released in 1992 alongside Microsoft's Video for Windows, was one of the first video codecs to enable full-speed software-only video playback — no hardware acceleration required. At launch, it was the only codec supported across both Video for Windows and Apple's QuickTime.

## What changed

Indeo became the default video codec for a generation of CD-ROM multimedia titles, interactive encyclopedias, educational software, game cutscenes, and early digital art distributed on disc. Titles like the Compton's Interactive Encyclopedia, Myst-era adventure games, and numerous 1990s multimedia art CD-ROMs relied on Indeo 3, 4, or 5.

In December 2009, Microsoft published Security Advisory 954157, disclosing remote code execution vulnerabilities in the Indeo codec. Because Intel had sold the codec to Ligos Corporation in 2000, and Microsoft likely did not have access to the source code needed to patch it, the response was to disable Indeo entirely: the update blocked the codec from being invoked by Internet Explorer or Windows Media Player. Windows Vista and all later versions had already shipped with the codec present but unregistered — effectively invisible to applications.

The result was that upgrading to a new version of Windows silently broke playback of any video encoded with Indeo. Users lost access to a swath of historical multimedia content without warning. The codec infrastructure remains on the system in later Windows versions, but it is not registered and cannot be used without manual intervention that circumvents security protections.

## Notes

Indeo's fate illustrates a pattern where security vulnerabilities in abandoned proprietary codecs lead to effective format death. Unlike open codecs that can be patched by the community, Indeo's proprietary ownership chain (Intel to Ligos to abandonment) meant no one could fix the vulnerabilities, and Microsoft's only option was to disable it. Community projects on GitHub now offer restoration patches for Windows 10 and 11, but these require users to knowingly accept the security risks.
