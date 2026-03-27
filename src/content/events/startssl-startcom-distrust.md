---
ai_generated: true
title: "Browsers distrust StartSSL/StartCom certificates"
date: "2016-10-21"
end_date: "2017-11-14"
dependency: "StartCom / StartSSL certificate authority"
event_type: "certificate-expiry"
severity: "minor"
summary: "After a covert acquisition by WoSign and evidence of certificate misissuance, major browsers distrusted all StartCom/StartSSL certificates, shutting down a CA that had been widely used by independent developers and artists for free HTTPS."
links:
  - url: "https://blog.mozilla.org/security/2016/10/24/distrusting-new-wosign-and-startcom-certificates/"
    label: "Mozilla: Distrusting New WoSign and StartCom Certificates"
  - url: "https://security.googleblog.com/2016/10/distrusting-wosign-and-startcom.html"
    label: "Google: Distrusting WoSign and StartCom Certificates"
  - url: "https://www.startssl.com/"
    label: "StartSSL (defunct)"
fixes:
  - type: migration
    description: "Site operators could replace StartSSL certificates with Let's Encrypt (free) or other trusted CA certificates."
  - type: none
    description: "Sites whose operators were unaware of or did not respond to the distrust lost HTTPS access in major browsers."
---

## What changed

StartSSL, operated by StartCom, was one of the first certificate authorities to offer free DV (domain-validated) SSL certificates, making it popular among independent developers, hobbyists, and artists who wanted HTTPS without cost. For years before Let's Encrypt launched in 2016, StartSSL was the go-to option for small personal sites and creative projects.

In September 2016, it was revealed that WoSign, a Chinese CA, had secretly acquired StartCom in a transaction completed in November 2015 — a fact both companies had actively concealed from browser trust programs. Investigation also uncovered that WoSign had been backdating SHA-1 certificates to circumvent browser deadlines for SHA-1 deprecation, and that StartCom's infrastructure had been merged with WoSign's while maintaining a facade of independence.

Mozilla led the distrust action in October 2016, initially restricting newly issued certificates. Chrome 56 (January 2017) followed. By Chrome 61 (September 2017) and Firefox 58 (November 2017), full distrust was enforced for all StartCom and WoSign certificates regardless of issuance date. StartCom ceased operations entirely in November 2017, and its final root certificates expired in 2020.

The impact fell disproportionately on small, independent sites — exactly the kind of projects that had relied on StartSSL's free certificates. While actively maintained sites migrated to Let's Encrypt, many older personal pages, artist portfolios, and small creative projects lost HTTPS functionality.

## Notes

The timing was partly mitigated by Let's Encrypt's rapid growth during the same period, providing a free alternative. However, migration required active intervention by site operators, and sites that were no longer maintained simply lost their TLS trust.
