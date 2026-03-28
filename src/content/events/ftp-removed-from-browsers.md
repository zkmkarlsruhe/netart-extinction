---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/File_Transfer_Protocol"
title: "FTP removed from modern browsers"
date: "2021-01-19"
end_date: "2021-07-13"
dependency: "FTP protocol in browsers"
event_type: "protocol-change"
severity: "major"
summary: "Chrome removed FTP support (Chrome 88, January 2021) and Firefox followed (Firefox 90, July 2021), breaking ftp:// links used for distributing assets and archival materials referenced by older net artworks."
links:
  - url: "https://developer.chrome.com/blog/chrome-88-deps-rems"
    label: "Chrome 88 deprecations/removals (FTP removed)"
  - url: "https://blog.mozilla.org/security/2021/07/20/stopping-ftp-support-in-firefox-90/"
    label: "Mozilla Security Blog: stopping FTP support in Firefox 90"
fixes:
  - type: migration
    description: "Replace ftp:// URLs with https:// mirrors; provide checksums."
  - type: archive
    description: "Capture FTP-hosted materials into WARC or institutional repositories."
---

Browsers removed built-in FTP clients, citing lack of encryption support, low usage, and better external clients. The practical effect: ftp:// URLs no longer resolve in the default browsing workflow.

## Notes

FTP removal is a "small" extinction example: it rarely kills the core logic, but it kills access paths that artworks depended on (especially for installation instructions and downloadable components).
