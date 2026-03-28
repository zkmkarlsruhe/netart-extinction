---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/MacOS_Catalina"
title: "Apple enforces mandatory notarization for macOS software"
date: "2020-02-03"
dependency: "macOS Catalina notarization requirement"
event_type: "os-deprecation"
summary: "Apple began strictly enforcing notarization requirements on February 3, 2020, meaning all Mac software distributed outside the App Store had to be cryptographically signed and scanned by Apple before macOS would allow it to run — blocking hundreds of unsigned creative tools, audio plugins, and independent art software."
links:
  - url: "https://developer.apple.com/news/?id=09032019a"
    label: "Apple Developer: Notarizing Your Mac Software for macOS Catalina"
  - url: "https://eclecticlight.co/2020/02/03/hardening-and-notarization-finally-arrive-in-catalina/"
    label: "Eclectic Light: Hardening and notarization finally arrive in Catalina"
  - url: "https://www.kvraudio.com/forum/viewtopic.php?t=531663"
    label: "KVR Audio Forum: macOS notarization for plugins"
  - url: "https://www.sweetwater.com/sweetcare/articles/macos-security-warnings-and-gatekeeper-de-mystified/"
    label: "Sweetwater: macOS Security Warnings and Gatekeeper De-Mystified"
fixes:
  - type: workaround
    description: "Users can bypass Gatekeeper on a per-app basis via System Preferences > Security & Privacy, or by right-clicking and selecting Open. macOS Sequoia (2024) made this workaround harder by removing the Control-click override."
  - type: workaround
    description: "Developers with an active Apple Developer account ($99/year) can notarize existing software by submitting it to Apple's automated scanning service."
  - type: none
    description: "Abandoned or orphaned software from developers who no longer maintain an Apple Developer account cannot be notarized and will be blocked by default on modern macOS."
---

## What changed

Beginning with macOS 10.15 Catalina, Apple required all software distributed outside the Mac App Store to be notarized — submitted to Apple's servers for automated malware scanning and cryptographically stamped. After a transition period with relaxed rules, Apple began strict enforcement on February 3, 2020. Software built after June 1, 2019 that was not notarized would be blocked by Gatekeeper with a warning dialog, and users would have to navigate to System Preferences to manually override the block.

The audio production community was hit especially hard. Hundreds of VST and AU plugins from small developers, freeware creators, and abandoned projects triggered Gatekeeper warnings or failed to load entirely in DAWs after the enforcement date. The KVR Audio developer forums filled with threads about notarization problems — plugins that were code-signed but not notarized, distribution via ZIP files (which required the contents themselves to be notarized, unlike DMG or PKG installers), and the fundamental problem that audio plugins cannot carry their own entitlements and depend on the host application's hardened runtime settings.

For independent creative tool developers, the $99/year Apple Developer Program membership became a hard requirement for distribution. Hobbyist developers, academic researchers distributing experimental software, and artists sharing custom tools faced a new barrier: software they had freely distributed for years would now be blocked by default on any Mac running Catalina or later. Abandoned creative software — tools whose developers had moved on, died, or simply stopped paying Apple's annual fee — became progressively harder to run as each macOS version tightened the Gatekeeper bypass process. By macOS Sequoia (2024), Apple removed the simple Control-click override, requiring users to navigate deep into Privacy & Security settings and authenticate with an admin password to open unsigned software.
