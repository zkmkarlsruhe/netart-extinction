---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning"
title: "HTTP Public Key Pinning locks sites out of their own domains"
date: "2017"
end_date: "2018-05"
dependency: "HTTP Public Key Pinning (HPKP)"
event_type: "protocol-change"
severity: "minor"
summary: "HPKP allowed sites to pin specific certificate keys in browsers, but misconfiguration or key loss made sites permanently inaccessible to returning visitors — a self-inflicted extinction mechanism that led browsers to deprecate the feature entirely."
links:
  - url: "https://groups.google.com/a/chromium.org/g/blink-dev/c/he9tr7p3rZ8"
    label: "Chrome intent to deprecate and remove HPKP"
  - url: "https://scotthelme.co.uk/using-security-features-to-do-bad-things/"
    label: "Scott Helme: Using Security Features to Do Bad Things (HPKP risks)"
  - url: "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Public-Key-Pins"
    label: "MDN: Public-Key-Pins (deprecated)"
fixes:
  - type: none
    description: "For sites that pinned keys and then lost access to those keys, there was no fix — browsers that had cached the pin would refuse all connections until the pin's max-age expired, which could be months or years."
  - type: workaround
    description: "Chrome removed HPKP support in version 72 (January 2019) and Firefox in version 72 (January 2020), eventually freeing trapped sites — but only after the feature had already caused damage."
---

## What changed

HTTP Public Key Pinning (HPKP), standardized in RFC 7469 in 2015, allowed website operators to send a header instructing browsers to remember ("pin") the cryptographic public keys associated with the site's certificate. On subsequent visits, if the certificate's key did not match a pinned key, the browser would refuse to connect — with no override option.

The intent was to prevent man-in-the-middle attacks using fraudulently issued certificates. The reality was a loaded gun pointed at site operators. If a site pinned its keys and then needed to change certificates — due to a CA distrust event, key compromise, hosting migration, or simple operational error — returning browsers would reject the new certificate. The site would be unreachable to those users until the pin's `max-age` expired, which operators sometimes set to months or even a year.

Several high-profile incidents demonstrated the danger. SmashingMagazine.com accidentally deployed HPKP headers that locked visitors out. The Dutch government's DigiNotar incident, while predating HPKP, motivated its creation — ironically, the mechanism designed to prevent such attacks became a bigger threat to site availability than the attacks themselves. Security researcher Scott Helme documented how HPKP could be weaponized: an attacker who briefly compromised a site could set HPKP headers pinning their own keys, creating a persistent denial-of-service even after the compromise was cleaned up (dubbed "HPKP Suicide").

For creative and artistic sites, the risk was acute. Small site operators who followed security best practices and enabled HPKP could find themselves locked out of their own domains after routine certificate renewals. Let's Encrypt's 90-day certificate rotation made HPKP especially treacherous, as frequent renewals multiplied the chances of a key mismatch.

Chrome deprecated HPKP in Chrome 67 (May 2018) and removed it in Chrome 72 (January 2019). Firefox removed support in version 72 (January 2020). The feature's removal was itself a form of preservation — it freed sites that had accidentally trapped themselves.

## Notes

HPKP is a cautionary example of a security feature that created more destruction than it prevented. Its brief life (roughly 2015-2019) left a small but real trail of temporarily or permanently broken sites, particularly among security-conscious small operators who were most likely to adopt it.
