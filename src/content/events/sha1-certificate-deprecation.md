---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/SHA-1"
title: "Browsers reject SHA-1 signed certificates"
date: "2016-01-01"
end_date: "2017-02-23"
dependency: "SHA-1 certificate signatures"
event_type: "certificate-expiry"
severity: "major"
summary: "Major browsers phased out trust in SHA-1 signed TLS certificates between 2016 and early 2017, rendering HTTPS sites with older certificates untrusted and triggering interstitial warnings or outright connection refusals."
links:
  - url: "https://blog.mozilla.org/security/2017/02/23/the-end-of-sha-1-on-the-public-web/"
    label: "Mozilla Security Blog: The End of SHA-1 on the Public Web"
  - url: "https://security.googleblog.com/2014/09/gradually-sunsetting-sha-1.html"
    label: "Google Security Blog: Gradually Sunsetting SHA-1"
  - url: "https://shattered.io/"
    label: "SHAttered: SHA-1 collision attack demonstration"
---

## What changed

Starting in 2014, Google began a graduated visual deprecation of SHA-1 certificates in Chrome, showing degraded security indicators for sites using them. By January 1, 2016, major CAs stopped issuing new SHA-1 certificates under CA/Browser Forum Ballot 118. Chrome 56 (January 2017) and Firefox 51 (January 2017) began outright rejecting SHA-1 certificates issued by public CAs. Microsoft Edge followed in mid-2017.

The theoretical basis was confirmed on February 23, 2017, when Google and CWI Amsterdam published "SHAttered," demonstrating a practical SHA-1 collision. But by then the browser enforcement was already in place.

Sites that had obtained long-lived SHA-1 certificates before the cutoff — common for small organizations, personal sites, and institutional pages that purchased multi-year certificates — found their HTTPS connections rejected by modern browsers with no user override available. This disproportionately affected unmaintained sites: university art departments, small gallery hosting, and artist portfolio pages where the administrator had moved on. The certificates were technically still within their validity period, but browsers no longer trusted the signature algorithm.

Embedded devices and appliances with SHA-1 certificates in their management interfaces also became inaccessible from modern browsers, requiring direct IP access or legacy browser versions to reach.
