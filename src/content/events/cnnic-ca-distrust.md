---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/China_Internet_Network_Information_Center"
title: "Google and Mozilla distrust CNNIC root certificate"
date: "2015-04-01"
dependency: "CNNIC root certificate authority"
event_type: "certificate-expiry"
severity: "major"
summary: "After CNNIC's subordinate CA MCS Holdings issued unauthorized certificates for Google domains, Chrome and Firefox removed CNNIC from their trust stores, breaking HTTPS for sites chained to CNNIC roots — primarily Chinese institutional and governmental sites."
links:
  - url: "https://security.googleblog.com/2015/03/maintaining-digital-certificate-security.html"
    label: "Google Security Blog: Maintaining Digital Certificate Security"
  - url: "https://blog.mozilla.org/security/2015/04/02/distrusting-new-cnnic-certificates/"
    label: "Mozilla Security Blog: Distrusting New CNNIC Certificates"
  - url: "https://www.cnnic.cn/"
    label: "China Internet Network Information Center"
---

## What changed

In March 2015, Google discovered that MCS Holdings, an intermediate CA operating under the China Internet Network Information Center (CNNIC), had issued unauthorized digital certificates for several Google domains. MCS Holdings had installed these certificates in a man-in-the-middle proxy device, violating the baseline requirements that govern certificate authorities.

On April 1, 2015, Google announced it would remove CNNIC's root certificate from Chrome's trust store via a phased distrust: existing certificates would continue to work temporarily through whitelisting, but no new certificates chained to CNNIC would be trusted. Mozilla followed with a similar action on April 2, 2015, implemented in Firefox 39.

This had significant collateral effects. Chinese universities, government agencies, research institutions, and cultural organizations that had obtained legitimate certificates from CNNIC found their sites flagged as untrusted in Western browsers. Several Chinese digital art and new media archives hosted on .cn domains with CNNIC-chained certificates became inaccessible to international audiences without certificate warning overrides. CNNIC eventually partnered with other CAs to transition affected sites, but smaller institutional sites were slow to migrate or never did.

The event established a precedent: root CA trust is not permanent. A sovereign CA serving a large national population could be removed from global browser trust stores based on operational failures, with downstream effects on every site in its chain.
