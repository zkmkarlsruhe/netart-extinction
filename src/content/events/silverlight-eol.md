---
ai_generated: true
title: "Microsoft Silverlight reaches end of support"
date: "2021-10-12"
dependency: "Microsoft Silverlight plugin"
event_type: "plugin-eol"
severity: "total"
summary: "Microsoft Silverlight reached end of support on October 12, 2021. Chrome had dropped support in 2015, Firefox in 2017 — only IE11 on Windows remained. Any web art or interactive project built in Silverlight is now inaccessible in modern browsers."
links:
  - url: "https://learn.microsoft.com/en-us/lifecycle/products/silverlight-5"
    label: "Microsoft Lifecycle: Silverlight 5"
  - url: "https://en.wikipedia.org/wiki/Microsoft_Silverlight"
    label: "Wikipedia: Microsoft Silverlight"
fixes:
  - type: none
    description: "No emulator equivalent to Ruffle (Flash) exists for Silverlight. Content must be rebuilt from source in modern web technologies."
  - type: rebuild
    description: "Silverlight applications can theoretically be rewritten as HTML5/JavaScript, but the XAML-based UI framework has no direct web equivalent."
---

Microsoft Silverlight reached end of support on October 12, 2021. In practice, Silverlight had been dying for years: Chrome dropped NPAPI plugin support (and thus Silverlight) in September 2015, Firefox followed in March 2017.

## What changed

Released in 2007 as Microsoft's competitor to Flash, Silverlight was used for rich interactive web applications, streaming video (Netflix relied on it), and data visualization. It offered a .NET-based programming model with XAML layouts — powerful but proprietary and entirely dependent on a browser plugin.

Apple's refusal to allow browser plugins on iOS (2007 onward) signaled Silverlight's eventual irrelevance on mobile. When desktop browsers dropped plugin support through the NPAPI removal wave (2015–2017), Silverlight was effectively dead years before Microsoft's official end-of-support date.

## Notes

Unlike Flash, which has the Ruffle emulator preserving legacy content, no equivalent preservation tool exists for Silverlight. Silverlight content is simply gone from the web, recoverable only if the source code exists and someone rebuilds it.
