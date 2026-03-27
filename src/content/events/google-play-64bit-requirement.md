---
ai_generated: true
title: "Google Play stops serving 32-bit-only apps on 64-bit Android devices"
date: "2021-08-01"
dependency: "Google Play 32-bit app support on 64-bit devices"
event_type: "os-deprecation"
summary: "On August 1, 2021, Google Play stopped serving apps without 64-bit native code to 64-bit Android devices, rendering thousands of abandoned 32-bit-only apps — including creative tools, art apps, and games built on older Unity versions — invisible and uninstallable on modern phones."
links:
  - url: "https://android-developers.googleblog.com/2019/01/get-your-apps-ready-for-64-bit.html"
    label: "Android Developers Blog: Get your apps ready for the 64-bit requirement"
  - url: "https://developer.android.com/google/play/requirements/64-bit"
    label: "Android Developers: Support 64-bit architectures"
  - url: "https://www.androidpolice.com/2019/01/16/play-store-to-phase-out-32-bit-apps-on-64-bit-devices-by-2021-all-new-apps-from-august-1-must-be-64-bit/"
    label: "Android Police: Play Store to phase out 32-bit apps on 64-bit devices by 2021"
fixes:
  - type: workaround
    description: "Users who had previously installed 32-bit apps could sometimes continue using them, but could not reinstall after a device reset or on a new device."
  - type: workaround
    description: "Sideloading APKs from third-party sources bypasses the Play Store restriction, but requires users to find and trust alternative distribution channels."
  - type: none
    description: "Apps built on Unity 5.6 or older, or other frameworks lacking 64-bit support, cannot be updated without a full engine migration — often impractical for abandoned projects."
---

## What changed

On August 1, 2021, Google Play stopped delivering apps that lacked 64-bit native code to devices with 64-bit processors. The policy had been announced in January 2019, with an initial requirement that all new apps and updates include 64-bit support starting August 1, 2019. The 2021 deadline extended this to the serving layer: 32-bit-only apps simply disappeared from the Play Store for users on modern 64-bit phones and tablets.

The requirement applied only to apps using native code (C/C++ libraries, game engines), not pure Java/Kotlin apps. But this distinction meant that creative applications were disproportionately affected — games, audio tools, camera apps, drawing applications, and interactive art pieces frequently use native code for performance. Games built on Unity 5.6 or older were especially vulnerable, as Unity did not add 64-bit Android support until versions 2017.4 and 2018.2. Google granted these games an extension to August 2021, but for abandoned projects whose developers had moved on, no update would ever come.

The effect was a quiet mass disappearance. Thousands of apps that had been available for years — including experimental art apps, indie games, creative tools from small studios, and interactive pieces distributed via the Play Store — vanished from search results and could no longer be installed on 64-bit devices. Unlike Apple's iOS 32-bit purge (which removed the ability to run 32-bit apps entirely), Google's approach was a distribution cutoff: the apps could theoretically still run if sideloaded, but for most users, an app that does not appear in the Play Store effectively does not exist. No archive or preservation mechanism was provided for the delisted apps.
