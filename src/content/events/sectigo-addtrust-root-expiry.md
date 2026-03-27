---
ai_generated: true
title: "Sectigo AddTrust External CA Root expires, breaking certificate chains"
date: "2020-05-30"
dependency: "AddTrust External CA Root cross-sign"
event_type: "certificate-expiry"
severity: "major"
summary: "The expiration of the AddTrust External CA Root certificate on May 30, 2020 caused widespread TLS failures for clients that followed the full chain including the expired cross-sign, breaking Stripe, Roku, Heroku, and many smaller sites relying on Sectigo/Comodo certificates."
links:
  - url: "https://support.sectigo.com/articles/Knowledge/Sectigo-AddTrust-External-CA-Root-Expiring-May-30-2020"
    label: "Sectigo: AddTrust External CA Root Expiring May 30, 2020"
  - url: "https://www.agwa.name/blog/post/fixing_the_addtrust_root_expiration"
    label: "Andrew Ayer: Fixing the AddTrust Root Expiration"
  - url: "https://status.stripe.com/incidents/pdavh2spxh2v"
    label: "Stripe status incident report"
---

## What changed

On May 30, 2020, the AddTrust External CA Root certificate expired. This root had been used for years as a cross-signing anchor for Sectigo (formerly Comodo) intermediate certificates. The cross-sign existed to ensure backward compatibility with very old clients that did not yet trust Sectigo's newer USERTrust roots.

In theory, modern clients should have been unaffected: they trusted the USERTrust root directly and could build a valid chain without the expired AddTrust cross-sign. In practice, many TLS implementations — particularly OpenSSL versions before 1.1.1 — performed path building incorrectly. When a server sent the full certificate chain including the expired AddTrust root, these clients would follow that path, encounter the expired certificate, and reject the connection rather than finding the shorter valid path to USERTrust.

The breakage was extensive. Stripe's payment processing was disrupted. Roku devices could not reach streaming services. Heroku-hosted applications experienced outages. cURL on older Linux distributions failed. Any service using Sectigo certificates with the legacy chain was potentially affected.

For smaller sites — including artist portfolios, independent project hosting, and institutional pages on shared hosting — the fix required the hosting provider to update their certificate chain configuration. Many shared hosting providers were slow to respond. Sites whose operators did not understand certificate chains had no way to diagnose the problem themselves, and simply appeared broken to a subset of visitors for days or weeks until their hosting provider updated the chain or they found help.

The event illustrated how cross-signing, intended as a compatibility bridge, could become a time bomb when the old root expired.
