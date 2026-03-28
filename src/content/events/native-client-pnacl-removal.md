---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Google_Native_Client"
title: "Chrome Native Client and PNaCl removed"
date: "2020-06-23"
dependency: "Google Native Client (NaCl) and Portable Native Client (PNaCl)"
event_type: "browser-change"
severity: "total"
summary: "Chrome removed support for Native Client (NaCl) and Portable Native Client (PNaCl) in 2020, ending the ability to run compiled C/C++ code as browser-embedded art."
links:
  - url: "https://blog.chromium.org/2020/01/pnacl-deprecation-update.html"
    label: "Chromium Blog: PNaCl deprecation update"
  - url: "https://en.wikipedia.org/wiki/Google_Native_Client"
    label: "Wikipedia: Google Native Client"
---

Google Native Client (NaCl), launched in 2011, allowed compiled C and C++ code to run inside the Chrome browser at near-native speed. Portable Native Client (PNaCl) extended this with architecture-independent binaries. Artists and creative coders used NaCl/PNaCl to bring computationally intensive work — real-time 3D, audio synthesis, physics simulations — into the browser without plugin dependencies.

## What changed

Google began deprecating PNaCl in 2017, directing developers toward WebAssembly instead. Support was removed from Chrome in mid-2020 (Chrome 76+ for new apps, with remaining support stripped by Chrome 83-85). NaCl/PNaCl modules simply fail to load in current browsers. The recommended migration path is WebAssembly, which covers many of the same use cases but requires porting effort.

## Notes

NaCl was always Chrome-only, which limited its adoption, but the works that did use it were often technically ambitious pieces that pushed browser capabilities. Porting to WebAssembly is feasible but not automatic — the toolchain, APIs, and sandboxing model differ. Works that were never ported are now inaccessible outside of archived Chrome builds.
