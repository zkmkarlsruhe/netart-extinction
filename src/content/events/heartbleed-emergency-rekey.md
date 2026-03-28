---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Heartbleed"
title: "Heartbleed forces mass certificate revocation and reissue"
date: "2014-04-07"
dependency: "OpenSSL TLS library / existing TLS certificates"
event_type: "certificate-expiry"
severity: "major"
summary: "The Heartbleed vulnerability in OpenSSL forced the emergency revocation and reissue of an estimated 500,000+ TLS certificates; sites whose operators failed to rekey experienced certificate revocation failures, and the mass revocation itself overwhelmed CRL and OCSP infrastructure."
links:
  - url: "https://heartbleed.com/"
    label: "Heartbleed Bug disclosure site"
  - url: "https://www.openssl.org/news/secadv/20140407.txt"
    label: "OpenSSL Security Advisory - CVE-2014-0160"
  - url: "https://www.netcraft.com/blog/keys-left-unchanged-in-many-heartbleed-replacement-certificates/"
    label: "Netcraft: Keys Left Unchanged in Many Heartbleed Replacement Certificates"
---

## What changed

On April 7, 2014, CVE-2014-0160 — known as Heartbleed — was publicly disclosed. The bug in OpenSSL's implementation of the TLS heartbeat extension allowed remote attackers to read up to 64KB of server memory per request, potentially exposing private keys, session tokens, and other sensitive data. Any server running OpenSSL 1.0.1 through 1.0.1f (roughly two years of releases) was affected.

The vulnerability meant that the private keys for any affected server's TLS certificate should be considered compromised. Certificate authorities urged mass revocation and reissuance. In the weeks following disclosure, hundreds of thousands of certificates were revoked and replaced. This created two distinct failure modes:

First, the certificate revocation infrastructure itself buckled. OCSP responders and CRL distribution points for major CAs experienced severe load. Browsers that performed online revocation checks saw increased connection latency or timeouts. Some browsers responded by soft-failing on revocation checks, effectively ignoring revoked certificates — undermining the entire point of revocation.

Second, many site operators never rekeyed. A Netcraft study found that 14% of affected sites reissued certificates using the same potentially-compromised private key, and many others never reissued at all. Small organizations, personal sites, and abandoned projects were least likely to respond. For unmaintained web art projects running on vulnerable OpenSSL versions, the situation was doubly grim: the works were both exploitable and unlikely to ever be patched. Some hosting providers revoked certificates for non-responsive customers, taking sites offline entirely.

The Heartbleed aftermath demonstrated how a single library vulnerability could cascade through the entire certificate ecosystem, with the remediation itself causing breakage.
