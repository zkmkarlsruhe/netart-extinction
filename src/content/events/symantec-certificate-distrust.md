---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Symantec"
title: "Browsers distrust Symantec-issued TLS certificates"
date: "2018-04-17"
end_date: "2018-10-23"
dependency: "Symantec / VeriSign / Thawte / GeoTrust / RapidSSL certificate authorities"
event_type: "certificate-expiry"
severity: "major"
summary: "After years of CA policy violations, Chrome 66 and 70 progressively distrusted all certificates issued by Symantec and its subsidiaries (VeriSign, Thawte, GeoTrust, RapidSSL), forcing mass certificate replacement across the web."
links:
  - url: "https://security.googleblog.com/2017/09/chromes-plan-to-distrust-symantec.html"
    label: "Google Security Blog: Chrome's plan to distrust Symantec certificates"
  - url: "https://blog.mozilla.org/security/2018/03/12/distrust-symantec-tls-certificates/"
    label: "Mozilla: Distrust of Symantec TLS Certificates"
  - url: "https://wiki.mozilla.org/CA/Symantec_Issues"
    label: "Mozilla Wiki: Symantec CA issues timeline"
fixes:
  - type: workaround
    description: "Site operators could obtain replacement certificates from a trusted CA. DigiCert, which acquired Symantec's CA business, offered free replacements."
  - type: none
    description: "Unmaintained sites that did not replace their Symantec-issued certificates became inaccessible via HTTPS in Chrome, Firefox, and other major browsers."
---

## What changed

In 2015 and 2016, Google researchers discovered that Symantec's certificate authority infrastructure had issued thousands of certificates improperly, including unauthorized test certificates for domains like google.com. Investigation revealed systemic problems: inadequate auditing of Symantec's sub-CAs (including CrossCert, a South Korean partner), backdated certificates, and failure to follow industry baseline requirements.

Google announced in September 2017 that Chrome would progressively distrust all Symantec-issued certificates. The rollout happened in two phases: Chrome 66 (April 17, 2018) distrusted certificates issued before June 1, 2016, and Chrome 70 (October 23, 2018) distrusted all remaining Symantec certificates. Mozilla, Apple, and Microsoft followed similar timelines.

At the time of distrust, Symantec and its subsidiaries (VeriSign, Thawte, GeoTrust, RapidSSL) collectively had the largest market share of any CA — estimates ranged from 30% to 40% of all HTTPS certificates. The distrust forced the largest certificate migration in the history of the web.

Actively maintained sites replaced their certificates, but unmaintained sites — including many hosting net art, creative projects, and institutional archives — simply went dark in modern browsers. HTTPS sites with Symantec certificates showed full-page security warnings and required users to click through interstitials, effectively rendering the content inaccessible to casual visitors.

## Notes

This was not a technical expiry but a policy-driven trust revocation, which has the same practical effect: browsers refuse to establish a secure connection. For unmaintained creative sites, the distinction is immaterial — the artwork becomes unreachable either way.
