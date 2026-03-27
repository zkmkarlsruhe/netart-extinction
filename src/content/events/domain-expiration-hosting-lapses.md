---
ai_generated: true
title: "Domain expiration and hosting lapses"
date: "2010"
dependency: "Domain renewals and web hosting"
event_type: "other"
severity: "total"
summary: "Net art can disappear without any platform shutdown when domains expire, hosting is not renewed, or credentials are lost — often producing silent 404s and partial file loss that complicates restoration."
links:
  - url: "https://about.mouchette.org/wp-content/uploads/2012/08/zen-archive2020.pdf"
    label: "Zen and the Art of Database Maintenance (Archive2020 text)"
  - url: "https://about.mouchette.org/wp-content/uploads/2021/09/LIMA_Can-Mouchette-be-preserved-as-an-identity.pdf"
    label: "LIMA case study: Can Mouchette be preserved as an identity?"
affected_artworks:
  - artwork: "mouchette"
    severity: total
    status: restored
    note: "Requires ongoing domain registration, email, moderation tools, and hosting maintenance. Actively maintained by artist; still at structural risk."
  - artwork: "agatha-appears"
    severity: total
    status: degraded
    note: "Distributed web files/locations across the network. Partial destruction through code obsolescence and liquidation of some locations."
  - artwork: "onewordmovie"
    severity: major
    status: degraded
    note: "Depends on a maintained project domain plus server-side code and upstream services."
fixes:
  - type: workaround
    description: "Prevention: auto-renew domains, institutional escrow for accounts/credentials, redundancy for DNS and storage."
  - type: archive
    description: "Periodic WARC captures plus complete server-side source escrow; store build/deploy instructions."
---

Not a single "switch-off," but a recurring failure mode: registrars delete domains after expiry; hosts delete sites after non-payment; credentials and moderation access become unavailable.

## Notes

This entry pairs well with hosting shutdown entries because it explains "why works vanish even when the web still exists."
