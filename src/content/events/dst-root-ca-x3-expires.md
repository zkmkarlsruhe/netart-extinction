---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Let's_Encrypt"
title: "DST Root CA X3 expires, breaking legacy TLS trust"
date: "2021-09-30"
dependency: "TLS trust chain / root certificates"
event_type: "protocol-change"
severity: "major"
summary: "When the DST Root CA X3 cross-sign expired, older clients without ISRG Root X1 trust began failing TLS validation for many HTTPS sites — an under-documented but common failure mode for net art on legacy hardware."
links:
  - url: "https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/"
    label: "Let's Encrypt DST Root CA X3 expiration"
affected_artworks:
  - artwork: "mouchette"
    severity: major
    status: degraded
    note: "Long-lived net artwork often accessed/preserved via legacy setups. Legacy clients may fail HTTPS validation."
  - artwork: "onewordmovie"
    severity: major
    status: degraded
    note: "Loads many third-party resources over HTTPS. Legacy clients may reject certificate chains."
fixes:
  - type: workaround
    description: "Update OS/browser trust stores or replace legacy clients with a maintained environment."
  - type: archive
    description: "For exhibitions: local mirroring (WARC replay) to minimize live TLS dependencies."
---

Certificate trust shifted as older cross-signatures expired and modern roots became the default. Legacy devices and unpatched OS/browser stacks can no longer validate common certificate chains.

## Notes

This is a "hidden extinction": the dependency change is global infrastructure, not an art platform. It disproportionately affects museums using older kiosk systems.
