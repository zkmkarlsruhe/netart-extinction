---
title: "Internet Explorer retired"
date: "2022-06-15"
dependency: "Internet Explorer"
event_type: "browser-change"
severity: "major"
summary: "Internet Explorer 11 ended support on June 15, 2022 and was retired, pushing legacy-IE-dependent artworks toward Edge IE Mode and virtualization."
links:
  - url: "https://learn.microsoft.com/en-us/lifecycle/announcements/internet-explorer-11-end-of-support"
    label: "Microsoft lifecycle notice"
  - url: "https://blogs.windows.com/windowsexperience/2022/06/15/internet-explorer-11-has-retired-and-is-officially-out-of-support-what-you-need-to-know/"
    label: "Windows blog: IE retired (Jun 15, 2022)"
fixes:
  - type: emulation
    description: "Use Edge IE Mode where adequate; document rendering divergences."
  - type: emulation
    description: "For authenticity: VM snapshots with period-correct IE versions and offline mirrors."
  - type: rebuild
    description: "Migrate to standards-based rendering; treat differences as conservation decisions."
---

IE 11 desktop application ended support on certain Windows 10 versions as of June 15, 2022. Microsoft positions Microsoft Edge with IE Mode as the compatibility pathway, but IE Mode does not reproduce all historical IE behaviors (especially for very old DHTML/ActiveX patterns).

## Notes

Unlike Flash, IE retirement is not a single runtime removal. It is a support and deployment extinction that accelerates the disappearance of IE-specific works over time.
