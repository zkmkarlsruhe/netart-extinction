---
title: "Browsers drop TLS 1.0 and 1.1 support"
date: "2020-03"
end_date: "2020-09"
dependency: "TLS 1.0 / TLS 1.1 cryptographic protocols"
event_type: "protocol-change"
severity: "minor"
summary: "Apple, Google, Microsoft, and Mozilla jointly deprecated TLS 1.0 and 1.1 in early 2020 (delayed from March to ~September due to COVID-19). Legacy servers that were never updated became unreachable over HTTPS — disproportionately affecting unmaintained servers hosting abandoned net art."
links:
  - url: "https://webkit.org/blog/8462/deprecation-of-legacy-tls-1-0-and-1-1-versions/"
    label: "WebKit Blog: Deprecation of Legacy TLS 1.0 and 1.1"
fixes:
  - type: workaround
    description: "Server administrators can update their TLS configuration to support TLS 1.2+, but this requires active maintenance of the server."
  - type: none
    description: "For abandoned servers with no maintainer, the content is unreachable over HTTPS in modern browsers."
---

In October 2018, Apple, Google, Microsoft, and Mozilla jointly announced they would deprecate TLS 1.0 and TLS 1.1, with enforcement originally planned for March 2020. The rollout was delayed to approximately September 2020 due to the COVID-19 pandemic.

## What changed

After enforcement, modern browsers refuse to establish HTTPS connections using TLS 1.0 or 1.1. Servers that were never updated to support TLS 1.2 or later became inaccessible. This primarily affects unmaintained older servers — exactly the kind of infrastructure that hosts abandoned net art from the early 2000s: university pages, personal servers, small institutional sites, and artist portfolios on forgotten hosting.

## Notes

Unlike the mixed-content blocking event (which affected HTTP resources on HTTPS pages), TLS deprecation makes entire sites unreachable. The fix is simple — update the server's TLS configuration — but requires someone with access and motivation to do so. For abandoned sites, there is no one.
